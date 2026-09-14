# -*- coding: utf-8 -*-
"""V11186 §AB-K — RECEIPT COLLECTOR: bằng chứng SỐNG cho roster, CHỈ ĐỌC.

TUYỆT ĐỐI:
  · KHÔNG gọi provider. KHÔNG gọi API. KHÔNG ghi bảng official. KHÔNG ghi DB.
  · Chỉ đọc `predictions`, `final_bundles`, `prediction_trace.jsonl`, journal, config, process.
  · Ghi bằng chứng theo kiểu APPEND vào `artifacts/` — không sửa dòng cũ.

VÌ SAO CÓ TỆP NÀY: §AB hạ `MODEL_OUTSIDE_ROSTER_HTTP_CALLS=ZERO` của V11185 xuống
`STATIC_SCHEDULER_PROOF_ONLY` cho tới khi có receipt tự nhiên ba miền. Đây là bộ thu receipt đó.
Không được gọi provider tay để tạo bằng chứng (§AB-K).

GIỚI HẠN ĐÃ BIẾT, ghi thẳng chứ không giấu:
  · `prediction_trace.jsonl` là nguồn DUY NHẤT còn sống ghi token; nó KHÔNG ghi
    `request_fingerprint`, `caller`, `execution_class`. Nên receipt này phân biệt được
    «model nào chạm HTTP» và «bao nhiêu lượt», nhưng **chưa** phân biệt được lượt nào của
    scheduler và lượt nào của Combo. Việc đó cần patch dispatch của §AB-E/§AB-G.
  · Vì vậy mọi lượt vượt quá roster được ghi là `LUOT_THEM_CHUA_QUY_DUOC_NGUON`, KHÔNG
    được đoán bừa là của Combo.
"""
from __future__ import annotations

import hashlib
import io
import json
import os
import subprocess
import sys
from collections import Counter

BE = os.path.dirname(os.path.abspath(__file__))
GOC = os.path.dirname(os.path.dirname(BE))
DB = GOC + "/data/lottery_ai.db"
TRACE = BE + "/prediction_trace.jsonl"

CUTOFF = {"MN": "15:45", "MT": "16:58", "MB": "17:58"}


def sh(cmd):
    try:
        return subprocess.check_output(cmd, shell=True, cwd=GOC,
                                       stderr=subprocess.DEVNULL).decode().strip()
    except Exception as e:
        return "ERR:%s" % e


def doc_roster(region):
    sys.path.insert(0, BE)
    from _v11185_roster_goi_token import get_token_call_roster
    return get_token_call_roster(region=region)


def doc_cach_ly():
    sys.path.insert(0, BE)
    import _v11184_cach_ly_provider as CL
    return sorted(CL.danh_sach().keys())


def doc_trace(ngay):
    ra = []
    if not os.path.exists(TRACE):
        return ra
    for line in io.open(TRACE, encoding="utf-8", errors="replace"):
        line = line.strip()
        if not line:
            continue
        try:
            o = json.loads(line)
        except Exception:
            continue
        d = str(o.get("date") or o.get("date_str") or "")
        ts = str(o.get("ts") or o.get("timestamp") or o.get("created_at") or "")
        if d.startswith(ngay) or ts.startswith(ngay):
            ra.append(o)
    return ra


