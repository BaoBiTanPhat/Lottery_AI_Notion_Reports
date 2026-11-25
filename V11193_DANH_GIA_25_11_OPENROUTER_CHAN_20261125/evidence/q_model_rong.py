import sqlite3, sys
sys.stdout.reconfigure(encoding="utf-8")
c = sqlite3.connect("file:/root/Lottery_AI_Test/data/lottery_ai.db?mode=ro", uri=True)
print("== dòng predictions hôm nay của 2 model OpenRouter")
for r in c.execute("""SELECT target_region, ai_model, run_source, substr(created_at,12,8), status,
        COALESCE(main_numbers,'<NULL>'), substr(COALESCE(verdict_reason,''),1,160)
        FROM predictions WHERE date='2026-11-25' AND ai_model IN ('gpt-oss-120b','glm-5.1') ORDER BY created_at"""):
    print(r)
print("\n== theo ngày: số dòng / dòng có số, 4 model AI (30 ngày)")
q = """SELECT date, ai_model, count(*), sum(CASE WHEN main_numbers IS NOT NULL AND main_numbers NOT IN ('','[]','null') THEN 1 ELSE 0 END)
       FROM predictions WHERE date>='2026-10-27' AND ai_model IN ('gpt-oss-120b','glm-5.1','gemini-2.5-flash','claude-opus-4-6')
       GROUP BY 1,2 ORDER BY 1,2"""
rows = list(c.execute(q))
from collections import defaultdict
d = defaultdict(dict)
for date, m, n, ok in rows:
    d[date][m] = "%d/%d" % (ok, n)
ms = ['gpt-oss-120b','glm-5.1','gemini-2.5-flash','claude-opus-4-6']
print("date       " + "  ".join("%-16s" % m for m in ms))
for date in sorted(d):
    print(date, "  ".join("%-16s" % d[date].get(m, "-") for m in ms))
print("\n== lý do rỗng hay gặp nhất (30 ngày)")
for r in c.execute("""SELECT ai_model, substr(COALESCE(verdict_reason,''),1,90) AS ly_do, count(*) FROM predictions
        WHERE date>='2026-10-27' AND ai_model IN ('gpt-oss-120b','glm-5.1')
          AND (main_numbers IS NULL OR main_numbers IN ('','[]','null'))
        GROUP BY 1,2 ORDER BY 3 DESC LIMIT 8"""):
    print(r)
print("\n== ngày cuối cùng có số")
for r in c.execute("""SELECT ai_model, max(date) FROM predictions WHERE ai_model IN ('gpt-oss-120b','glm-5.1')
        AND main_numbers IS NOT NULL AND main_numbers NOT IN ('','[]','null') GROUP BY 1"""):
    print(r)
