# -*- coding: utf-8 -*-
"""V11184 §Z-E5/§Z-H2 — CÁCH LY NHÀ CUNG CẤP, KHÔNG RETRY, BỀN QUA RESTART.

ĐO ĐƯỢC NGÀY 13/09/2026 (§Z-P6, 30 ngày):
  · `deepseek-reasoner` trả **402 Insufficient Balance 25 lần trong 3 ngày** (3+11+11), lặp đều
    mỗi lượt mỗi miền, **không hề bị chặn**;
  · `openai` 429 `credit_balance_exhausted` ngày 13/09 sinh **12 lượt HTTP từ 4 lần thử logic**
    vì SDK tự retry 2 lần;
  · bộ ngắt mạch hiện có (`_openrouter_circuit_check`, `gpt_analyzer.py:3795`) **CHỈ** được gọi
    bên trong `_call_openrouter` (`gpt_analyzer.py:3969`). Bốn hàm `_call_openai` /
    `_call_anthropic` / `_call_gemini` / `_call_deepseek` **không kiểm circuit lần nào**;
  · và nó nằm trong **bộ nhớ tiến trình** — restart là mất sạch, trong khi một lỗi 402 kéo dài
    nhiều NGÀY.

HAI THỨ MODULE NÀY LÀM KHÁC:
  1. **BỀN**: trạng thái ghi ra đĩa, sống qua restart.
  2. **PHÂN BIỆT HAI LOẠI LỖI** — đây là điểm cốt lõi:
     · `DETERMINISTIC` (402 · 401 · 403 · insufficient balance · credit exhausted · invalid key):
       gọi lại **chắc chắn hỏng nữa**. Không cooldown theo thời gian, vì thời gian không nạp tiền
       hộ. Chỉ mở lại bằng **BẰNG CHỨNG SỨC KHOẺ**, và mở ra hàng **CHALLENGER**, KHÔNG trả thẳng
       về CORE (khoá §Z E5).
     · `TRANSIENT` (429 rate limit · 5xx · timeout mạng): cooldown theo thời gian là hợp lý.

TUYỆT ĐỐI KHÔNG: gọi provider, retry lỗi deterministic, hay tính một dòng rỗng là voter.
"""
from __future__ import annotations

import io
import json
import os
import re
import sys
import time

BE = os.path.dirname(os.path.abspath(__file__))
GOC = os.path.dirname(os.path.dirname(BE))
TEP_TRANG_THAI = GOC + "/data/provider_quarantine.json"

COOLDOWN_TRANSIENT_SEC = 900        # 15 phút cho lỗi tạm thời
PHIEN_BAN = "v11184.1"

# Dấu hiệu lỗi DETERMINISTIC — gọi lại chắc chắn hỏng. Khai TƯỜNG MINH để đọc được, cấm đoán.
# CẢNH BÁO ĐÃ SẬP MỘT LẦN: bản đầu của danh sách này do TÔI ĐOÁN chuỗi, và nó BỎ SÓT ca thật.
# Thông điệp thật của `gpt-5.4` ngày 13/09 (đọc từ `predictions.verdict_reason`) là
#   "Error code: 429 - {'error': {'message': 'You have no credits remaining. Add credits..."
# — KHÔNG chứa `credit_balance_exhausted`. Với mã 429 nó sẽ rơi vào TRANSIENT và được gọi lại
# sau 15 phút, trong khi thực chất là HẾT TIỀN. Mọi chuỗi dưới đây nay lấy từ THÔNG ĐIỆP THẬT
# đã quan sát, không phải từ trí nhớ (RM-10, RM-17).
DAU_HIEU_DETERMINISTIC = (
    "insufficient balance",           # deepseek-reasoner 402, 13/09, cả ba miền — nguyên văn
    "no credits remaining",           # gpt-5.4 429, 13/09 MB — nguyên văn
    "insufficient_quota", "credit_balance_exhausted", "credit exhausted",
    "add credits", "billing", "payment required", "invalid api key",
    "invalid_api_key", "authentication", "unauthorized", "forbidden",
    "account is not active", "quota exceeded", "exceeded your current quota",
)
MA_HTTP_DETERMINISTIC = (401, 402, 403)
MA_HTTP_TRANSIENT = (408, 409, 425, 429, 500, 502, 503, 504)


