# -*- coding: utf-8 -*-
"""§Z-E6 — REPLAY: neu CHI giu roster da tinh gon, bach_thu co doi khong, va co te hon khong?
Dung cong thuc DAY DU da chung minh 99.38%: sum(components) x pp1 dampener.
CHI chay tren ngay KHONG override (vi ngay override do lane quyet, khong do phieu model).
"""
import json, sqlite3, sys, io
from datetime import date, timedelta
sys.stdout.reconfigure(encoding="utf-8")
CHOT="2026-09-13"; FACTOR=0.85; NGUONG=3
QD=json.load(io.open("/tmp/z_roster_quyet_dinh.json",encoding="utf-8"))
GIU={}
for reg,v in QD["mien"].items():
    s={u["id"] for u in v["CORE"]}
    if v["CHALLENGER"]: s.add(v["CHALLENGER"]["id"])
    GIU[reg]=s
print("Roster giu lai:"); 
for r,s in GIU.items(): print("  %s: %s"%(r,sorted(s)))
print()
def so_trong(o,ra):
    if isinstance(o,str): ra.append(o)
    elif isinstance(o,list):
        for x in o: so_trong(x,ra)
    elif isinstance(o,dict):
        for x in o.values(): so_trong(x,ra)
con=sqlite3.connect("file:/root/Lottery_AI_Test/data/lottery_ai.db?mode=ro",uri=True); c=con.cursor()
c.execute("SELECT substr(date,1,10),region,prizes_json FROM lottery_results WHERE substr(date,1,10)<=?",(CHOT,))
d2={}
for d,reg,pj in c.fetchall():
    ra=[]; so_trong(json.loads(pj),ra); s=d2.setdefault((d,reg),set())
    for x in ra:
        if x.isdigit() and len(x)>=2: s.add(x[-2:])
c.execute("SELECT date,region,bach_thu,source_predictions_json FROM final_bundles "
          "WHERE date<=? AND status='ACTIVE' ORDER BY date",(CHOT,))
rows=c.fetchall(); con.close()

# BO DIRECT-TOKEN LLM bi loai; GIU nguyen ML local + derived (khong ton token, khong trong pham vi)
LLM_TOKEN={"claude-opus-4-6","claude-sonnet-4-6","deepseek-reasoner","gemini-2.5-flash",
           "gemini-2.5-pro","glm-5.1","gpt-5.4","gpt-oss-120b"}
def diem(sb,pp1,giu_llm):
    ra={}
    for m in sb:
        n=m["number"]; s=0.0
        for cp in m.get("components",[]):
            mo=cp.get("model")
            if mo in LLM_TOKEN and mo not in giu_llm: continue
            s+=cp.get("score",0.0)
        if n in pp1:
            herd={v for v in pp1[n] if not(v in LLM_TOKEN and v not in giu_llm)}
            if len(herd)>=NGUONG: s*=FACTOR
        ra[n]=s
    return ra
kq={}
for d,reg,bt,spj in rows:
    if not spj: continue
    try: sp=json.loads(spj)
    except Exception: continue
    sb=sp.get("score_breakdown"); rn=sp.get("ranked_numbers")
    tails=d2.get((d,reg))
    if not sb or not rn or not tails: continue
    if rn[0]["number"]!=bt: continue      # ngay OVERRIDE — bo
    ev=(sp.get("pp1_convergence_dampener") or {}).get("events") or []
    pp1={e["number"]:set(e.get("herd_voters") or []) for e in ev}
    dm=diem(sb,pp1,GIU.get(reg,set()))
    if not dm: continue
    t1=max(dm,key=lambda k:(dm[k],k))
    e=kq.setdefault(reg,{"n":0,"cu_trung":0,"moi_trung":0,"doi":0,"xau_di":0,"tot_len":0})
    e["n"]+=1
    cu=bt in tails; moi=t1 in tails
    e["cu_trung"]+=cu; e["moi_trung"]+=moi; e["doi"]+= (t1!=bt)
    if cu and not moi: e["xau_di"]+=1
    if moi and not cu: e["tot_len"]+=1
print("="*104)
print("REPLAY — giu roster tinh gon, tinh lai bach_thu tren TOAN BO ngay khong-override")
print("="*104)
print("%-4s %6s %10s %10s %8s %9s %9s %10s"%("mien","n","BT_cu_trung","BT_moi_trung","doi_so","xau_di","tot_len","delta_pp"))
print("-"*104)
for reg in ("MN","MT","MB"):
    e=kq.get(reg)
    if not e: continue
    a=100.0*e["cu_trung"]/e["n"]; b=100.0*e["moi_trung"]/e["n"]
    print("%-4s %6d %6d %4.1f%% %6d %4.1f%% %8d %9d %9d %+9.2f"%(reg,e["n"],e["cu_trung"],a,
          e["moi_trung"],b,e["doi"],e["xau_di"],e["tot_len"],b-a))
print("-"*104)
print()
print("DOC DUNG: delta duong khong co nghia la 'tot hon' — day la do TRONG MAU tren chinh")
print("du lieu lich su, khong phai du bao. Xem test dau ben duoi.")
from math import comb
for reg in ("MN","MT","MB"):
    e=kq.get(reg)
    if not e: continue
    n=e["xau_di"]+e["tot_len"]
    if n==0: print("  %s: 0 ngay doi ket qua => KHONG co bang chung khac biet"%reg); continue
    k=max(e["xau_di"],e["tot_len"])
    p=min(1.0,2*sum(comb(n,i) for i in range(k,n+1))/2**n)
    print("  %s: %d ngay doi ket qua (%d xau di / %d tot len), test dau p=%.4f => %s"
          %(reg,n,e["xau_di"],e["tot_len"],p,"CO Y NGHIA" if p<0.05 else "khong khac 0"))
