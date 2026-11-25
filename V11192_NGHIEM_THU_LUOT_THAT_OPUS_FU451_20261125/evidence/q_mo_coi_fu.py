import sys
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, r"e:\Lottery_AI_Test\web\backend")
import _v10958_fu_reader as R
rows = R.load_fu_latest()
for r in rows:
    if r["id"] in ("FU-451", "FU-452"):
        print(r["id"], "|", r["status"], "|", r["title"][:70])
f = getattr(R, "trang_thai_mo_coi", None)
if f:
    out = f()
    print("mo_coi:", out if not isinstance(out, (list, dict)) else (out if len(str(out)) < 800 else str(out)[:800]))
