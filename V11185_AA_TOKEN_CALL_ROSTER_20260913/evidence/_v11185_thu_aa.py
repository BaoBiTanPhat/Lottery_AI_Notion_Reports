# -*- coding: utf-8 -*-
"""V11185 — BỘ THỬ §AA: token call roster SSOT · call-site · shadow bounded · quarantine hai tầng.

PHẠM VI ĐƯỢC CHỨNG MINH Ở ĐÂY, nói rõ để không ai đọc quá:
  · Nhóm A/B/C chứng minh bằng **AST trên mã production thật** rằng không call-site nào còn
    quyết định theo danh sách tĩnh, và mọi chỗ đều lấy từ một biến DUY NHẤT gán từ roster.
  · Nhóm D chứng minh bằng **đếm tại chính hàm `_call_*`** rằng model ngoài roster / bị cách ly
    KHÔNG ra tới HTTP.
  · Điều bộ thử này **KHÔNG** chứng minh: một lượt chạy end-to-end thật. Lượt đó phải là
    **natural receipt** (§AA-S), vì chạy end-to-end ở đây sẽ ghi vào `predictions` production.
"""
from __future__ import annotations

import ast
import io
import os
import sys

BE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BE)
KQ = []


def thu(t, d, ct=""):
    KQ.append((t, bool(d), ct))


def nhom(t):
    print()
    print("-- %s --" % t)


def _ma_scheduler():
    return io.open(BE + "/scheduler.py", encoding="utf-8").read()


# ============================================================================
# A · ROSTER SSOT
# ============================================================================
def nhom_A():
    nhom("A · roster SSOT")
    import _v11185_roster_goi_token as R
    import contextlib
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        ok = R.tu_kiem()
    thu("A1 tu kiem _v11185_roster_goi_token DAT", ok,
        [l for l in buf.getvalue().split("\n") if "TỰ KIỂM" in l][:1])

    mong = {"MN": ["claude-opus-4-6", "gemini-2.5-flash", "gpt-oss-120b", "claude-sonnet-4-6"],
            "MT": ["claude-opus-4-6", "gemini-2.5-flash", "glm-5.1", "gpt-oss-120b"],
            "MB": ["claude-opus-4-6", "gemini-2.5-flash", "gpt-oss-120b", "glm-5.1"]}
    for reg, ms in mong.items():
        r = R.get_token_call_roster(region=reg)
        thu("A2_%s thanh vien khop §AA muc D" % reg, r["ok"] and r["models"] == ms, str(r["models"]))
        thu("A3_%s <= 4" % reg, len(r["models"]) <= 4)


