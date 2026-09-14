# -*- coding: utf-8 -*-
"""V11187 §AB-J/§AB-V — PREFLIGHT DEPLOY gói §AB: trả lời ĐÚNG MỘT câu «giờ deploy được chưa?».

CHỈ ĐỌC. Không copy tệp, không restart, không gọi provider, không ghi DB.
Mặc định in bảng người đọc; `--json` in máy đọc; `--ghi` lưu ảnh chụp vào artifacts/.

VÌ SAO CÓ TỆP NÀY — §AB-J cấm tuyệt đối: «deploy patch nửa vời · thay code giữa MN/MT/MB ·
MN một version, MT/MB version khác · restart khi provider job đang chạy · backdate config ·
ép xanh để kịp giờ». Sáu điều đó là sáu phép kiểm máy chạy được, không phải lời dặn. Phiên
14/09 suýt phá epoch chỉ vì tin mốc giờ viết trong prompt mà không chạy `date` — nên phép
đầu tiên ở đây là ĐỒNG HỒ THẬT.

Chạy TRÊN VPS:
    /root/Lottery_AI_Test/venv/bin/python3 _v11187_preflight_deploy.py
Mã thoát 0 = GO (mọi phép ĐẠT) · 1 = NO-GO (in đúng phép nào chặn và vì sao).
"""
from __future__ import annotations

import datetime as dt
import hashlib
import io
import json
import os
import sqlite3
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8")
BE = os.path.dirname(os.path.abspath(__file__))
GOC = os.path.dirname(os.path.dirname(BE))
DB = os.path.join(GOC, "data", "lottery_ai.db")
TRACE = os.path.join(BE, "prediction_trace.jsonl")
RECEIPTS = os.path.join(GOC, "artifacts", "v11178", "ROSTER_RECEIPTS.jsonl")
BACKUPS = os.path.join(GOC, "backups")

NGAY_EPOCH = "2026-09-14"          # ngày phải khép trọn dưới V11185
MO_CUA_TU = dt.datetime(2026, 9, 14, 20, 0, 0)    # sau EOD ba miền
DONG_CUA_LUC = dt.datetime(2026, 9, 15, 4, 0, 0)  # §AA-I: hiệu lực trước 04:00
PHUT_IM_LANG_TOI_THIEU = 20        # trace phải im ngần này mới coi là không có run đang bay
TEP_DEPLOY = ["combo_super.py", "gpt_analyzer.py", "scheduler.py", "main.py",
              "_v11185_roster_goi_token.py"]
BANG_KHOA = ["predictions", "final_bundles", "lottery_results", "model_daily_eval"]

KQ = []


def phep(ma, ten, dat, chi_tiet=""):
    KQ.append({"ma": ma, "ten": ten, "dat": bool(dat), "chi_tiet": str(chi_tiet)})


def _sha(duong):
    try:
        return hashlib.sha256(io.open(duong, "rb").read()).hexdigest()
    except Exception as e:
        return "KHONG_DOC_DUOC:%r" % e


def _chay(lenh):
    try:
        r = subprocess.run(lenh, shell=True, capture_output=True, text=True, timeout=30)
        return r.returncode, (r.stdout or "") + (r.stderr or "")
    except Exception as e:
        return -1, repr(e)


# ---------------------------------------------------------------- C1 · đồng hồ thật
bay_gio = dt.datetime.now()
trong_cua = MO_CUA_TU <= bay_gio < DONG_CUA_LUC
phep("C1", "Dong ho THAT nam trong cua so deploy",
     trong_cua,
     "bay gio %s · cua so [%s, %s)" % (bay_gio.strftime("%Y-%m-%d %H:%M:%S"),
                                       MO_CUA_TU.strftime("%m-%d %H:%M"),
                                       DONG_CUA_LUC.strftime("%m-%d %H:%M")))

# ---------------------------------------------------------------- C2 · epoch đã khép
co_bundle = {}
try:
    cn = sqlite3.connect("file:%s?mode=ro" % DB.replace("\\", "/"), uri=True)
    for m in ("MN", "MT", "MB"):
        r = cn.execute("SELECT COUNT(*), MAX(created_at) FROM final_bundles "
                       "WHERE date=? AND region=? AND status='ACTIVE'",
                       (NGAY_EPOCH, m)).fetchone()
        co_bundle[m] = {"so": r[0], "tao_luc": r[1]}
