# -*- coding: utf-8 -*-
"""V11183 §Y5/§Y10-C — CỔNG GHI LEARNED WEIGHTS.

VÌ SAO CÓ TỆP NÀY — ba khuyết tật ĐO ĐƯỢC trong `weight_optimizer.py`, ngày 13/09/2026:

  D1 NỀN SAI THƯỚC (`weight_optimizer.py:141,148,162`)
     `total_actual += len(actual_tails)` — `backtester.get_actual_tails` trả list CÓ TRÙNG
     và còn cộng thêm `tail_db`/`tail_g8` vốn ĐÃ nằm trong `prizes_json`. Đo ngày 13/09 trên
     cửa sổ 2026-07-14→2026-09-12: MN đếm 63,0 đuôi/ngày trong khi số đuôi KHÁC NHAU là 43,1;
     MT 48,5 vs 35,1; MB 29,0 vs 23,6. Nền `1-(1-b)^3` do đó phồng +12,70 / +12,46 / +8,36 điểm,
     và `lift = win_rate - random_chance` bị HẠ đúng chừng ấy. Hệ quả: mọi con số lift của
     optimizer đều âm giả tạo.
     ĐỐI CHỨNG TRONG CHÍNH KHO: `stat_weight_optimizer.py:90` làm ĐÚNG — `actual_set =
     set(actual_tails)` rồi `total_possible += len(actual_set)`. Hai module, một sai một đúng,
     và cái SAI là cái ghi weights production.

  D2 NỀN CÓ-HOÀN-LẠI CHO PHÉP CHỌN KHÔNG-HOÀN-LẠI (`weight_optimizer.py:164`)
     top-3 là 3 đuôi KHÁC NHAU ⇒ nền đúng là `1 - C(100-M,3)/C(100,3)`, không phải
     `1-(1-M/100)^3`. Chênh nhỏ (~0,3-0,8 điểm) nhưng luôn cùng một chiều: nền thật CAO hơn.

  D3 CỔNG GHI KHÔNG PHẢI LÀ CỔNG (`weight_optimizer.py:441`)
     `if save_weights and result['best_lift'] > -50:` — ngưỡng -50 nghĩa là hầu như mọi kết quả
     đều ghi. Đo lịch sử `logs/optimizer_once.log`: 6/6 lần chạy đều GHI (100%). Cổng này
     KHÔNG so với control, KHÔNG có held-out, KHÔNG kiểm ý nghĩa, và KHÔNG chỉnh cho việc
     `best_lift` là GIÁ TRỊ LỚN NHẤT của 69 ước lượng trong mẫu — thứ luôn dương-thiên-vị.

TỆP NÀY KHÔNG TỰ TRIỂN KHAI. Nó là bản cài đặt tham chiếu + bộ chứng minh cổng chặn được
(RM-15), để dựng gói quyết định cho Owner. Nó KHÔNG ghi `app_settings`, KHÔNG gọi
`save_learned_weights`, KHÔNG sửa `weight_optimizer.py`.
"""
from __future__ import annotations

import json
import os
import sqlite3
import sys
from math import comb, sqrt

BE = os.path.dirname(os.path.abspath(__file__))
GOC = os.path.dirname(os.path.dirname(BE))
DB = GOC + "/data/lottery_ai.db"

# Ngưỡng cổng — khai báo TƯỜNG MINH, không giấu trong biểu thức.
TOI_THIEU_NGAY_HELDOUT = 30      # dưới mức này: chưa được phép kết luận (RM-04)
MUC_Y_NGHIA = 0.05
CONTROL_MAC_DINH = {"convergence": 0.35, "trend": 0.25, "gan": 0.20, "recency": 0.20}


# ----------------------------------------------------------------------------
# NỀN ĐÚNG
# ----------------------------------------------------------------------------
def nen_khong_hoan_lai(m_khac, k, n=100):
    """P(ít nhất 1 trong k đuôi KHÁC NHAU trúng) khi ngày đó có m_khac đuôi khác nhau.

    Đây là nền ĐÚNG cho phép chọn top-k. `1-(1-m/n)^k` là bản CÓ hoàn lại và luôn THẤP hơn,
    tức làm lift trông ĐẸP hơn thực tế.
    """
    if m_khac <= 0:
        return 0.0
    if n - m_khac < k:
        return 1.0
    return 1.0 - comb(n - m_khac, k) / comb(n, k)


