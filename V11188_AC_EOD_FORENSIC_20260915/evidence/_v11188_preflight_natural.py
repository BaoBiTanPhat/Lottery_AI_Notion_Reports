# -*- coding: utf-8 -*-
"""V11188 §AC-M — PREFLIGHT LƯỢT TỰ NHIÊN ĐẦU TIÊN dưới V11186/§AB.

CHỈ ĐỌC. Không restart, không deploy, không gọi provider, không ghi DB.
Owner §AC-M: «Không restart chỉ để "cho chắc". Không deploy thêm change vào official path
trước MN.» Tệp này chỉ TRẢ LỜI một câu: lượt MN 05:15 ngày 15/09 có sẵn sàng chạy không.

KHÁC với `_v11187_preflight_deploy.py`: tệp kia hỏi «có được deploy không», tệp này hỏi
«bản đã deploy có sẵn sàng đón lượt tự nhiên không».

Chạy TRÊN VPS:
    /root/Lottery_AI_Test/venv/bin/python3 _v11188_preflight_natural.py [--json]
Mã thoát 0 = V11186_FIRST_NATURAL_READY · 1 = NO_GO_WITH_EXACT_BLOCKER
"""
from __future__ import annotations

import datetime as dt
import hashlib
import io
import json
import os
import shutil
import sqlite3
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8")
BE = os.path.dirname(os.path.abspath(__file__))
GOC = os.path.dirname(os.path.dirname(BE))
DB = os.path.join(GOC, "data", "lottery_ai.db")
TRACE = os.path.join(BE, "prediction_trace.jsonl")

# SHA của gói §AB đã deploy 20:05 ngày 14/09 — chép từ biên bản deploy, không tính lại từ đĩa.
SHA_AB = {
    "combo_super.py": "9b3fdaa263498d9b",
    "gpt_analyzer.py": "11de9ea0530a5c0a",
    "scheduler.py": "1cdc402ad49e9019",
    "main.py": "5d897def9035e035",
    "_v11185_roster_goi_token.py": "2b88d4f9ea43af28",
}
PID_SAU_DEPLOY = "169960"
PID_WATCHER = "170282"
NGAY_MOI = "2026-09-15"
PHUT_IM_LANG = 15
DIA_TOI_THIEU_GB = 2.0
RAM_TOI_THIEU_MB = 200

KQ = []


def phep(ma, ten, dat, chi_tiet="", chan=True):
    KQ.append({"ma": ma, "ten": ten, "dat": bool(dat), "chi_tiet": str(chi_tiet),
               "chan": bool(chan)})


def _chay(lenh, timeout=30):
    try:
        r = subprocess.run(lenh, shell=True, capture_output=True, text=True, timeout=timeout)
        return r.returncode, (r.stdout or "") + (r.stderr or "")
    except Exception as e:
        return -1, repr(e)


def _sha16(p):
    try:
        return hashlib.sha256(io.open(p, "rb").read()).hexdigest()[:16]
    except Exception as e:
        return "KHONG_DOC_DUOC:%r" % e


bay_gio = dt.datetime.now()

# ---------------------------------------------------------------- M1 service
ma, out = _chay("systemctl show -p MainPID,NRestarts,ActiveState,ActiveEnterTimestamp lottery")
sv = {}
for d in out.split("\n"):
    if "=" in d:
        k, v = d.split("=", 1)
        sv[k.strip()] = v.strip()
pid = sv.get("MainPID", "?")
phep("M1", "Service active va PID dung ban da deploy",
     sv.get("ActiveState") == "active" and pid == PID_SAU_DEPLOY,
     "ActiveState=%s MainPID=%s (deploy ghi %s) NRestarts=%s len tu %s"
     % (sv.get("ActiveState"), pid, PID_SAU_DEPLOY, sv.get("NRestarts"),
        sv.get("ActiveEnterTimestamp")))

# ---------------------------------------------------------------- M2 health
ma, out = _chay("curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:8000/api/health")
phep("M2", "Health 200", out.strip() == "200", "health=%s" % out.strip())

# ---------------------------------------------------------------- M3 sha gói §AB
lech = {}
for f, mong in SHA_AB.items():
    that = _sha16(os.path.join(BE, f))
    if that != mong:
        lech[f] = "%s (mong %s)" % (that, mong)
