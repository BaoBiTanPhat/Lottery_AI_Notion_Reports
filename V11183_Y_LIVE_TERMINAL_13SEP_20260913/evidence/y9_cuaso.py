# -*- coding: utf-8 -*-
"""V11183 §Y9 — Bach thu theo CUA SO CO DINH 30/90/180 + cohort sau ranh gioi.
NEN DUNG CHO TUNG NGAY-MIEN: p_d = (so duoi-2 KHAC NHAU that su co mat hom do)/100.
KHONG dung hang so, KHONG gop ba mien (RL-039: gop lam nen sai grain).
Kiem dinh: Poisson-binomial CHINH XAC (moi ngay mot p khac nhau) — khong xap xi.
"""
import json, sqlite3, sys
from datetime import date, timedelta
from fractions import Fraction
sys.stdout.reconfigure(encoding="utf-8")

DB = "/root/Lottery_AI_Test/data/lottery_ai.db"
NGAY_CHOT = date(2026, 9, 13)

def pb_p_tren(ps, k):
    """P(X >= k) cho Poisson-binomial voi cac xac suat ps. DP chinh xac bang Fraction."""
    dp = [Fraction(1)]
    for p in ps:
        p = Fraction(p).limit_denominator(10**6)
        moi = [Fraction(0)] * (len(dp) + 1)
        for i, v in enumerate(dp):
            if v:
                moi[i] += v * (1 - p)
                moi[i + 1] += v * p
        dp = moi
    return float(sum(dp[k:]))

def tu_kiem():
    """ps deu nhau => phai bang nhi thuc. Kiem bang gia tri tinh tay."""
    ok = []
    # n=3, p=1/2, P(X>=2) = 4/8 = 0.5
    ok.append(abs(pb_p_tren([0.5] * 3, 2) - 0.5) < 1e-12)
    # n=2, p=0.3, P(X>=1) = 1-0.49 = 0.51
    ok.append(abs(pb_p_tren([0.3, 0.3], 1) - 0.51) < 1e-12)
    # khac nhau: p=[0.2,0.8], P(X>=2)=0.16 ; P(X>=1)=1-0.2*0.8=0.84
    ok.append(abs(pb_p_tren([0.2, 0.8], 2) - 0.16) < 1e-12)
    ok.append(abs(pb_p_tren([0.2, 0.8], 1) - 0.84) < 1e-12)
    # P(X>=0) = 1
    ok.append(abs(pb_p_tren([0.1, 0.9, 0.35], 0) - 1.0) < 1e-12)
    return ok

def so_trong(obj, ra):
    if isinstance(obj, str): ra.append(obj)
    elif isinstance(obj, list):
        for x in obj: so_trong(x, ra)
    elif isinstance(obj, dict):
        for x in obj.values(): so_trong(x, ra)

kq = tu_kiem()
print("TU KIEM Poisson-binomial: %d/%d" % (sum(kq), len(kq)))
if not all(kq):
    print("TU KIEM HONG — DUNG"); sys.exit(1)
print()

con = sqlite3.connect("file:" + DB + "?mode=ro", uri=True); c = con.cursor()

# 1) duoi-2 that su co mat, theo (ngay, mien)
c.execute("SELECT substr(date,1,10), region, prizes_json FROM lottery_results WHERE substr(date,1,10) <= ?", (NGAY_CHOT.isoformat(),))
duoi2 = {}
for d, reg, pj in c.fetchall():
    ra = []; so_trong(json.loads(pj), ra)
    s = duoi2.setdefault((d, reg), set())
    for x in ra:
        if x.isdigit() and len(x) >= 2: s.add(x[-2:])

# 2) bundle bach thu
c.execute("SELECT date, region, bach_thu, bundle_version, generation_method, status FROM final_bundles WHERE date <= ? AND status='ACTIVE'", (NGAY_CHOT.isoformat(),))
bund = c.fetchall()
con.close()

quan_sat = {}   # (ngay,mien) -> (hit, p_d, bundle_version)
for d, reg, bt, bv, gm, st in bund:
    tails = duoi2.get((d, reg))
    if not tails or not bt: continue
    quan_sat[(d, reg)] = (1 if bt in tails else 0, len(tails) / 100.0, bv)

print("=" * 100)
print("BACH THU — CUA SO CO DINH ket thuc %s · don vi bang chung = (ngay x mien) · ba mien DO RIENG" % NGAY_CHOT)
print("=" * 100)
print("%-4s %-8s %5s %6s %9s %9s %9s %10s" % ("mien", "cua_so", "n", "trung", "ty_le", "nen_TB", "ky_vong", "p_mot_phia"))
print("-" * 100)
bang = {}
for reg in ("MN", "MT", "MB"):
    for w in (30, 90, 180):
        tu = NGAY_CHOT - timedelta(days=w - 1)
        rows = [v for (d, r), v in quan_sat.items()
                if r == reg and tu.isoformat() <= d <= NGAY_CHOT.isoformat()]
        if not rows: continue
        ps = [p for _, p, _ in rows]
        h = sum(x for x, _, _ in rows)
        n = len(rows); ky_vong = sum(ps)
        p_val = pb_p_tren(ps, h)
        bang[(reg, w)] = (n, h, h / n, ky_vong / n, ky_vong, p_val)
        print("%-4s %-8s %5d %6d %8.1f%% %8.1f%% %9.2f %10.4f"
              % (reg, "%dd" % w, n, h, 100.0 * h / n, 100.0 * ky_vong / n, ky_vong, p_val))
    print("-" * 100)

# 3) cohort sau ranh gioi THAT (bundle_version doi) — tim ranh gioi tu du lieu, khong dat tay
print()
print("=" * 100)
print("RANH GIOI THAT: ngay dau tien moi bundle_version xuat hien (doc tu du lieu, khong dat tay)")
print("=" * 100)
theo_bv = {}
for (d, reg), (h, p, bv) in quan_sat.items():
    theo_bv.setdefault(bv, []).append(d)
for bv in sorted(theo_bv):
    ds = sorted(theo_bv[bv])
    print("bundle_version=%s : %d ban ghi, tu %s den %s" % (bv, len(ds), ds[0], ds[-1]))

bv_moi = max(theo_bv)
moc = min(theo_bv[bv_moi])
print()
print("COHORT DAY DU SAU RANH GIOI bundle_version=%s (tu %s, KHONG cat cua so):" % (bv_moi, moc))
print("%-4s %5s %6s %9s %9s %9s %10s" % ("mien", "n", "trung", "ty_le", "nen_TB", "ky_vong", "p_mot_phia"))
print("-" * 100)
for reg in ("MN", "MT", "MB"):
    rows = [v for (d, r), v in quan_sat.items() if r == reg and d >= moc and v[2] == bv_moi]
    if not rows: continue
    ps = [p for _, p, _ in rows]; h = sum(x for x, _, _ in rows); n = len(rows)
    print("%-4s %5d %6d %8.1f%% %8.1f%% %9.2f %10.4f"
          % (reg, n, h, 100.0 * h / n, 100.0 * sum(ps) / n, sum(ps), pb_p_tren(ps, h)))
print("-" * 100)
print()
print("GHI CHU RM-04: n nho => 'CHUA DUOC PHEP KET LUAN', khong phai 'yeu'.")
print("GHI CHU RL-039: ba mien do RIENG. Gop lai se so ty le hop-mien voi nen mot-dai => nen sai grain.")