def duoi_khac_nhau_theo_ngay(con, region, tu, den):
    """{ngày: số đuôi-2 KHÁC NHAU} — đọc thẳng prizes_json, KHÔNG dùng get_actual_tails.

    Cố ý không tái dùng `get_actual_tails`: chính nó là nguồn của D1, và nó được 20 nơi khác
    gọi nên sửa nó sẽ lan rộng. Sửa đúng chỗ là ở nơi ĐẾM, không ở nơi TRẢ VỀ.
    """
    def _so(o, ra):
        if isinstance(o, str):
            ra.append(o)
        elif isinstance(o, list):
            for x in o:
                _so(x, ra)
        elif isinstance(o, dict):
            for x in o.values():
                _so(x, ra)

    ra = {}
    cur = con.execute(
        "SELECT substr(date,1,10), prizes_json FROM lottery_results "
        "WHERE region=? AND substr(date,1,10) BETWEEN ? AND ?", (region, tu, den))
    for d, pj in cur.fetchall():
        acc = []
        _so(json.loads(pj), acc)
        s = ra.setdefault(d, set())
        for x in acc:
            if x.isdigit() and len(x) >= 2:
                s.add(x[-2:])
    return {d: len(s) for d, s in ra.items()}


# ----------------------------------------------------------------------------
# KIỂM ĐỊNH
# ----------------------------------------------------------------------------
def poisson_binomial(ps):
    dp = [1.0]
    for p in ps:
        moi = [0.0] * (len(dp) + 1)
        for i, v in enumerate(dp):
            if v:
                moi[i] += v * (1.0 - p)
                moi[i + 1] += v * p
        dp = moi
    return dp


def p_tren(ps, k):
    """P(X >= k). Mỗi ngày một p riêng ⇒ Poisson-binomial, KHÔNG phải nhị thức."""
    dp = poisson_binomial(ps)
    return sum(dp[max(k, 0):])


def chinh_cho_phep_chon(p, n_to_hop):
    """Sidak: `best_lift` là MAX của n_to_hop ước lượng trong mẫu ⇒ p thô là p của ứng viên
    TỐT NHẤT, không phải của một ứng viên định trước. Bỏ bước này là `PRJ_WINDOW_LEAK`."""
    if n_to_hop <= 1:
        return p
    return 1.0 - (1.0 - p) ** n_to_hop


# ----------------------------------------------------------------------------
# CỔNG
# ----------------------------------------------------------------------------
def cong_ghi_weights(ung_vien, control, n_to_hop_da_thu,
                     toi_thieu_ngay=TOI_THIEU_NGAY_HELDOUT, muc=MUC_Y_NGHIA):
    """Quyết định CÓ được ghi bộ weights ứng viên vào production không.

    `ung_vien` / `control` mỗi cái là dict:
        n_ngay      số ngày HELD-OUT (ngoài cửa sổ đã fit)
        thang       số ngày có ít nhất 1 trong top-3 trúng
        nen_tung_ngay  [p_d] — nền KHÔNG hoàn lại, tính từ số đuôi KHÁC NHAU của chính ngày đó

    Trả dict có `quyet` ∈:
        GHI
        TU_CHOI_KHONG_CO_HELDOUT
        TU_CHOI_MAU_QUA_NHO
        TU_CHOI_KHONG_HON_CONTROL
        TU_CHOI_KHONG_CO_Y_NGHIA_SAU_CHINH_CHON
    Quyết định và lý do tách rời — một lý do một dòng, không gộp.
    """
    ra = {"quyet": None, "ly_do": [], "so": {}}

    if not ung_vien or not ung_vien.get("nen_tung_ngay"):
        ra["quyet"] = "TU_CHOI_KHONG_CO_HELDOUT"
        ra["ly_do"].append("khong co cua so held-out: moi lift deu la TRONG MAU")
        return ra

    n = ung_vien["n_ngay"]
    if n < toi_thieu_ngay:
        ra["quyet"] = "TU_CHOI_MAU_QUA_NHO"
        ra["ly_do"].append("n_heldout=%d < %d: chua duoc phep ket luan (RM-04)" % (n, toi_thieu_ngay))
        ra["so"]["n_heldout"] = n
        return ra

    ps = ung_vien["nen_tung_ngay"]
    k = ung_vien["thang"]
    ky_vong = sum(ps)
    lift_uv = 100.0 * (k / n) - 100.0 * (ky_vong / n)
    p_tho = p_tren(ps, k)
    p_chinh = chinh_cho_phep_chon(p_tho, n_to_hop_da_thu)

    lift_ct = None
    if control and control.get("nen_tung_ngay"):
        lift_ct = (100.0 * control["thang"] / control["n_ngay"]
                   - 100.0 * sum(control["nen_tung_ngay"]) / control["n_ngay"])

    ra["so"] = {"n_heldout": n, "thang": k, "ky_vong": round(ky_vong, 2),
                "lift_ung_vien_pp": round(lift_uv, 2),
                "lift_control_pp": (round(lift_ct, 2) if lift_ct is not None else None),
                "p_tho": round(p_tho, 6), "n_to_hop_da_thu": n_to_hop_da_thu,
                "p_sau_chinh_chon": round(p_chinh, 6), "muc_y_nghia": muc}

    if lift_ct is not None and lift_uv <= lift_ct:
        ra["quyet"] = "TU_CHOI_KHONG_HON_CONTROL"
        ra["ly_do"].append("lift ung vien %+.2fpp KHONG hon control %+.2fpp tren cung held-out"
                           % (lift_uv, lift_ct))
        return ra

    if p_chinh >= muc:
        ra["quyet"] = "TU_CHOI_KHONG_CO_Y_NGHIA_SAU_CHINH_CHON"
        ra["ly_do"].append("p tho %.5f -> sau chinh cho %d lan chon la %.5f, khong duoi %.3f"
                           % (p_tho, n_to_hop_da_thu, p_chinh, muc))
        return ra

    ra["quyet"] = "GHI"
    ra["ly_do"].append("hon control %+.2fpp va p sau chinh chon %.5f < %.3f"
                       % (lift_uv - (lift_ct or 0.0), p_chinh, muc))
    return ra


