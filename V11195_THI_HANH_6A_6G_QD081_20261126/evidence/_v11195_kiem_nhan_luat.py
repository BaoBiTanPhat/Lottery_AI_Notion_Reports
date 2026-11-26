# -*- coding: utf-8 -*-
"""V11195 — CỔNG THỬ CHẶN cho nhãn đo tiến của luật (FU-456 · RM-15). Chạy trên DB TRONG BỘ NHỚ.

Owner 26/11/2026 ~10:10: *«6e --> theo khuyến nghị»* — khuyến nghị là «cho em sửa cách gắn nhãn
rồi đo lại». Cổng này chứng minh cách gắn nhãn mới:
  · VẪN gắn `DO_TIEN` cho luật đang chạy liên tục (không bóp chết bằng chứng thật);
  · KHÔNG gắn `DO_TIEN` cho ngày luật đang NGHỈ rồi được chấm bù (chỗ rò cũ);
  · theo đúng nhật ký lần đào khi có (`rule_key_lan_dao`);
  · chạy lại lần đào cùng ngày KHÔNG cộng `so_lan_dao` hai lần.
Và chứng minh phép thử PHÂN BIỆT được: quy tắc cũ (`date >= mốc`) phải TRƯỢT đúng ca rò.

    python web/backend/_v11195_kiem_nhan_luat.py        → thoát 0 khi mọi ca đúng
"""
from __future__ import annotations

import os
import sqlite3
import sys

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _v11025_khoa_luat_ben as K  # noqa: E402

RUNS = ["2026-08-03", "2026-08-10", "2026-08-17", "2026-08-24", "2026-08-31",
        "2026-09-07", "2026-09-14", "2026-09-21", "2026-09-28"]


def _db() -> sqlite3.Connection:
    con = sqlite3.connect(":memory:")
    con.execute(K.DDL_REGISTRY)
    for ddl in K.DDL_LAN_DAO:
        con.execute(ddl)
    con.execute("CREATE TABLE mined_rule_effectiveness (id INTEGER PRIMARY KEY, rule_key TEXT, "
                "date TEXT, giai_doan TEXT)")
    con.execute("CREATE TABLE mined_rules (id INTEGER PRIMARY KEY, target_region TEXT, target_weekday INT, "
                "source_station_slot TEXT, source_station TEXT, source_region TEXT, source_offset TEXT, "
                "prize_keys TEXT, is_active INT)")
    K.nap_lich_su_lan_dao(con, RUNS, "THU")
    return con


def _reg(con, k, dau, nguon, cuoi, so, created="2026-08-07 10:00:00"):
    con.execute("INSERT INTO rule_key_registry VALUES (?,?,?,?,?,?,?,?)",
                (k, dau, nguon, cuoi, so, "thu", created, created))