except Exception as e:
    co_bundle = {"LOI": repr(e)}
    cn = None
du_ba_mien = all(isinstance(co_bundle.get(m), dict) and co_bundle[m]["so"] >= 1
                 for m in ("MN", "MT", "MB"))
phep("C2", "Ca BA mien da co bundle ACTIVE ngay %s (epoch V11185 khep tron)" % NGAY_EPOCH,
     du_ba_mien,
     " · ".join("%s=%s@%s" % (m, co_bundle.get(m, {}).get("so"),
                              co_bundle.get(m, {}).get("tao_luc"))
                for m in ("MN", "MT", "MB")) if isinstance(co_bundle, dict) else str(co_bundle))

# ---------------------------------------------------------------- C3 · không có run đang bay
cuoi_trace = None
try:
    with io.open(TRACE, "rb") as f:
        f.seek(0, os.SEEK_END)
        cuoi = min(f.tell(), 200000)
        f.seek(-cuoi, os.SEEK_END)
        dong = [l for l in f.read().decode("utf-8", "replace").split("\n") if l.strip()]
    cuoi_trace = json.loads(dong[-1]).get("timestamp")
except Exception as e:
    cuoi_trace = "KHONG_DOC_DUOC:%r" % e
im_lang_phut = None
try:
    im_lang_phut = (bay_gio - dt.datetime.fromisoformat(cuoi_trace)).total_seconds() / 60.0
except Exception:
    pass
phep("C3", "KHONG co provider job dang bay (trace im >= %d phut)" % PHUT_IM_LANG_TOI_THIEU,
     im_lang_phut is not None and im_lang_phut >= PHUT_IM_LANG_TOI_THIEU,
     "dong trace cuoi %s · im %s phut"
     % (cuoi_trace, "?" if im_lang_phut is None else round(im_lang_phut, 1)))

# ---------------------------------------------------------------- C4 · ba receipt tự nhiên
mien_co_receipt = {}
try:
    for l in io.open(RECEIPTS, encoding="utf-8"):
        l = l.strip()
        if not l:
            continue
        d = json.loads(l)
        if d.get("ngay") == NGAY_EPOCH or d.get("date") == NGAY_EPOCH:
            m = d.get("mien") or d.get("region")
            if m:
                mien_co_receipt[m] = d.get("terminal") or d.get("ket_qua") or "?"
except Exception as e:
    mien_co_receipt = {"LOI": repr(e)}
du_receipt = all(m in mien_co_receipt for m in ("MN", "MT", "MB"))
phep("C4", "Da thu receipt TU NHIEN ca ba mien ngay %s" % NGAY_EPOCH,
     du_receipt,
     json.dumps(mien_co_receipt, ensure_ascii=False))

# ---------------------------------------------------------------- C5 · backup CẤP 1 dùng được
thieu, lech = [], []
for f in TEP_DEPLOY:
    bk = os.path.join(BACKUPS, f + ".pre_v11186")
    live = os.path.join(BE, f)
    if not os.path.exists(bk):
        thieu.append(f)
    elif _sha(bk) != _sha(live):
        lech.append(f)
phep("C5", "Backup CAP 1 .pre_v11186 co DU va KHOP ban dang chay",
     not thieu and not lech,
     "thieu=%s · lech=%s" % (thieu or "khong", lech or "khong"))

# ---------------------------------------------------------------- C6 · service lành
ma, out = _chay("systemctl show -p MainPID,NRestarts,ActiveState lottery")
pid_truoc = nrestarts = active = "?"
for d in out.split("\n"):
    if d.startswith("MainPID="):
        pid_truoc = d.split("=", 1)[1].strip()
    elif d.startswith("NRestarts="):
        nrestarts = d.split("=", 1)[1].strip()
    elif d.startswith("ActiveState="):
        active = d.split("=", 1)[1].strip()