def _doc():
    try:
        d = json.load(io.open(TEP_TRANG_THAI, encoding="utf-8"))
        return d if isinstance(d, dict) else {}
    except Exception:
        return {}


def _ghi(d):
    try:
        os.makedirs(os.path.dirname(TEP_TRANG_THAI), exist_ok=True)
        tam = TEP_TRANG_THAI + ".tmp"
        with io.open(tam, "w", encoding="utf-8", newline="\n") as f:
            f.write(json.dumps(d, ensure_ascii=False, indent=1))
            f.flush()
            os.fsync(f.fileno())
        os.replace(tam, TEP_TRANG_THAI)
        return True
    except Exception as e:
        print("[CACH-LY] KHONG ghi duoc trang thai: %r" % e)
        return False


def phan_loai_loi(thong_bao, ma_http=None):
    """DETERMINISTIC · TRANSIENT · KHONG_PHAI_LOI_PROVIDER.

    RM-09: PHÂN LOẠI, không đếm chuỗi thô — mã HTTP xét trước, rồi mới tới dấu hiệu văn bản.
    """
    if ma_http in MA_HTTP_DETERMINISTIC:
        return "DETERMINISTIC"
    t = str(thong_bao or "").lower()
    for k in DAU_HIEU_DETERMINISTIC:
        if k in t:
            return "DETERMINISTIC"
    if ma_http in MA_HTTP_TRANSIENT:
        return "TRANSIENT"
    m = re.search(r"\b(4\d\d|5\d\d)\b", t)
    if m:
        code = int(m.group(1))
        if code in MA_HTTP_DETERMINISTIC:
            return "DETERMINISTIC"
        if code in MA_HTTP_TRANSIENT:
            return "TRANSIENT"
    if "rate limit" in t or "too many requests" in t:
        return "TRANSIENT"
    return "KHONG_PHAI_LOI_PROVIDER"


def kiem(model, _bay_gio=None):
    """Model này có đang bị cách ly không? Trả dict CHẶN, hoặc None nếu được gọi.

    Gọi TRƯỚC mỗi lần gọi provider. Không tốn gì, chỉ đọc một tệp nhỏ.
    """
    now = _bay_gio if _bay_gio is not None else time.time()
    d = _doc()
    e = d.get(str(model))
    if not e:
        return None
    loai = e.get("loai")
    if loai == "DETERMINISTIC":
        return {"ok": False, "bi_chan": True, "loai": loai,
                "error": ("⛔ %s dang CACH LY (loi deterministic: %s). Khong goi lai cho toi khi "
                          "co BANG CHUNG SUC KHOE." % (model, e.get("ly_do"))),
                "error_type": "PROVIDER_QUARANTINED_DETERMINISTIC",
                "tu_luc": e.get("tu_luc"), "ly_do": e.get("ly_do"),
                "so_lan_gap": e.get("so_lan_gap", 0), "retry": False}
    het = e.get("het_luc", 0)
    if now < het:
        return {"ok": False, "bi_chan": True, "loai": loai,
                "error": "⛔ %s dang cooldown tam thoi, con %ds" % (model, int(het - now)),
                "error_type": "PROVIDER_COOLDOWN_TRANSIENT",
                "con_lai_sec": int(het - now), "ly_do": e.get("ly_do"), "retry": False}
    d.pop(str(model), None)
    _ghi(d)
    print("[CACH-LY] ✅ HET COOLDOWN: %s" % model)
    return None


def ghi_nhan_loi(model, thong_bao, ma_http=None, _bay_gio=None):
    """Sau một lần gọi hỏng: phân loại và mở cách ly nếu cần. Trả loại lỗi đã phân."""
    loai = phan_loai_loi(thong_bao, ma_http)
    if loai == "KHONG_PHAI_LOI_PROVIDER":
        return loai
    now = _bay_gio if _bay_gio is not None else time.time()
    d = _doc()
    cu = d.get(str(model)) or {}
    e = {
        "loai": loai, "ly_do": str(thong_bao or "")[:300], "ma_http": ma_http,
        "tu_luc": cu.get("tu_luc") or time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(now)),
        "cap_nhat": time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(now)),
        "so_lan_gap": int(cu.get("so_lan_gap", 0)) + 1,
        "phien_ban": PHIEN_BAN,
    }
    if loai == "TRANSIENT":
        e["het_luc"] = now + COOLDOWN_TRANSIENT_SEC
    else:
        # DETERMINISTIC: KHÔNG đặt `het_luc`. Thời gian không nạp tiền hộ, không đổi khoá hộ.
        e["het_luc"] = None
        e["can_bang_chung_suc_khoe"] = True
        e["tra_ve_hang"] = "CHALLENGER"   # §Z E5: KHÔNG tự trả về CORE
    d[str(model)] = e
    _ghi(d)
    print("[CACH-LY] ⛔ MO CACH LY %s (%s): %s" % (model, loai, str(thong_bao)[:90]))
    return loai


