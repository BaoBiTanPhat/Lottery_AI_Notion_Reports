"""V10918 — theo dõi lớp ghi đè: phiếu bầu vs số công bố, mỗi ngày, ba miền.

## Vì sao cần bảng này

01/08 phát hiện: 37% số ngày, bạch thủ công bố KHÔNG phải số thắng phiếu bầu — 5 lớp ghi đè
chạy sau khi bỏ phiếu xong đã đổi số, và 5/6 lớp làm tệ đi (đo tiến 60 ngày:
V10913–V10916). Owner duyệt tắt 5 lớp, giữ lớp V10640 của MN.

Chuyện này lẽ ra phải lộ ra từ nhiều tháng trước. Nó không lộ vì KHÔNG CÓ CHỖ NÀO đối chiếu
"số phiếu bầu muốn chọn" với "số thực sự công bố". Bảng này lấp đúng lỗ đó: mỗi ngày, mỗi
miền, hai số đó nằm cạnh nhau, kèm ai đúng ai sai.

## Ngưỡng hành động đã ghi sẵn (không phải chờ nhớ ra)

Lớp V10640 của MN được giữ vì +14,7tr/60 ngày, NHƯNG p=0,754 tức CHƯA đạt chuẩn chắc chắn.
Ngưỡng: rà lại 2026-08-31. Nếu tính từ 2026-08-01 lớp MN âm tiền thì TẮT NỐT, không hỏi lại.
Bảng tự tính và tự kết luận `NEN_TAT` / `NEN_GIU` / `CHUA_DU_MAU` để khỏi phải nhớ.

V11195 · QD-081 6c (owner 26/11/2026): mốc 31/08 đã qua; owner chốt «âm tiền» đọc là âm SO VỚI KHÔNG
GHI ĐÈ (cộng dồn từ 01/08: +14,7tr) ⇒ GIỮ. Mốc mới: đo từ 2026-11-26, xem lại 2027-02-26; trước mốc
bảng báo `ĐANG ĐO`. Bản cũ chấm trên cửa sổ trượt 30 ngày nên in «NÊN TẮT» trái quyết định owner.

Chỉ đọc. `require_admin`, `Cache-Control: no-store`.
"""

from __future__ import annotations

import json
import math
from typing import Any, Dict, List

DIEM = 50
THU_MOI_DIEM = 98_000
GIA_MOI_DIEM = {"MN": 18_000, "MT": 18_000, "MB": 27_000}

NGAY_TAT_LOP = "2026-08-01"      # V10917 tắt 5 lớp ghi đè xấu
# V11195 · QD-081 6c (owner 26/11/2026 ~10:10 «6c --> theo khuyến nghị»): mốc 31/08 đã qua — lớp MN
# được GIỮ, đọc theo «chênh so với không ghi đè» (cộng dồn từ 01/08: +14,7tr · 7 cứu / 5 phá).
# Mốc xem lại MỚI, tính từ ngày owner quyết; trước mốc bảng chỉ báo «ĐANG ĐO», không xui tắt.
# Trước đây ngưỡng chấm trên cửa sổ TRƯỢT 30 ngày nên 26/11 bảng in «NÊN TẮT −9,8tr» —
# ngược với quyết định của owner. Cửa sổ trượt không phải luật owner duyệt.
NGAY_BAT_DAU_MOC_MN = "2026-11-26"   # QD-081 6c — bắt đầu cửa sổ đo mới
NGAY_RA_SOAT_MN = "2027-02-26"       # QD-081 6c — mốc xem lại (cũ: 2026-08-31)

# Trạng thái mong đợi sau V10917. Bảng đối chiếu với thực tế để bắt trường hợp
# ai đó bật lại mà quên báo.
CO_MONG_DOI = {
    "V10640 · MN specialist": True,
    "V10640 · MT nt_consensus": False,
    "V10640 · MB prior_region": False,
    "V10767 · MB hôm trước": False,
    "V10789 · MB luồng test": False,
    "V10790 · MT luồng test": False,
}


def _duoi(x) -> str:
    s = str(x or "").strip()
    return s.zfill(2)[-2:] if s.isdigit() else ""


def _duoi_theo_dai(con, ngay: str, mien: str) -> Dict[str, set]:
    out: Dict[str, set] = {}
    for r in con.execute(
        "SELECT station, prizes_json FROM lottery_results WHERE date=? AND region=?",
        (ngay, mien),
    ):
        s = set()
        try:
            p = json.loads(r["prizes_json"] or "{}")
        except Exception:
            p = {}
        stack = [p]
        while stack:
            n = stack.pop()
            if isinstance(n, str) and n.isdigit():
                s.add(n[-2:])
            elif isinstance(n, list):
                stack.extend(n)
            elif isinstance(n, dict):
                stack.extend(n.values())
        if s:
            out[r["station"]] = s
    return out


