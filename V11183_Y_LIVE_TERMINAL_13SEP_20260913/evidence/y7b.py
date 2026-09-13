# -*- coding: utf-8 -*-
"""V11183 §Y7/§Y8 (ban sua) — TACH HAI TANG.
SUA hai loi cua ban truoc:
  (a) Fraction DP bung no voi ~6000 phep => dung float DP.
  (b) Cac duoi trong pool la rut KHONG HOAN LAI tu cung tap 100 => phan phoi dung la SIEU BOI
      theo tung ngay, roi tich chap qua cac ngay. Bernoulli doc lap la SAI GRAIN (RM-18).
"""
import json, sqlite3, sys
from math import comb
sys.stdout.reconfigure(encoding="utf-8")
DB = "/root/Lottery_AI_Test/data/lottery_ai.db"; CHOT = "2026-09-13"

def sieu_boi(N, M, K):
    """P(X=i) cho rut K tu N, M la so 'trung'."""
    lo, hi = max(0, K - (N - M)), min(K, M)
    tong = comb(N, K)
    return lo, [comb(M, i) * comb(N - M, K - i) / tong for i in range(lo, hi + 1)]

def tich_chap(phan_phoi):
    """Tich chap nhieu phan phoi roi rac. Moi phan tu = (offset, [p...])."""
    off, dp = 0, [1.0]
    for o, ps in phan_phoi:
        moi = [0.0] * (len(dp) + len(ps) - 1)
        for i, a in enumerate(dp):
            if a:
                for j, b in enumerate(ps):
                    if b: moi[i + j] += a * b
        dp = moi; off += o
    return off, dp

def duoi_tren(off, dp, k):
    i = k - off
    tren = sum(dp[max(i, 0):]) if i < len(dp) else 0.0
    duoi = sum(dp[:min(i + 1, len(dp))]) if i >= 0 else 0.0
    return tren, duoi

def pb_float(ps):
    dp = [1.0]
    for p in ps:
        moi = [0.0] * (len(dp) + 1)
        for i, v in enumerate(dp):
            if v: moi[i] += v * (1 - p); moi[i + 1] += v * p
        dp = moi
    return dp

def so_trong(o, ra):
    if isinstance(o, str): ra.append(o)
    elif isinstance(o, list):
        for x in o: so_trong(x, ra)
    elif isinstance(o, dict):
        for x in o.values(): so_trong(x, ra)

con = sqlite3.connect("file:" + DB + "?mode=ro", uri=True); c = con.cursor()
c.execute("SELECT substr(date,1,10), region, prizes_json FROM lottery_results WHERE substr(date,1,10) <= ?", (CHOT,))
duoi2 = {}
for d, reg, pj in c.fetchall():
    ra = []; so_trong(json.loads(pj), ra)
    s = duoi2.setdefault((d, reg), set())
    for x in ra:
        if x.isdigit() and len(x) >= 2: s.add(x[-2:])
c.execute("SELECT date, region, bach_thu, created_at FROM final_bundles WHERE date <= ? AND status='ACTIVE'", (CHOT,))
bundles = {(d, r): (bt, ca) for d, r, bt, ca in c.fetchall()}
c.execute("SELECT date, target_region, main_numbers, created_at, run_source FROM predictions WHERE date <= ?", (CHOT,))
pool = {}; bo_shadow = bo_muon = giu = 0
for d, reg, mn, ca, rs in c.fetchall():
    if rs == "shadow_auto_eval": bo_shadow += 1; continue
    b = bundles.get((d, reg))
    if not b: continue
    if ca.replace("T", " ")[:19] > b[1][:19]: bo_muon += 1; continue
    giu += 1
    try: nums = json.loads(mn)
    except Exception: continue
    s = pool.setdefault((d, reg), set())
    for x in nums:
        x = str(x).strip()
        if x.isdigit() and len(x) == 2: s.add(x)
con.close()
print("LOC PRJ-SELECTION-WINDOW-001: bo %d danh-gia-lai · bo %d tao-sau-khi-chot · giu %d" % (bo_shadow, bo_muon, giu))
print()

t1 = {}; t2 = {}; phu = {}
for (d, reg), pl in pool.items():
    tails = duoi2.get((d, reg)); b = bundles.get((d, reg))
    if not tails or not b or not pl: continue
    tr = len([x for x in pl if x in tails])
    t1.setdefault(reg, []).append((tr, len(pl), len(tails)))
    phu.setdefault(reg, []).append(1 if tr > 0 else 0)
    if b[0] in pl:
        t2.setdefault(reg, []).append((1 if b[0] in tails else 0, tr / len(pl)))

print("=" * 110)
print("TANG 1 — GENERATOR: pool ung vien co hon boc ngau nhien khong?")
print("Nen dung = SIEU BOI tung ngay (rut |pool| duoi KHAC NHAU tu 100, M_d trung), tich chap qua cac ngay.")
print("=" * 110)
print("%-4s %6s %8s %10s %11s %11s %10s %10s %9s" % ("mien","n_ngay","pool_TB","phu_kin","trung_that","trung_nen","p_HON","p_KEM","z"))
print("-" * 110)
for reg in ("MN", "MT", "MB"):
    r = t1.get(reg)
    if not r: continue
    n = len(r); that = sum(x[0] for x in r)
    pps = [sieu_boi(100, M, K) for _, K, M in r]
    off, dp = tich_chap(pps)
    ky = sum(i + off for i, p in enumerate(dp)) if False else sum((i + off) * p for i, p in enumerate(dp))
    var = sum(((i + off) ** 2) * p for i, p in enumerate(dp)) - ky ** 2
    tren, duoi = duoi_tren(off, dp, that)
    z = (that - ky) / (var ** 0.5) if var > 0 else 0.0
    print("%-4s %6d %8.1f %9.1f%% %11d %11.1f %10.4f %10.4f %+9.2f"
          % (reg, n, sum(x[1] for x in r) / n, 100.0 * sum(phu[reg]) / n, that, ky, tren, duoi, z))
print("-" * 110)
print()
print("=" * 110)
print("TANG 2 — RANKER/SELECTOR: bach_thu co hon BOC NGAU NHIEN TU CHINH POOL khong?")
print("(chi ngay bach_thu THUC SU nam trong pool; nen rieng tung ngay = trung_trong_pool/|pool|)")
print("=" * 110)
NG = 0.05 / 6
print("%-4s %5s %6s %9s %9s %11s %11s %-22s" % ("mien","n","trung","ty_le","nen_TB","p_HON","p_KEM","ket_luan"))
print("-" * 110)
for reg in ("MN", "MT", "MB"):
    r = t2.get(reg)
    if not r: continue
    ps = [p for _, p in r]; h = sum(x for x, _ in r); n = len(r)
    dp = pb_float(ps); pt = sum(dp[h:]); pd = sum(dp[:h + 1])
    kl = "RANKER CO GIA TRI" if pt < NG else ("RANKER HAI" if pd < NG else "ranker KHONG them gi")
    print("%-4s %5d %6d %8.1f%% %8.1f%% %11.4f %11.4f %-22s" % (reg, n, h, 100.0 * h / n, 100.0 * sum(ps) / n, pt, pd, kl))
print("-" * 110)
print("Nguong Bonferroni 6 phep = %.5f" % NG)
