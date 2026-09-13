# -*- coding: utf-8 -*-
"""Cham lai 13/09 tu prizes_json THO. Doc lap voi nhan cua production (RM-13)."""
import json, sqlite3, io, sys
sys.stdout.reconfigure(encoding="utf-8")
DB = "/root/Lottery_AI_Test/data/lottery_ai.db"
NGAY = "2026-09-13"
con = sqlite3.connect("file:" + DB + "?mode=ro", uri=True); c = con.cursor()

def so_trong(obj, ra):
    if isinstance(obj, str): ra.append(obj)
    elif isinstance(obj, list):
        for x in obj: so_trong(x, ra)
    elif isinstance(obj, dict):
        for x in obj.values(): so_trong(x, ra)

c.execute("SELECT region, station, prizes_json FROM lottery_results WHERE substr(date,1,10)=? ORDER BY region, station", (NGAY,))
theo_mien = {}
for reg, st, pj in c.fetchall():
    ra = []; so_trong(json.loads(pj), ra)
    so = [s for s in ra if s.isdigit()]
    d = theo_mien.setdefault(reg, {"dai": [], "duoi2": set(), "duoi3": set(), "n_giai": 0})
    d["dai"].append(st); d["n_giai"] += len(so)
    for s in so:
        if len(s) >= 2: d["duoi2"].add(s[-2:])
        if len(s) >= 3: d["duoi3"].add(s[-3:])

c.execute("SELECT region, bach_thu, lo2, lo3, bach_thu_status, lo2_status, lo3_status FROM final_bundles WHERE date=? ORDER BY region", (NGAY,))
bund = c.fetchall(); con.close()

print("=" * 96)
print("CHAM DOC LAP 13/09 — nguon: prizes_json tho")
print("=" * 96)
for reg in ("MN", "MT", "MB"):
    d = theo_mien.get(reg)
    if not d: print(reg, "KHONG CO KET QUA"); continue
    print("%-3s | %d dai (%s) | %d so giai | %d duoi-2 khac nhau | %d duoi-3 khac nhau"
          % (reg, len(d["dai"]), ", ".join(d["dai"]), d["n_giai"], len(d["duoi2"]), len(d["duoi3"])))
print()
hdr = "%-4s %-6s %-10s %-12s %-10s %-12s %-8s %-10s %-12s"
print(hdr % ("mien", "BT", "BT_doc_lap", "BT_production", "lo3", "lo3_doc_lap", "lo3_prod", "lo2_doc_lap", "lo2_prod"))
print("-" * 96)
tong_bt = 0
for reg, bt, lo2, lo3, bts, lo2s, lo3s in bund:
    d = theo_mien.get(reg, {"duoi2": set(), "duoi3": set()})
    bt_hit = bt in d["duoi2"]
    tong_bt += 1 if bt_hit else 0
    l2 = json.loads(lo2) if lo2 else []
    n2 = sum(1 for x in l2 if x in d["duoi2"])
    l2v = "WIN" if n2 == len(l2) and l2 else ("PARTIAL" if n2 else "LOSE")
    l3_hit = (lo3 in d["duoi3"]) if lo3 else None
    print(hdr % (reg, bt, "WIN" if bt_hit else "LOSE", bts,
                 lo3 or "-", ("WIN" if l3_hit else "LOSE") if lo3 else "-", lo3s,
                 "%s(%d/%d)" % (l2v, n2, len(l2)), lo2s))
print("-" * 96)
print("BACH THU DOC LAP: %d/3 WIN" % tong_bt)
print()
lech = []
for reg, bt, lo2, lo3, bts, lo2s, lo3s in bund:
    d = theo_mien.get(reg, {"duoi2": set(), "duoi3": set()})
    if ("WIN" if bt in d["duoi2"] else "LOSE") != bts: lech.append((reg, "bach_thu", bts))
    if lo3 and ("WIN" if lo3 in d["duoi3"] else "LOSE") != lo3s: lech.append((reg, "lo3", lo3s))
    l2 = json.loads(lo2) if lo2 else []
    n2 = sum(1 for x in l2 if x in d["duoi2"])
    l2v = "WIN" if n2 == len(l2) and l2 else ("PARTIAL" if n2 else "LOSE")
    if l2v != lo2s: lech.append((reg, "lo2", lo2s))
print("LECH giua cham doc lap va nhan production:", lech if lech else "KHONG CO — 9/9 khop")
