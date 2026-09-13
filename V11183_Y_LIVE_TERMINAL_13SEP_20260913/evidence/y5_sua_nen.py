# -*- coding: utf-8 -*-
"""V11183 §Y5 — TINH LAI LIFT voi NEN DUNG.
Loi da tim: backtester.get_actual_tails tra list CO TRUNG va CONG THEM tail_db/tail_g8
von da nam trong prizes_json => len() phong to => random_chance phong to => lift bi ha.
Nen dung: 1 - C(100-M,3)/C(100,3) voi M = so duoi-2 KHAC NHAU that su, tinh RIENG TUNG NGAY.
Kiem dinh: Poisson-binomial chinh xac tren cac p_d rieng tung ngay.
"""
import json, sqlite3, sys
from math import comb
sys.stdout.reconfigure(encoding="utf-8")
DB = "/root/Lottery_AI_Test/data/lottery_ai.db"
TU, DEN = "2026-07-14", "2026-09-12"
# win_rate do duoc o buoc truoc (backtest that, khong doan)
WR = {("MN","CONTROL"):85.25, ("MN","DA_HOC"):91.80,
      ("MT","CONTROL"):75.41, ("MT","DA_HOC"):80.33,
      ("MB","CONTROL"):54.10, ("MB","DA_HOC"):73.77}

def so_trong(o, ra):
    if isinstance(o, str): ra.append(o)
    elif isinstance(o, list):
        for x in o: so_trong(x, ra)
    elif isinstance(o, dict):
        for x in o.values(): so_trong(x, ra)

con = sqlite3.connect("file:" + DB + "?mode=ro", uri=True); c = con.cursor()
c.execute("SELECT substr(date,1,10), region, prizes_json, tail_db, tail_g8 FROM lottery_results WHERE substr(date,1,10) BETWEEN ? AND ?", (TU, DEN))
khac, trung = {}, {}
for d, reg, pj, tdb, tg8 in c.fetchall():
    ra = []; so_trong(json.loads(pj), ra)
    ds = khac.setdefault((d, reg), set()); ls = trung.setdefault((d, reg), [])
    for x in ra:
        if x.isdigit() and len(x) >= 2: ds.add(x[-2:]); ls.append(x[-2:])
    for t in (tdb, tg8):
        if t: ls.append(str(t)[-2:])
con.close()

def pb(ps):
    dp = [1.0]
    for p in ps:
        m = [0.0]*(len(dp)+1)
        for i, v in enumerate(dp):
            if v: m[i] += v*(1-p); m[i+1] += v*p
        dp = m
    return dp

print("=" * 118)
print("SO SANH HAI CACH DEM DUOI (cua so %s -> %s)" % (TU, DEN))
print("=" * 118)
print("%-4s %6s %12s %12s %14s %14s %10s" % ("mien","n_ngay","duoi_KHAC_TB","duoi_TRUNG_TB","nen_DUNG_TB","nen_MA_HIEN_TAI","phong_to"))
print("-" * 118)
nen_ngay = {}
for reg in ("MN","MT","MB"):
    ds = sorted(d for (d, r) in khac if r == reg)
    if not ds: continue
    Mk = [len(khac[(d,reg)]) for d in ds]; Mt = [len(trung[(d,reg)]) for d in ds]
    pd_ = [1 - comb(100-m,3)/comb(100,3) if 100-m >= 3 else 1.0 for m in Mk]
    pm = [1 - (1 - min(m,100)/100.0)**3 for m in Mt]
    nen_ngay[reg] = (ds, pd_)
    print("%-4s %6d %12.1f %12.1f %13.2f%% %13.2f%% %+9.2f pp"
          % (reg, len(ds), sum(Mk)/len(Mk), sum(Mt)/len(Mt), 100*sum(pd_)/len(pd_), 100*sum(pm)/len(pm),
             100*sum(pm)/len(pm) - 100*sum(pd_)/len(pd_)))
print("-" * 118)
print()
print("=" * 118)
print("LIFT TINH LAI voi NEN DUNG — win_rate giu nguyen (do that), chi doi NEN")
print("=" * 118)
NG = 0.05/6
print("%-4s %-8s %5s %6s %9s %11s %11s %11s %11s %-22s" % ("mien","bo","n","thang","win%","nen_MA","lift_MA","nen_DUNG","lift_DUNG","p_HON_nen_dung"))
print("-" * 118)
for reg in ("MN","MT","MB"):
    ds, pd_ = nen_ngay[reg]; n = len(ds)
    for bo in ("CONTROL","DA_HOC"):
        wr = WR[(reg,bo)]; k = round(wr/100*n)
        nen_d = 100*sum(pd_)/n
        Mt = [len(trung[(d,reg)]) for d in ds]
        nen_m = 100*sum(1-(1-min(m,100)/100.0)**3 for m in Mt)/n
        dp = pb(pd_); pt = sum(dp[k:])
        print("%-4s %-8s %5d %6d %8.2f%% %10.2f%% %+10.2f %10.2f%% %+10.2f %11.5f %s"
              % (reg, bo, n, k, wr, nen_m, wr-nen_m, nen_d, wr-nen_d, pt,
                 "<= CO Y NGHIA" if pt < NG else ""))
    print("-" * 118)
print("Nguong Bonferroni 6 phep = %.5f" % NG)