def giai_phong(model, bang_chung=None, _bay_gio=None):
    """Mở cách ly. Với DETERMINISTIC bắt buộc có `bang_chung`; thiếu là TỪ CHỐI."""
    d = _doc()
    e = d.get(str(model))
    if not e:
        return {"ok": True, "ghi_chu": "khong bi cach ly"}
    if e.get("loai") == "DETERMINISTIC" and not bang_chung:
        return {"ok": False, "tu_choi": True,
                "ly_do": ("loi DETERMINISTIC chi mo lai bang BANG CHUNG SUC KHOE (vi du mot luot "
                          "goi that thanh cong), khong mo bang thoi gian")}
    d.pop(str(model), None)
    _ghi(d)
    return {"ok": True, "da_giai_phong": model, "bang_chung": bang_chung,
            "tra_ve_hang": e.get("tra_ve_hang", "CHALLENGER")}


def danh_sach():
    return _doc()


# ---------------------------------------------------------------- tự kiểm
def tu_kiem():
    global TEP_TRANG_THAI
    import tempfile
    kq = []

    def thu(t, d, ct=""):
        kq.append((t, bool(d), ct))

    goc = TEP_TRANG_THAI
    tm = tempfile.mkdtemp(prefix="thu_cachly_")
    TEP_TRANG_THAI = tm + "/q.json"
    try:
        # --- phân loại ---
        thu("Q1 402 => DETERMINISTIC", phan_loai_loi("boom", 402) == "DETERMINISTIC")
        thu("Q2 'Insufficient Balance' => DETERMINISTIC",
            phan_loai_loi("Error code: 402 - Insufficient Balance") == "DETERMINISTIC")
        thu("Q3 'credit_balance_exhausted' => DETERMINISTIC",
            phan_loai_loi("429 credit_balance_exhausted") == "DETERMINISTIC",
            "429 nhung noi dung la het tien => deterministic, KHONG phai rate limit")
        thu("Q4 429 rate limit thuan => TRANSIENT",
            phan_loai_loi("rate limit exceeded", 429) == "TRANSIENT")
        thu("Q5 503 => TRANSIENT", phan_loai_loi("service unavailable", 503) == "TRANSIENT")
        thu("Q6 loi parse => KHONG_PHAI_LOI_PROVIDER",
            phan_loai_loi("json decode error") == "KHONG_PHAI_LOI_PROVIDER")
        thu("Q7 401 => DETERMINISTIC", phan_loai_loi("x", 401) == "DETERMINISTIC")

        # --- deterministic: chặn và KHÔNG hết hạn theo thời gian ---
        thu("Q8 chua co gi thi khong chan", kiem("m1") is None)
        ghi_nhan_loi("m1", "Error code: 402 - Insufficient Balance", 402, _bay_gio=1000)
        r = kiem("m1", _bay_gio=1000)
        thu("Q9 sau 402 => BI CHAN", r and r["bi_chan"] and
            r["error_type"] == "PROVIDER_QUARANTINED_DETERMINISTIC", str(r and r["error_type"]))
        thu("Q10 chan => retry=False (KHONG retry)", r and r.get("retry") is False)
        r = kiem("m1", _bay_gio=1000 + 86400 * 30)
        thu("Q11 sau 30 NGAY van BI CHAN (thoi gian khong nap tien ho)",
            r and r["bi_chan"], "van chan")

        # --- BỀN QUA RESTART: đọc lại từ đĩa ---
        thu("Q12 trang thai ghi ra DIA (ben qua restart)", os.path.exists(TEP_TRANG_THAI))
        d = json.load(io.open(TEP_TRANG_THAI, encoding="utf-8"))
        thu("Q13 doc lai tu dia thay dung model", "m1" in d and d["m1"]["loai"] == "DETERMINISTIC")

        # --- giải phóng cần bằng chứng ---
        r = giai_phong("m1")
        thu("Q14 giai phong DETERMINISTIC khong bang chung => TU CHOI",
            r.get("tu_choi") is True, r.get("ly_do", "")[:40])
        r = giai_phong("m1", bang_chung={"luot_goi_that": "200 OK", "luc": "2026-09-20"})
        thu("Q15 co bang chung => giai phong duoc", r.get("ok") and r.get("da_giai_phong") == "m1")
        thu("Q16 giai phong tra ve hang CHALLENGER, KHONG phai CORE",
            r.get("tra_ve_hang") == "CHALLENGER", r.get("tra_ve_hang"))
        thu("Q17 sau giai phong khong con bi chan", kiem("m1") is None)

        # --- transient: hết hạn theo thời gian ---
        ghi_nhan_loi("m2", "rate limit", 429, _bay_gio=2000)
        thu("Q18 transient: trong cooldown thi chan", kiem("m2", _bay_gio=2100) is not None)
        thu("Q19 transient: het cooldown thi thong",
            kiem("m2", _bay_gio=2000 + COOLDOWN_TRANSIENT_SEC + 1) is None)

        # --- đếm số lần gặp ---
        ghi_nhan_loi("m3", "402 Insufficient Balance", 402, _bay_gio=3000)
        ghi_nhan_loi("m3", "402 Insufficient Balance", 402, _bay_gio=3100)
        ghi_nhan_loi("m3", "402 Insufficient Balance", 402, _bay_gio=3200)
        thu("Q20 dem duoc so lan gap (3)", danh_sach()["m3"]["so_lan_gap"] == 3,
            str(danh_sach()["m3"]["so_lan_gap"]))

        # --- CA THẬT ngày 13/09, NGUYÊN VĂN từ `predictions.verdict_reason` ---
        # Đây là hai chuỗi ĐÃ QUAN SÁT, không phải chuỗi tự nghĩ ra. Bản đầu của bộ phân loại
        # BỎ SÓT ca gpt-5.4 vì tôi đoán chuỗi là `credit_balance_exhausted`.
        DS_THAT = ("[PERSISTED_DIAGNOSTIC_EMPTY] ERROR: DeepSeek thinking API error: "
                   "Error code: 402 - {'error': {'message': 'Insufficient Balance', "
                   "'type': 'unknown_error'}}")
        GPT_THAT = ("[PERSISTED_DIAGNOSTIC_EMPTY] ERROR: API invocation wrapper error: "
                    "Error code: 429 - {'error': {'message': 'You have no credits remaining. "
                    "Add credits to continue.'}}")
        thu("Q21 deepseek-reasoner 402 NGUYEN VAN 13/09 => DETERMINISTIC",
            phan_loai_loi(DS_THAT) == "DETERMINISTIC", phan_loai_loi(DS_THAT))
        thu("Q22 gpt-5.4 429 NGUYEN VAN 13/09 => DETERMINISTIC, KHONG phai TRANSIENT",
            phan_loai_loi(GPT_THAT, 429) == "DETERMINISTIC", phan_loai_loi(GPT_THAT, 429))
        thu("Q23 gpt-5.4: neu CHI xet ma 429 thi se sai thanh TRANSIENT — noi dung phai thang",
            phan_loai_loi("rate limit exceeded", 429) == "TRANSIENT"
            and phan_loai_loi(GPT_THAT, 429) == "DETERMINISTIC")
    finally:
        TEP_TRANG_THAI = goc
        import shutil
        shutil.rmtree(tm, ignore_errors=True)

    dat = sum(1 for _, v, _ in kq if v)
    print("=" * 92)
    print("  TỰ KIỂM _v11184_cach_ly_provider: %d/%d" % (dat, len(kq)))
    print("=" * 92)
    for t, v, ct in kq:
        print("  %s  %-60s %s" % ("DAT " if v else "HONG", t, str(ct)[:30]))
    print("=" * 92)
    return dat == len(kq)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    if "--danh-sach" in sys.argv:
        print(json.dumps(danh_sach(), ensure_ascii=False, indent=1))
        sys.exit(0)
    sys.exit(0 if tu_kiem() else 1)
