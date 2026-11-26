# -*- coding: utf-8 -*-
"""V11197 · Đợt 2a dọn dẹp — dừng 5 dòng cron phép đo đã có phán quyết (comment, KHÔNG xoá). Chạy TRÊN VPS.

Mỗi dòng phải chứa đúng tên script mong đợi, không thì DỪNG. Ghi bản cũ ra backups/ trước.
    python3 /tmp/dung_cron_v11197.py            # THỬ: in diff, không cài
    python3 /tmp/dung_cron_v11197.py --cai      # CÀI
Gỡ về: crontab /root/Lottery_AI_Test/backups/crontab.pre_v11197.txt
"""
import difflib
import os
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8")
SAO_LUU = "/root/Lottery_AI_Test/backups/crontab.pre_v11197.txt"
MOI = "/tmp/crontab_v11197.txt"
DUNG = {  # số dòng (đếm từ 1 trong `crontab -l`) → (script phải có, lý do)
    131: ("_v10984_ghep_lane_official.py", "FU-264 KHÔNG ĐẠT — 5 cách ghép đều dưới ngưỡng, cần thêm ~578 ngày"),
    132: ("_v11017_bay_dan_shadow.py", "FU-287 ĐẠT — phân tán 0,47 → 0,61; chạy tay lại sau lần đổi prompt (FU-461)"),
    133: ("_v11018_ma_doi_chung.py", "FU-317 KHÔNG CÓ LỢI THẾ — 3 nguồn 43,2% vs 1 nguồn 43,1%, z +0,04"),
    134: ("_v11037_g2mb_lane.py", "FU-367 KHÔNG CÓ — đo tiến 109/60 ngày, 9/9 mức không đạt"),
    142: ("_v11089_cham_lane_tb.py", "FU-398 KHÔNG ĐẠT — |z| 0,76 < 1,96; lane nguồn tắt từ 13/09, 470/470 dòng đã chấm"),
}

cu = subprocess.run(["crontab", "-l"], capture_output=True, text=True, check=True).stdout
dong = cu.split("\n")
for so, (ten, _) in DUNG.items():
    d = dong[so - 1]
    if ten not in d or d.lstrip().startswith("#"):
        print(f"✗ DỪNG: dòng {so} không phải dòng đang bật của {ten}: {d[:120]}")
        sys.exit(1)
moi_dong = list(dong)
for so, (ten, ly_do) in DUNG.items():
    moi_dong[so - 1] = f"# V11197 DỪNG 26/11 ({ly_do}) | " + dong[so - 1]
moi = "\n".join(moi_dong)
bat_cu = sum(1 for d in dong if d.strip() and not d.lstrip().startswith("#"))
bat_moi = sum(1 for d in moi_dong if d.strip() and not d.lstrip().startswith("#"))
khac = [i + 1 for i, (a, b) in enumerate(zip(dong, moi_dong)) if a != b]
print(f"dòng đang bật: {bat_cu} → {bat_moi} · dòng đổi: {khac} · tổng số dòng giữ nguyên: {len(dong)} = {len(moi_dong)}")
for l in difflib.unified_diff(dong, moi_dong, "cu", "moi", lineterm="", n=0):
    print(l[:230])
assert khac == sorted(DUNG) and bat_moi == bat_cu - len(DUNG) and len(dong) == len(moi_dong)
if "--cai" not in sys.argv:
    print("(THỬ — chưa cài)")
    sys.exit(0)
if not os.path.exists(SAO_LUU):
    open(SAO_LUU, "w", encoding="utf-8").write(cu)
    print("✓ sao lưu:", SAO_LUU)
open(MOI, "w", encoding="utf-8").write(moi)
subprocess.run(["crontab", MOI], check=True)
sau = subprocess.run(["crontab", "-l"], capture_output=True, text=True, check=True).stdout
print("✓ đã cài · crontab -l khớp bản mới:", sau == moi)
sys.exit(0 if sau == moi else 2)
