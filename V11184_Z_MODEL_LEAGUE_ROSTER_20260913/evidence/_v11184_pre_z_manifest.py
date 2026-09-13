# -*- coding: utf-8 -*-
"""V11184 — PRE_Z_MANIFEST §Z-B1: chụp sự thật sống TRƯỚC khi sửa production, 13/09/2026.

CHỈ ĐỌC. Chạy trên VPS. Phần Git canonical truyền vào từ máy canonical (VPS deploy là COPY FILE,
`git rev-parse HEAD` trên VPS là commit lạc, KHÔNG dùng làm neo).

Khác `PRE_Y_MANIFEST` ở chỗ §Z đòi thêm:
  - roster THẬT đang chạy (model nào được gọi, miền nào) + phân loại direct-token / ML / derived
  - hash của bundle official 13/09 (để chứng minh không sửa lịch sử)
  - hash của khối mã tính TOTAL (để chứng minh không đổi công thức)
  - trạng thái kho công khai
  - bảng token/cost nếu có
"""
from __future__ import annotations

import argparse
import glob
import hashlib
import io
import json
import os
import re
import sqlite3
import subprocess
import sys

BE = os.path.dirname(os.path.abspath(__file__))
GOC = os.path.dirname(os.path.dirname(BE))
DB = GOC + "/data/lottery_ai.db"
NGAY = "2026-09-13"

TEP_OFFICIAL = ("main.py", "scheduler.py", "database.py", "gpt_analyzer.py",
                "model_registry.py", "combo_super.py", "daily_evaluation.py",
                "weight_optimizer.py", "backtester.py", "statistical_analyzer.py")

BANG_TRONG_YEU = ("predictions", "final_bundles", "lottery_results", "model_daily_eval",
                  "day_governance", "shadow_candidates", "training_history",
                  "ml_retrain_guard_log", "app_settings", "scheduler_logs",
                  "v11178_attempts", "model_latency_cost_audit_daily")

NGUON_CUTOFF = {
    "_v10782_freeze.py": "FREEZE_MARKS",
    "_v10759_money_board.py": "OUTPUT_DUE",
    "_v10861_runtime_contract_audit.py": "DEADLINE",
    "_v10692_mn_mt_multidir_lane.py": "OUTPUT_FREEZE_HHMM",
}


def sh(cmd, cwd=None):
    try:
        return subprocess.check_output(cmd, shell=True, cwd=cwd or GOC,
                                       stderr=subprocess.DEVNULL).decode().strip()
    except Exception as e:
        return "ERR:%s" % e


def sha(p):
    try:
        return hashlib.sha256(io.open(p, "rb").read()).hexdigest()
    except Exception:
        return None


def doc_cutoff():
    """Mốc chốt khai ở BỐN nơi. Lệch nhau là finding, không phải chuyện nhỏ."""
    ra = {}
    for tep, ten in NGUON_CUTOFF.items():
        p = BE + "/" + tep
        if not os.path.exists(p):
            ra[tep] = {"ton_tai": False, "bien": ten}
            continue
        src = io.open(p, encoding="utf-8", errors="replace").read()
        m = re.search(re.escape(ten) + r"\s*[:=]\s*\{([^}]{0,400})\}", src)
        ra[tep] = {"ton_tai": True, "bien": ten, "tim_thay": bool(m),
                   "gia_tri_tho": (m.group(1).strip()[:300] if m else None),
                   "dong": (src[:m.start()].count("\n") + 1) if m else None}
    return ra


