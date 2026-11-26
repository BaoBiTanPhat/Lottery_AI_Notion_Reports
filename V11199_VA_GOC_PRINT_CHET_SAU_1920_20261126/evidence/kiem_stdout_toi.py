# -*- coding: utf-8 -*-
"""V11199 — kiểm tối 26/11: sau 19:20 print của service CÒN tới journal, và không còn «closed file». CHỈ ĐỌC. Chạy trên VPS."""
import sqlite3
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8")


def dem_journal(tu, den, mau=None):
    out = subprocess.run(["journalctl", "-u", "lottery", "--since", tu, "--until", den, "--no-pager", "-o", "cat"],
                         capture_output=True, text=True).stdout.splitlines()
    log = [l for l in out if " - INFO - " in l or " - WARNING - " in l or " - ERROR - " in l]
    in_ra = [l for l in out if l not in log]
    if mau:
        return sum(1 for l in out if mau in l)
    return len(out), len(log), len(in_ra)


c = sqlite3.connect("file:/root/Lottery_AI_Test/data/lottery_ai.db?mode=ro", uri=True, timeout=60)
for ngay in ("2026-11-25", "2026-11-26"):
    tong, log, in_ra = dem_journal(f"{ngay} 19:21", f"{ngay} 21:00")
    closed_j = dem_journal(f"{ngay} 19:18", f"{ngay} 23:59", "closed file")
    # scheduler_logs lưu UTC naive: 19:18 VN = 12:18 UTC
    closed_s = c.execute("SELECT COUNT(*) FROM scheduler_logs WHERE log_time >= ? AND log_time < ? AND message LIKE '%closed file%'",
                         (f"{ngay} 12:18:00", f"{ngay} 16:59:59")).fetchone()[0]
    print(f"{ngay}: journal 19:21–21:00 = {tong} dòng (logging {log} · print {in_ra}) · 'closed file' journal {closed_j} · scheduler_logs {closed_s}")
print("MainPID:", subprocess.run(["systemctl", "show", "-p", "MainPID", "--value", "lottery"], capture_output=True, text=True).stdout.strip())