# ----------------------------------------------------------------------------
# TỰ KIỂM — RM-15: cổng không qua thử coi như KHÔNG TỒN TẠI
# ----------------------------------------------------------------------------
def tu_kiem():
    kq = []

    def ghi(ten, dat):
        kq.append((ten, bool(dat)))

    # --- nền ---
    # M=0 -> 0 ; M=100 -> 1
    ghi("nen M=0 bang 0", abs(nen_khong_hoan_lai(0, 3)) < 1e-12)
    ghi("nen M=100 bang 1", abs(nen_khong_hoan_lai(100, 3) - 1.0) < 1e-12)
    # tinh tay: N=100,M=43,k=3 -> 1 - C(57,3)/C(100,3) = 1 - 29260/161700
    tay = 1.0 - 29260.0 / 161700.0
    ghi("nen M=43 k=3 khop tinh tay", abs(nen_khong_hoan_lai(43, 3) - tay) < 1e-12)
    # nen KHONG hoan lai phai LON HON ban co hoan lai
    ghi("nen khong-hoan-lai > co-hoan-lai",
        nen_khong_hoan_lai(43, 3) > 1 - (1 - 0.43) ** 3)

    # --- Poisson-binomial ---
    ghi("PB p deu = nhi thuc", abs(p_tren([0.5] * 3, 2) - 0.5) < 1e-12)
    ghi("PB p khac nhau", abs(p_tren([0.2, 0.8], 2) - 0.16) < 1e-12)
    ghi("PB P(X>=0)=1", abs(p_tren([0.1, 0.9], 0) - 1.0) < 1e-12)

    # --- chinh cho phep chon ---
    ghi("chinh chon n=1 khong doi", abs(chinh_cho_phep_chon(0.01, 1) - 0.01) < 1e-12)
    ghi("chinh chon n=69 lam p to len", chinh_cho_phep_chon(0.01, 69) > 0.4)

    # --- CONG PHAI CHAN ---
    nen50 = [0.5] * 60
    # vi pham 1: khong co held-out
    ghi("chan: khong co held-out",
        cong_ghi_weights({}, None, 69)["quyet"] == "TU_CHOI_KHONG_CO_HELDOUT")
    # vi pham 2: mau qua nho
    ghi("chan: mau qua nho",
        cong_ghi_weights({"n_ngay": 7, "thang": 7, "nen_tung_ngay": [0.5] * 7}, None, 69)["quyet"]
        == "TU_CHOI_MAU_QUA_NHO")
    # vi pham 3: khong hon control
    uv = {"n_ngay": 60, "thang": 33, "nen_tung_ngay": nen50}
    ct = {"n_ngay": 60, "thang": 40, "nen_tung_ngay": nen50}
    ghi("chan: khong hon control",
        cong_ghi_weights(uv, ct, 69)["quyet"] == "TU_CHOI_KHONG_HON_CONTROL")
    # vi pham 4: hon control nhung khong co y nghia sau chinh chon
    # CHON THAM SO CO CHU Y: thang=38/60 voi nen 0,5 cho p tho ~0,026 — DUOI 0,05,
    # nen neu cong cho qua thi la do THIEU buoc chinh chon, khong phai do p tho lon.
    # (Ban dau to dat thang=36 -> p tho ~0,077, vot da truot nguong san => bai thu MU.)
    uv2 = {"n_ngay": 60, "thang": 38, "nen_tung_ngay": nen50}
    ct2 = {"n_ngay": 60, "thang": 30, "nen_tung_ngay": nen50}
    r4 = cong_ghi_weights(uv2, ct2, 69)
    ghi("chan: khong y nghia sau chinh chon",
        r4["quyet"] == "TU_CHOI_KHONG_CO_Y_NGHIA_SAU_CHINH_CHON")
    # sach: hon control VA co y nghia manh
    uv3 = {"n_ngay": 60, "thang": 48, "nen_tung_ngay": nen50}
    ct3 = {"n_ngay": 60, "thang": 30, "nen_tung_ngay": nen50}
    r5 = cong_ghi_weights(uv3, ct3, 69)
    ghi("cho qua: sach thi GHI", r5["quyet"] == "GHI")
    # cung mot ung vien do, neu KHONG chinh cho phep chon thi cong cu se cho qua
    # -> chung minh buoc chinh chon THUC SU co tac dung, khong phai trang tri
    ghi("chinh chon THUC SU doi ket qua",
        cong_ghi_weights(uv2, ct2, 1)["quyet"] == "GHI")

    dat = sum(1 for _, v in kq if v)
    print("=" * 78)
    print("TU KIEM _v11183_cong_optimizer: %d/%d" % (dat, len(kq)))
    print("=" * 78)
    for ten, v in kq:
        print("  %s  %s" % ("PASS" if v else "FAIL", ten))
    return dat == len(kq)


