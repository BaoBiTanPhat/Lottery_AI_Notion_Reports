# -*- coding: utf-8 -*-
"""V11186b §AB-L — BÀI THỬ CỬA GỠ VỀ KHẨN CẤP CẤP 2 (alert + expiry).

RM-15: «cổng không qua thử coi như KHÔNG TỒN TẠI». Runbook gỡ về của V11186 viết cửa
CẤP 2 như một đòn bẩy có thật; trước bản này nó KHÔNG có hạn và KHÔNG có alert nhìn
thấy được. Bộ thử này chứng minh từng điều một, bằng cách giả lập vi phạm rồi xem cửa
có đóng đúng không, và khôi phục nguyên trạng sau mỗi bài.

Chạy: python _v11186_thu_khan_cap.py
"""
from __future__ import annotations

import datetime as dt
import io
import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
BE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BE)

import _v11185_roster_goi_token as R

DAT = 0
HONG = []

BIEN = ("LOTTERY_ROSTER_KHAN_CAP", "LOTTERY_ROSTER_KHAN_CAP_GIO",
        "LOTTERY_ROSTER_KHAN_CAP_HET_HAN")


def kiem(ten, dieu_kien, chi_tiet=""):
    global DAT
    if dieu_kien:
        DAT += 1
    else:
        HONG.append("%s %s" % (ten, chi_tiet))
        print("  HONG: %s %s" % (ten, chi_tiet))


class MoiTruongSach(object):
    """Đặt env + dọn tệp trạng thái, rồi TRẢ LẠI NGUYÊN TRẠNG (RM-15)."""

    def __init__(self, **env):
        self.env = env
        self.cu = {}
        self.duong = R._duong_khan_cap()
        self.noi_dung_cu = None

    def __enter__(self):
        for k in BIEN:
            self.cu[k] = os.environ.get(k)
            os.environ.pop(k, None)
        for k, v in self.env.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v
        if os.path.exists(self.duong):
            self.noi_dung_cu = io.open(self.duong, encoding="utf-8").read()
            os.remove(self.duong)
        R._DA_ALERT_KHAN_CAP["xong"] = False
        return self

    def __exit__(self, *a):
        for k, v in self.cu.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v
        if os.path.exists(self.duong):
            os.remove(self.duong)
        if self.noi_dung_cu is not None:
            with io.open(self.duong, "w", encoding="utf-8", newline="\n") as f:
                f.write(self.noi_dung_cu)
        R._DA_ALERT_KHAN_CAP["xong"] = False
        return False


class BatStderr(object):
    def __enter__(self):
        self.that = sys.stderr
        self.bo = io.StringIO()
        sys.stderr = self.bo
        return self

    def __exit__(self, *a):
        sys.stderr = self.that
        return False

    @property
    def chu(self):
        return self.bo.getvalue()


print("=" * 96)
print("  §AB-L — CUA GO VE KHAN CAP CAP 2: ALERT + EXPIRY")
print("=" * 96)

# ---------------------------------------------------------------- A. mặc định TẮT
with MoiTruongSach() as _m:
    tt = R._khan_cap_trang_thai()
    kiem("A1 mac dinh TAT", tt["bat"] is False, tt["ly_do"])
    kiem("A2 khong tao tep trang thai khi TAT", not os.path.exists(_m.duong))
    r = R.get_token_call_roster(region="MN", execution_class="official")
    kiem("A3 TAT => roster binh thuong <= tran",
         r.get("ok") and len(r["models"]) <= R.TRAN_MOI_MIEN, str(r.get("models")))
    kiem("A4 TAT => khong co canh_bao_khan_cap", "canh_bao_khan_cap" not in r)

# ---------------------------------------------------------------- B. bật, còn hạn
with MoiTruongSach(LOTTERY_ROSTER_KHAN_CAP="1") as _m:
    with BatStderr() as se:
        tt = R._khan_cap_trang_thai()
    kiem("B1 bat co => cua MO", tt["bat"] is True, tt["ly_do"])
    kiem("B2 co moc het han", bool(tt["het_han_luc"]))
    kiem("B3 han mac dinh %.0f gio" % R.KHAN_CAP_GIO_MAC_DINH,
         23.0 * 60 < (tt["con_lai_phut"] or 0) <= 24.0 * 60, str(tt["con_lai_phut"]))
    kiem("B4 ALERT ra stderr", "[ROSTER_KHAN_CAP]" in se.chu, repr(se.chu[:80]))
    kiem("B5 ALERT noi ro dang chay hanh vi truoc §AA", "TRUOC §AA" in se.chu)
    kiem("B6 co ghi tep trang thai", os.path.exists(_m.duong))
    luu = json.loads(io.open(_m.duong, encoding="utf-8").read())
    kiem("B7 tep luu bat_dau", "bat_dau" in luu, str(luu))
    r = R.get_token_call_roster(region="MN", execution_class="official")
    kiem("B8 cua MO => quay ve 8 model truoc §AA", len(r["models"]) > R.TRAN_MOI_MIEN,
         "%d model" % len(r["models"]))
    kiem("B9 roster_version doi thanh KHAN_CAP_PRE_AA", r["roster_version"] == "KHAN_CAP_PRE_AA")
    kiem("B10 dict mang canh_bao", "canh_bao" in r and "KHAN_CAP" in r["canh_bao"])
    kiem("B11 dict mang moc het han", bool(r.get("khan_cap_het_han_luc")))

