# -*- coding: utf-8 -*-
"""V11187 §AB-K — QUY NGUỒN LƯỢT GỌI NGOÀI ROSTER bằng LỒNG THỜI GIAN.

VÌ SAO CÓ TỆP NÀY. Receipt MB ngày 14/09 ra `MB_ROSTER_LIVE_PROOF_FAIL`:
`gemini-2.5-pro` — model NGOÀI roster MB — chạm HTTP một lượt dưới chính bản V11185
đang chạy. `prediction_trace.jsonl` KHÔNG ghi `caller`/`execution_class`, nên bộ thu
receipt (đúng đắn) chỉ dám ghi `LUOT_THEM_CHUA_QUY_DUOC_NGUON` và KHÔNG đoán.

Tệp này quy nguồn bằng một thứ ĐỘC LẬP với trace: `scheduler_logs` ghi mốc bắt đầu và
mốc kết thúc của Combo Super cho từng miền. Nếu khoảng [bắt đầu, kết thúc] của Combo
CHỨA TRỌN lượt gọi (suy từ `timestamp` và `latency_seconds` của trace), thì lượt đó
thuộc Combo.

MỨC BẰNG CHỨNG — ghi đúng tầng, KHÔNG nâng cấp:
    `QUY_DUOC_BANG_LONG_THOI_GIAN` ≠ `QUY_DUOC_BANG_TRUONG_CALLER`.
Lồng thời gian là bằng chứng ngoại vi rất mạnh (Combo là bước CUỐI CÙNG của
`_run_ai_models_predict`, sau diversity pass — `scheduler.py:5114`), nhưng bằng chứng
DỨT ĐIỂM chỉ có sau khi §AB deploy: khi ấy mỗi lượt mang `caller` + `execution_class` +
`request_fingerprint` và câu hỏi này tự trả lời.

Chạy TRÊN VPS (chỉ đọc):
    /root/Lottery_AI_Test/venv/bin/python3 _v11187_quy_nguon_combo.py [--ngay=YYYY-MM-DD]
"""
from __future__ import annotations

import datetime as dt
import io
import json
import os
import re
import sqlite3
import sys

sys.stdout.reconfigure(encoding="utf-8")
BE = os.path.dirname(os.path.abspath(__file__))
GOC = os.path.dirname(os.path.dirname(BE))
DB = os.path.join(GOC, "data", "lottery_ai.db")
TRACE = os.path.join(BE, "prediction_trace.jsonl")

NGAY = "2026-09-14"
for a in sys.argv[1:]:
    if a.startswith("--ngay="):
        NGAY = a.split("=", 1)[1]


def _roster(mien):
    sys.path.insert(0, BE)
    import _v11185_roster_goi_token as R
    r = R.get_token_call_roster(region=mien, execution_class="official")
    return (set(r["models"]), r.get("roster_version")) if r.get("ok") else (None, r.get("ma_loi"))


# ---------------------------------------------------------------- 1 · cửa sổ Combo
# `scheduler_logs.log_time` là NAIVE và là UTC (§55) ⇒ PHẢI cộng 7 giờ.
cua_so = {}
cn = sqlite3.connect("file:%s?mode=ro" % DB.replace("\\", "/"), uri=True)
q = ("SELECT datetime(log_time,'+7 hours'), message FROM scheduler_logs "
     "WHERE date(log_time,'+7 hours')=? AND message LIKE '%COMBO Super%' ORDER BY id")
for vn, msg in cn.execute(q, (NGAY,)):
    m = re.search(r"COMBO Super:?\s+(MN|MT|MB)", msg)
    if not m:
        m = re.search(r"COMBO Super\s+(MN|MT|MB)\s*:", msg)
    if not m:
        continue
    mien = m.group(1)
    d = cua_so.setdefault(mien, {"bat_dau": None, "ket_thuc": None})
    if "🚀" in msg or "COMBO Super:" in msg:
        if d["bat_dau"] is None:
            d["bat_dau"] = vn
    if "✅" in msg:
        d["ket_thuc"] = vn