def thu_receipt(ngay, region):
    """Thu receipt cho MỘT miền. Trả dict đầy đủ + terminal."""
    import sqlite3
    r = {"artifact": "ROSTER_LIVE_RECEIPT", "muc": "Prompt 43 R1 §AB-K",
         "ngay": ngay, "mien": region,
         "thu_luc": sh("date '+%Y-%m-%dT%H:%M:%S%:z'")}

    ros = doc_roster(region)
    r["roster_version"] = ros.get("roster_version")
    r["roster_ok"] = ros.get("ok")
    r["model_duoc_phep"] = list(ros.get("models") or [])
    r["core"] = list(ros.get("core") or [])
    r["challenger"] = list(ros.get("challenger") or [])
    r["quarantined"] = doc_cach_ly()

    con = sqlite3.connect("file:" + DB + "?mode=ro", uri=True)
    c = con.cursor()

    # --- model ĐÃ SINH DÒNG predictions (bằng chứng scheduled + thành công) ---
    c.execute("SELECT ai_model, run_source, substr(created_at,12,8), main_numbers, late "
              "FROM predictions WHERE date=? AND target_region=? ORDER BY created_at",
              (ngay, region))
    dong = c.fetchall()
    r["predictions_rows"] = len(dong)
    r["model_co_dong_predictions"] = sorted({d[0] for d in dong})
    r["run_source_phan_bo"] = dict(Counter(d[1] for d in dong))
    r["so_dong_late"] = sum(1 for d in dong if d[4])
    r["so_dong_rong"] = sum(1 for d in dong if d[3] in ("[]", "", None))

    # --- cutoff compliance ---
    cut = CUTOFF.get(region)
    r["cutoff"] = cut
    r["dong_sau_cutoff"] = [{"model": d[0], "gio": d[2]} for d in dong if cut and d[2] > cut]

    # --- bundle ---
    c.execute("SELECT bach_thu, lo2, lo3, model_count, status, created_at, bundle_version "
              "FROM final_bundles WHERE date=? AND region=? AND status='ACTIVE'", (ngay, region))
    b = c.fetchone()
    r["bundle"] = ({"bach_thu": b[0], "lo2": b[1], "lo3": b[2], "model_count": b[3],
                    "status": b[4], "created_at": b[5], "bundle_version": b[6]} if b else None)
    con.close()

    # --- LƯỢT HTTP THẬT từ trace ---
    tr = [o for o in doc_trace(ngay)
          if str(o.get("region") or o.get("target_region") or "").upper() == region]
    r["trace_rows"] = len(tr)
    dem = Counter(str(o.get("model") or o.get("ai_model") or "?") for o in tr)
    r["model_cham_HTTP"] = dict(sorted(dem.items()))
    r["tong_token"] = sum(int(o.get("token_count") or 0) for o in tr)
    r["so_dong_co_cost"] = sum(1 for o in tr if o.get("cost_estimate") is not None)
    r["so_dong_thieu_cost"] = len(tr) - r["so_dong_co_cost"]

    cho_phep = set(r["model_duoc_phep"])
    cl = set(r["quarantined"])
    r["model_NGOAI_ROSTER_cham_HTTP"] = {m: n for m, n in dem.items() if m not in cho_phep}
    r["model_CACH_LY_cham_HTTP"] = {m: n for m, n in dem.items() if m in cl}
    r["so_model_duy_nhat_cham_HTTP"] = len(dem)

    # Lượt vượt quá 1/model — KHÔNG đoán nguồn (trace không ghi caller/fingerprint)
    r["luot_them_chua_quy_duoc_nguon"] = {m: n - 1 for m, n in dem.items() if n > 1}
    r["ghi_chu_luot_them"] = (
        "prediction_trace.jsonl KHONG ghi caller/execution_class/request_fingerprint, nen KHONG "
        "the quy luot them cho scheduler hay Combo. Can patch dispatch (§AB-E/§AB-G) moi phan "
        "biet duoc. KHONG doan.")

    # --- journal ---
    # CANH BAO DA SAP MOT LAN: `grep -c` tra MA THOAT 1 khi dem ra 0, nen `... || echo 0`
    # lam CA HAI cung chay va cho ra chuoi hai dong -> ban dau cua bo thu nay bao FAIL OAN.
    # Dung `; true` de nuot ma thoat, ep ve int, va -1 nghia la KHONG DOC DUOC (khac 0).
    def _dem(mau):
        v = sh("journalctl -u lottery --since '%s 00:00:00' --no-pager 2>/dev/null "
               "| grep -cE %s; true" % (ngay, mau))
        try:
            return int(str(v).strip().split(chr(10))[0])
        except Exception:
            return -1

    r["journal"] = {
        "ERROR_CRITICAL": _dem("' - (ERROR|CRITICAL) - '"),
        "traceback": _dem("'Traceback'"),
        "TOKEN_ROSTER_INVALID": _dem("'TOKEN_ROSTER_INVALID'"),
        "SHADOW_BOUNDED": _dem("'SHADOW_BOUNDED_V11185'"),
    }
    r["service"] = {
        "MainPID": sh("systemctl show lottery -p MainPID --value"),
        "NRestarts": sh("systemctl show lottery -p NRestarts --value"),
        "health": sh("curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:8000/api/health"),
    }

    # ================= CHẤM PASS/FAIL theo §AB-K =================
    kiem = []

    def k(ten, dat, ct=""):
        kiem.append({"phep": ten, "dat": bool(dat), "chi_tiet": ct})

    k("outside-roster HTTP = 0", not r["model_NGOAI_ROSTER_cham_HTTP"],
      str(r["model_NGOAI_ROSTER_cham_HTTP"]))
    k("quarantined HTTP = 0", not r["model_CACH_LY_cham_HTTP"], str(r["model_CACH_LY_cham_HTTP"]))
    k("so model duy nhat cham HTTP <= 4", r["so_model_duy_nhat_cham_HTTP"] <= 4,
      str(r["so_model_duy_nhat_cham_HTTP"]))
    k("khong dong nao sau cutoff", not r["dong_sau_cutoff"], str(r["dong_sau_cutoff"]))
    k("bundle sinh duoc", r["bundle"] is not None,
      (r["bundle"] or {}).get("bach_thu") if r["bundle"] else "KHONG CO")
    k("khong co TOKEN_ROSTER_INVALID", r["journal"]["TOKEN_ROSTER_INVALID"] == 0,
      str(r["journal"]["TOKEN_ROSTER_INVALID"]))
    k("0 ERROR/CRITICAL", r["journal"]["ERROR_CRITICAL"] == 0,
      str(r["journal"]["ERROR_CRITICAL"]))
    k("0 traceback", r["journal"]["traceback"] == 0, str(r["journal"]["traceback"]))
    k("health 200", r["service"]["health"] == "200", r["service"]["health"])
    k("roster doc duoc", r["roster_ok"] is True)

    r["kiem"] = kiem
    r["so_phep_dat"] = sum(1 for x in kiem if x["dat"])
    r["so_phep"] = len(kiem)
    dat_het = all(x["dat"] for x in kiem)

    # Trace có phủ hết không — nếu không thì KHÔNG được ghi terminal OK
    du_trace = r["trace_rows"] > 0
    r["trace_du_de_ket_luan"] = du_trace
    if not du_trace:
        r["terminal"] = "%s_ROSTER_LIVE_PROOF_FAIL" % region
        r["ly_do"] = "khong co dong trace nao cho mien nay — KHONG du bang chung de ket luan"
    elif dat_het:
        r["terminal"] = "%s_ROSTER_LIVE_PROOF_OK" % region
    else:
        r["terminal"] = "%s_ROSTER_LIVE_PROOF_FAIL" % region
        r["ly_do"] = "; ".join("%s (%s)" % (x["phep"], x["chi_tiet"])
                               for x in kiem if not x["dat"])

    r["receipt_sha256"] = hashlib.sha256(
        json.dumps({kk: vv for kk, vv in r.items() if kk != "thu_luc"},
                   sort_keys=True, ensure_ascii=False, default=str).encode()).hexdigest()
    return r