# ------------------------------------------------- C. đồng hồ KHÔNG chạy lại khi restart
with MoiTruongSach(LOTTERY_ROSTER_KHAN_CAP="1") as _m:
    R._khan_cap_trang_thai()
    luu = json.loads(io.open(_m.duong, encoding="utf-8").read())
    # giả lập: đã bật từ 20 giờ trước, rồi service restart
    xua = (dt.datetime.now() - dt.timedelta(hours=20)).isoformat(timespec="seconds")
    luu["bat_dau"] = xua
    with io.open(_m.duong, "w", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(luu, ensure_ascii=False))
    tt = R._khan_cap_trang_thai()
    kiem("C1 restart KHONG dat lai dong ho", tt["bat"] is True and
         3.0 * 60 < (tt["con_lai_phut"] or 0) <= 4.0 * 60 + 1, str(tt["con_lai_phut"]))
    luu2 = json.loads(io.open(_m.duong, encoding="utf-8").read())
    kiem("C2 khong ghi de bat_dau cu", luu2["bat_dau"] == xua)

# ---------------------------------------------------------------- D. HẾT HẠN
with MoiTruongSach(LOTTERY_ROSTER_KHAN_CAP="1") as _m:
    R._khan_cap_trang_thai()
    luu = json.loads(io.open(_m.duong, encoding="utf-8").read())
    luu["bat_dau"] = (dt.datetime.now() - dt.timedelta(hours=30)).isoformat(timespec="seconds")
    with io.open(_m.duong, "w", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(luu, ensure_ascii=False))
    R._DA_ALERT_KHAN_CAP["xong"] = False
    with BatStderr() as se:
        tt = R._khan_cap_trang_thai()
    kiem("D1 qua han => cua DONG", tt["bat"] is False, tt["ly_do"])
    kiem("D2 ly do noi ro DA HET HAN", "DA HET HAN" in tt["ly_do"])
    kiem("D3 ly do nhac go co ra", "VAN CON BAT" in tt["ly_do"])
    kiem("D4 ALERT het han ra stderr", "[ROSTER_KHAN_CAP]" in se.chu and "HET HAN" in se.chu)
    r = R.get_token_call_roster(region="MN", execution_class="official")
    kiem("D5 het han => QUAY VE roster binh thuong, KHONG fail-closed",
         r.get("ok") and 0 < len(r["models"]) <= R.TRAN_MOI_MIEN, str(r.get("models")))
    kiem("D6 het han => roster_version binh thuong", r["roster_version"] == R.ROSTER_VERSION)
    kiem("D7 het han van de lai dau nhin thay duoc", "canh_bao_khan_cap" in r)

# ------------------------------------------------- E. mốc tuyệt đối do người vận hành đặt
qua_khu = (dt.datetime.now() - dt.timedelta(minutes=5)).isoformat(timespec="minutes")
tuong_lai = (dt.datetime.now() + dt.timedelta(minutes=90)).isoformat(timespec="minutes")
with MoiTruongSach(LOTTERY_ROSTER_KHAN_CAP="1",
                   LOTTERY_ROSTER_KHAN_CAP_HET_HAN=qua_khu):
    tt = R._khan_cap_trang_thai()
    kiem("E1 moc tuyet doi qua khu => DONG", tt["bat"] is False, tt["ly_do"])
with MoiTruongSach(LOTTERY_ROSTER_KHAN_CAP="1",
                   LOTTERY_ROSTER_KHAN_CAP_HET_HAN=tuong_lai) as _m:
    tt = R._khan_cap_trang_thai()
    kiem("E2 moc tuyet doi tuong lai => MO", tt["bat"] is True, tt["ly_do"])
    kiem("E3 dung dung moc do", tt["het_han_luc"].startswith(tuong_lai[:16]))
    kiem("E4 moc tuyet doi KHONG can tep trang thai", not os.path.exists(_m.duong))