ma2, out2 = _chay("curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:8000/api/health")
health = out2.strip()
phep("C6", "Service lanh TRUOC khi dong vao", active == "active" and health == "200",
     "ActiveState=%s · health=%s · MainPID=%s · NRestarts=%s"
     % (active, health, pid_truoc, nrestarts))

# ---------------------------------------------------------------- C7 · ảnh chụp để so SAU deploy
anh = {"thoi_diem": bay_gio.isoformat(timespec="seconds"),
       "pid_truoc": pid_truoc, "nrestarts_truoc": nrestarts,
       "sha_dang_chay": {f: _sha(os.path.join(BE, f))[:16] for f in TEP_DEPLOY},
       "bang_khoa": {}}
try:
    if cn:
        for b in BANG_KHOA:
            r = cn.execute("SELECT COUNT(*) FROM %s" % b).fetchone()
            anh["bang_khoa"][b] = r[0]
except Exception as e:
    anh["bang_khoa"] = {"LOI": repr(e)}
ma3, out3 = _chay("crontab -l")
if ma3 == 0:
    _d = out3.split("\n")
    anh["crontab_sha"] = hashlib.sha256(out3.encode("utf-8")).hexdigest()[:16]
    # BA con so, moi con do MOT thu — de khong ai doc thanh hai so mau thuan (RM-09/RM-11).
    # Bao cao V11186 ghi «90 dong» nghia la DONG JOB (bo chu thich va dong rong).
    anh["crontab_dong_job"] = len([d for d in _d
                                   if d.strip() and not d.lstrip().startswith("#")])
    anh["crontab_dong_khong_rong"] = len([d for d in _d if d.strip()])
    anh["crontab_dong_tong"] = len(_d)
else:
    anh["crontab_sha"] = "KHONG_DOC_DUOC"
    anh["crontab_dong_job"] = anh["crontab_dong_khong_rong"] = anh["crontab_dong_tong"] = -1
phep("C7", "Chup duoc moc TRUOC deploy (4 bang khoa + crontab + PID)",
     "LOI" not in anh["bang_khoa"] and anh["crontab_sha"] != "KHONG_DOC_DUOC",
     "bang khoa=%s · crontab %s (%d dong JOB · %d khong rong · %d tong)"
     % (anh["bang_khoa"], anh["crontab_sha"], anh["crontab_dong_job"],
        anh["crontab_dong_khong_rong"], anh["crontab_dong_tong"]))

if cn:
    cn.close()

# ---------------------------------------------------------------- kết luận
chan = [k for k in KQ if not k["dat"]]
go = not chan
ket = {"terminal": "GO" if go else "NO_GO", "thoi_diem": anh["thoi_diem"],
       "phep": KQ, "anh_chup_truoc": anh,
       "phep_chan": [k["ma"] for k in chan]}

if "--json" in sys.argv:
    print(json.dumps(ket, ensure_ascii=False, indent=2))
else:
    print("=" * 96)
    print("  §AB-J PREFLIGHT DEPLOY — %s" % anh["thoi_diem"])
    print("=" * 96)
    for k in KQ:
        print("  %-4s %-5s %s" % (k["ma"], "DAT" if k["dat"] else "CHAN", k["ten"]))
        print("       %s" % k["chi_tiet"])
    print("-" * 96)
    if go:
        print("  TERMINAL: GO — du dieu kien deploy goi §AB.")
    else:
        print("  TERMINAL: NO_GO — bi chan boi %s. KHONG deploy."
              % ", ".join(k["ma"] for k in chan))
        print("  §AB-J: khong deploy nua voi, khong ep xanh de kip gio.")
    print("=" * 96)

if "--ghi" in sys.argv:
    d = os.path.join(GOC, "artifacts", "v11178")
    os.makedirs(d, exist_ok=True)
    p = os.path.join(d, "PREFLIGHT_DEPLOY_%s.json" % bay_gio.strftime("%Y%m%d_%H%M%S"))
    tam = p + ".tmp"
    with io.open(tam, "w", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(ket, ensure_ascii=False, indent=2))
        f.flush()
        os.fsync(f.fileno())
    os.replace(tam, p)
    print("da ghi %s" % p)

sys.exit(0 if go else 1)
