# -*- coding: utf-8 -*-
"""V11172 — xac minh FU-446 (bang hieu chinh suc manh) + truy pp1 ngung ghi. CHI DOC."""
import sqlite3, json, subprocess, sys, importlib, collections
sys.path.insert(0, "/root/Lottery_AI_Test/web/backend")
NGAY = "2026-09-08"
c = sqlite3.connect("file:/root/Lottery_AI_Test/data/lottery_ai.db?mode=ro", uri=True)
c.row_factory = sqlite3.Row
q = lambda s, *a: c.execute(s, a).fetchall()
def sh(x): return subprocess.run(x, shell=True, capture_output=True, text=True).stdout.strip()

print("=== A · FU-446: bang hieu chinh suc manh con lac hau khong? ===")
try:
    import strength_calibrator as SC
    D = getattr(SC, "MODEL_STRENGTH_DISCOUNT", {})
    DEF = getattr(SC, "DEFAULT_DISCOUNT", None)
    print("  MODEL_STRENGTH_DISCOUNT: %d khoa · DEFAULT_DISCOUNT=%s" % (len(D), DEF))
    print("  khoa:", sorted(D.keys()))
except Exception as e:
    print("  KHONG nap duoc strength_calibrator:", type(e).__name__, e)
    D, DEF = {}, None

mods = [r["ai_model"] for r in q(
    "SELECT DISTINCT ai_model FROM predictions WHERE date>=date(?, '-29 day') ORDER BY ai_model", NGAY)]
print("\n  model SINH DU DOAN 30 ngay: %d" % len(mods))
thieu = [m for m in mods if m not in D]
print("  ROI VE MAC DINH (%s): %d model" % (DEF, len(thieu)))
for m in thieu: print("     -", m)
print("  co trong bang ma KHONG con sinh du doan:", sorted(set(D) - set(mods)))

print("\n=== B · strength_weight THUC TE trong bundle hom nay ===")
r = q("SELECT region, source_predictions_json FROM final_bundles WHERE date=? ORDER BY id", NGAY)
seen = {}
for x in r:
    j = json.loads(x["source_predictions_json"] or "{}")
    for sb in (j.get("score_breakdown") or []):
        for comp in (sb.get("components") or []):
            seen.setdefault(comp.get("model"), set()).add(comp.get("strength_weight"))
print("  model -> strength_weight quan sat duoc (bundle hom nay)")
for m in sorted(seen):
    v = sorted(x for x in seen[m] if x is not None)
    cln = " <== ROI MAC DINH?" if v == [0.7] else ""
    print("     %-24s %s%s" % (m, v, cln))
n070 = sum(1 for m in seen if sorted(x for x in seen[m] if x is not None) == [0.7])
print("  => %d/%d model quan sat duoc co strength_weight DUNG BANG 0.7" % (n070, len(seen)))

print("\n=== C · pp1_live_watch_daily ngung ghi tu bao gio, ai la writer ===")
for x in q("SELECT date, COUNT(*) n FROM pp1_live_watch_daily GROUP BY date ORDER BY date DESC LIMIT 8"):
    print("     %s : %s dong" % (x["date"], x["n"]))
print("  cot:", [y[1] for y in c.execute("PRAGMA table_info(pp1_live_watch_daily)").fetchall()])
print("  -- writer trong ma nguon --")
print(sh("grep -rn 'pp1_live_watch_daily' /root/Lottery_AI_Test/web/backend/*.py | head -12"))
print("  -- dieu kien PP1-WATCH ghi (tim ham) --")
print(sh("grep -rn 'PP1-WATCH' /root/Lottery_AI_Test/web/backend/*.py | head -8"))

print("\n=== D · pp1_convergence_dampener con kich hoat khong (3 ngay) ===")
for x in q("SELECT date, region, source_predictions_json FROM final_bundles "
           "WHERE date>=date(?, '-2 day') ORDER BY date, region", NGAY):
    j = json.loads(x["source_predictions_json"] or "{}")
    pp1 = j.get("pp1_convergence_dampener") or {}
    ev = pp1.get("events") or []
    print("     %s %s enabled=%s events=%d" % (x["date"], x["region"], pp1.get("enabled"), len(ev)))