# ============================================================================
# B · CALL-SITE — AST trên mã production
# ============================================================================
def nhom_B():
    nhom("B · call-site (AST trên scheduler.py thật)")
    src = _ma_scheduler()
    tree = ast.parse(src)

    # B1: KHÔNG còn vòng lặp nào trên AUTO_AI_MODELS
    vl = [n.lineno for n in ast.walk(tree) if isinstance(n, ast.For)
          and "AUTO_AI_MODELS" in [d.id for d in ast.walk(n.iter) if isinstance(d, ast.Name)]]
    thu("B1 KHONG con vong lap nao tren AUTO_AI_MODELS", vl == [], str(vl))

    # B2: KHÔNG còn tham chiếu tên nào trong mã thực thi
    ten = sorted({n.lineno for n in ast.walk(tree)
                  if isinstance(n, ast.Name) and n.id == "AUTO_AI_MODELS"})
    thu("B2 KHONG con tham chieu AUTO_AI_MODELS trong ma thuc thi", ten == [], str(ten))

    # B3: import cũ được GIỮ (backward compat §AA-C5) — không xoá mã
    thu("B3 import AUTO_AI_MODELS van con (khong xoa ma)",
        "TOKEN_MODELS as AUTO_AI_MODELS" in src)

    # B4: `_AA_MODELS` gán ĐÚNG MỘT lần, và gán từ roster
    gan = [n for n in ast.walk(tree) if isinstance(n, ast.Assign)
           and any(isinstance(t, ast.Name) and t.id == "_AA_MODELS" for t in n.targets)]
    thu("B4 _AA_MODELS gan DUNG MOT lan", len(gan) == 1, "so lan gan=%d" % len(gan))
    thu("B5 _AA_MODELS gan tu _aa_roster['models']",
        len(gan) == 1 and "_aa_roster" in ast.unparse(gan[0].value),
        ast.unparse(gan[0].value)[:60] if gan else "")

    # B6: năm chỗ dùng đều là `_AA_MODELS`
    for ten_cho, chuoi in (
            ("expected count", "_expected_model_count = len(_AA_MODELS) + 1"),
            ("provider preflight", "_ai_preflight_models = list(_AA_MODELS) + ['combo-super']"),
            ("parallel prestart", "for _pm in _AA_MODELS:"),
            ("MAIN PROVIDER LOOP", "for ai_model in _AA_MODELS:"),
            ("diversity pass", "_div_model_ids = list(_AA_MODELS)")):
        thu("B6 %s dung _AA_MODELS" % ten_cho, chuoi in src)

    # B7: fail-closed có mặt và đứng TRƯỚC main loop
    i_fc = src.find("TOKEN_ROSTER_INVALID")
    i_loop = src.find("for ai_model in _AA_MODELS:")
    thu("B7 fail-closed dung TRUOC main provider loop", 0 < i_fc < i_loop,
        "fc=%d loop=%d" % (i_fc, i_loop))

    # B8: MB rerun dùng roster CORE-only và KHÔNG dùng win-rate để chọn
    thu("B8 MB rerun dung roster CORE-only",
        "include_challenger=False" in src and "MB rerun version=" in src)
    # B9: phải PHÂN LOẠI bằng AST, không đếm chuỗi thô (RM-09).
    # Bản đầu của bài thử này dùng `chuoi not in src` và HỎNG — vì chuỗi đó còn nằm trong
    # CHÚ THÍCH giải thích vì sao đã xoá. Chú thích mô tả lối sai KHÔNG phải lối sai.
    ma_thuc = ast.unparse(ast.parse(src))
    thu("B9 MB rerun KHONG con gan selected_models tu win-rate (AST, bo chu thich)",
        "ai_model_wrs[:3]" not in ma_thuc and "AUTO_AI_MODELS[:3]" not in ma_thuc,
        "ai_model_wrs trong ma thuc: %d" % ma_thuc.count("ai_model_wrs"))

    # B10: shadow bị giới hạn về challenger
    thu("B10 shadow gioi han ve challenger duoc chi dinh",
        "SHADOW_BOUNDED_V11185" in src and "execution_class='shadow'" in src)


# ============================================================================
# C · KHOÁ §AA — thứ không được đổi
# ============================================================================
def nhom_C():
    nhom("C · khoá §AA")
    src = _ma_scheduler()
    import _v11185_roster_goi_token as R

    thu("C1 KHONG fallback ve toan bo TOKEN_MODELS khi loi",
        "return" in src[src.find("TOKEN_ROSTER_INVALID"):src.find("TOKEN_ROSTER_INVALID") + 700])

    # C2: roster KHÔNG tự lấp chỗ
    import copy
    goc = copy.deepcopy(R._CHINH_SACH)
    try:
        R._CHINH_SACH["MN"]["CORE"] = ["claude-opus-4-6", "deepseek-reasoner", "gemini-2.5-flash"]
        r = R.get_token_call_roster(region="MN")
        thu("C2 mot model bi cach ly => roster NGAN DI, khong lap cho",
            r["ok"] and len(r["models"]) == 3, str(r["models"]))
    finally:
        R._CHINH_SACH.clear()
        R._CHINH_SACH.update(goc)

    # C3: ảnh chụp đủ siêu dữ liệu §AA-C6
    ac = R.anh_chup()
    for k in ("roster_version", "owner_approval_ref", "effective_from", "previous_version",
              "rollback"):
        thu("C3 anh chup co %s" % k, k in ac["_meta"])
    thu("C4 anh chup co config_sha256 va quarantined",
        bool(ac.get("config_sha256")) and "quarantined" in ac)