def _co_hien_tai() -> Dict[str, Any]:
    """Đọc cờ thật từ các module, không tin vào tài liệu."""
    ra: Dict[str, Any] = {}
    try:
        import _v10640_official_perslice_override as a
        for m in ("MN", "MT", "MB"):
            cfg = a.OVERRIDE_CONFIG.get(m) or {}
            ra[f"V10640 · {m} {cfg.get('chooser', '?')}"] = bool(cfg.get("enabled"))
    except Exception as e:
        ra["V10640 · lỗi đọc"] = str(e)[:80]
    for mod, ten, bien in (
        ("_v10767_mb_prevday_override", "V10767 · MB hôm trước",
         "_V10767_MB_PREVDAY_ENABLED"),
        ("_v10789_mb_lane_promote", "V10789 · MB luồng test",
         "_V10789_MB_LANE_PROMOTE_ENABLED"),
        ("_v10790_mt_lane_promote", "V10790 · MT luồng test",
         "_V10790_MT_LANE_PROMOTE_ENABLED"),
    ):
        try:
            ra[ten] = bool(getattr(__import__(mod), bien))
        except Exception as e:
            ra[ten] = f"lỗi: {str(e)[:60]}"
    return ra


def _sign_p(a: int, b: int):
    n = a + b
    if n == 0:
        return None
    k = max(a, b)
    return round(min(1.0, 2 * sum(math.comb(n, i) for i in range(k, n + 1)) / 2 ** n), 4)