# ------------------------------- F. §AB-E3: viết sai => TỪ CHỐI, không suy đoán mặc định
with MoiTruongSach(LOTTERY_ROSTER_KHAN_CAP="1",
                   LOTTERY_ROSTER_KHAN_CAP_HET_HAN="hom qua"):
    with BatStderr() as se:
        tt = R._khan_cap_trang_thai()
    kiem("F1 moc ISO sai => TU CHOI mo cua", tt["bat"] is False, tt["ly_do"])
    kiem("F2 ly do neu ro TU CHOI", "TU CHOI" in tt["ly_do"])
    kiem("F3 KHONG tu gan cua so mac dinh", tt["het_han_luc"] is None)
    kiem("F4 co ALERT", "[ROSTER_KHAN_CAP]" in se.chu)
for xau in ("khong-phai-so", "-3", "0"):
    with MoiTruongSach(LOTTERY_ROSTER_KHAN_CAP="1", LOTTERY_ROSTER_KHAN_CAP_GIO=xau):
        tt = R._khan_cap_trang_thai()
        kiem("F5 _GIO=%r => TU CHOI" % xau,
             tt["bat"] is False and "TU CHOI" in tt["ly_do"], tt["ly_do"])

# ---------------------------------------------------------------- G. số giờ hợp lệ
with MoiTruongSach(LOTTERY_ROSTER_KHAN_CAP="1", LOTTERY_ROSTER_KHAN_CAP_GIO="2"):
    tt = R._khan_cap_trang_thai()
    kiem("G1 _GIO=2 => cua so 2 gio", tt["bat"] is True and
         1.9 * 60 < (tt["con_lai_phut"] or 0) <= 2.0 * 60, str(tt["con_lai_phut"]))

# ------------------------------------------- H. tệp trạng thái hỏng => KHÔNG kéo dài vô hạn
with MoiTruongSach(LOTTERY_ROSTER_KHAN_CAP="1") as _m:
    os.makedirs(os.path.dirname(_m.duong), exist_ok=True)
    with io.open(_m.duong, "w", encoding="utf-8", newline="\n") as f:
        f.write("{khong-phai-json")
    tt = R._khan_cap_trang_thai()
    kiem("H1 tep hong => mo CUA SO MOI, khong vo han", tt["bat"] is True and
         23.0 * 60 < (tt["con_lai_phut"] or 0) <= 24.0 * 60, str(tt["con_lai_phut"]))
    kiem("H2 tep hong duoc ghi de bang ban hop le",
         "bat_dau" in json.loads(io.open(_m.duong, encoding="utf-8").read()))

# ---------------------------------------------- I. tắt cờ => dọn dấu, lần sau là cửa sổ mới
with MoiTruongSach(LOTTERY_ROSTER_KHAN_CAP="1") as _m:
    R._khan_cap_trang_thai()
    kiem("I1 dang bat thi co tep", os.path.exists(_m.duong))
    os.environ["LOTTERY_ROSTER_KHAN_CAP"] = "0"
    tt = R._khan_cap_trang_thai()
    kiem("I2 tat co => cua DONG", tt["bat"] is False)
    kiem("I3 tat co => XOA tep trang thai", not os.path.exists(_m.duong))

# ---------------------------------------------- J. alert chỉ một lần mỗi tiến trình
with MoiTruongSach(LOTTERY_ROSTER_KHAN_CAP="1"):
    with BatStderr() as se:
        R._khan_cap_trang_thai()
        R._khan_cap_trang_thai()
        R._khan_cap_trang_thai()
    kiem("J1 alert khong spam journal", se.chu.count("[ROSTER_KHAN_CAP]") == 1,
         "dem=%d" % se.chu.count("[ROSTER_KHAN_CAP]"))

# ---------------------------------------------- K. uỷ quyền tầng 2 cũng theo cửa này
with MoiTruongSach(LOTTERY_ROSTER_KHAN_CAP="1"):
    kq, ct = R.uy_quyen_goi("gemini-2.5-pro", "MN", "official", caller="thu_khan_cap")
    kiem("K1 cua MO => model ngoai roster duoc phep (dung y do disaster)",
         kq == "ALLOW", "%s %s" % (kq, ct.get("ly_do", "")))
with MoiTruongSach():
    kq, ct = R.uy_quyen_goi("gemini-2.5-pro", "MN", "official", caller="thu_khan_cap")
    kiem("K2 cua DONG => model ngoai roster bi CHAN",
         kq == "DENY_OUTSIDE_ROSTER", "%s %s" % (kq, ct.get("ly_do", "")))

# ---------------------------------------------- L. khôi phục nguyên trạng sau bộ thử
kiem("L1 khong con bien moi truong ro ri",
     all(os.environ.get(k) is None for k in BIEN),
     str({k: os.environ.get(k) for k in BIEN}))

print("-" * 96)
if HONG:
    print("  TONG §AB-L: %d DAT · %d HONG" % (DAT, len(HONG)))
    for h in HONG:
        print("   - %s" % h)
    sys.exit(1)
print("  TONG §AB-L: %d/%d DAT" % (DAT, DAT))
print("=" * 96)
