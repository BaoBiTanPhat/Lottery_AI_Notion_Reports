# -*- coding: utf-8 -*-
"""V11196 · Đợt 1 dọn dẹp — dừng 4 dòng cron hết việc (comment, KHÔNG xoá). Chạy TRÊN VPS.

Mỗi dòng phải chứa đúng tên script mong đợi, không thì DỪNG. Ghi bản cũ ra backups/ trước.
    python3 /tmp/dung_cron_v11196.py            # THỬ: in diff, không cài
    python3 /tmp/dung_cron_v11196.py --cai      # CÀI
Gỡ về: crontab /root/Lottery_AI_Test/backups/crontab.pre_v11196.txt
"""
import difflib
import os
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8")
SAO_LUU = "/root/Lottery_AI_Test/backups/crontab.pre_v11196.txt"
MOI = "/tmp/crontab_v11196.txt"
DUNG = {  # số dòng (đếm từ 1 trong `crontab -l`) → (script phải có, lý do)
    17: ("_v10661_live_edge_monitor.py", "bảng live_edge_monitor không ai đọc ngoài chính tệp"),
    56: ("_perpos_matrix_report.py", "báo cáo .md không ai đọc"),
    82: ("_v10784_verify_0607.py", "phép kiểm chỉ cho ngày 06/07 — skip mỗi ngày từ 07/07"),
    141: ("_v11067_lay_mau_khoa_db.py", "FU-402 đã đủ mẫu (112.007 mẫu · 1% khoá); chính nó giữ khoá ghi mỗi 5 giây — bật lại khi thử bản vá"),
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
    moi_dong[so - 1] = f"# V11196 DỪNG 26/11 ({ly_do}) | " + dong[so - 1]
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
