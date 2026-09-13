# -*- coding: utf-8 -*-
"""V11184 §Z-I — INTAKE MODEL MỚI CÓ HẠN ĐỊNH. Chống lỗi thời, chống "đo tiếp" vô hạn.

VÌ SAO CÓ TỆP NÀY: §Z cấm kết thúc bằng «cần đo thêm» nếu không kèm ĐỦ BỐN thứ — dữ liệu còn
thiếu chính xác, người/tiến trình chịu trách nhiệm, hạn cuối, và terminal BẮT BUỘC khi tới hạn.
Viết thành mã thay vì văn xuôi để nó **cưỡng chế được**: hàm `terminal_bat_buoc()` KHÔNG BAO GIỜ
trả về "continue measuring" — tới hạn là phải có nhãn dứt khoát.

CÁC MỐC (§Z mục I, nguyên văn khoá Owner):
  Day 0–2   availability · API/contract/parser · latency · token/cost · contamination
            · ZERO production influence
  Day 3–7   low-budget shadow · tối đa MỘT challenger slot/miền · không chạy hàng loạt
  Day 14    PROVISIONAL_CHALLENGER | REGION_ONLY | RETIRE          ← cấm để trống
  Day 28    CORE | SHADOW (có lý do đặc biệt + hạn cuối) | RETIRE  ← cấm để trống

TỆP NÀY KHÔNG GỌI PROVIDER và KHÔNG ghi DB. Nó là bộ luật + bộ kiểm.
"""
from __future__ import annotations

import sys
from datetime import date, timedelta

# Nhãn hợp lệ — khai TƯỜNG MINH để cổng dò được, cấm đặt nhãn mới tuỳ tiện
TERMINAL_D14 = ("PROVISIONAL_CHALLENGER", "REGION_ONLY", "RETIRE")
TERMINAL_D28 = ("CORE", "SHADOW", "RETIRE")
TERMINAL_MODEL = ("CORE", "REGION_ONLY", "CHALLENGER", "SHADOW", "QUARANTINE", "RETIRE")

# Cụm từ BỊ CẤM ở mọi terminal. Đây là danh sách đen, không phải lời khuyên.
CUM_TU_CAM = ("continue measuring", "cần đo thêm", "can do them", "đo tiếp", "do tiep",
              "wait data", "WAIT_DATA", "tbd", "TBD", "chờ thêm", "cho them")

GIAI_DOAN = (
    (0, 2, "SANG_LOC_KY_THUAT", "availability · API/contract/parser · latency · token/cost · "
                                "contamination · KHONG anh huong production"),
    (3, 7, "SHADOW_NGAN_SACH_THAP", "toi da MOT challenger slot/mien · khong chay hang loat"),
    (8, 13, "TICH_LUY_TRUOC_D14", "gom du lieu cho quyet dinh D14"),
    (14, 27, "DA_CO_TERMINAL_D14", "phai da mang mot trong %s" % (TERMINAL_D14,)),
    (28, 10 ** 6, "DA_CO_TERMINAL_D28", "phai da mang mot trong %s" % (TERMINAL_D28,)),
)


def giai_doan(ngay_nhan: str, hom_nay: str):
    """Model nhận ngày `ngay_nhan` thì hôm nay đang ở giai đoạn nào (ISO date)."""
    d0 = date.fromisoformat(ngay_nhan)
    dn = date.fromisoformat(hom_nay)
    tuoi = (dn - d0).days
    for tu, den, ten, mo_ta in GIAI_DOAN:
        if tu <= tuoi <= den:
            return {"tuoi_ngay": tuoi, "giai_doan": ten, "mo_ta": mo_ta,
                    "han_D14": (d0 + timedelta(days=14)).isoformat(),
                    "han_D28": (d0 + timedelta(days=28)).isoformat()}
    return {"tuoi_ngay": tuoi, "giai_doan": "TRUOC_KHI_NHAN", "mo_ta": "",
            "han_D14": (d0 + timedelta(days=14)).isoformat(),
            "han_D28": (d0 + timedelta(days=28)).isoformat()}