phep("M3", "SHA 5 tep deploy KHOP goi §AB", not lech, lech or "khop ca 5")

# ---------------------------------------------------------------- M4 mã nằm trên đĩa TRƯỚC khi service khởi động
# Nếu một tệp được ghi SAU mốc service lên, tiến trình đang chạy KHÔNG có mã đó.
sau_moc = {}
try:
    moc = dt.datetime.strptime(sv.get("ActiveEnterTimestamp", "").rsplit(" ", 1)[0],
                               "%a %Y-%m-%d %H:%M:%S")
    for f in SHA_AB:
        t = dt.datetime.fromtimestamp(os.path.getmtime(os.path.join(BE, f)))
        if t > moc:
            sau_moc[f] = t.strftime("%Y-%m-%d %H:%M:%S")
    phep("M4", "Khong tep nao duoc ghi SAU khi service khoi dong", not sau_moc,
         sau_moc or "moc service %s, moi tep deu cu hon" % moc.strftime("%H:%M:%S"))
except Exception as e:
    phep("M4", "Doi chieu mtime tep vs moc service", False, "khong doc duoc moc: %r" % e)

# ---------------------------------------------------------------- M5 roster + cửa khẩn cấp
try:
    sys.path.insert(0, BE)
    import _v11185_roster_goi_token as R
    ver = R.ROSTER_VERSION
    ok_ba_mien = {}
    for m in ("MN", "MT", "MB"):
        r = R.get_token_call_roster(region=m, execution_class="official")
        ok_ba_mien[m] = (r.get("models") if r.get("ok") else "LOI:%s" % r.get("ma_loi"))
    du = all(isinstance(v, list) and 1 <= len(v) <= R.TRAN_MOI_MIEN for v in ok_ba_mien.values())
    phep("M5", "Roster doc duoc ca ba mien, trong tran %d" % R.TRAN_MOI_MIEN, du,
         "%s · %s" % (ver, {k: (len(v) if isinstance(v, list) else v) for k, v in ok_ba_mien.items()}))
    kc = R._khan_cap_trang_thai()
    phep("M6", "Cua go ve khan cap CAP 2 dang TAT", kc["bat"] is False, kc["ly_do"])
    # uỷ quyền có thật sự chặn
    k1, _ = R.uy_quyen_goi("gemini-2.5-pro", "MB", "combo_super", caller="preflight")
    k2, _ = R.uy_quyen_goi("claude-opus-4-6", "MB", "official", caller="preflight")
    k3, _ = R.uy_quyen_goi("deepseek-reasoner", "MB", "official", caller="preflight")
    k4, _ = R.uy_quyen_goi("claude-opus-4-6", None, "official", caller="preflight")
    phep("M7", "Uy quyen dispatcher: chan dung, khong chan oan",
         k1 == "DENY_OUTSIDE_ROSTER" and k2 == "ALLOW"
         and k3 == "DENY_QUARANTINED" and k4 == "DENY_INVALID_CONTEXT",
         "ngoai_roster=%s · trong_roster=%s · cach_ly=%s · thieu_mien=%s" % (k1, k2, k3, k4))
except Exception as e:
    phep("M5", "Roster doc duoc ca ba mien", False, "EXCEPTION: %r" % e)
    phep("M6", "Cua go ve khan cap CAP 2 dang TAT", False, "khong kiem duoc")
    phep("M7", "Uy quyen dispatcher", False, "khong kiem duoc")

# ---------------------------------------------------------------- M8/M9 cổng có mặt trong mã đã deploy
# CẨN THẬN — bản đầu của hai phép này cho FALSE BLOCKER lúc 02:11 ngày 15/09: nó tìm lời gọi
# mang đúng tên `get_token_call_roster`/`uy_quyen_goi`, trong khi mã thật import dưới BÍ DANH
# (`... as _v11186_gtcr`, `... as _uqg`). Tên trong nút Call là bí danh, không phải tên gốc ⇒
# phép kiểm báo "KHÔNG tìm thấy" cho một cổng đang có mặt. Một cổng báo nhầm cũng nguy hiểm
# như một cổng không tồn tại: nó có thể kích hoạt rollback vô cớ. Nay GIẢI BÍ DANH trước.
import ast