def ghi_append(r, out=None):
    """APPEND — không bao giờ sửa dòng cũ."""
    out = out or (GOC + "/artifacts/v11178/ROSTER_RECEIPTS.jsonl")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with io.open(out, "a", encoding="utf-8", newline=chr(10)) as f:
        f.write(json.dumps(r, ensure_ascii=False, default=str) + chr(10))
        f.flush()
        os.fsync(f.fileno())
    return out


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ngay = "2026-09-14"
    miens = ["MN", "MT", "MB"]
    for a in sys.argv[1:]:
        if a.startswith("--ngay="):
            ngay = a.split("=", 1)[1]
        elif a.startswith("--mien="):
            miens = [a.split("=", 1)[1].upper()]

    tong = []
    for reg in miens:
        r = thu_receipt(ngay, reg)
        tong.append(r)
        p = ghi_append(r)
        print("=" * 96)
        print("RECEIPT %s %s  ->  %s" % (reg, ngay, r["terminal"]))
        print("=" * 96)
        print("  roster %s: %s" % (r["roster_version"], r["model_duoc_phep"]))
        print("  predictions rows=%d  model=%s" % (r["predictions_rows"],
                                                   r["model_co_dong_predictions"]))
        print("  model chạm HTTP (trace): %s" % r["model_cham_HTTP"])
        print("  NGOÀI ROSTER chạm HTTP : %s" % (r["model_NGOAI_ROSTER_cham_HTTP"] or "{} ✓"))
        print("  CÁCH LY chạm HTTP      : %s" % (r["model_CACH_LY_cham_HTTP"] or "{} ✓"))
        print("  lượt thêm chưa quy nguồn: %s" % (r["luot_them_chua_quy_duoc_nguon"] or "{}"))
        print("  token=%d  thiếu cost=%d/%d" % (r["tong_token"], r["so_dong_thieu_cost"],
                                                r["trace_rows"]))
        print("  bundle=%s" % ((r["bundle"] or {}).get("bach_thu") or "CHƯA CÓ"))
        print("  phép đạt: %d/%d" % (r["so_phep_dat"], r["so_phep"]))
        for x in r["kiem"]:
            if not x["dat"]:
                print("     ✗ %s — %s" % (x["phep"], x["chi_tiet"]))
        print("  -> append %s" % p)
        print()

    ok = [r for r in tong if r["terminal"].endswith("_OK")]
    print("=" * 96)
    if len(miens) == 3 and len(ok) == 3:
        print("ROSTER_SYSTEM_WIDE_LIVE_PROOF_OK — đủ ba miền")
    else:
        print("CHƯA đủ ba miền PASS ⇒ KHÔNG được ghi ROSTER_SYSTEM_WIDE_LIVE_PROOF_OK")
        print("   đạt: %s" % [r["mien"] for r in ok])
    print("=" * 96)
    return 0


if __name__ == "__main__":
    sys.exit(main())
