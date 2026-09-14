# -*- coding: utf-8 -*-
"""V11187 §AB-D/§AB-E — THỬ NGƯỢC: bản vá §AB có chặn ĐÚNG lượt đã xảy ra thật hôm nay không?

RM-15: cổng chưa thử coi như KHÔNG TỒN TẠI. Nhưng có một mức mạnh hơn bài thử tổng hợp —
**dựng lại đúng sự cố ĐÃ XẢY RA TRONG SẢN XUẤT** rồi xem bản vá có chặn không.

SỰ CỐ THẬT (14/09, dưới V11185):
    Combo Super MB 17:33:05 → 17:33:43 gọi `gemini-2.5-pro` (NGOÀI roster MB) chạm HTTP 200.
    Receipt: `MB_ROSTER_LIVE_PROOF_FAIL`, trượt "outside-roster HTTP = 0" và "≤ 4 model".

Bài thử này KHÔNG gọi provider (§AB-K). Nó hỏi ba câu trên mã ĐÃ VÁ:
    T1 · tầng uỷ quyền có DENY `gemini-2.5-pro` @MB lớp `combo_super` không?
    T2 · pool của Combo sau khi giao với roster có còn `gemini-2.5-pro` không?
    T3 · lượt Combo ở MN (`claude-opus-4-6`, trong roster) có được ALLOW không —
         tức bản vá chặn ĐÚNG thứ phải chặn, không chặn bừa?
Và hai câu đối chứng:
    T4 · cả bốn model roster MB đều ALLOW (không chặn oan chuỗi chính).
    T5 · model bị cách ly vẫn bị chặn, và bị chặn vì LÝ DO ĐÚNG.

Chạy: python _v11187_thu_chan_su_co_mb.py
"""
from __future__ import annotations

import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
BE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BE)

import _v11185_roster_goi_token as R

DAT = 0
HONG = []

# Đúng những gì trace ghi lại ngày 14/09.
SU_CO = {"model": "gemini-2.5-pro", "mien": "MB", "lop": "combo_super",
         "caller": "combo_super.run_combo_super", "luc": "17:33:07"}
LUOT_MN = {"model": "claude-opus-4-6", "mien": "MN", "lop": "combo_super"}
ROSTER_MB_THAT = ["claude-opus-4-6", "gemini-2.5-flash", "gpt-oss-120b", "glm-5.1"]


def kiem(ten, dieu_kien, chi_tiet=""):
    global DAT
    if dieu_kien:
        DAT += 1
        print("  DAT   %-58s %s" % (ten, chi_tiet))
    else:
        HONG.append(ten)
        print("  HONG  %-58s %s" % (ten, chi_tiet))


print("=" * 100)
print("  THU NGUOC SU CO THAT: Combo Super @MB goi gemini-2.5-pro luc 17:33:07 ngay 14/09")
print("=" * 100)

# ------------------------------------------------------------------ T1
kq, ct = R.uy_quyen_goi(SU_CO["model"], SU_CO["mien"], SU_CO["lop"],
                        caller=SU_CO["caller"])
kiem("T1 uy quyen DENY dung luot da xay ra", kq == "DENY_OUTSIDE_ROSTER",
     "%s · %s" % (kq, ct.get("ly_do", "")))
kiem("T1b ly do la NGOAI ROSTER, khong phai cach ly",
     kq == "DENY_OUTSIDE_ROSTER" and "cach ly" not in str(ct.get("ly_do", "")).lower(),
     str(ct.get("ly_do", ""))[:70])

# ------------------------------------------------------------------ T2
r = R.get_token_call_roster(region="MB", execution_class="combo_super",
                            include_challenger=True)
kiem("T2 roster MB cho lop combo_super doc duoc", bool(r.get("ok")), str(r.get("ma_loi")))
kiem("T2b gemini-2.5-pro KHONG nam trong danh sach cho phep",
     SU_CO["model"] not in (r.get("models") or []), str(r.get("models")))