def bam_khoi_total(cur):
    """Hash khối mã tính điểm bundle + chọn bach_thu.

    VÌ SAO CẦN: §Z khoá «không thay công thức TOTAL». Muốn CHỨNG MINH không đổi thì phải có mốc
    băm TRƯỚC. Neo theo TÊN HÀM tìm được trong mã, không theo số dòng (số dòng trôi khi sửa chỗ khác).
    """
    ra = {}
    p = BE + "/main.py"
    if not os.path.exists(p):
        return {"loi": "khong co main.py"}
    src = io.open(p, encoding="utf-8", errors="replace").read()
    # tìm các hàm có tên gợi ý chấm điểm bundle — ghi CẢ tên tìm thấy để người đọc kiểm lại
    ten_ham = re.findall(r"^(?:async +)?def +(\w*(?:bundle|rank|vote|score|bach_thu)\w*)\s*\(",
                         src, re.M | re.I)
    ra["ham_ung_vien"] = sorted(set(ten_ham))
    for ten in sorted(set(ten_ham)):
        m = re.search(r"^((?:async +)?def +%s\s*\(.*?)(?=^(?:async +)?def |\Z)" % re.escape(ten),
                      src, re.M | re.S)
        if m:
            ra.setdefault("bam_ham", {})[ten] = {
                "sha256": hashlib.sha256(m.group(1).encode()).hexdigest(),
                "so_dong": m.group(1).count("\n") + 1,
                "dong_bat_dau": src[:m.start()].count("\n") + 1,
            }
    return ra


