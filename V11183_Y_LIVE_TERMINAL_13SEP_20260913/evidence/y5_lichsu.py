# -*- coding: utf-8 -*-
"""V11183 §Y5 — LICH SU weights tu optimizer_once.log + DIEN LAI cong de xuat.
CHI DOC + CHI IN. Khong ghi gi vao production.
"""
import re, io, sys
sys.stdout.reconfigure(encoding="utf-8")
P = "/root/Lottery_AI_Test/web/backend/logs/optimizer_once.log"
txt = io.open(P, encoding="utf-8", errors="replace").read()

# moi lan chay ghi dong: "<ISO> <REGION> DONE <n> s best_lift= <x>"
lan = re.findall(r"^(\d{4}-\d{2}-\d{2}T[\d:.]+)\s+(MN|MT|MB)\s+DONE\s+(\d+)\s+s\s+best_lift=\s*([+-]?[\d.]+)", txt, re.M)
saved = re.findall(r"\[OPTIMIZER\] Saved learned weights for (MN|MT|MB): (\{[^}]*\})", txt)

print("=" * 100)
print("LICH SU OPTIMIZER (tu logs/optimizer_once.log) — %d lan chay ghi nhan, %d lan GHI weights" % (len(lan), len(saved)))
print("=" * 100)
print("%-22s %-4s %8s %10s %-14s" % ("thoi diem", "mien", "giay", "best_lift", "cong_de_xuat"))
print("-" * 100)
n_am = n_duong = 0
theo_mien = {}
for ts, reg, gy, lf in lan:
    lf = float(lf)
    quyet = "GHI (hien tai)" if lf > -50 else "TU CHOI"
    de_xuat = "TU CHOI" if lf <= 0 else "GHI"
    if lf <= 0: n_am += 1
    else: n_duong += 1
    theo_mien.setdefault(reg, []).append((ts[:19], lf))
    print("%-22s %-4s %8s %+10.2f %-14s" % (ts[:19], reg, gy, lf, de_xuat))
print("-" * 100)
print("TONG: %d lan chay · %d lan best_lift <= 0 (%.0f%%) · %d lan > 0" % (len(lan), n_am, 100.0*n_am/max(len(lan),1), n_duong))
print()
print("CONG HIEN TAI  (best_lift > -50) : GHI %d/%d lan = %.0f%%" % (len(lan), len(lan), 100.0))
print("CONG DE XUAT   (best_lift > 0)   : GHI %d/%d lan = %.0f%%  => chan %d lan ghi de vo ich/co hai"
      % (n_duong, len(lan), 100.0*n_duong/max(len(lan),1), n_am))
print()
print("=" * 100)
print("THEO MIEN — best_lift qua cac lan")
print("=" * 100)
for reg in ("MN", "MT", "MB"):
    r = theo_mien.get(reg, [])
    if not r: continue
    am = sum(1 for _, x in r if x <= 0)
    print("%-4s: %d lan · %d lan <= 0 (%.0f%%) · day du: %s"
          % (reg, len(r), am, 100.0*am/len(r), ", ".join("%s=%+.2f" % (t[:10], x) for t, x in r)))
print()
print("=" * 100)
print("GIA TRI WEIGHTS DA GHI (theo thu tu trong log) — dung de ROLLBACK")
print("=" * 100)
for reg, w in saved:
    print("%-4s %s" % (reg, w))
