import sqlite3
import sys
sys.stdout.reconfigure(encoding="utf-8")
c = sqlite3.connect("file:/root/Lottery_AI_Test/data/lottery_ai.db?mode=ro", uri=True)
print("== Claude được gọi lúc nào trong một ngày bình thường (09-10/11) ==")
for r in c.execute("""SELECT substr(created_at,1,10), substr(created_at,12,5), target_region, ai_model,
       COALESCE(run_source,'-'), COALESCE(status,'-')
  FROM predictions WHERE ai_model LIKE 'claude%'
   AND created_at >= '2026-11-09' AND created_at < '2026-11-11T00' ORDER BY created_at"""):
    print(r)
print("== Lượt cuối cùng của Claude trước khi cách ly ==")
for r in c.execute("""SELECT created_at, target_region, ai_model, COALESCE(run_source,'-'),
       substr(COALESCE(verdict_reason,''),1,90) FROM predictions WHERE ai_model LIKE 'claude%'
   ORDER BY created_at DESC LIMIT 4"""):
    print(r)
print("== Hôm nay 25/11 theo model ==")
for r in c.execute("""SELECT target_region, ai_model, count(*), min(substr(created_at,12,5)), max(substr(created_at,12,5))
  FROM predictions WHERE created_at >= '2026-11-25' GROUP BY 1,2 ORDER BY 1,2"""):
    print(r)