def terminal_bat_buoc(ngay_nhan: str, hom_nay: str, terminal_hien_tai=None):
    """Tới hạn thì PHẢI có nhãn. Hàm này không bao giờ cho phép để trống.

    Trả `{'bat_buoc': bool, 'moc': 'D14'|'D28'|None, 'hop_le': [...], 'vi_pham': str|None}`.
    """
    g = giai_doan(ngay_nhan, hom_nay)
    tuoi = g["tuoi_ngay"]
    ra = {"tuoi_ngay": tuoi, "giai_doan": g["giai_doan"], "bat_buoc": False,
          "moc": None, "hop_le": [], "vi_pham": None,
          "han_D14": g["han_D14"], "han_D28": g["han_D28"]}

    if tuoi >= 28:
        ra.update({"bat_buoc": True, "moc": "D28", "hop_le": list(TERMINAL_D28)})
    elif tuoi >= 14:
        ra.update({"bat_buoc": True, "moc": "D14", "hop_le": list(TERMINAL_D14)})
    else:
        return ra

    t = (terminal_hien_tai or "").strip()
    if not t:
        ra["vi_pham"] = ("qua moc %s (%d ngay) ma KHONG co terminal — day chinh la vong "
                         "'do tiep' ma §Z cam" % (ra["moc"], tuoi))
        return ra
    thap = t.lower()
    for c in CUM_TU_CAM:
        if c.lower() in thap:
            ra["vi_pham"] = "terminal chua cum tu BI CAM %r — phai la nhan dut khoat" % c
            return ra
    if t not in ra["hop_le"]:
        ra["vi_pham"] = "terminal %r khong thuoc %s" % (t, ra["hop_le"])
    return ra


def kiem_ho_so(ho_so, hom_nay):
    """Soát một danh sách model đang intake. Trả các mục VI PHẠM — rỗng nghĩa là sạch.

    `ho_so` = [{'model':..., 'ngay_nhan': 'YYYY-MM-DD', 'terminal': ... , 'mien': ...}, ...]
    """
    vi_pham = []
    for h in ho_so:
        r = terminal_bat_buoc(h.get("ngay_nhan"), hom_nay, h.get("terminal"))
        if r["vi_pham"]:
            vi_pham.append({"model": h.get("model"), "mien": h.get("mien"),
                            "tuoi_ngay": r["tuoi_ngay"], "moc": r["moc"],
                            "terminal": h.get("terminal"), "vi_pham": r["vi_pham"],
                            "han_D14": r["han_D14"], "han_D28": r["han_D28"]})
    return vi_pham


def dieu_kien_thay_incumbent():
    """Sáu điều kiện §Z đòi khi model mới muốn thay model đang chạy. Trả dạng máy kiểm được."""
    return [
        ("tot_hon_theo_mien", "phai tot hon TREN CHINH MIEN do, khong duoc gop ba mien"),
        ("reliability_du", "coverage >= nguong Gate 1, khong co loi deterministic"),
        ("marginal_tot_hon", "net rescue-minus-break tot hon incumbent"),
        ("cost_hop_ly", "cost tren mot lan rescue khong te hon dang ke"),
        ("khong_mat_diversity", "khong lam giam so HO NGUON DOC LAP cua mien do"),
        ("qua_replay_va_rollback", "replay cung ngay/mien + rollback proof chay duoc"),
    ]