def dien_lai_lich_su():
    """Diễn lại quyết định của cổng HIỆN TẠI vs cổng NÀY trên lịch sử đã ghi.

    CHỈ ĐỌC log + app_settings. Không gọi lại optimizer, không ghi gì.
    """
    import re
    p = BE + "/logs/optimizer_once.log"
    if not os.path.exists(p):
        print("(khong co %s tren may nay — chay tren VPS)" % p)
        return
    txt = open(p, encoding="utf-8", errors="replace").read()
    lan = re.findall(r"^(\d{4}-\d{2}-\d{2}T[\d:.]+)\s+(MN|MT|MB)\s+DONE\s+\d+\s+s\s+best_lift=\s*([+-]?[\d.]+)",
                     txt, re.M)
    print()
    print("=" * 78)
    print("DIEN LAI: cong HIEN TAI (best_lift > -50) vs cong NAY")
    print("=" * 78)
    print("%-21s %-4s %10s %-16s %-34s" % ("thoi diem", "mien", "best_lift", "cong_HIEN_TAI", "cong_NAY"))
    print("-" * 78)
    for ts, reg, lf in lan:
        # Cổng này TỪ CHỐI mọi lần chạy hiện có, vì không lần nào có held-out.
        r = cong_ghi_weights({}, None, 69)
        print("%-21s %-4s %+10s %-16s %-34s" % (ts[:19], reg, lf, "GHI", r["quyet"]))
    print("-" * 78)
    print("Ket luan dien lai: 0/%d lan chay hien co qua duoc cong nay — vi KHONG lan nao" % len(lan))
    print("co cua so held-out. Day la khuyet tat QUY TRINH, khong phai khuyet tat cua mot lan chay.")


def main():
    ok = tu_kiem()
    dien_lai_lich_su()
    print()
    print("LUU Y: tep nay KHONG sua weight_optimizer.py va KHONG ghi app_settings.")
    print("No la ban cai dat tham chieu cho goi quyet dinh Owner (§Y10 nhanh C).")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
