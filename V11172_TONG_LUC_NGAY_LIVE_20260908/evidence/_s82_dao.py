# -*- coding: utf-8 -*-
"""V11172 — dao ba tin hieu: MT mc=6 · tran che loi that · PP1-WATCH rong. CHI DOC."""
import sqlite3, json, collections
NGAY = "2026-09-08"
c = sqlite3.connect("file:/root/Lottery_AI_Test/data/lottery_ai.db?mode=ro", uri=True)
c.row_factory = sqlite3.Row
q = lambda s, *a: c.execute(s, a).fetchall()

print("=== A · MT nhung ngay model_count BAT THUONG (30 ngay) ===")
for r in q("SELECT date, model_count, bach_thu, bach_thu_status, is_fallback, notes, "
           "source_predictions_json FROM final_bundles WHERE region='MT' AND model_count<13 "
           "AND date>=date(?, '-29 day') ORDER BY date", NGAY):
    j = json.loads(r["source_predictions_json"] or "{}")
    ex = j.get("model_exclusion_reasons") or []
    print("  %s mc=%s BT=%s (%s) fb=%s notes=%s" % (r["date"], r["model_count"], r["bach_thu"],
          r["bach_thu_status"], r["is_fallback"], (r["notes"] or "")[:30]))
    print("     quality_filtered=%s · hard_timeout=%s · empty=%s"
          % (j.get("quality_filtered_models"), j.get("hard_timeout_models"), j.get("diagnostic_empty_models")))
    for e in ex[:8]:
        print("       - %s | %s | %s | active=%s" % (e.get("model"), e.get("reason"),
              (e.get("detail") or "")[:45], e.get("active")))

print("\n=== B · MT HOM NAY: tran co CHE MAT loi that khong? ===")
r = q("SELECT source_predictions_json, model_count FROM final_bundles WHERE date=? AND region='MT'", NGAY)
if r:
    j = json.loads(r[0]["source_predictions_json"] or "{}")
    print("  model_count=%s · output_eligible_row_count=%s · scoreable=%s · total_models=%s"
          % (r[0]["model_count"], j.get("output_eligible_row_count"), j.get("scoreable_model_count"), j.get("total_models")))
    print("  incomplete_bundle=%s · quality_filtered_count=%s" % (j.get("incomplete_bundle"), j.get("quality_filtered_model_count")))
    print("  quality_filtered_models =", j.get("quality_filtered_models"))
    print("  wr_gate_filtered        =", j.get("wr_gate_filtered"))
    print("  hard_timeout_models     =", j.get("hard_timeout_models"))
    print("  diagnostic_empty_models =", j.get("diagnostic_empty_models"))
    print("  model_exclusion_reasons:")
    for e in (j.get("model_exclusion_reasons") or []):
        print("    - %s | reason=%s | %s | active=%s" % (e.get("model"), e.get("reason"),
              (e.get("detail") or "")[:50], e.get("active")))
    gd = j.get("gate_diagnostics") or {}
    print("  gate_diagnostics: %d model -> %s" % (len(gd), sorted(gd.keys())))
print("  -- combo-super co dong predictions cho MT hom nay khong --")
for x in q("SELECT ai_model, run_source, created_at, status, "
           "length(COALESCE(main_numbers,'')) len_mn FROM predictions "
           "WHERE date=? AND target_region='MT' AND ai_model IN ('combo-super','glm-5.1') ORDER BY ai_model", NGAY):
    print("     %-14s src=%-14s tao=%s st=%-8s len(main_numbers)=%s"
          % (x["ai_model"], x["run_source"], x["created_at"][11:19], x["status"], x["len_mn"]))

print("\n=== C · PP1-WATCH bao 'regions_with_data=none' — bang nao rong? ===")
cols = [x[1] for x in c.execute("PRAGMA table_info(scheduler_logs)").fetchall()]
m = "message" if "message" in cols else cols[-1]
for x in q("SELECT datetime(log_time,'+7 hours') vn, %s msg FROM scheduler_logs "
           "WHERE %s LIKE '%%PP1-WATCH%%' AND datetime(log_time,'+7 hours')>=date(?,'-2 day') "
           "ORDER BY log_time DESC LIMIT 6" % (m, m), NGAY):
    print("  %s %s" % (x["vn"][11:19], (x["msg"] or "")[:150]))
print("  -- bang pp1 co dong nao khong --")
for t in [x[0] for x in q("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE '%pp1%'")]:
    try:
        n = c.execute("SELECT COUNT(*) FROM %s" % t).fetchone()[0]
        cc = [y[1] for y in c.execute("PRAGMA table_info(%s)" % t).fetchall()]
        dc = next((y for y in ("created_at","date") if y in cc), None)
        moi = c.execute("SELECT MAX(%s) FROM %s" % (dc, t)).fetchone()[0] if dc else "?"
        print("     %-40s %6d dong · moi nhat %s" % (t, n, moi))
    except Exception as e:
        print("     %-40s LOI %s" % (t, e))

print("\n=== D · CON SO NGAY HOM NAY: 68 co that trong tap duoi MN khong (kiem nhan WIN) ===")
def duoi(pz):
    d = set()
    def w(v):
        if isinstance(v, str) and v.isdigit(): d.add(v[-2:])
        elif isinstance(v, list):
            for x in v: w(x)
        elif isinstance(v, dict):
            for x in v.values(): w(x)
    w(pz); return d
for reg, bt in (("MN","68"), ("MT","15"), ("MB","63")):
    s = set()
    for r in q("SELECT prizes_json FROM lottery_results WHERE date=? AND region=?", NGAY, reg):
        s |= duoi(json.loads(r["prizes_json"] or "{}"))
    print("  %s: |tap duoi|=%d · BT=%s co trong tap? %s" % (reg, len(s), bt, bt in s))