def doc_roster(cur):
    """Roster THẬT = model nào đã thực sự chạy, đọc từ predictions của ngày đích.

    KHÔNG đọc từ hằng số trong mã, vì hằng số có thể khai nhiều hơn thực tế chạy (RM-13).
    Hằng số được ghi RIÊNG ở `roster_khai_bao` để đối chiếu.
    """
    ra = {"tu_predictions_ngay_dich": {}, "roster_khai_bao": {}}
    try:
        cur.execute("SELECT target_region, ai_model, run_source, COUNT(*) FROM predictions "
                    "WHERE date=? GROUP BY 1,2,3 ORDER BY 1,2", (NGAY,))
        for reg, m, rs, n in cur.fetchall():
            ra["tu_predictions_ngay_dich"].setdefault(reg, {}).setdefault(m, {})[rs] = n
    except Exception as e:
        ra["tu_predictions_ngay_dich"] = {"loi": str(e)[:80]}

    # hằng số khai báo — đọc, KHÔNG đoán tên biến
    for tep, bien in (("model_registry.py", r"OPENROUTER_MODELS\b"),
                      ("gpt_analyzer.py", r"OPENROUTER_MODELS_SET\b"),
                      ("combo_super.py", r"ML_MODELS\b"),
                      ("combo_super.py", r"AI_MODELS\b")):
        p = BE + "/" + tep
        if not os.path.exists(p):
            continue
        src = io.open(p, encoding="utf-8", errors="replace").read()
        m = re.search(bien + r"\s*[:=]\s*[\[\{\(]([^\]\}\)]{0,900})", src)
        if m:
            ra["roster_khai_bao"]["%s:%s" % (tep, bien.strip(r"\b"))] = {
                "dong": src[:m.start()].count("\n") + 1,
                "gia_tri_tho": m.group(1).strip()[:700],
            }
    return ra


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--git-json", default="")
    ap.add_argument("--out", default=GOC + "/artifacts/v11178/PRE_Z_MANIFEST_20260913.json")
    a = ap.parse_args()

    con = sqlite3.connect("file:" + DB + "?mode=ro", uri=True)
    c = con.cursor()

    def dem(b, dk=None):
        try:
            c.execute("SELECT COUNT(*) FROM %s%s" % (b, (" WHERE " + dk) if dk else ""))
            return c.fetchone()[0]
        except Exception as e:
            return "ERR:%s" % str(e)[:60]

    cot_ngay = {"predictions": "date", "final_bundles": "date",
                "lottery_results": "substr(date,1,10)", "model_daily_eval": "date",
                "day_governance": "date", "shadow_candidates": "date",
                "training_history": "date", "ml_retrain_guard_log": "substr(run_at,1,10)",
                "app_settings": "substr(updated_at,1,10)",
                "scheduler_logs": "substr(datetime(log_time,'+7 hours'),1,10)"}

    bang = {}
    for b in BANG_TRONG_YEU:
        cn = cot_ngay.get(b)
        bang[b] = {"tong": dem(b), "ngay_dich": dem(b, "%s='%s'" % (cn, NGAY)) if cn else None}
        try:
            c.execute("PRAGMA table_info(%s)" % b)
            bang[b]["cot"] = [r[1] for r in c.fetchall()]
        except Exception:
            bang[b]["cot"] = None

    # hash bundle official ngày đích — để chứng minh KHÔNG sửa lịch sử
    bundle_hash = {}
    try:
        c.execute("SELECT region, bach_thu, lo2, lo3, xien2, xien3, bach_thu_status, lo2_status, "
                  "lo3_status, model_count, top_score, bundle_version, generation_method, "
                  "created_at, source_predictions_json FROM final_bundles "
                  "WHERE date=? AND status='ACTIVE' ORDER BY region", (NGAY,))
        for r in c.fetchall():
            reg = r[0]
            bundle_hash[reg] = {
                "bach_thu": r[1], "lo2": r[2], "lo3": r[3],
                "trang_thai": {"bt": r[6], "lo2": r[7], "lo3": r[8]},
                "model_count": r[9], "bundle_version": r[11],
                "generation_method": r[12], "created_at": r[13],
                "sha256_toan_dong": hashlib.sha256(
                    "|".join(str(x) for x in r).encode()).hexdigest(),
                "sha256_source_predictions_json": hashlib.sha256(
                    (r[14] or "").encode()).hexdigest(),
            }
    except Exception as e:
        bundle_hash = {"loi": str(e)[:90]}

    weights = []
    try:
        c.execute("SELECT category, setting_key, setting_value, updated_at FROM app_settings "
                  "WHERE lower(setting_key) LIKE '%weight%' OR lower(category) LIKE '%weight%' "
                  "OR lower(setting_key) LIKE '%learned%' OR lower(setting_key) LIKE '%optimi%' "
                  "ORDER BY updated_at DESC")
        for cat, k, v, u in c.fetchall():
            weights.append({"category": cat, "setting_key": k,
                            "value_sha256": hashlib.sha256(str(v or "").encode()).hexdigest(),
                            "value_len": len(str(v or "")), "value_preview": str(v or "")[:160],
                            "updated_at": u})
    except Exception as e:
        weights = [{"loi": str(e)[:80]}]

    try:
        c.execute("SELECT date, region, evaluation_policy FROM day_governance "
                  "WHERE date<=? ORDER BY date, region", ("2026-09-09",))
        rows = c.fetchall()
        raw = "\n".join("%s|%s|%s" % (d, r, p or "") for d, r, p in rows)
        digest = {"pham_vi": "day_governance date<=2026-09-09", "n_rows": len(rows),
                  "sha256": hashlib.sha256(raw.encode()).hexdigest()}
    except Exception as e:
        digest = {"loi": str(e)[:80]}

    roster = doc_roster(c)
    total_bam = bam_khoi_total(c)
    con.close()

    arts = {}
    for p in sorted(glob.glob(GOC + "/data/models/*")):
        st = os.lstat(p)
        arts[os.path.basename(p)] = {
            "path": p, "size": st.st_size, "mtime": sh("stat -c '%%y' '%s'" % p),
            "sha256": sha(p) if not os.path.islink(p) else None,
            "inode": st.st_ino, "la_symlink": os.path.islink(p),
            "symlink_target": os.readlink(p) if os.path.islink(p) else None,
        }

    crontab = sh("crontab -l 2>/dev/null")

    m = {
        "artifact": "PRE_Z_MANIFEST", "muc": "Prompt 43 R1 §Z-B1", "target_date": NGAY,
        "chup_luc_vps": sh("date '+%Y-%m-%dT%H:%M:%S%:z'"),
        "timezone": sh("date '+%Z %:z'"), "host": sh("hostname"),
        "db_mtime": sh("stat -c '%%y' '%s'" % DB), "db_size": os.path.getsize(DB),

        "git_canonical": json.loads(a.git_json) if a.git_json else {"ghi_chu": "CHUA TRUYEN"},
        "vps_git_head": sh("git rev-parse HEAD"),
        "vps_git_head_ghi_chu": "VPS deploy la COPY FILE; HEAD o day KHONG phai commit canonical",

        "service": {
            "name": "lottery",
            "MainPID": sh("systemctl show lottery -p MainPID --value"),
            "NRestarts": sh("systemctl show lottery -p NRestarts --value"),
            "ActiveState": sh("systemctl show lottery -p ActiveState --value"),
            "ActiveEnterTimestamp": sh("systemctl show lottery -p ActiveEnterTimestamp --value"),
            "MemoryCurrent": sh("systemctl show lottery -p MemoryCurrent --value"),
            "health": sh("curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:8000/api/health"),
            "pm2": sh("pm2 jlist 2>/dev/null | head -c 200") or "(khong dung pm2)",
        },
        "he_thong": {
            "uptime": sh("uptime"), "load": sh("cat /proc/loadavg"),
            "mem_MB": sh("free -m | awk 'NR==2{print $2\" tong, \"$3\" dung, \"$7\" kha dung\"}'"),
            "swap_MB": sh("free -m | awk 'NR==3{print $2}'"),
            "disk": sh("df -h / | tail -1"),
        },

        "crontab_sha256": hashlib.sha256(crontab.encode()).hexdigest(),
        "crontab_n_dong_dang_chay": len([d for d in crontab.split("\n")
                                         if d.strip() and not d.strip().startswith("#")]),
        "cron_tro_file_mat": [d for d in crontab.split("\n")
                              if d.strip() and not d.strip().startswith("#")
                              for mm in [re.search(r"(/root/\S+\.(?:py|sh))", d)]
                              if mm and not os.path.exists(mm.group(1))],

        "bang_trong_yeu": bang,
        "bundle_official_ngay_dich": bundle_hash,
        "immutable_historical_digest": digest,
        "output_counterfactual_rank_NOT_NULL": (lambda: (
            lambda cc: (cc.execute("SELECT COUNT(*) FROM shadow_model_promotion_scorecard_daily "
                                   "WHERE output_counterfactual_rank IS NOT NULL"),
                        cc.fetchone()[0])[1])(
            sqlite3.connect("file:" + DB + "?mode=ro", uri=True).cursor()))(),

        "roster": roster,
        "learned_weights": weights,
        "cutoff_doc_tu_ma": doc_cutoff(),
        "bam_khoi_TOTAL": total_bam,
        "model_artifacts": arts,
        "deployed_sha256_official": {f: sha(BE + "/" + f) for f in TEP_OFFICIAL},

        "active_writer": {
            "wal_ton_tai": os.path.exists(DB + "-wal"),
            "shm_ton_tai": os.path.exists(DB + "-shm"),
            "tien_trinh_mo_db": sh("lsof '%s' 2>/dev/null | tail -n +2 | awk '{print $1\":\"$2}' "
                                   "| sort -u | tr '\\n' ' '" % DB) or "(lsof khong co hoac rong)",
        },
    }
    m["manifest_sha256"] = hashlib.sha256(
        json.dumps({k: v for k, v in m.items() if k != "chup_luc_vps"},
                   sort_keys=True, ensure_ascii=False, default=str).encode()).hexdigest()

    os.makedirs(os.path.dirname(a.out), exist_ok=True)
    noi = json.dumps(m, ensure_ascii=False, indent=1, default=str)
    tam = a.out + ".tmp"
    with io.open(tam, "w", encoding="utf-8", newline=chr(10)) as f:
        f.write(noi)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tam, a.out)
    if len(io.open(a.out, encoding="utf-8").read()) != len(noi):
        raise IOError("GHI HONG")

    gon = {k: v for k, v in m.items()
           if k not in ("model_artifacts", "deployed_sha256_official", "learned_weights",
                        "cutoff_doc_tu_ma", "roster", "bam_khoi_TOTAL", "bang_trong_yeu")}
    gon["n_model_artifacts"] = len(arts)
    gon["n_learned_weights"] = len(weights)
    gon["roster_so_model_theo_mien"] = {
        r: len(v) for r, v in (roster.get("tu_predictions_ngay_dich") or {}).items()
        if isinstance(v, dict)}
    gon["bang_tong_ngay_dich"] = {b: (bang[b]["tong"], bang[b]["ngay_dich"]) for b in BANG_TRONG_YEU}
    print(json.dumps(gon, ensure_ascii=False, indent=1, default=str))
    print("\n-> %s" % a.out)
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
