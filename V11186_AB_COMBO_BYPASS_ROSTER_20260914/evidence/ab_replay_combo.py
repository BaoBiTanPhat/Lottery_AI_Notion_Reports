# -*- coding: utf-8 -*-
"""§AB-H — replay Combo: pool truoc vs sau roster gate, tren du lieu that.
CHI DOC. Khong goi provider. Khong ghi DB."""
import json, sqlite3, sys
from collections import Counter
sys.path.insert(0,"/root/Lottery_AI_Test/web/backend")
sys.stdout.reconfigure(encoding="utf-8")
import _v11185_roster_goi_token as R

POOL = ["claude-sonnet-4-6","gemini-2.5-flash","claude-opus-4-6","gemini-2.5-pro",
        "deepseek-reasoner","glm-5.1","gpt-oss-120b","gemini-3.5-flash","gemini-3.6-flash"]
con=sqlite3.connect("file:/root/Lottery_AI_Test/data/lottery_ai.db?mode=ro",uri=True)
c=con.cursor()
print("="*100)
print("§AB-H REPLAY COMBO — pool 9 model TRUOC vs SAU roster gate")
print("="*100)
print("%-5s %-46s %-28s %s"%("mien","duoc phep sau gate","bi loai","so luot goi tiet kiem/ngay"))
print("-"*100)
tong_tiet_kiem=0
for reg in ("MN","MT","MB"):
    r=R.get_token_call_roster(region=reg)
    cho=set(r["models"])
    sau=[m for m in POOL if m in cho]
    loai=[m for m in POOL if m not in cho]
    # Combo chon top-3 TOAN BANG (ML+AI), so AI thuc te duoc goi <= min(3, len(sau))
    tiet=max(0,min(3,len(POOL))-min(3,len(sau))) if len(sau)<3 else 0
    print("%-5s %-46s %-28s %s"%(reg,", ".join(sau),"%d model"%len(loai),
          "toi da %d"%min(3,len(sau))))
    tong_tiet_kiem+=len(loai)
print("-"*100)
print("Model bi loai khoi pool Combo (moi mien):")
for reg in ("MN","MT","MB"):
    cho=set(R.get_token_call_roster(region=reg)["models"])
    print("  %s: %s"%(reg,[m for m in POOL if m not in cho]))
print()
print("="*100)
print("LICH SU: Combo da tung chon model NGOAI roster bao nhieu lan? (30 ngay)")
print("="*100)
c.execute("""SELECT date, region, source_predictions_json FROM final_bundles
             WHERE date BETWEEN '2026-08-15' AND '2026-09-13' AND status='ACTIVE'""")
dem_ngoai=Counter(); tong_ngay=0
for d,reg,spj in c.fetchall():
    if not spj: continue
    try: sp=json.loads(spj)
    except Exception: continue
    sb=sp.get("score_breakdown") or []
    models={cp.get("model") for m in sb for cp in m.get("components",[])}
    r=R.get_token_call_roster(region=reg)
    if not r["ok"]: continue
    cho=set(r["models"]); tong_ngay+=1
    for m in models:
        if m in POOL and m not in cho: dem_ngoai[(reg,m)]+=1
con.close()
print("so ngay-mien xet: %d"%tong_ngay)
if dem_ngoai:
    print("%-5s %-22s %s"%("mien","model NGOAI roster","so ngay co mat trong bundle"))
    print("-"*100)
    for (reg,m),n in sorted(dem_ngoai.items(),key=lambda x:-x[1]):
        print("%-5s %-22s %d"%(reg,m,n))
else:
    print("KHONG co model ngoai roster nao tung vao bundle trong 30 ngay")
print()
print("DOC DUNG: day la so ngay model do CO MAT trong score_breakdown — tuc da duoc GOI.")
print("Sau roster gate, nhung luot goi do se KHONG con xay ra.")
