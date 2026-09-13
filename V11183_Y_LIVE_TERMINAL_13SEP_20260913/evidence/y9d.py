# -*- coding: utf-8 -*-
"""V11183 §Y9b — duoi DUOI (kem nen) + chinh boi so + cohort DAY DU khong cat cua so.
SUA: bundle_version KHONG phai moc thoi gian (v1 va v2 chong nhau ca ky) => bo cach chia do.
Cohort thay the = TOAN BO ngay co du lieu (khong chon cua so nao ca).
"""
import json, sqlite3, sys
from datetime import date, timedelta
from fractions import Fraction
sys.stdout.reconfigure(encoding="utf-8")
DB = "/root/Lottery_AI_Test/data/lottery_ai.db"; NGAY_CHOT = date(2026, 9, 13)

def pb_dp(ps):
    dp = [Fraction(1)]
    for p in ps:
        p = Fraction(p).limit_denominator(10**6)
        moi = [Fraction(0)] * (len(dp) + 1)
        for i, v in enumerate(dp):
            if v: moi[i] += v * (1 - p); moi[i + 1] += v * p
        dp = moi
    return dp
def p_tren(ps, k): d = pb_dp(ps); return float(sum(d[k:]))
def p_duoi(ps, k): d = pb_dp(ps); return float(sum(d[:k + 1]))

def so_trong(o, ra):
    if isinstance(o, str): ra.append(o)
    elif isinstance(o, list):
        for x in o: so_trong(x, ra)
    elif isinstance(o, dict):
        for x in o.values(): so_trong(x, ra)

con = sqlite3.connect("file:" + DB + "?mode=ro", uri=True); c = con.cursor()
c.execute("SELECT substr(date,1,10), region, prizes_json FROM lottery_results WHERE substr(date,1,10) <= ?", (NGAY_CHOT.isoformat(),))
duoi2 = {}
for d, reg, pj in c.fetchall():
    ra = []; so_trong(json.loads(pj), ra)
    s = duoi2.setdefault((d, reg), set())
    for x in ra:
        if x.isdigit() and len(x) >= 2: s.add(x[-2:])
c.execute("SELECT date, region, bach_thu FROM final_bundles WHERE date <= ? AND status='ACTIVE'", (NGAY_CHOT.isoformat(),))
qs = {}
for d, reg, bt in c.fetchall():
    t = duoi2.get((d, reg))
    if t and bt: qs[(d, reg)] = (1 if bt in t else 0, len(t) / 100.0)
con.close()

print("=" * 104)
print("§Y9b — HAI DUOI + CHINH BOI SO (9 phep kiem: 3 mien x 3 cua so)")
print("Bonferroni nguong 0.05/9 = 0.00556. Ba cua so LONG NHAU => KHONG doc lap, Bonferroni la BAO THU.")
print("=" * 104)
print("%-4s %-6s %5s %6s %8s %8s %11s %11s %-22s" % ("mien","cua_so","n","trung","ty_le","nen_TB","p_HON_nen","p_KEM_nen","ket_luan_sau_chinh"))
print("-" * 104)
NG = 0.05 / 9
for reg in ("MN", "MT", "MB"):
    for w in (14, 30, 90, 180):
        tu = (NGAY_CHOT - timedelta(days=w - 1)).isoformat()
        rows = [v for (d, r), v in qs.items() if r == reg and tu <= d <= NGAY_CHOT.isoformat()]
        if not rows: continue
        ps = [p for _, p in rows]; h = sum(x for x, _ in rows); n = len(rows)
        pt = p_tren(ps, h); pd = p_duoi(ps, h)
        if pt < NG: kl = "HON NEN"
        elif pd < NG: kl = "KEM NEN (co y nghia)"
        else: kl = "khong khac nen"
        print("%-4s %-6s %5d %6d %7.1f%% %7.1f%% %11.4f %11.4f %-22s" % (reg,"%dd"%w,n,h,100.0*h/n,100.0*sum(ps)/n,pt,pd,kl))
    print("-" * 104)

print()
print("=" * 104)
print("COHORT DAY DU — TOAN BO ngay co du lieu, KHONG chon cua so nao (PRJ-SELECTION-WINDOW-001)")
print("=" * 104)
print("%-4s %5s %6s %8s %8s %11s %11s %-12s %-12s" % ("mien","n","trung","ty_le","nen_TB","p_HON_nen","p_KEM_nen","tu_ngay","den_ngay"))
print("-" * 104)
for reg in ("MN", "MT", "MB"):
    rows = [(d, v) for (d, r), v in qs.items() if r == reg]
    if not rows: continue
    ds = sorted(x[0] for x in rows)
    ps = [v[1] for _, v in rows]; h = sum(v[0] for _, v in rows); n = len(rows)
    print("%-4s %5d %6d %7.1f%% %7.1f%% %11.4f %11.4f %-12s %-12s"
          % (reg, n, h, 100.0*h/n, 100.0*sum(ps)/n, p_tren(ps,h), p_duoi(ps,h), ds[0], ds[-1]))
print("-" * 104)
