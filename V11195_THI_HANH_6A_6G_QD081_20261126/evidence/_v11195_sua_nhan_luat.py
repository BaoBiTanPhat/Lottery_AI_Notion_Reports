# -*- coding: utf-8 -*-
"""V11195 — ÁP nhãn đo tiến mới cho `mined_rule_effectiveness` trên DB production (FU-456).

Owner 26/11/2026 ~10:10: *«6e --> theo khuyến nghị»* (khuyến nghị: sửa cách gắn nhãn rồi đo lại).
Quy tắc nhãn nằm trong `_v11025_khoa_luat_ben.tinh_giai_doan()` và đã qua cổng
`_v11195_kiem_nhan_luat.py` (RM-15: quy tắc mới ĐẠT · quy tắc cũ TRƯỢT đúng ca rò).

Việc làm (chạy TRÊN VPS, trong web/backend):
  1. lấy lịch lần đào THẬT: `mining_log` (status SUCCESS) — đối chiếu `scheduler_logs`
     («Bắt đầu Weekly Rule Mining», log_time UTC +7) và mọi ngày `OBSERVED` trong sổ khoá;
     ngày nào sổ khoá có mà lịch không có ⇒ DỪNG, không ghi (thiếu lần đào là chỗ duy nhất làm
     phép suy «luật liên tục» nhận nhầm ⇒ rò trở lại);
  2. sao lưu nhãn hiện tại (id, giai_doan) ra backups/mre_giai_doan.pre_v11195.json;
  3. tạo hai bảng chỉ thêm, nạp lịch lần đào, ghi bộ khoá đang active cho lần đào gần nhất;
  4. gắn lại nhãn bằng `phan_loai_giai_doan()` (chỉ ghi dòng đổi nhãn).
Không đụng 4 bảng khoá, không đụng `mined_rules`, không restart.

    venv/bin/python3 _v11195_sua_nhan_luat.py           # THỬ: in số, không ghi
    venv/bin/python3 _v11195_sua_nhan_luat.py --ghi     # GHI
"""
from __future__ import annotations

import io
import json
import os
import sqlite3
import sys
from collections import Counter
from datetime import datetime

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
GOC = os.path.abspath(os.path.join(HERE, "..", ".."))
DB = os.path.join(GOC, "data", "lottery_ai.db")
SAO_LUU = os.path.join(GOC, "backups", "mre_giai_doan.pre_v11195.json")
TU_NGAY = "2026-08-01"

import _v11025_khoa_luat_ben as K  # noqa: E402


def lich_lan_dao(con) -> tuple[list[str], dict]:
    ml = sorted({str(r[0])[:10] for r in con.execute(
        "SELECT run_date FROM mining_log WHERE status='SUCCESS' AND run_date >= ?", (TU_NGAY,))})
    sl = sorted({r[0] for r in con.execute(
        "SELECT date(datetime(log_time, '+7 hours')) FROM scheduler_logs "
        "WHERE message LIKE '%Bắt đầu Weekly Rule Mining%' AND log_time >= ?", (TU_NGAY,))})
    obs = sorted({r[0] for r in con.execute(
        "SELECT lan_dau_thay FROM rule_key_registry WHERE nguon_lan_dau='OBSERVED'")}
                 | {r[0] for r in con.execute(
                     "SELECT lan_cuoi_thay FROM rule_key_registry WHERE so_lan_dao > 1 "
                     "OR nguon_lan_dau='OBSERVED'")})
    thieu = [d for d in obs if d not in ml]
    return ml, {"mining_log_success": ml, "scheduler_logs_bat_dau": sl,
                "scheduler_logs_khong_co_trong_mining_log": [d for d in sl if d not in ml],
                "mining_log_khong_co_trong_scheduler_logs": [d for d in ml if d not in sl],
                "ngay_so_khoa_khong_co_trong_lich": thieu}