def tu_kiem():
    kq = []

    def thu(t, d, ct=""):
        kq.append((t, bool(d), ct))

    # I1–I5 giai đoạn
    thu("I1 ngay 0 => SANG_LOC_KY_THUAT",
        giai_doan("2026-09-13", "2026-09-13")["giai_doan"] == "SANG_LOC_KY_THUAT")
    thu("I2 ngay 5 => SHADOW_NGAN_SACH_THAP",
        giai_doan("2026-09-13", "2026-09-18")["giai_doan"] == "SHADOW_NGAN_SACH_THAP")
    thu("I3 ngay 14 => DA_CO_TERMINAL_D14",
        giai_doan("2026-09-13", "2026-09-27")["giai_doan"] == "DA_CO_TERMINAL_D14")
    thu("I4 ngay 28 => DA_CO_TERMINAL_D28",
        giai_doan("2026-09-13", "2026-10-11")["giai_doan"] == "DA_CO_TERMINAL_D28")
    thu("I5 han D14/D28 tinh dung",
        giai_doan("2026-09-13", "2026-09-13")["han_D14"] == "2026-09-27"
        and giai_doan("2026-09-13", "2026-09-13")["han_D28"] == "2026-10-11")

    # I6–I8 chưa tới hạn thì không bắt buộc
    r = terminal_bat_buoc("2026-09-13", "2026-09-20", None)
    thu("I6 ngay 7 chua bat buoc terminal", r["bat_buoc"] is False and r["vi_pham"] is None)

    # I9–I13 tới hạn D14
    r = terminal_bat_buoc("2026-09-13", "2026-09-27", None)
    thu("I7 D14 khong co terminal => VI PHAM", r["bat_buoc"] and r["vi_pham"])
    r = terminal_bat_buoc("2026-09-13", "2026-09-27", "PROVISIONAL_CHALLENGER")
    thu("I8 D14 + PROVISIONAL_CHALLENGER => hop le", r["vi_pham"] is None)
    r = terminal_bat_buoc("2026-09-13", "2026-09-27", "CORE")
    thu("I9 D14 + CORE => VI PHAM (CORE chi hop le tu D28)", bool(r["vi_pham"]), r["vi_pham"])

    # I10–I12 CỤM TỪ BỊ CẤM — đây là điều §Z nhấn mạnh nhất
    for cam in ("continue measuring", "cần đo thêm", "WAIT_DATA", "TBD"):
        r = terminal_bat_buoc("2026-09-13", "2026-09-27", cam)
        thu("I10 D14 + %r => VI PHAM (cum tu bi cam)" % cam, bool(r["vi_pham"]))

    # I13–I15 D28
    r = terminal_bat_buoc("2026-09-13", "2026-10-11", "CORE")
    thu("I11 D28 + CORE => hop le", r["vi_pham"] is None)
    r = terminal_bat_buoc("2026-09-13", "2026-10-11", "PROVISIONAL_CHALLENGER")
    thu("I12 D28 + PROVISIONAL_CHALLENGER => VI PHAM (phai chot CORE/SHADOW/RETIRE)",
        bool(r["vi_pham"]))
    r = terminal_bat_buoc("2026-09-13", "2026-10-11", None)
    thu("I13 D28 khong terminal => VI PHAM", bool(r["vi_pham"]))

    # I14 soát hồ sơ
    vp = kiem_ho_so([
        {"model": "a", "ngay_nhan": "2026-09-13", "terminal": None, "mien": "MN"},
        {"model": "b", "ngay_nhan": "2026-08-01", "terminal": None, "mien": "MT"},
        {"model": "c", "ngay_nhan": "2026-08-01", "terminal": "CORE", "mien": "MB"},
        {"model": "d", "ngay_nhan": "2026-08-01", "terminal": "continue measuring", "mien": "MN"},
    ], "2026-09-13")
    thu("I14 soat ho so bat dung 2 vi pham (b thieu terminal, d dung cum tu cam)",
        len(vp) == 2 and {v["model"] for v in vp} == {"b", "d"},
        str([v["model"] for v in vp]))

    # I15 điều kiện thay incumbent đủ sáu
    thu("I15 du SAU dieu kien thay incumbent", len(dieu_kien_thay_incumbent()) == 6)

    # I16 nhãn terminal model khớp §Z (đúng sáu nhãn)
    thu("I16 dung SAU nhan terminal model",
        set(TERMINAL_MODEL) == {"CORE", "REGION_ONLY", "CHALLENGER", "SHADOW",
                                "QUARANTINE", "RETIRE"})

    dat = sum(1 for _, v, _ in kq if v)
    print("=" * 92)
    print("  TỰ KIỂM _v11184_intake_model: %d/%d" % (dat, len(kq)))
    print("=" * 92)
    for t, v, ct in kq:
        print("  %s  %-64s %s" % ("DAT " if v else "HONG", t, str(ct)[:28]))
    print("=" * 92)
    return dat == len(kq)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(0 if tu_kiem() else 1)
