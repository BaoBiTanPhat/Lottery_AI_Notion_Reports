# -*- coding: utf-8 -*-
"""§Z-E — TINH GON ROSTER, thu tu gate DUNG: Gate1 -> Gate2(khong phan biet) -> Gate3 -> Gate4.
SUA so voi ban truoc: challenger uu tien HO CHUA CO DAI DIEN (Gate 3) TRUOC coverage (Gate 4).
"""
import json, sqlite3, sys, io
from datetime import date, timedelta
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0,"/root/Lottery_AI_Test/web/backend")
CHOT="2026-09-13"
import _v11184_cach_ly_provider as CL
from _v10872_deherd_selector import MODEL_FAMILY
from model_registry import MODEL_REGISTRY
dt=[m for m in MODEL_REGISTRY if m.get("class")=="TOKEN" and m.get("status")=="ACTIVE"
    and m.get("output_eligible") and m.get("provider")!="hybrid"]
ids=[m["id"] for m in dt]
HO={m["id"]: (MODEL_FAMILY.get(m["id"]) or ("PROV_"+str(m.get("provider")).upper())) for m in dt}
con=sqlite3.connect("file:/root/Lottery_AI_Test/data/lottery_ai.db?mode=ro",uri=True); c=con.cursor()
q=",".join("?"*len(ids)); kq={}
for w in (30,90):
    tu=(date.fromisoformat(CHOT)-timedelta(days=w-1)).isoformat()
    c.execute("SELECT ai_model,target_region,COUNT(*),"
              "SUM(CASE WHEN main_numbers NOT IN ('[]','') AND main_numbers IS NOT NULL THEN 1 ELSE 0 END) "
              "FROM predictions WHERE date BETWEEN ? AND ? AND run_source<>'shadow_auto_eval' "
              "AND ai_model IN (%s) GROUP BY 1,2"%q,[tu,CHOT]+ids)
    for mm,r,n,o in c.fetchall():
        kq.setdefault((mm,r),{})[w]=(100.0*(o or 0)/n if n else 0)
con.close()
ra={"ngay":CHOT,"nguon":"model_registry.MODEL_REGISTRY","mien":{}}
print("="*100); print("TINH GON ROSTER — Gate1 -> Gate3 -> Gate4"); print("="*100)
for reg in ("MN","MT","MB"):
    loai=[]; ung=[]
    for mm in ids:
        c30=kq.get((mm,reg),{}).get(30); c90=kq.get((mm,reg),{}).get(90)
        if c30 is None: loai.append((mm,"KHONG_CHAY_O_MIEN",None)); continue
        if CL.kiem(mm): loai.append((mm,"QUARANTINE_DETERMINISTIC",c30)); continue
        if c30<90: loai.append((mm,"QUARANTINE_COVERAGE",c30)); continue
        ung.append({"id":mm,"ho":HO[mm],"c30":c30,"c90":c90,
                    "gate1":"CORE_DU_DK" if c30>=95 else "PROBATION"})
    # Gate 3: moi ho mot dai dien tot nhat
    theo_ho={}
    for u in ung: theo_ho.setdefault(u["ho"],[]).append(u)
    dd=[]
    for f,ms in theo_ho.items():
        ms.sort(key=lambda z:(-z["c30"],-z["c90"],z["id"]))   # Gate 4
        dd.append(ms[0])
    dd.sort(key=lambda z:(-z["c30"],-z["c90"],z["id"]))
    core=[u for u in dd if u["gate1"]=="CORE_DU_DK"][:3]
    if len(core)<3:
        for u in dd:
            if u not in core and len(core)<3: core.append(u)
    ten_core={u["id"] for u in core}; ho_core={u["ho"] for u in core}
    # CHALLENGER: GATE 3 TRUOC — uu tien ho CHUA CO dai dien trong CORE
    con_lai=[u for u in ung if u["id"] not in ten_core]
    con_lai.sort(key=lambda z:(z["ho"] in ho_core, -z["c30"], -z["c90"], z["id"]))
    ch=con_lai[0] if con_lai else None
    bo=[u["id"] for u in con_lai[1:]]
    ra["mien"][reg]={"CORE":[{"id":u["id"],"ho":u["ho"],"cov30":round(u["c30"],1)} for u in core],
                     "CHALLENGER":({"id":ch["id"],"ho":ch["ho"],"cov30":round(ch["c30"],1)} if ch else None),
                     "BO_KHOI_ROSTER":bo,
                     "LOAI_BOI_GATE1":[{"id":a,"ly_do":b,"cov30":(round(c,1) if c is not None else None)} for a,b,c in loai],
                     "truoc":len(ids),"sau":len(core)+(1 if ch else 0),
                     "so_ho_doc_lap_CORE":len(ho_core)}
    print("--- %s ---"%reg)
    print("  CORE (%d ho doc lap): %s"%(len(ho_core),
          ", ".join("%s[%s] %.0f%%"%(u["id"],u["ho"],u["c30"]) for u in core)))
    print("  CHALLENGER: %s"%("%s[%s] %.0f%%  (ho %s CORE)"%(ch["id"],ch["ho"],ch["c30"],
          "TRUNG" if ch["ho"] in ho_core else "MOI, khong trung") if ch else "(khong)"))
    print("  BO KHOI ROSTER: %s"%(", ".join(bo) if bo else "(khong)"))
    print("  LOAI o Gate 1  : %s"%", ".join("%s(%s)"%(a,b) for a,b,_ in loai))
    print("  direct-token call/luot: %d -> %d (tran 4)"%(len(ids),len(core)+(1 if ch else 0)))
io.open("/tmp/z_roster_quyet_dinh.json","w",encoding="utf-8",newline="\n").write(
    json.dumps(ra,ensure_ascii=False,indent=1))
print(); print("-> /tmp/z_roster_quyet_dinh.json")