def main() -> int:
    ghi = "--ghi" in sys.argv
    con = sqlite3.connect(DB, timeout=60)
    con.row_factory = sqlite3.Row
    runs, chan_doan = lich_lan_dao(con)
    print("=" * 92)
    print(f"  V11195 — ÁP NHÃN ĐO TIẾN MỚI · chế độ {'GHI' if ghi else 'THỬ (không ghi)'} · "
          f"{datetime.now():%Y-%m-%d %H:%M:%S}")
    print("=" * 92)
    for k, v in chan_doan.items():
        print(f"  {k:<46}: {len(v):>3} · {', '.join(v) if len(v) <= 20 else ', '.join(v[:20]) + ' …'}")
    if chan_doan["ngay_so_khoa_khong_co_trong_lich"]:
        print("  ✗ DỪNG: sổ khoá có ngày đào không nằm trong mining_log — thiếu lần đào làm phép suy sai")
        return 1

    moi_nhat = con.execute("SELECT MAX(date(mined_at)) FROM mined_rules WHERE is_active=1").fetchone()[0]
    print(f"  bộ luật đang active được chọn ở lần đào  : {moi_nhat} "
          f"({'có' if moi_nhat in runs else 'KHÔNG có'} trong lịch)")
    if moi_nhat not in runs:
        print("  ✗ DỪNG: lần đào sinh bộ luật hiện hành không nằm trong lịch")
        return 1

    hien = Counter(r[0] or "(trống)" for r in con.execute("SELECT giai_doan FROM mined_rule_effectiveness"))

    # Tính nhãn mới trên bản sao TRONG BỘ NHỚ của đúng ba bảng nhỏ cần dùng (KHÔNG chép cả DB
    # 1,1 GB) ⇒ chế độ THỬ không chạm DB thật.
    keys = {K.khoa_luat(r["target_region"], r["target_weekday"], r["source_station_slot"],
                        r["source_station"], r["source_region"], r["source_offset"], r["prize_keys"])
            for r in con.execute("SELECT * FROM mined_rules WHERE is_active=1")}
    mem = sqlite3.connect(":memory:")
    mem.row_factory = sqlite3.Row
    mem.execute(K.DDL_REGISTRY)
    mem.executemany("INSERT INTO rule_key_registry VALUES (?,?,?,?,?,?,?,?)",
                    [tuple(r) for r in con.execute(
                        "SELECT rule_key, lan_dau_thay, nguon_lan_dau, lan_cuoi_thay, so_lan_dao, mo_ta, "
                        "created_at, updated_at FROM rule_key_registry")])
    mem.execute("CREATE TABLE mined_rule_effectiveness (id INTEGER PRIMARY KEY, rule_key TEXT, date TEXT, "
                "giai_doan TEXT)")
    mem.executemany("INSERT INTO mined_rule_effectiveness VALUES (?,?,?,?)",
                    [tuple(r) for r in con.execute(
                        "SELECT id, rule_key, date, giai_doan FROM mined_rule_effectiveness")])
    for ddl in K.DDL_LAN_DAO:
        mem.execute(ddl)
    K.nap_lich_su_lan_dao(mem, runs, "NAP_TU_MINING_LOG_V11195")
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for k in keys:
        mem.execute("INSERT OR IGNORE INTO rule_key_lan_dao VALUES (?, ?, 'NAP_TU_MINED_RULES_V11195', ?)",
                    (moi_nhat, k, now))
    moi = Counter(K.tinh_giai_doan(mem).values())
    mem.close()
    print(f"\n  {'nhãn':<28} {'hiện tại':>10} {'sau khi áp':>11}")
    for g in sorted(set(hien) | set(moi)):
        print(f"  {g:<28} {hien.get(g, 0):>10} {moi.get(g, 0):>11}")
    print(f"  {'tổng':<28} {sum(hien.values()):>10} {sum(moi.values()):>11}")
    print(f"  khoá đang active ghi cho lần đào {moi_nhat}: {len(keys)}")

    if not ghi:
        print("\n  (THỬ — không ghi gì. Thêm --ghi để áp.)")
        return 0

    if not os.path.exists(SAO_LUU):
        rows = [[r[0], r[1]] for r in con.execute("SELECT id, giai_doan FROM mined_rule_effectiveness")]
        os.makedirs(os.path.dirname(SAO_LUU), exist_ok=True)
        with io.open(SAO_LUU, "w", encoding="utf-8", newline="\n") as fh:
            json.dump({"luc": now, "bang": "mined_rule_effectiveness", "cot": ["id", "giai_doan"],
                       "dong": rows}, fh, ensure_ascii=False)
        print(f"\n  ✓ sao lưu {len(rows)} nhãn → {SAO_LUU}")
    else:
        print(f"\n  · bản sao lưu đã có, giữ nguyên: {SAO_LUU}")
    K.nang_cap_luoc_do(con)
    n_run = K.nap_lich_su_lan_dao(con, runs, "NAP_TU_MINING_LOG_V11195")
    n_k = 0
    for k in keys:
        n_k += con.execute("INSERT OR IGNORE INTO rule_key_lan_dao VALUES (?, ?, 'NAP_TU_MINED_RULES_V11195', ?)",
                           (moi_nhat, k, now)).rowcount or 0
    r = K.phan_loai_giai_doan(con)
    con.commit()
    con.close()
    print(f"  ✓ nạp {n_run} ngày đào · {n_k} khoá cho {moi_nhat} · đổi nhãn {r['_doi_nhan']} dòng")
    print(f"  ✓ phân bố sau khi áp: { {k: v for k, v in r.items() if not k.startswith('_')} }")
    print("  gỡ về: đọc lại backups/mre_giai_doan.pre_v11195.json rồi UPDATE giai_doan theo id; "
          "khôi phục _v11025_khoa_luat_ben.py từ backups/_v11025_khoa_luat_ben.py.pre_v11195")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