def main() -> int:
    con = _db()
    # A — OBSERVED, liên tục: thấy 10/08, 17/08, 24/08 (3 lần đào) rồi nghỉ từ 31/08.
    _reg(con, "A", "2026-08-10", "OBSERVED", "2026-08-24", 3)
    # B — OBSERVED, CÓ QUÃNG NGHỈ: thấy 10/08 và 07/09 (2 lần) — vắng 17/08, 24/08, 31/08.
    _reg(con, "B", "2026-08-10", "OBSERVED", "2026-09-07", 2)
    # S — gieo mầm 07/08, rồi thấy đủ 10/08, 17/08, 24/08 ⇒ so_lan_dao = 1 + 3.
    _reg(con, "S", "2026-01-05", "SEED_TU_MRE", "2026-08-24", 4)
    # C — có nhật ký: có mặt ở lần đào 21/09, vắng ở 28/09.
    _reg(con, "C", "2026-09-21", "OBSERVED", "2026-09-21", 1)
    for rd in ("2026-09-21", "2026-09-28"):
        con.execute("INSERT INTO rule_key_lan_dao VALUES (?, ?, 'THU', 'x')", (rd, "Z_KHAC"))
    con.execute("INSERT INTO rule_key_lan_dao VALUES ('2026-09-21', 'C', 'THU', 'x')")

    ca = [  # (id, khoá, ngày, nhãn phải ra, vì sao)
        (1, "A", "2026-08-20", K.NHAN_DO_TIEN, "luật liên tục, đang chạy"),
        (2, "A", "2026-08-30", K.NHAN_DO_TIEN, "sau lần thấy cuối 24/08 nhưng TRƯỚC lần đào 31/08"),
        (3, "A", "2026-09-02", K.NHAN_NGOAI_HOAT_DONG, "sau lần đào 31/08 không còn khoá A"),
        (4, "B", "2026-08-12", K.NHAN_DO_TIEN, "tuần ngay sau lần thấy đầu — chắc chắn chạy"),
        (5, "B", "2026-08-25", K.NHAN_CHUA_XAC_MINH, "QUÃNG NGHỈ — chỗ rò cũ: chấm bù khi đào lại 07/09"),
        (6, "B", "2026-09-09", K.NHAN_DO_TIEN, "tuần ngay sau lần thấy cuối 07/09"),
        (7, "S", "2026-08-05", K.NHAN_TRUOC_MOC, "trước ngày gieo mầm 07/08"),
        (8, "S", "2026-08-15", K.NHAN_DO_TIEN, "gieo mầm rồi chạy liên tục"),
        (9, "C", "2026-09-23", K.NHAN_DO_TIEN, "nhật ký 21/09 có khoá C"),
        (10, "C", "2026-09-29", K.NHAN_NGOAI_HOAT_DONG, "nhật ký 28/09 vắng khoá C"),
        (11, "X", "2026-09-01", K.NHAN_KHONG_RO, "khoá không có trong sổ"),
    ]
    for i, k, d, _, _ in ca:
        con.execute("INSERT INTO mined_rule_effectiveness VALUES (?,?,?,NULL)", (i, k, d))

    nhan = K.tinh_giai_doan(con)
    truot = []
    print("=" * 92)
    print("  V11195 — CỔNG NHÃN ĐO TIẾN CỦA LUẬT (FU-456 · RM-15)")
    print("=" * 92)
    for i, k, d, phai, vi_sao in ca:
        ra = nhan.get(i)
        dung = ra == phai
        print(f"  {'✓' if dung else '✗'} ca {i:>2} khoá {k} ngày {d} → {ra:<26} (phải {phai}) — {vi_sao}")
        if not dung:
            truot.append(f"ca {i}: ra {ra}, phải {phai}")

    # Phép thử phải PHÂN BIỆT được: quy tắc cũ `date >= mốc` gắn DO_TIEN cho ca 5 (rò).
    cu_ca5 = K.NHAN_DO_TIEN if "2026-08-25" >= "2026-08-10" else K.NHAN_TRUOC_MOC
    if cu_ca5 != K.NHAN_DO_TIEN:
        truot.append("phép thử không phân biệt được: quy tắc cũ cũng không gắn DO_TIEN cho ca rò")
    print(f"  {'✓' if cu_ca5 == K.NHAN_DO_TIEN else '✗'} quy tắc CŨ (`date >= mốc`) gắn ca 5 là {cu_ca5} "
          f"⇒ phép thử bắt đúng chỗ rò")

    # phan_loai_giai_doan ghi đúng nhãn và chỉ ghi dòng đổi nhãn.
    r = K.phan_loai_giai_doan(con)
    ghi = {i: g for i, g in con.execute("SELECT id, giai_doan FROM mined_rule_effectiveness")}
    if ghi != nhan or r["_doi_nhan"] != len(ca):
        truot.append(f"phan_loai_giai_doan ghi lệch ({r['_doi_nhan']} dòng đổi, phải {len(ca)})")
    r2 = K.phan_loai_giai_doan(con)
    if r2["_doi_nhan"] != 0:
        truot.append(f"chạy lại phan_loai_giai_doan vẫn đổi {r2['_doi_nhan']} dòng — phải 0")
    print(f"  {'✓' if not truot else '·'} phan_loai_giai_doan ghi {r['_doi_nhan']} dòng · chạy lại đổi "
          f"{r2['_doi_nhan']} dòng")

    # Chạy lại lần đào CÙNG NGÀY không được cộng so_lan_dao hai lần.
    con.execute("INSERT INTO mined_rules VALUES (1,'MN',0,'','DAI1','MN','1','G7',1)")
    k_moi = K.khoa_luat("MN", 0, "", "DAI1", "MN", "1", "G7")
    K.ghi_nhan_lan_dao(con, ngay="2026-10-05")
    K.ghi_nhan_lan_dao(con, ngay="2026-10-05")
    so = con.execute("SELECT so_lan_dao FROM rule_key_registry WHERE rule_key=?", (k_moi,)).fetchone()[0]
    K.ghi_nhan_lan_dao(con, ngay="2026-10-12")
    so2 = con.execute("SELECT so_lan_dao FROM rule_key_registry WHERE rule_key=?", (k_moi,)).fetchone()[0]
    n_run = con.execute("SELECT COUNT(*) FROM rule_mining_runs WHERE run_date IN ('2026-10-05','2026-10-12')"
                        ).fetchone()[0]
    ok = so == 1 and so2 == 2 and n_run == 2
    print(f"  {'✓' if ok else '✗'} đào hai lần cùng ngày 05/10 ⇒ so_lan_dao {so} (phải 1); thêm 12/10 ⇒ {so2} "
          f"(phải 2); rule_mining_runs ghi {n_run} ngày (phải 2)")
    if not ok:
        truot.append("ghi_nhan_lan_dao cộng trùng hoặc không ghi lịch lần đào")

    print("=" * 92)
    if truot:
        for t in truot:
            print(f"  ✗ {t}")
        print("  ✗ [cong] NHAN_DO_TIEN_V11195=TRUOT")
        return 1
    print("  ✓ [cong] NHAN_DO_TIEN_V11195=DAT — luật nghỉ rồi được chấm bù không còn mang nhãn đo tiến")
    print("=" * 92)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