def compute_view(con, so_ngay: int = 30) -> Dict[str, Any]:
    con.row_factory = con.row_factory or None
    rows: List[Dict[str, Any]] = []
    # V11195: nạp từ NGAY_TAT_LOP để ngưỡng lớp MN (QD-081) có đủ dữ liệu từ 26/11 và số cộng dồn
    # từ 01/08; các bảng tổng hợp vẫn chỉ tính trong cửa sổ xem `so_ngay` như trước.
    moc_xem = con.execute("SELECT date('now','localtime',?)", (f"-{so_ngay} days",)).fetchone()[0]
    for r in con.execute(
        "SELECT date, region, bach_thu, source_predictions_json FROM final_bundles "
        "WHERE status='ACTIVE' AND source_predictions_json IS NOT NULL "
        "AND date >= MIN(date('now','localtime',?), ?) ORDER BY date DESC, region",
        (f"-{so_ngay} days", NGAY_TAT_LOP),
    ):
        try:
            rn = (json.loads(r["source_predictions_json"]).get("ranked_numbers") or [])
        except Exception:
            continue
        if not rn:
            continue
        phieu = _duoi(rn[0].get("number"))
        congbo = _duoi(r["bach_thu"])
        if not phieu or not congbo:
            continue
        dai = _duoi_theo_dai(con, r["date"], r["region"])
        co_kq = bool(dai)
        h_phieu = sum(1 for v in dai.values() if phieu in v) if co_kq else None
        h_congbo = sum(1 for v in dai.values() if congbo in v) if co_kq else None
        if not co_kq:
            ket = "CHỜ KẾT QUẢ"
        elif phieu == congbo:
            ket = "KHÔNG ĐỔI"
        elif h_congbo > h_phieu:
            ket = "GHI ĐÈ CỨU"
        elif h_congbo < h_phieu:
            ket = "GHI ĐÈ PHÁ"
        else:
            ket = "GHI ĐÈ HÒA"
        rows.append({
            "ngay": r["date"], "mien": r["region"],
            "so_phieu_bau": phieu, "so_cong_bo": congbo,
            "co_ghi_de": phieu != congbo,
            "trung_phieu": h_phieu, "trung_cong_bo": h_congbo,
            "so_dai": len(dai) if co_kq else None,
            "ket_cuc": ket,
            "sau_khi_tat_lop": r["date"] >= NGAY_TAT_LOP,
            "trong_cua_so_xem": r["date"] >= moc_xem,
        })

    def _gom(lc):
        s = [x for x in rows if lc(x) and x["ket_cuc"] != "CHỜ KẾT QUẢ"]
        if not s:
            return None
        von = sum(DIEM * GIA_MOI_DIEM[x["mien"]] * (x["so_dai"] or 0) for x in s)
        tp = sum((x["trung_phieu"] or 0) for x in s) * DIEM * THU_MOI_DIEM
        tc = sum((x["trung_cong_bo"] or 0) for x in s) * DIEM * THU_MOI_DIEM
        cuu = sum(1 for x in s if x["ket_cuc"] == "GHI ĐÈ CỨU")
        pha = sum(1 for x in s if x["ket_cuc"] == "GHI ĐÈ PHÁ")
        return {
            "so_luot": len(s),
            "so_lan_ghi_de": sum(1 for x in s if x["co_ghi_de"]),
            "cuu": cuu, "pha": pha,
            "hoa": sum(1 for x in s if x["ket_cuc"] == "GHI ĐÈ HÒA"),
            "p": _sign_p(cuu, pha),
            "lai_neu_theo_phieu_tr": round((tp - von) / 1e6, 1),
            "lai_thuc_te_tr": round((tc - von) / 1e6, 1),
            "chenh_tr": round((tc - tp) / 1e6, 1),
        }

    tong = _gom(lambda x: x["trong_cua_so_xem"])
    theo_mien = {m: _gom(lambda x, r=m: x["mien"] == r and x["trong_cua_so_xem"]) for m in ("MN", "MT", "MB")}
    sau_tat = _gom(lambda x: x["sau_khi_tat_lop"] and x["trong_cua_so_xem"])

    # --- Ngưỡng hành động cho lớp V10640 của MN — V11195 · QD-081 6c ---
    # Luật owner duyệt: GIỮ; đọc theo chênh so với không ghi đè, tính từ NGAY_BAT_DAU_MOC_MN; tới
    # NGAY_RA_SOAT_MN mới kết luận: âm ⇒ NÊN TẮT · dương/hoà ⇒ NÊN GIỮ · chưa có lần ghi đè nào ⇒
    # CHƯA ĐỦ MẪU (gia hạn 3 tháng). Trước mốc: ĐANG ĐO — không phải tín hiệu tắt.
    mn_sau = _gom(lambda x: x["mien"] == "MN" and x["ngay"] >= NGAY_BAT_DAU_MOC_MN)
    mn_tich_luy = _gom(lambda x: x["mien"] == "MN" and x["sau_khi_tat_lop"])
    hom_nay = con.execute("SELECT date('now','localtime')").fetchone()[0]
    nen = (f"cộng dồn từ {NGAY_TAT_LOP}: {mn_tich_luy['chenh_tr']:+}tr "
           f"({mn_tich_luy['cuu']} cứu / {mn_tich_luy['pha']} phá)") if mn_tich_luy else "chưa có dữ liệu cộng dồn"
    dang = (f"từ {NGAY_BAT_DAU_MOC_MN}: {mn_sau['chenh_tr']:+}tr sau {mn_sau['so_luot']} ngày "
            f"({mn_sau['so_lan_ghi_de']} lần ghi đè · {mn_sau['cuu']} cứu / {mn_sau['pha']} phá)"
            ) if mn_sau else f"từ {NGAY_BAT_DAU_MOC_MN}: chưa có ngày nào có kết quả"
    if hom_nay < NGAY_RA_SOAT_MN:
        mn_ket = "ĐANG ĐO"
        mn_ly_do = (f"QD-081 (owner 26/11/2026): GIỮ lớp MN, đọc theo chênh so với không ghi đè · {dang} · "
                    f"{nen} · mốc xem lại {NGAY_RA_SOAT_MN} — chưa tới mốc, KHÔNG tắt")
    elif not mn_sau or mn_sau["so_lan_ghi_de"] == 0:
        mn_ket = "CHƯA ĐỦ MẪU"
        mn_ly_do = f"{dang} · chưa có lần ghi đè nào để chấm ⇒ gia hạn 3 tháng (QD-081)"
    elif mn_sau["chenh_tr"] < 0:
        mn_ket = "NÊN TẮT"
        mn_ly_do = (f"{dang} · âm so với không ghi đè ⇒ đặt OVERRIDE_CONFIG['MN']['enabled']=False "
                    f"(ngưỡng FU-183 owner duyệt trước, đọc theo QD-081)")
    else:
        mn_ket = "NÊN GIỮ"
        mn_ly_do = f"{dang} · không âm so với không ghi đè ⇒ giữ (QD-081)"

    co = _co_hien_tai()
    lech_co = [{"lop": k, "dang_la": co.get(k), "mong_doi": v}
               for k, v in CO_MONG_DOI.items()
               if k in co and co.get(k) is not v]

    return {
        "version": "V10918",
        "tieu_de": "Phiếu bầu vs số công bố — theo dõi lớp ghi đè",
        "ngay_tat_lop": NGAY_TAT_LOP,
        "ngay_ra_soat_mn": NGAY_RA_SOAT_MN,
        "co_hien_tai": co,
        "lech_co": lech_co,
        "canh_bao_co": (
            f"⚠ {len(lech_co)} lớp khác trạng thái đã duyệt — có người bật lại?"
            if lech_co else "✓ đúng trạng thái đã duyệt V10917"),
        "tong": tong,
        "theo_mien": theo_mien,
        "sau_khi_tat_lop": sau_tat,
        "nguong_mn": {"ket_luan": mn_ket, "ly_do": mn_ly_do, "so_lieu": mn_sau,
                      "cong_don_tu_01_08": mn_tich_luy, "bat_dau_moc": NGAY_BAT_DAU_MOC_MN,
                      "quyet_dinh": "QD-081 6c"},
        "bang": [x for x in rows if x["trong_cua_so_xem"]][:45],
        "ghi_chu": (
            "Số phiếu bầu = số thắng cuộc bỏ phiếu của các model (ranked_numbers[0] trong "
            "bundle). Số công bố = bạch thủ thật trên /du-doan. Hai số khác nhau nghĩa là "
            "một lớp ghi đè đã đổi số. Bằng chứng gốc: artifacts/v10914_per_layer.json, "
            "v10915_chain.json, v10916_significance.json."),
    }
