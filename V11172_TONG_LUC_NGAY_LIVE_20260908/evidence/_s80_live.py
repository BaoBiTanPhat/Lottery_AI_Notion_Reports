# -*- coding: utf-8 -*-
"""V11172 SCOUT — ngay live 08/09/2026. CHI DOC."""
import sqlite3, json, subprocess, collections
NGAY = "2026-09-08"
HOM_QUA = "2026-09-07"
def sh(c): return subprocess.run(c, shell=True, capture_output=True, text=True).stdout.strip()

print("=== MAY ===")
print("  gio VN    :", sh("TZ=Asia/Ho_Chi_Minh date '+%Y-%m-%d %H:%M:%S'"))
print("  PID       :", sh("systemctl show -p MainPID --value lottery"),
      "· NRestarts", sh("systemctl show -p NRestarts --value lottery"))
print("  health    :", sh("curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:8000/api/health"))
print("  dia       :", sh("df -h / | tail -1 | awk '{print $5\" dung, \"$4\" con\"}'"))
print("  load      :", sh("cat /proc/loadavg | cut -d' ' -f1-3"))
print("  uptime svc:", sh("systemctl show -p ActiveEnterTimestamp --value lottery"))

c = sqlite3.connect("file:/root/Lottery_AI_Test/data/lottery_ai.db?mode=ro", uri=True)
c.row_factory = sqlite3.Row
q = lambda s, *a: c.execute(s, a).fetchall()

for ng, nhan in ((NGAY, "HOM NAY 08/09"), (HOM_QUA, "HOM QUA 07/09")):
    print("\n=== BUNDLE %s ===" % nhan)
    r = q("SELECT id,region,bach_thu,lo2,lo3,xien2,xien3,model_count,top_score,consensus_level,"
          "is_fallback,bundle_version,created_at,updated_at,bach_thu_status,lo2_status,lo3_status,"
          "xien2_status,xien3_status,verified_at,notes FROM final_bundles WHERE date=? ORDER BY id", ng)
    if not r:
        print("   (chua co bundle nao)")
    for x in r:
        print("  id=%s %s BT=%s lo2=%s lo3=%s mc=%s top=%s cons=%s fb=%s ver=%s"
              % (x["id"], x["region"], x["bach_thu"], x["lo2"], x["lo3"], x["model_count"],
                 x["top_score"], x["consensus_level"], x["is_fallback"], x["bundle_version"]))
        print("     tao=%s sua=%s verify=%s" % (x["created_at"], x["updated_at"], x["verified_at"]))
        print("     KQ: bt=%s lo2=%s lo3=%s x2=%s x3=%s  notes=%s"
              % (x["bach_thu_status"], x["lo2_status"], x["lo3_status"],
                 x["xien2_status"], x["xien3_status"], (x["notes"] or "")[:40]))
    print("  -- ket qua xo so --")
    rr = q("SELECT region,station,tail_db,tail_g8,created_at FROM lottery_results WHERE date=? ORDER BY region", ng)
    if not rr: print("     (chua ve)")
    for x in rr:
        print("     %-3s %-20s db=%-4s g8=%-4s ve=%s" % (x["region"], x["station"], x["tail_db"], x["tail_g8"], x["created_at"][11:19]))

print("\n=== DU DOAN HOM NAY theo mien/nguon ===")
for x in q("SELECT target_region reg, run_source, COUNT(*) n, "
           "SUM(CASE WHEN main_numbers IS NULL OR main_numbers='' OR main_numbers='[]' THEN 1 ELSE 0 END) rong, "
           "SUM(COALESCE(late,0)) late, MIN(created_at) t0, MAX(created_at) t1 "
           "FROM predictions WHERE date=? GROUP BY 1,2 ORDER BY 1,2", NGAY):
    print("  %-3s %-20s n=%-3s rong=%-2s late=%-2s %s..%s"
          % (x["reg"], x["run_source"], x["n"], x["rong"], x["late"], x["t0"][11:19], x["t1"][11:19]))

print("\n=== day_governance HOM NAY ===")
for x in q("SELECT * FROM day_governance WHERE date=? ORDER BY region", NGAY):
    print("  %s %s day=%s pub=%s qual=%s exp=%s done=%s fail=%s ratio=%s reason=%s"
          % (x["date"], x["region"], x["day_status"], x["publication_status"], x["bundle_quality"],
             x["expected_model_count"], x["completed_model_count"], x["failed_model_count"],
             x["completeness_ratio"], x["degradation_reason"]))

print("\n=== scheduler_logs HOM NAY (gio VN, chi loi/canh bao + t10_chot) ===")
try:
    cols = [x[1] for x in c.execute("PRAGMA table_info(scheduler_logs)").fetchall()]
    ncol = "message" if "message" in cols else cols[-1]
    tot = q("SELECT COUNT(*) n FROM scheduler_logs WHERE substr(datetime(log_time,'+7 hours'),1,10)=?", NGAY)[0]["n"]
    print("  tong dong hom nay:", tot)
    for x in q("SELECT job_name, datetime(log_time,'+7 hours') vn, %s msg FROM scheduler_logs "
               "WHERE substr(datetime(log_time,'+7 hours'),1,10)=? AND "
               "(job_name LIKE '%%chot%%' OR %s LIKE '%%ERROR%%' OR %s LIKE '%%FAIL%%' "
               " OR %s LIKE '%%TIMEOUT%%' OR %s LIKE '%%loi%%') ORDER BY log_time" % (ncol,ncol,ncol,ncol,ncol), NGAY):
        print("  %s %-24s %s" % (x["vn"][11:19], x["job_name"], (x["msg"] or "")[:90]))
except Exception as e:
    print("  LOI:", e)

print("\n=== 30 NGAY: bach thu trung/truot theo mien ===")
for x in q("SELECT region, COUNT(*) n, SUM(bach_thu_status='WIN') w FROM final_bundles "
           "WHERE date>=date(?, '-29 day') AND date<=? AND bach_thu_status IN ('WIN','LOSE') "
           "GROUP BY region ORDER BY region", NGAY, NGAY):
    print("  %s  %s/%s = %.1f%%" % (x["region"], x["w"], x["n"], 100*x["w"]/x["n"]))
print("  -- 7 ngay gan nhat theo ngay --")
for x in q("SELECT date, SUM(bach_thu_status='WIN') w, COUNT(*) n FROM final_bundles "
           "WHERE date>=date(?, '-6 day') AND date<=? AND bach_thu_status IN ('WIN','LOSE') "
           "GROUP BY date ORDER BY date", NGAY, NGAY):
    print("     %s  %s/%s" % (x["date"], x["w"], x["n"]))