def _co_goi_ham(duong, module_nguon, ten_ham):
    """True nếu tệp có lời gọi `ten_ham` từ `module_nguon`, KỂ CẢ khi import dưới bí danh.

    Trả `(co, chi_tiet)`. Chỉ xét mã THỰC THI — chú thích và chuỗi không tính.
    """
    try:
        cay = ast.parse(io.open(duong, encoding="utf-8").read())
    except Exception as e:
        return False, "khong parse duoc: %r" % e
    ten_cuc_bo = set()
    for nut in ast.walk(cay):
        if isinstance(nut, ast.ImportFrom) and nut.module and module_nguon in nut.module:
            for a in nut.names:
                if a.name == ten_ham:
                    ten_cuc_bo.add(a.asname or a.name)
        elif isinstance(nut, ast.Import):
            for a in nut.names:
                if module_nguon in a.name:
                    ten_cuc_bo.add((a.asname or a.name) + "." + ten_ham)
    if not ten_cuc_bo:
        return False, "khong tim thay import %s tu %s" % (ten_ham, module_nguon)
    goi = []
    for nut in ast.walk(cay):
        if isinstance(nut, ast.Call):
            f = nut.func
            ten = getattr(f, "id", None)
            if ten is None and isinstance(f, ast.Attribute):
                goc = getattr(f.value, "id", "")
                ten = "%s.%s" % (goc, f.attr)
            if ten in ten_cuc_bo:
                goi.append((ten, getattr(nut, "lineno", "?")))
    if goi:
        return True, "import as %s · goi tai dong %s" % (sorted(ten_cuc_bo),
                                                         [d for _t, d in goi])
    return False, "co import as %s nhung KHONG co loi goi nao" % sorted(ten_cuc_bo)


co8, ct8 = _co_goi_ham(os.path.join(BE, "combo_super.py"),
                       "_v11185_roster_goi_token", "get_token_call_roster")
phep("M8", "Combo gate CO MAT trong ma da deploy (AST, giai bi danh)", co8, ct8)

co9, ct9 = _co_goi_ham(os.path.join(BE, "gpt_analyzer.py"),
                       "_v11185_roster_goi_token", "uy_quyen_goi")
phep("M9", "Uy quyen tai dispatcher CO MAT trong gpt_analyzer (AST, giai bi danh)", co9, ct9)

# ---------------------------------------------------------------- M10 bộ thu receipt
ma, out = _chay("ps -p %s -o pid= 2>/dev/null" % PID_WATCHER)
phep("M10", "Bo thu receipt 15/09 con song", out.strip() == PID_WATCHER,
     "PID %s %s" % (PID_WATCHER, "song" if out.strip() == PID_WATCHER else "KHONG THAY"),
     chan=False)

# ---------------------------------------------------------------- M11 không có provider job đang bay
cuoi = None
try:
    with io.open(TRACE, "rb") as f:
        f.seek(0, os.SEEK_END)
        n = min(f.tell(), 200000)
        f.seek(-n, os.SEEK_END)
        dong = [l for l in f.read().decode("utf-8", "replace").split("\n") if l.strip()]
    cuoi = json.loads(dong[-1]).get("timestamp")
    im = (bay_gio - dt.datetime.fromisoformat(cuoi)).total_seconds() / 60.0
except Exception as e:
    im = None
    cuoi = "KHONG_DOC_DUOC:%r" % e
phep("M11", "Khong co provider job dang bay (trace im >= %d phut)" % PHUT_IM_LANG,
     im is not None and im >= PHUT_IM_LANG,
     "trace cuoi %s · im %s phut" % (cuoi, "?" if im is None else round(im, 1)))

# ---------------------------------------------------------------- M12 lịch cron lượt MN
ma, out = _chay("crontab -l")
ma2, out2 = _chay("journalctl -u lottery --since '-6 hours' --no-pager -o cat | "
                  "grep -c 'next run at: 2026-09-15' ; true")
# Job MN nằm trong APScheduler của service, không nằm trong crontab hệ thống.
ma3, out3 = _chay("journalctl -u lottery --since '-8 hours' --no-pager -o cat | "
                  "grep -oE 'next run at: 2026-09-15 [0-9:]+' | sort -u | head -20 ; true")
moc_moi = sorted(set([d.strip() for d in out3.split("\n") if d.strip()]))
phep("M12", "Scheduler da xep lich cho ngay %s" % NGAY_MOI, len(moc_moi) > 0,
     "%d moc: %s" % (len(moc_moi), moc_moi[:6]))