kiem("T2c danh sach cho phep dung bang roster MB that",
     sorted(r.get("models") or []) == sorted(ROSTER_MB_THAT), str(sorted(r.get("models") or [])))

# Mô phỏng đúng phép giao mà `combo_super.py` đã vá thực hiện: pool gốc ∩ roster.
POOL_COMBO_V11185 = ["claude-sonnet-4-6", "gemini-2.5-flash", "claude-opus-4-6",
                     "gemini-2.5-pro", "deepseek-reasoner", "glm-5.1", "gpt-oss-120b",
                     "gemini-3.5-flash", "gemini-3.6-flash"]
cho_phep = set(r.get("models") or [])
sau_giao = [m for m in POOL_COMBO_V11185 if m in cho_phep]
kiem("T2d pool Combo sau khi giao KHONG con gemini-2.5-pro",
     SU_CO["model"] not in sau_giao, str(sau_giao))
kiem("T2e pool Combo sau khi giao KHONG con model bi cach ly nao",
     not (set(sau_giao) & set(r.get("quarantined") or [])), str(r.get("quarantined")))
kiem("T2f pool Combo sau khi giao KHONG rong (khong chan oan ca Combo)",
     len(sau_giao) >= 1, "%d model: %s" % (len(sau_giao), sau_giao))

# ------------------------------------------------------------------ T3
kq3, ct3 = R.uy_quyen_goi(LUOT_MN["model"], LUOT_MN["mien"], LUOT_MN["lop"],
                          caller="combo_super.run_combo_super")
kiem("T3 luot Combo @MN (trong roster) van duoc ALLOW", kq3 == "ALLOW",
     "%s · %s" % (kq3, ct3.get("ly_do", "")))

# ------------------------------------------------------------------ T4
for m in ROSTER_MB_THAT:
    k, c = R.uy_quyen_goi(m, "MB", "official", caller="scheduler.main_loop")
    kiem("T4 chuoi chinh MB: %s ALLOW" % m, k == "ALLOW", "%s %s" % (k, c.get("ly_do", "")))

# ------------------------------------------------------------------ T5
cach_ly = list(r.get("quarantined") or [])
if cach_ly:
    m = cach_ly[0]
    k, c = R.uy_quyen_goi(m, "MB", "combo_super", caller="combo_super.run_combo_super")
    kiem("T5 model bi cach ly (%s) van bi chan" % m, k.startswith("DENY"), k)
    kiem("T5b chan vi ly do DUNG (cach ly hoac ngoai roster)",
         k in ("DENY_QUARANTINED", "DENY_OUTSIDE_ROSTER"), k)
else:
    kiem("T5 co du lieu cach ly de thu", False,
         "khong doc duoc trang thai cach ly — dong bo data/provider_quarantine.json tu VPS")

# ------------------------------------------------------------------ T6 fail-closed
k6, c6 = R.uy_quyen_goi(SU_CO["model"], None, "combo_super", caller="x")
kiem("T6 thieu target_region => DENY_INVALID_CONTEXT (khong suy doan)",
     k6 == "DENY_INVALID_CONTEXT", k6)
k7, c7 = R.uy_quyen_goi(SU_CO["model"], "MB", None, caller="x")
kiem("T6b thieu execution_class => DENY_INVALID_CONTEXT", k7 == "DENY_INVALID_CONTEXT", k7)

print("-" * 100)
if HONG:
    print("  KET LUAN: %d DAT · %d HONG — BAN VA CHUA CHAN DUOC SU CO THAT" % (DAT, len(HONG)))
    for h in HONG:
        print("   - %s" % h)
    sys.exit(1)
print("  KET LUAN: %d/%d DAT — ban va §AB CHAN DUNG luot da xay ra that, va KHONG chan oan" % (DAT, DAT))
print("  LUU Y: day la chung minh TREN MA DA VA o repo. No KHONG phai bang chung runtime.")
print("         Bang chung runtime chi co sau khi deploy + mot luot MB tu nhien ngay 15/09.")
print("=" * 100)