# ---------------------------------------------------------------- 2 · lượt gọi trong trace
luot = {}
for l in io.open(TRACE, encoding="utf-8"):
    l = l.strip()
    if not l:
        continue
    try:
        d = json.loads(l)
    except Exception:
        continue
    if d.get("date") != NGAY:
        continue
    mien = d.get("target_region") or d.get("region")
    if mien not in ("MN", "MT", "MB"):
        continue
    ts = d.get("timestamp")
    lat = d.get("latency_seconds") or d.get("duration_seconds") or 0.0
    try:
        xong = dt.datetime.fromisoformat(ts)
    except Exception:
        continue
    luot.setdefault(mien, []).append({
        "model": d.get("model"), "xong": xong,
        "bat_dau": xong - dt.timedelta(seconds=float(lat)),
        "lat": round(float(lat), 1),
        "prompt_chars": d.get("runtime_prompt_chars"),
    })

# ---------------------------------------------------------------- 3 · quy nguồn
bang = []
for mien in ("MN", "MT", "MB"):
    rs, ver = _roster(mien)
    cs = cua_so.get(mien, {})
    try:
        cs_bd = dt.datetime.fromisoformat(cs["bat_dau"]) if cs.get("bat_dau") else None
        cs_kt = dt.datetime.fromisoformat(cs["ket_thuc"]) if cs.get("ket_thuc") else None
    except Exception:
        cs_bd = cs_kt = None
    for g in sorted(luot.get(mien, []), key=lambda x: x["xong"]):
        trong_combo = (cs_bd is not None and cs_kt is not None
                       and cs_bd <= g["bat_dau"] and g["xong"] <= cs_kt)
        ngoai_roster = (rs is not None and g["model"] not in rs)
        bang.append({
            "mien": mien, "model": g["model"],
            "bat_dau": g["bat_dau"].strftime("%H:%M:%S"),
            "xong": g["xong"].strftime("%H:%M:%S"), "lat": g["lat"],
            "prompt_chars": g["prompt_chars"],
            "ngoai_roster": ngoai_roster,
            "nguon": ("COMBO_SUPER" if trong_combo else "CHUOI_CHINH_HOAC_KHAC"),
            "muc_bang_chung": ("QUY_DUOC_BANG_LONG_THOI_GIAN" if trong_combo
                               else "SUY_LOAI_TRU_KHONG_PHAI_COMBO"),
        })

cn.close()

print("=" * 100)
print("  QUY NGUON LUOT GOI — ngay %s · moc Combo lay tu scheduler_logs (UTC +7 theo §55)" % NGAY)
print("=" * 100)
for mien in ("MN", "MT", "MB"):
    cs = cua_so.get(mien, {})
    giay = ""
    try:
        giay = " (%.0fs)" % (dt.datetime.fromisoformat(cs["ket_thuc"])
                             - dt.datetime.fromisoformat(cs["bat_dau"])).total_seconds()
    except Exception:
        pass
    print("  %s · Combo Super: %s -> %s%s"
          % (mien, cs.get("bat_dau", "?"), cs.get("ket_thuc", "?"), giay))
print("-" * 100)
print("  %-4s %-20s %-9s %-9s %-8s %-8s %-6s %s"
      % ("mien", "model", "bat dau", "xong", "lat", "prompt", "ngoai?", "nguon"))
for r in bang:
    print("  %-4s %-20s %-9s %-9s %-8s %-8s %-6s %s"
          % (r["mien"], r["model"], r["bat_dau"], r["xong"], r["lat"],
             r["prompt_chars"], "NGOAI" if r["ngoai_roster"] else "", r["nguon"]))
print("-" * 100)
vi_pham = [r for r in bang if r["ngoai_roster"]]
if vi_pham:
    for r in vi_pham:
        print("  VI PHAM ROSTER: %s@%s do %s goi — muc bang chung %s"
              % (r["model"], r["mien"], r["nguon"], r["muc_bang_chung"]))
else:
    print("  Khong co luot nao ngoai roster.")
print("  LUU Y: long thoi gian KHONG phai truong `caller`. Bang chung dut diem chi co sau khi")
print("         §AB deploy — moi luot se mang caller + execution_class + request_fingerprint.")
print("=" * 100)

if "--json" in sys.argv:
    print(json.dumps({"ngay": NGAY, "cua_so_combo": cua_so, "luot": bang},
                     ensure_ascii=False, indent=1))
