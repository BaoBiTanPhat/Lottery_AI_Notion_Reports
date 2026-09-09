# -*- coding: utf-8 -*-
"""Q2 — MEMBERSHIP DIFF so voi so handoff (as_of 2026-09-09). CHI DOC."""
import sqlite3, datetime, json
DB="file:/root/Lottery_AI_Test/data/lottery_ai.db?mode=ro"
c=sqlite3.connect(DB,uri=True); c.row_factory=sqlite3.Row
SEL="SELECT p.date d, p.target_region r FROM predictions p "
JG=("LEFT JOIN day_governance dg ON p.date=dg.date AND p.target_region=dg.region "
    "WHERE p.ai_model='combo-super' AND p.status IN ('WIN','LOSE','PARTIAL') "
    "AND COALESCE(dg.evaluation_policy,'INCLUDE') NOT IN ('EXCLUDE_PRIMARY','EXCLUDE_ALL') ")
BF=("AND NOT EXISTS (SELECT 1 FROM final_bundles fb WHERE fb.date=p.date "
    "AND fb.region=p.target_region AND fb.status='ACTIVE' "
    "AND COALESCE(fb.notes,'') LIKE '%Phase 1.5 backfill%') ")
def rows(sql,*a): return [(x["d"],x["r"]) for x in c.execute(sql,a).fetchall()]
cur = rows(SEL+JG+"ORDER BY p.date DESC LIMIT 270")
new = rows(SEL+JG+"AND p.date>=? "+BF+"ORDER BY p.date DESC LIMIT 270","2026-06-12")
print("=== SO HANDOFF (chot 09/09 luc ~13:00) vs LIVE (bay gio) ===")
print("  handoff current : 270 dong / 156 ngay · MT 83 MN 145 MB 42")
print("  live    current : %d dong / %d ngay · %s" % (len(cur), len({d for d,_ in cur}),
      {r:sum(1 for _,x in cur if x==r) for r in ('MT','MN','MB')}))
print("  handoff both    : 161 dong / 86 ngay  (V11173+VA-h12)")
print("  handoff V11173  : 112 dong / 82 ngay · MT 12 MN 79 MB 21")
print("  live    V11173  : %d dong / %d ngay · %s" % (len(new), len({d for d,_ in new}),
      {r:sum(1 for _,x in new if x==r) for r in ('MT','MN','MB')}))
print("\n=== MEMBERSHIP DIFF: dong MOI xuat hien so voi anh chup handoff ===")
print("  (handoff chup truoc khi ngay 09/09 duoc verify)")
for d,r in sorted(x for x in new if x[0] >= "2026-09-09"):
    st=c.execute("SELECT status FROM predictions WHERE date=? AND target_region=? AND ai_model='combo-super'",(d,r)).fetchone()
    print("   + ADDED  %s %s  status=%s  ly do: auto_verify da cham ngay 09/09 sau khi handoff chup" % (d,r,st["status"] if st else "?"))
old_min=min(d for d,_ in cur)
print("\n=== dong bi DAY RA khoi LIMIT 270 (cua so truot — chinh la loi dang sua) ===")
print("   ranh duoi cua LIMIT 270 hien nay:", old_min, "(handoff ghi 2026-03-29)")
print("\n=== KIEM DOI SOAT: 90 bundle gan nhan vs 40 dong metric bi loai ===")
n_tag=c.execute("SELECT COUNT(*) FROM final_bundles WHERE status='ACTIVE' AND COALESCE(notes,'') LIKE '%Phase 1.5 backfill%'").fetchone()[0]
n_dr=c.execute("SELECT COUNT(DISTINCT date||'|'||region) FROM final_bundles WHERE status='ACTIVE' AND COALESCE(notes,'') LIKE '%Phase 1.5 backfill%'").fetchone()[0]
n_cs=c.execute("SELECT COUNT(*) FROM predictions p "+JG.replace("WHERE","WHERE")+
  "AND EXISTS(SELECT 1 FROM final_bundles fb WHERE fb.date=p.date AND fb.region=p.target_region "
  "AND fb.status='ACTIVE' AND COALESCE(fb.notes,'') LIKE '%Phase 1.5 backfill%')").fetchone()[0]
print("   bundle gan nhan backfill        : %d dong (grain = bundle)" % n_tag)
print("   cap (date,region) rieng biet    : %d" % n_dr)
print("   dong combo-super LOT qua WHERE  : %d  <== day moi la 'metric rows'" % n_cs)
print("   => 90 vs 40 KHONG mau thuan: 90 la grain BUNDLE (moi mien-ngay),")
print("      40 la grain METRIC ROW (chi combo-super, da qua loc status + day_governance).")
print("\n=== MT: 7 luot gan nhat HIEN NAY (chung minh chi so dang cu) ===")
for x in c.execute(SEL+JG+"AND p.target_region='MT' ORDER BY p.date DESC LIMIT 7").fetchall():
    print("   ", x["d"])