# ---------------------------------------------------------------- M13 đĩa / RAM
try:
    du = shutil.disk_usage(GOC)
    con_gb = du.free / (1024.0 ** 3)
except Exception:
    con_gb = -1
ma, out = _chay("free -m | awk '/^Mem:/{print $2\" \"$3\" \"$7}'")
try:
    tong, dung, kha_dung = [int(x) for x in out.split()]
except Exception:
    tong = dung = kha_dung = -1
phep("M13", "Dia con >= %.1f GB va RAM kha dung >= %d MB" % (DIA_TOI_THIEU_GB, RAM_TOI_THIEU_MB),
     con_gb >= DIA_TOI_THIEU_GB and kha_dung >= RAM_TOI_THIEU_MB,
     "dia con %.2f GB · RAM tong=%s dung=%s kha_dung=%s MB" % (con_gb, tong, dung, kha_dung))

# ---------------------------------------------------------------- M14 DB lành, không migration treo
try:
    cn = sqlite3.connect("file:%s?mode=ro" % DB.replace("\\", "/"), uri=True)
    iv = cn.execute("PRAGMA quick_check").fetchone()[0]
    jm = cn.execute("PRAGMA journal_mode").fetchone()[0]
    dem = {}
    for b in ("predictions", "final_bundles", "lottery_results", "model_daily_eval"):
        dem[b] = cn.execute("SELECT COUNT(*) FROM %s" % b).fetchone()[0]
    co_15 = cn.execute("SELECT COUNT(*) FROM predictions WHERE date=?", (NGAY_MOI,)).fetchone()[0]
    cn.close()
    phep("M14", "DB lanh, chua co ban ghi nao cua ngay moi", iv == "ok" and co_15 == 0,
         "quick_check=%s journal=%s · %s · predictions[%s]=%d" % (iv, jm, dem, NGAY_MOI, co_15))
except Exception as e:
    phep("M14", "DB lanh", False, "EXCEPTION: %r" % e)

# ---------------------------------------------------------------- M15 cách ly đọc được
try:
    import _v11184_cach_ly_provider as CL
    ds = CL.danh_sach()
    phep("M15", "Trang thai cach ly doc duoc", isinstance(ds, dict),
         "%d model bi cach ly: %s" % (len(ds), sorted(ds.keys())))
except Exception as e:
    phep("M15", "Trang thai cach ly doc duoc", False, "EXCEPTION: %r" % e)

# ---------------------------------------------------------------- kết luận
chan = [k for k in KQ if not k["dat"] and k["chan"]]
canh = [k for k in KQ if not k["dat"] and not k["chan"]]
san_sang = not chan
ket = {"terminal": "V11186_FIRST_NATURAL_READY" if san_sang else "NO_GO_WITH_EXACT_BLOCKER",
       "thoi_diem": bay_gio.isoformat(timespec="seconds"),
       "phep": KQ, "phep_chan": [k["ma"] for k in chan],
       "canh_bao_khong_chan": [k["ma"] for k in canh]}

if "--json" in sys.argv:
    print(json.dumps(ket, ensure_ascii=False, indent=1))
else:
    print("=" * 104)
    print("  §AC-M PREFLIGHT LUOT TU NHIEN DAU TIEN duoi V11186 — %s" % ket["thoi_diem"])
    print("=" * 104)
    for k in KQ:
        nhan = "DAT" if k["dat"] else ("CHAN" if k["chan"] else "CANH")
        print("  %-4s %-5s %s" % (k["ma"], nhan, k["ten"]))
        print("       %s" % k["chi_tiet"])
    print("-" * 104)
    if san_sang:
        print("  TERMINAL: V11186_FIRST_NATURAL_READY")
        if canh:
            print("  (canh bao khong chan: %s)" % ", ".join(k["ma"] for k in canh))
        print("  KHONG restart. KHONG deploy them. Cho luot MN 05:15 chay tu nhien.")
    else:
        print("  TERMINAL: NO_GO_WITH_EXACT_BLOCKER — %s" % ", ".join(k["ma"] for k in chan))
        for k in chan:
            print("     %s · %s · %s" % (k["ma"], k["ten"], k["chi_tiet"]))
    print("=" * 104)

sys.exit(0 if san_sang else 1)
