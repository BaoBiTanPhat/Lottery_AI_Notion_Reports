# -*- coding: utf-8 -*-
"""V11183 §Y5 — DO CONTROL: bo weights MAC DINH vs bo DA HOC, cung cua so optimizer da dung.
CHI DOC: backtest_with_weights khong ghi gi. Khong dung lai optimizer, khong ghi app_settings.
Them: hieu chinh nen KHONG HOAN LAI (RL-040) — top-3 la 3 duoi KHAC NHAU.
"""
import sys, json, sqlite3
sys.path.insert(0, "/root/Lottery_AI_Test/web/backend")
from math import comb
sys.stdout.reconfigure(encoding="utf-8")
from weight_optimizer import backtest_with_weights

TU, DEN = "2026-07-14", "2026-09-12"
MAC_DINH = {"convergence": 0.35, "trend": 0.25, "gan": 0.20, "recency": 0.20}
con = sqlite3.connect("file:/root/Lottery_AI_Test/data/lottery_ai.db?mode=ro", uri=True)
DA_HOC = {}
for R in ("MN", "MT", "MB"):
    v = con.execute("SELECT setting_value FROM app_settings WHERE setting_key=?", ("weights_" + R,)).fetchone()
    DA_HOC[R] = json.loads(v[0])["weights"]
con.close()

print("CUA SO: %s -> %s (dung cua so optimizer da fit)" % (TU, DEN))
print("CONTROL (mac dinh): %s" % MAC_DINH)
print()
print("=" * 112)
print("%-4s %-10s %8s %9s %9s %8s %11s %11s" % ("mien","bo_weights","n_ngay","win_rate","nen_cu","lift_cu","nen_DUNG","lift_DUNG"))
print("  (nen_cu = 1-(1-b)^3 CO hoan lai, dung trong ma hien tai · nen_DUNG = 1-C(100-M,3)/C(100,3) KHONG hoan lai, RL-040)")
print("=" * 112)
bang = {}
for R in ("MN", "MT", "MB"):
    for ten, w in (("CONTROL", MAC_DINH), ("DA_HOC", DA_HOC[R])):
        r = backtest_with_weights(region=R, start_date=TU, end_date=DEN, weights=w, top_n=3, history_days=30)
        if "error" in r:
            print("%-4s %-10s LOI: %s" % (R, ten, r["error"])); continue
        wr, nen_cu, n = r["win_rate"], r["random_baseline"], r["verified"]
        # suy nguoc M trung binh tu nen cu: nen_cu = 1-(1-M/100)^3
        b = 1 - (1 - nen_cu / 100.0) ** (1.0 / 3)
        M = int(round(b * 100))
        nen_dung = (1 - comb(100 - M, 3) / comb(100, 3)) * 100 if 100 - M >= 3 else 100.0
        bang[(R, ten)] = (wr, nen_cu, r["lift"], nen_dung, wr - nen_dung, n, M)
        print("%-4s %-10s %8d %8.2f%% %8.2f%% %+8.2f %10.2f%% %+11.2f" % (R, ten, n, wr, nen_cu, r["lift"], nen_dung, wr - nen_dung))
    print("-" * 112)

print()
print("=" * 112)
print("PHEP SO CHUA TUNG DUOC LAM: DA_HOC co hon CONTROL khong?")
print("=" * 112)
print("%-4s %11s %11s %12s %-34s" % ("mien","lift_CONTROL","lift_DA_HOC","chenh_lech","ket_luan"))
print("-" * 112)
for R in ("MN", "MT", "MB"):
    a = bang.get((R, "CONTROL")); b2 = bang.get((R, "DA_HOC"))
    if not a or not b2: continue
    d = b2[4] - a[4]
    if b2[4] <= 0 and a[4] <= 0: kl = "CA HAI KEM NEN NGAU NHIEN"
    elif d > 0: kl = "da hoc hon control %+.2f pp" % d
    else: kl = "DA HOC KEM HON CONTROL %+.2f pp" % d
    print("%-4s %+11.2f %+11.2f %+12.2f %-34s" % (R, a[4], b2[4], d, kl))
print("-" * 112)
print()
print("GHI CHU RM-04: n ngay moi mien ~%d; day la do TRONG MAU (cua so da fit), chua co held-out." % bang[("MN","CONTROL")][5])
