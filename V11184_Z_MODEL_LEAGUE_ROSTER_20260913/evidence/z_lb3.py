# -*- coding: utf-8 -*-
"""V11184 §Z-D (ban cuoi) — LEADERBOARD. Cong thuc DAY DU:
   score(n) = sum(components cua n) x (0.85 neu n bi pp1 dampener, nguoc lai 1.0)
   bach_thu = ranked[0]  TRU KHI mot trong 4 tang ghi de V10640/V10767/V10789/V10790 nổ.
LOO: bo model M => (a) tru components cua M, (b) neu M nam trong herd_voters va herd tut
     duoi 3 thi KHONG con dampener.
"""
import json, sqlite3, sys, io
from math import comb
from datetime import date, timedelta
sys.stdout.reconfigure(encoding="utf-8")
DB="/root/Lottery_AI_Test/data/lottery_ai.db"; CHOT="2026-09-13"; CUA_SO=(14,30,90,180)
FACTOR=0.85; NGUONG_HERD=3

def so_trong(o,ra):
    if isinstance(o,str): ra.append(o)
    elif isinstance(o,list):
        for x in o: so_trong(x,ra)
    elif isinstance(o,dict):
        for x in o.values(): so_trong(x,ra)

con=sqlite3.connect("file:"+DB+"?mode=ro",uri=True); c=con.cursor()
c.execute("SELECT substr(date,1,10),region,prizes_json FROM lottery_results WHERE substr(date,1,10)<=?",(CHOT,))
duoi2={}
for d,reg,pj in c.fetchall():
    ra=[]; so_trong(json.loads(pj),ra); s=duoi2.setdefault((d,reg),set())
    for x in ra:
        if x.isdigit() and len(x)>=2: s.add(x[-2:])
c.execute("SELECT date,region,bach_thu,source_predictions_json FROM final_bundles "
          "WHERE date<=? AND status='ACTIVE' ORDER BY date",(CHOT,))
rows=c.fetchall(); con.close()

def diem_so(sb, pp1_map, bo=None):
    """pp1_map: {number: set(herd_voters)}"""
    ra={}
    for m in sb:
        n=m["number"]
        s=sum(cp.get("score",0.0) for cp in m.get("components",[]) if cp.get("model")!=bo)
        if n in pp1_map:
            herd={v for v in pp1_map[n] if v!=bo}
            if len(herd)>=NGUONG_HERD: s*=FACTOR
        ra[n]=s
    return ra

du=[]
n_tl=0;k_tl=0;n_ovr=0
for d,reg,bt,spj in rows:
    if not spj: continue
    try: sp=json.loads(spj)
    except Exception: continue
    sb=sp.get("score_breakdown"); rn=sp.get("ranked_numbers")
    if not sb or not rn: continue
    ev=(sp.get("pp1_convergence_dampener") or {}).get("events") or []
    pp1={e["number"]:set(e.get("herd_voters") or []) for e in ev}
    diem=diem_so(sb,pp1)
    if not diem: continue
    t1=max(diem,key=lambda k:(diem[k],k))
    n_tl+=1; k_tl+= (t1==rn[0]["number"])
    ovr=(rn[0]["number"]!=bt); n_ovr+=ovr
    du.append({"d":d,"reg":reg,"bt":bt,"rank0":rn[0]["number"],"sb":sb,"pp1":pp1,"ovr":ovr})

print("="*106)
print("CONG TAI LAP (cong thuc DAY DU: components + pp1 dampener)")
print("="*106)
print("n bundle                     : %d"%n_tl)
print("tai lap == ranked[0]         : %d (%.2f%%)"%(k_tl,100.0*k_tl/n_tl))
print("ngay CO OVERRIDE lane/slice  : %d (%.1f%%)"%(n_ovr,100.0*n_ovr/n_tl))
if 100.0*k_tl/n_tl < 99:
    print("!! CHUA DAT 99% — dung."); sys.exit(2)
print("=> CONG DAT.")
print()

sach=[x for x in du if not x["ovr"] and duoi2.get((x["d"],x["reg"]))]
tm={}
for x in sach: tm[x["reg"]]=tm.get(x["reg"],0)+1
print("Ngay dung cho rescue/break (KHONG override, co ket qua): %d | %s"%(len(sach),tm))
print()

ket={}
for x in sach:
    tails=duoi2[(x["d"],x["reg"])]; bt=x["bt"]; goc=bt in tails
    models={cp["model"] for m in x["sb"] for cp in m.get("components",[])}
    for mo in models:
        dm=diem_so(x["sb"],x["pp1"],bo=mo)
        t1=max(dm,key=lambda k:(dm[k],k)) if dm else None
        moi=(t1 in tails) if t1 else None
        gop=any(cp.get("model")==mo for m in x["sb"] if m["number"]==bt
                for cp in m.get("components",[]))
        ket.setdefault((mo,x["reg"]),[]).append(
            {"d":x["d"],"rescue":goc and not moi,"break":(not goc) and moi,"gop":goc and gop})

out=[]
for (mo,reg),ds in sorted(ket.items()):
    for w in CUA_SO:
        tu=(date.fromisoformat(CHOT)-timedelta(days=w-1)).isoformat()
        s=[x for x in ds if tu<=x["d"]<=CHOT]
        if not s: continue
        r=sum(1 for x in s if x["rescue"]); b=sum(1 for x in s if x["break"])
        out.append({"model":mo,"mien":reg,"cua_so":w,"n":len(s),"rescue":r,"break":b,
                    "net":r-b,"gop_bt_thang":sum(1 for x in s if x["gop"])})
print("="*106)
print("NET RESCUE-MINUS-BREAK — cua so 30 ngay (Gate 2 §Z uu tien thuoc nay)")
print("="*106)
print("%-20s %-4s %5s %7s %7s %6s %8s"%("model","mien","n","rescue","break","net","gop_BT"))
print("-"*106)
for reg in ("MN","MT","MB"):
    r30=[o for o in out if o["mien"]==reg and o["cua_so"]==30]
    for o in sorted(r30,key=lambda z:(-z["net"],-z["rescue"],z["model"])):
        print("%-20s %-4s %5d %7d %7d %+6d %8d"%(o["model"],o["mien"],o["n"],o["rescue"],
              o["break"],o["net"],o["gop_bt_thang"]))
    print("-"*106)
io.open("/tmp/z_lb3.json","w",encoding="utf-8",newline="\n").write(json.dumps(
 {"cong":{"n":n_tl,"khop":k_tl,"n_override":n_ovr},"n_sach":len(sach),"theo_mien":tm,
  "rows":out},ensure_ascii=False,indent=1))
print("-> /tmp/z_lb3.json (%d dong)"%len(out))
