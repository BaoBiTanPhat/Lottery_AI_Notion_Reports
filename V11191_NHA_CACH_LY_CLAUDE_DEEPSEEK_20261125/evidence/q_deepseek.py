import sqlite3
import sys
sys.stdout.reconfigure(encoding="utf-8")
c = sqlite3.connect("file:/root/Lottery_AI_Test/data/lottery_ai.db?mode=ro", uri=True)
print("== DeepSeek trong predictions, theo tháng × run_source ==")
for r in c.execute("""SELECT substr(created_at,1,7), ai_model, COALESCE(run_source,'-'), count(*),
       sum(CASE WHEN verdict_reason LIKE '%ERROR%' OR verdict_reason LIKE '%PERSISTED_DIAGNOSTIC_EMPTY%' THEN 1 ELSE 0 END)
  FROM predictions WHERE ai_model LIKE 'deepseek%' AND created_at >= '2026-07-01'
  GROUP BY 1,2,3 ORDER BY 1,2,3"""):
    print(r)
print("== Lượt DeepSeek cuối cùng ==")
for r in c.execute("""SELECT created_at, target_region, ai_model, COALESCE(run_source,'-'), substr(COALESCE(verdict_reason,''),1,80)
  FROM predictions WHERE ai_model LIKE 'deepseek%' ORDER BY created_at DESC LIMIT 3"""):
    print(r)
tabs = [r[0] for r in c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE '%test%'")]
print("bảng test:", tabs)
for t in tabs:
    cols = [x[1] for x in c.execute("PRAGMA table_info(%s)" % t)]
    mc = next((x for x in ("model_id", "ai_model", "model", "model_used") if x in cols), None)
    tc = next((x for x in ("created_at", "date", "draw_date") if x in cols), None)
    if mc and tc:
        q = "SELECT %s, max(%s), count(*) FROM %s WHERE %s LIKE 'deepseek%%' GROUP BY 1" % (mc, tc, t, mc)
        for r in c.execute(q):
            print(" ", t, r)
