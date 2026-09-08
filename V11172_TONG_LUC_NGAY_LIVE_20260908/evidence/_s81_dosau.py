# -*- coding: utf-8 -*-
"""V11172 — do sau: MT co that su kem nen khong · anti-trap hom nay · combo-super timeout ·
PP1-WATCH rong. Nen tinh RIENG TUNG MIEN-NGAY (RM-18). CHI DOC."""
import sqlite3, json, collections, math
NGAY = "2026-09-08"
c = sqlite3.connect("file:/root/Lottery_AI_Test/data/lottery_ai.db?mode=ro", uri=True)
c.row_factory = sqlite3.Row
q = lambda s, *a: c.execute(s, a).fetchall()

def duoi(pz):
    d = set()
    def w(v):
        if isinstance(v, str) and v.isdigit(): d.add(v[-2:])
        elif isinstance(v, list):
            for x in v: w(x)
        elif isinstance(v, dict):
            for x in v.values(): w(x)
    w(pz); return d

tap = collections.defaultdict(set)
for r in q("SELECT date, region, prizes_json FROM lottery_results"):
    try: tap[(r["date"], r["region"])] |= duoi(json.loads(r["prizes_json"] or "{}"))
    except Exception: pass

print("=== 1 · BACH THU vs NEN RIENG TUNG MIEN-NGAY (Poisson-binomial) ===")
print("  %-6s %-8s %5s %5s %8s %8s %8s %7s   %s" % ("cua so","mien","n","trung","ti le","nen","chenh","z","ket luan"))
for nhan, lui in (("30 ngay", 29), ("90 ngay", 89), ("180 ngay", 179)):
    for reg in ("MN", "MT", "MB"):
        n = w = 0; e = v = 0.0
        for r in q("SELECT date,region,bach_thu,notes FROM final_bundles "
                   "WHERE region=? AND date>=date(?, ?) AND date<=? AND bach_thu_status IN ('WIN','LOSE')",
                   reg, NGAY, "-%d day" % lui, NGAY):
            if (r["notes"] or "").find("Phase 1.5 backfill") >= 0: continue
            d = tap.get((r["date"], r["region"]));  bt = (r["bach_thu"] or "").strip()
            if not d or not bt: continue
            p = len(d)/100.0
            n += 1; w += 1 if bt in d else 0; e += p; v += p*(1-p)
        if not n: continue
        sd = math.sqrt(v) if v > 0 else 0
        z = (w-e)/sd if sd else 0
        kl = "KEM nen CO Y NGHIA" if z < -1.96 else ("HON nen" if z > 1.96 else "khong tach duoc khoi nen")
        print("  %-6s %-8s %5d %5d %7.1f%% %7.1f%% %+7.1f %+7.2f   %s"
              % (nhan, reg, n, w, 100*w/n, 100*e/n, 100*(w-e)/n, z, kl))
    print()

print("=== 2 · ANTI-TRAP hom nay — MB chon 63, MT co db=63 ===")
for r in q("SELECT id,region,bach_thu,bach_thu_status,source_predictions_json FROM final_bundles WHERE date=? ORDER BY id", NGAY):
    j = json.loads(r["source_predictions_json"] or "{}")
    at = j.get("main_number_anti_trap") or {}
    print("  %s %s BT=%s (%s) level=%s hit_in=%s canh_bao=%s"
          % (r["id"], r["region"], r["bach_thu"], r["bach_thu_status"],
             at.get("level"), at.get("hit_in_regions"), (j.get("main_number_anti_trap_warning") or "")[:80]))
    rn = j.get("ranked_numbers") or []
    if rn:
        print("      ranked[0]=%s (score %s) · cong bo=%s · %s"
              % (rn[0].get("number"), rn[0].get("score"), r["bach_thu"],
                 "KHOP" if rn[0].get("number") == r["bach_thu"] else "*** DA BI LAT ***"))

print("\n=== 3 · combo-super TIMEOUT — xu huong 30 ngay ===")
cols = [x[1] for x in c.execute("PRAGMA table_info(scheduler_logs)").fetchall()]
m = "message" if "message" in cols else cols[-1]
rows = q("SELECT substr(datetime(log_time,'+7 hours'),1,10) ng, COUNT(*) n FROM scheduler_logs "
         "WHERE %s LIKE '%%Combo Super%%TIMEOUT%%' AND datetime(log_time,'+7 hours')>=date(?, '-29 day') "
         "GROUP BY ng ORDER BY ng" % m, NGAY)
print("  so ngay co TIMEOUT combo-super trong 30 ngay: %d" % len(rows))
for x in rows: print("     %s  %s lan" % (x["ng"], x["n"]))
r2 = q("SELECT substr(datetime(log_time,'+7 hours'),1,10) ng, %s msg FROM scheduler_logs "
       "WHERE %s LIKE '%%FAILED MODELS%%' AND datetime(log_time,'+7 hours')>=date(?, '-29 day') "
       "ORDER BY log_time DESC LIMIT 15" % (m, m), NGAY)
print("  -- 15 dong FAILED MODELS gan nhat --")
for x in r2: print("     %s %s" % (x["ng"], (x["msg"] or "")[:85]))

print("\n=== 4 · MT model_count 30 ngay ===")
for x in q("SELECT model_count, COUNT(*) n FROM final_bundles WHERE region='MT' "
           "AND date>=date(?, '-29 day') AND date<=? GROUP BY model_count ORDER BY model_count", NGAY, NGAY):
    print("  mc=%s : %s ngay" % (x["model_count"], x["n"]))
print("  day_status 30 ngay:")
for x in q("SELECT region, day_status, COUNT(*) n FROM day_governance "
           "WHERE date>=date(?, '-29 day') AND date<=? GROUP BY region, day_status ORDER BY region", NGAY, NGAY):
    print("     %-3s %-22s %s" % (x["region"], x["day_status"], x["n"]))
