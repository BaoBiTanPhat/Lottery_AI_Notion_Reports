# -*- coding: utf-8 -*-
"""V11183 §Y9c — SUC MANH PHEP DO cho ket luan bach thu cua chinh toi.
Ly do: "khong bac bo duoc H0" KHONG PHAI "da chung minh H0" (RM-04).
Tinh: khoang Wilson 95% cho delta, va n CAN de bat +5pp voi power .90.
"""
import json, sqlite3, sys
from math import sqrt
sys.stdout.reconfigure(encoding="utf-8")
DB="/root/Lottery_AI_Test/data/lottery_ai.db"; CHOT="2026-09-13"
def so_trong(o,ra):
    if isinstance(o,str): ra.append(o)
    elif isinstance(o,list):
        for x in o: so_trong(x,ra)
    elif isinstance(o,dict):
        for x in o.values(): so_trong(x,ra)
con=sqlite3.connect("file:"+DB+"?mode=ro",uri=True); c=con.cursor()
c.execute("SELECT substr(date,1,10),region,prizes_json FROM lottery_results WHERE substr(date,1,10)<=?",(CHOT,))
d2={}
for d,reg,pj in c.fetchall():
    ra=[]; so_trong(json.loads(pj),ra); s=d2.setdefault((d,reg),set())
    for x in ra:
        if x.isdigit() and len(x)>=2: s.add(x[-2:])
c.execute("SELECT date,region,bach_thu FROM final_bundles WHERE date<=? AND status='ACTIVE'",(CHOT,))
qs={}
for d,reg,bt in c.fetchall():
    t=d2.get((d,reg))
    if t and bt: qs[(d,reg)]=(1 if bt in t else 0, len(t)/100.0)
con.close()
Z=1.959964; ZA=1.644854; ZB=1.281552
print("="*112)
print("SUC MANH — bach thu, don vi (ngay x mien), nen rieng tung ngay")
print("="*112)
print("%-4s %5s %8s %8s %9s %-24s %12s %-28s"%("mien","n","ty_le","nen_TB","delta_pp","KTC_95_cho_delta_pp","n_can_+5pp","loai_tru_duoc"))
print("-"*112)
for reg in ("MN","MT","MB"):
    r=[v for (d,rr),v in qs.items() if rr==reg]
    n=len(r); h=sum(x for x,_ in r); p=h/n; p0=sum(pp for _,pp in r)/n
    # Wilson cho p
    den=1+Z*Z/n; ctr=(p+Z*Z/(2*n))/den; hw=Z*sqrt(p*(1-p)/n+Z*Z/(4*n*n))/den
    lo,hi=ctr-hw,ctr+hw
    nc=((ZA*sqrt(p0*(1-p0))+ZB*sqrt((p0+0.05)*(1-p0-0.05)))/0.05)**2
    print("%-4s %5d %7.1f%% %7.1f%% %+8.2f  [%+6.2f , %+6.2f]     %12d  loai tru lift > %+.2f pp"
          %(reg,n,100*p,100*p0,100*(p-p0),100*(lo-p0),100*(hi-p0),int(nc+0.5),100*(hi-p0)))
print("-"*112)
print()
print("DOC DUNG: p >= 0.34 o moi mien la KHONG BAC BO duoc nen — KHONG phai da chung minh khong co lift.")
print("Voi n hien co, chi loai tru duoc lift LON HON can tren KTC. Muon bat +5pp can so ngay o cot n_can.")
