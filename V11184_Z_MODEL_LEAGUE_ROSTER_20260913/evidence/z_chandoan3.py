# -*- coding: utf-8 -*-
"""Trong ca LECH: bach_thu co nam trong ranked_numbers khong?
 - KHONG nam trong  => json DA CU (stale), bach_thu den tu lan ghi SAU
 - Nam nhung khong o vi tri 0 => co buoc CHON LAI sau khi xep hang
"""
import json, sqlite3, sys
sys.stdout.reconfigure(encoding="utf-8")
con=sqlite3.connect("file:/root/Lottery_AI_Test/data/lottery_ai.db?mode=ro",uri=True); c=con.cursor()
c.execute("SELECT date,region,bach_thu,created_at,updated_at,source_predictions_json "
          "FROM final_bundles WHERE status='ACTIVE' ORDER BY date")
rows=c.fetchall(); con.close()
khong_co=0; co_nhung_khac_vi_tri=0; vi_tri=[]; khop=0; tong=0
mau=[]
for d,reg,bt,ca,ua,spj in rows:
    if not spj: continue
    try: sp=json.loads(spj)
    except Exception: continue
    rn=sp.get("ranked_numbers")
    if not rn: continue
    tong+=1
    nums=[x["number"] for x in rn]
    if nums and nums[0]==bt: khop+=1; continue
    if bt not in nums:
        khong_co+=1
        if len(mau)<4: mau.append((d,reg,bt,nums[:5],(ca or "")[:19],(ua or "")[:19]))
    else:
        co_nhung_khac_vi_tri+=1; vi_tri.append(nums.index(bt))
print("="*96)
print("PHAN LOAI CA LECH (tong %d bundle co ranked_numbers)"%tong)
print("="*96)
lech=tong-khop
print("khop ranked[0]==bach_thu          : %d (%.1f%%)"%(khop,100.0*khop/tong))
print("LECH                              : %d (%.1f%%)"%(lech,100.0*lech/tong))
print("  - bach_thu KHONG CO trong ranked: %d (%.1f%% cua ca lech)  <= json DA CU"
      %(khong_co,100.0*khong_co/lech if lech else 0))
print("  - co nhung khac vi tri          : %d (%.1f%% cua ca lech)"
      %(co_nhung_khac_vi_tri,100.0*co_nhung_khac_vi_tri/lech if lech else 0))
if vi_tri:
    from collections import Counter
    print("    phan bo vi tri:",dict(sorted(Counter(vi_tri).items())))
print()
print("=== vai ca bach_thu KHONG CO trong ranked ===")
for d,reg,bt,top5,ca,ua in mau:
    print("  %s %s bach_thu=%s | ranked top5=%s | created=%s updated=%s"%(d,reg,bt,top5,ca,ua))