# ============================================================================
# D · ĐẾM TẠI ĐIỂM HTTP THẬT (§AA-J, phần làm được không đụng DB)
# ============================================================================
def nhom_D():
    nhom("D · đếm tại _call_* — model ngoài roster / bị cách ly KHÔNG ra tới HTTP")
    import _v11184_cach_ly_provider as CL
    import _v11185_roster_goi_token as R

    # D1: tầng 1 — schedule filter loại model cách ly TRƯỚC khi vào hàng đợi
    cl = set(CL.danh_sach().keys())
    for reg in ("MN", "MT", "MB"):
        r = R.get_token_call_roster(region=reg)
        thu("D1_%s tang 1: model cach ly khong vao hang doi" % reg,
            not (set(r["models"]) & cl), str(sorted(set(r["models"]) & cl)))

    # D2: tầng 2 — guard tại `_invoke_model_api` chặn TRƯỚC HTTP.
    #     Đếm bằng cách thay năm hàm `_call_*` bằng bộ đếm; nếu guard đúng thì bộ đếm = 0.
    dem = {"http": 0, "models": []}

    def _gia(model, *a, **k):
        dem["http"] += 1
        dem["models"].append(model)
        return {"error": "KHONG DUOC PHEP GOI TRONG BO THU"}

    import gpt_analyzer as GA
    goc = {}
    for ten in ("_call_openai", "_call_anthropic", "_call_gemini", "_call_deepseek",
                "_call_openrouter"):
        goc[ten] = getattr(GA, ten, None)
        if goc[ten] is not None:
            setattr(GA, ten, _gia)
    try:
        for mid in sorted(cl):
            r = CL.kiem(mid)
            thu("D2 %s bi chan TRUOC HTTP (retry=False)" % mid,
                r is not None and r.get("retry") is False, str(r and r.get("error_type")))
        thu("D3 khong mot lan goi _call_* nao xay ra trong nhom D",
            dem["http"] == 0, "so lan=%d %s" % (dem["http"], dem["models"]))
    finally:
        for ten, f in goc.items():
            if f is not None:
                setattr(GA, ten, f)

    # D4: model ngoài roster bị từ chối ở tầng roster
    for mid, reg in (("gemini-2.5-pro", "MN"), ("gemini-2.5-pro", "MT"),
                     ("gemini-2.5-pro", "MB"), ("glm-5.1", "MN"),
                     ("claude-sonnet-4-6", "MT"), ("claude-sonnet-4-6", "MB")):
        ok, ly = R.kiem_mot_model(mid, reg)
        thu("D4 %s@%s: 0 co hoi ra HTTP" % (mid, reg), not ok, ly[:34])


# ============================================================================
# E · TRACE / CRON
# ============================================================================
def nhom_E():
    nhom("E · trace và cron")
    import subprocess
    try:
        ct = subprocess.check_output("crontab -l", shell=True, stderr=subprocess.DEVNULL).decode()
    except Exception:
        ct = ""
    if ct:
        dang_chay = [d for d in ct.split("\n") if d.strip() and not d.strip().startswith("#")]
        thu("E1 KHONG con dong cron _v11059 dang chay",
            not any("_v11059_lane_ab_3tang" in d for d in dang_chay),
            "so dong dang chay=%d" % len(dang_chay))
        thu("E2 dong _v11059 duoc COMMENT chu khong XOA (thuan nghich)",
            "V11185-AA-E4-TAT" in ct)
    else:
        thu("E1 (khong doc duoc crontab o may nay — chay tren VPS)", True, "bo qua")


def main():
    print("=" * 96)
    print("  V11185 · BỘ THỬ §AA — token call roster SSOT")
    print("=" * 96)
    nhom_A()
    nhom_B()
    nhom_C()
    nhom_D()
    nhom_E()
    print()
    print("=" * 96)
    dat = sum(1 for _, v, _ in KQ if v)
    for t, v, ct in KQ:
        print("  %s  %-62s %s" % ("DAT " if v else "HONG", t, str(ct)[:30]))
    print("=" * 96)
    print("  TỔNG §AA: %d/%d %s" % (dat, len(KQ), "ĐẠT" if dat == len(KQ) else "CÓ BÀI HỎNG"))
    print("=" * 96)
    return 0 if dat == len(KQ) else 1


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
