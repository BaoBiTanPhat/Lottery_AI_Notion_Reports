# -*- coding: utf-8 -*-
"""V11025 (A1) — KHOÁ LUẬT BỀN: giữ được bằng chứng ĐO TIẾN qua mỗi lần đào lại.

═══════════════════════════════════════════════════════════════════════════════
VÌ SAO CÓ TỆP NÀY
═══════════════════════════════════════════════════════════════════════════════

Tra soát V11024 (07/08/2026) đo ra: **bộ đếm đo tiến bị xoá mỗi thứ Hai**.

`weekly_rule_miner.run_weekly_mining()` Step 4 làm hai việc:

    c.execute("DELETE FROM mined_rule_effectiveness WHERE date >= date('now','-112 days')")
    backfill_mined_rules(112)

Ý định ghi trong chú thích là đúng — *"Rebuild recent effectiveness window so new rule_ids keep
livingness/tracking continuity"*. Vấn đề nằm ở **gốc**: `_seed_rules.py:432` chạy
`DELETE FROM mined_rules` rồi INSERT lại, nên **`rule_id` đổi hết mỗi tuần**. Không có cách nào
nối bằng chứng cũ với luật mới ⇒ giải pháp cũ là **xoá sạch rồi chấm lại bằng hindsight**.

**Hậu quả đo được:**
- Mỗi thứ Hai, **1.680 dòng** bằng chứng bị xoá và thay bằng dòng chấm ngược.
- Số lượt ĐO TIẾN **không bao giờ vượt 35/miền** — nó bị bấm về 0 mỗi 7 ngày.
- Toàn bộ 105 luật cộng lại chỉ có **75 lượt** đo tiến, **0/105** đạt ngưỡng n≥20.
- Mọi kế hoạch dạng *"đo thêm N ngày rồi kết luận"* — kể cả FU-284, FU-325 — **vĩnh viễn không
  về đích**. Đây không phải "chưa đủ mẫu", là **bất khả thi về cấu trúc**.

═══════════════════════════════════════════════════════════════════════════════
CÁCH SỬA
═══════════════════════════════════════════════════════════════════════════════

**Không đụng `rule_id`** (nhiều chỗ đang đọc nó). Thay vào đó cấp cho mỗi luật một **KHOÁ BỀN**
không đổi qua các lần đào — chính là bộ sáu cột định danh nghiệp vụ của luật:

    (miền đích, thứ đích, đài nguồn, miền nguồn, lệch ngày, bộ giải)

Đo 07/08: **105 luật active → 105 khoá phân biệt**, tức khoá này **duy nhất**, dùng được.

Ba thứ dựng thêm:

1. **`rule_key_registry`** — sổ CHỈ THÊM, không bao giờ xoá. Ghi lần đầu tiên mỗi khoá xuất hiện.
   Đây là "ngày sinh thật" của một luật, thứ mà `mined_at` không cho biết vì nó bị đặt lại mỗi
   tuần.
2. **`mined_rule_effectiveness.rule_key`** + **`.giai_doan`** — mỗi dòng bằng chứng tự khai nó là
   `DO_TIEN` (ngày chấm ≥ ngày luật ra đời) hay `CHAM_NGUOC` (chấm vào quá khứ trước khi luật tồn
   tại). Suy ra được từ dữ liệu, không phụ thuộc lúc ghi.
3. **Step 4 mới**: thay `DELETE 112 ngày + backfill` bằng **NỐI LẠI + LẤP CHỖ TRỐNG**:
   - nối dòng cũ sang `rule_id` mới **theo khoá bền** (đúng mục tiêu ban đầu của Step 4)
   - **TUYỆT ĐỐI KHÔNG xoá dòng `DO_TIEN`** — đó là bằng chứng duy nhất không mua lại được
   - chỉ chấm lại những (ngày, khoá) **chưa có dòng nào**

**Điều thành thật phải ghi:** các luật đang có **không** biết ngày sinh thật, vì bảng lưu luật cũ
không tồn tại (`archived_previous` chỉ dùng để ghi log). Nên lần đầu chạy, sổ khoá sẽ **gieo
mầm** (`SEED_*`) từ bằng chứng sớm nhất còn lại. Chỉ những khoá xuất hiện **từ lần đào sau trở
đi** mới có ngày sinh `OBSERVED` — tức chắc chắn. Cột `nguon_lan_dau` nói rõ cái nào là cái nào.

**V11195 (26/11/2026, FU-456 · owner «6e --> theo khuyến nghị»):** nhãn `DO_TIEN` theo mục 2 ở
trên RÒ — luật nghỉ rồi được đào lại thì dòng chấm bù cho những ngày nghỉ vẫn mang `DO_TIEN`. Nay
nhãn do `tinh_giai_doan()` quyết (luật phải ĐANG HOẠT ĐỘNG ở ngày đó), dựa trên hai bảng chỉ thêm
`rule_mining_runs` + `rule_key_lan_dao` do `ghi_nhan_lan_dao()` ghi ở mỗi lần đào.
"""
from __future__ import annotations

import sqlite3
from datetime import datetime

# Sáu cột định danh nghiệp vụ. Đổi bộ này là đổi định nghĩa "cùng một luật" — phải đổi có ý thức.
COT_KHOA = ("target_region", "target_weekday", "source_station_slot|source_station",
            "source_region", "source_offset", "prize_keys")

DDL_REGISTRY = """
CREATE TABLE IF NOT EXISTS rule_key_registry (
    rule_key       TEXT PRIMARY KEY,
    lan_dau_thay   TEXT NOT NULL,     -- ngày đầu tiên khoá này được thấy
    nguon_lan_dau  TEXT NOT NULL,     -- OBSERVED | SEED_TU_MRE | SEED_TU_MINED_AT
    lan_cuoi_thay  TEXT NOT NULL,
    so_lan_dao     INTEGER NOT NULL DEFAULT 1,
    mo_ta          TEXT,
    created_at     TEXT NOT NULL,
    updated_at     TEXT NOT NULL
);
"""


# V11195 (FU-456, owner 26/11 «6e --> theo khuyến nghị») — NHẬT KÝ TỪNG LẦN ĐÀO, CHỈ THÊM.
# Sổ khoá chỉ giữ «thấy lần đầu / lần cuối / số lần» nên không biết luật NGHỈ ở tuần nào. Thiếu
# chỗ đó, dòng mà lần đào sau chấm bù cho đúng những ngày luật đang nghỉ — tức nằm TRONG cửa sổ
# đã dùng để chọn lại luật — vẫn được gắn `DO_TIEN`. Hai bảng dưới ghi lại sự thật lúc đào, để từ
# nay nhãn hết phải suy luận. Cả hai chỉ `INSERT OR IGNORE`: không UPDATE, không DELETE.
DDL_LAN_DAO = (
    """
CREATE TABLE IF NOT EXISTS rule_mining_runs (
    run_date    TEXT PRIMARY KEY,   -- ngày (giờ VN) của một lần đào thật
    so_khoa     INTEGER,            -- số khoá active thấy ở lần đào đó; NULL nếu nạp từ nhật ký cũ
    nguon       TEXT NOT NULL,      -- GHI_LUC_DAO | NAP_TU_SCHEDULER_LOGS_V11195
    created_at  TEXT NOT NULL
)
""",
    """
CREATE TABLE IF NOT EXISTS rule_key_lan_dao (
    run_date    TEXT NOT NULL,
    rule_key    TEXT NOT NULL,
    nguon       TEXT NOT NULL,      -- GHI_LUC_DAO | NAP_TU_MINED_RULES_V11195
    created_at  TEXT NOT NULL,
    PRIMARY KEY (run_date, rule_key)
)
""",
)

# Nhãn `giai_doan` — mọi phép đo chỉ được đếm `DO_TIEN` là đo tiến.
NHAN_DO_TIEN = "DO_TIEN"
NHAN_TRUOC_MOC = "KHONG_XAC_MINH_DUOC"
NHAN_KHONG_RO = "KHONG_RO_LUAT"
NHAN_NGOAI_HOAT_DONG = "NGOAI_THOI_GIAN_HOAT_DONG"   # V11195 — chắc chắn luật đang nghỉ hôm đó
NHAN_CHUA_XAC_MINH = "CHUA_XAC_MINH_HOAT_DONG"       # V11195 — luật có quãng nghỉ, không biết hôm đó có chạy


def khoa_luat(target_region, target_weekday, source_station_slot, source_station,
              source_region, source_offset, prize_keys) -> str:
    """Khoá bền của một luật. Cùng khoá = cùng một luật, dù `rule_id` có đổi bao nhiêu lần."""
    dai = (source_station_slot or source_station or "").strip()
    return "|".join([
        str(target_region or "").strip(),
        str(target_weekday if target_weekday is not None else ""),
        dai,
        str(source_region or "").strip(),
        str(source_offset or "").strip(),
        str(prize_keys or "").strip(),
    ])


def _co_cot(con: sqlite3.Connection, bang: str, cot: str) -> bool:
    return any(r[1] == cot for r in con.execute(f"PRAGMA table_info({bang})"))


def nang_cap_luoc_do(con: sqlite3.Connection) -> dict:
    """Thêm cột/bảng còn thiếu. Chạy được nhiều lần, không hỏng gì."""
    ra = {"them_cot": [], "them_bang": []}
    con.execute(DDL_REGISTRY)
    ra["them_bang"].append("rule_key_registry")
    # V11195 — từng câu `execute` riêng (KHÔNG `executescript`: nó tự COMMIT giao dịch đang dở của
    # lần đào hằng tuần).
    for ddl in DDL_LAN_DAO:
        con.execute(ddl)
    ra["them_bang"] += ["rule_mining_runs", "rule_key_lan_dao"]
    for cot, kieu in (("rule_key", "TEXT"), ("giai_doan", "TEXT")):
        if not _co_cot(con, "mined_rule_effectiveness", cot):
            con.execute(f"ALTER TABLE mined_rule_effectiveness ADD COLUMN {cot} {kieu}")
            ra["them_cot"].append(cot)
    con.execute("CREATE INDEX IF NOT EXISTS idx_mre_rule_key "
                "ON mined_rule_effectiveness(rule_key, date)")
    return ra


def _khoa_tu_dong_mre(r) -> str:
    return khoa_luat(r["target_region"], r["weekday"], r["source_station_slot"],
                     r["source_station"], r["source_region"], r["source_offset"],
                     r["prize_keys"])


def dien_khoa_cho_mre(con: sqlite3.Connection) -> int:
    """Điền `rule_key` cho mọi dòng MRE còn trống. Suy ra từ chính các cột đã có."""
    con.row_factory = sqlite3.Row
    n = 0
    for r in con.execute("SELECT id, target_region, weekday, source_station_slot, "
                         "source_station, source_region, source_offset, prize_keys "
                         "FROM mined_rule_effectiveness WHERE rule_key IS NULL").fetchall():
        con.execute("UPDATE mined_rule_effectiveness SET rule_key=? WHERE id=?",
                    (_khoa_tu_dong_mre(r), r["id"]))
        n += 1
    return n


def gieo_mam_registry(con: sqlite3.Connection) -> dict:
    """Gieo mầm sổ khoá từ bằng chứng còn lại.

    Bảng lưu luật cũ KHÔNG tồn tại, nên với khoá đã có sẵn ta chỉ biết được cận trên của ngày
    sinh: ngày chấm sớm nhất trong MRE, hoặc `mined_at` — lấy cái SỚM HƠN. Ghi rõ là SEED.
    """
    con.row_factory = sqlite3.Row
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    hom_nay = datetime.now().strftime("%Y-%m-%d")
    ra = {"moi": 0, "da_co": 0, "seed_tu_mre": 0, "seed_tu_mined_at": 0}

    som_nhat = {}
    for r in con.execute("SELECT rule_key, MIN(date) d FROM mined_rule_effectiveness "
                         "WHERE rule_key IS NOT NULL GROUP BY rule_key"):
        som_nhat[r["rule_key"]] = r["d"]

    for r in con.execute("SELECT target_region, target_weekday, source_station_slot, "
                         "source_station, source_region, source_offset, prize_keys, mined_at "
                         "FROM mined_rules WHERE is_active=1").fetchall():
        k = khoa_luat(r["target_region"], r["target_weekday"], r["source_station_slot"],
                      r["source_station"], r["source_region"], r["source_offset"],
                      r["prize_keys"])
        cu = con.execute("SELECT rule_key FROM rule_key_registry WHERE rule_key=?", (k,)).fetchone()
        if cu:
            con.execute("UPDATE rule_key_registry SET lan_cuoi_thay=?, so_lan_dao=so_lan_dao+1, "
                        "updated_at=? WHERE rule_key=?", (hom_nay, now, k))
            ra["da_co"] += 1
            continue
        mined = str(r["mined_at"] or "")[:10] or hom_nay
        tu_mre = som_nhat.get(k)
        if tu_mre and tu_mre < mined:
            dau, nguon = tu_mre, "SEED_TU_MRE"
            ra["seed_tu_mre"] += 1
        else:
            dau, nguon = mined, "SEED_TU_MINED_AT"
            ra["seed_tu_mined_at"] += 1
        con.execute("INSERT INTO rule_key_registry (rule_key, lan_dau_thay, nguon_lan_dau, "
                    "lan_cuoi_thay, so_lan_dao, mo_ta, created_at, updated_at) "
                    "VALUES (?,?,?,?,1,?,?,?)",
                    (k, dau, nguon, hom_nay,
                     "gieo mầm V11025 — bảng lưu luật cũ không tồn tại nên đây là CẬN TRÊN "
                     "của ngày sinh, không phải ngày sinh chắc chắn", now, now))
        ra["moi"] += 1
    return ra


def ghi_nhan_lan_dao(con: sqlite3.Connection, ngay: str | None = None) -> dict:
    """Gọi ở MỖI lần đào. Khoá mới ⇒ OBSERVED (ngày sinh CHẮC CHẮN). Khoá cũ ⇒ bump.

    V11195 (FU-456): ghi thêm `rule_mining_runs` + `rule_key_lan_dao` — sự thật «khoá nào có mặt
    ở lần đào nào» — để `tinh_giai_doan()` khỏi phải suy. Và chỉ cộng `so_lan_dao` khi khoá CHƯA
    được ghi cho ngày đào này: chạy lại cùng ngày trước đây cộng hai lần, làm phép suy «luật chạy
    liên tục» nhìn thấy số lần đào nhiều hơn số lần đào thật.
    """
    con.row_factory = sqlite3.Row
    for ddl in DDL_LAN_DAO:
        con.execute(ddl)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    hom_nay = ngay or datetime.now().strftime("%Y-%m-%d")
    ra = {"khoa_moi_observed": 0, "khoa_cu": 0, "khoa_da_ghi_cung_ngay": 0}
    thay = set()
    for r in con.execute("SELECT target_region, target_weekday, source_station_slot, "
                         "source_station, source_region, source_offset, prize_keys "
                         "FROM mined_rules WHERE is_active=1").fetchall():
        k = khoa_luat(r["target_region"], r["target_weekday"], r["source_station_slot"],
                      r["source_station"], r["source_region"], r["source_offset"],
                      r["prize_keys"])
        thay.add(k)
        lan_dau_cho_ngay_nay = con.execute(
            "INSERT OR IGNORE INTO rule_key_lan_dao (run_date, rule_key, nguon, created_at) "
            "VALUES (?, ?, 'GHI_LUC_DAO', ?)", (hom_nay, k, now)).rowcount == 1
        if con.execute("SELECT 1 FROM rule_key_registry WHERE rule_key=?", (k,)).fetchone():
            if not lan_dau_cho_ngay_nay:
                ra["khoa_da_ghi_cung_ngay"] += 1
                continue
            con.execute("UPDATE rule_key_registry SET lan_cuoi_thay=?, so_lan_dao=so_lan_dao+1, "
                        "updated_at=? WHERE rule_key=?", (hom_nay, now, k))
            ra["khoa_cu"] += 1
        else:
            con.execute("INSERT INTO rule_key_registry (rule_key, lan_dau_thay, nguon_lan_dau, "
                        "lan_cuoi_thay, so_lan_dao, mo_ta, created_at, updated_at) "
                        "VALUES (?,?, 'OBSERVED', ?, 1, ?, ?, ?)",
                        (k, hom_nay, hom_nay,
                         "thấy lần đầu ở đúng lần đào này — ngày sinh CHẮC CHẮN", now, now))
            ra["khoa_moi_observed"] += 1
    con.execute("INSERT OR IGNORE INTO rule_mining_runs (run_date, so_khoa, nguon, created_at) "
                "VALUES (?, ?, 'GHI_LUC_DAO', ?)", (hom_nay, len(thay), now))
    ra["so_khoa_lan_nay"] = len(thay)
    return ra


def _bang_co(con: sqlite3.Connection, bang: str) -> bool:
    return con.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name=?",
                       (bang,)).fetchone() is not None


def tinh_giai_doan(con: sqlite3.Connection) -> dict:
    """V11195 (FU-456) — tính nhãn `giai_doan` cho MỌI dòng MRE. CHỈ ĐỌC, trả {id: nhãn}.

    ═══ ĐO TIẾN NGHĨA LÀ GÌ ═══
    Một dòng (luật, ngày D) là đo tiến khi và chỉ khi **luật đã được CHỌN và ĐANG HOẠT ĐỘNG ở ngày
    D**, tức có mặt ở lần đào gần nhất ≤ D. Không phụ thuộc lúc dòng được chấm: chấm bù một ngày
    luật đang chạy vẫn ra đúng kết quả đo tiến; chấm bù một ngày luật đang NGHỈ thì là dữ liệu nằm
    trong cửa sổ đã dùng để chọn lại luật — đó chính là chỗ rò của bản cũ (`date >= mốc` là đủ).

    ═══ HAI NGUỒN, ƯU TIÊN NGUỒN GHI LÚC ĐÀO ═══
    1. `rule_key_lan_dao` có ghi lần đào gần nhất ≤ D ⇒ CHÍNH XÁC: có mặt ⇒ `DO_TIEN`,
       vắng ⇒ `NGOAI_THOI_GIAN_HOAT_DONG`.
    2. Ngày trước khi có nhật ký ⇒ SUY từ sổ khoá, theo hướng THẬN TRỌNG:
       · luật LIÊN TỤC (`so_lan_dao` = số lần đào thật trong [thấy đầu, thấy cuối]) ⇒ đo tiến cho
         [mốc chắc chắn, lần đào ngay sau lần thấy cuối);
       · luật CÓ QUÃNG NGHỈ ⇒ chỉ tuần ngay sau lần thấy đầu và tuần ngay sau lần thấy cuối là
         chắc chắn; phần giữa ⇒ `CHUA_XAC_MINH_HOAT_DONG` (không đếm là đo tiến);
       · từ lần đào ngay sau lần thấy cuối trở đi ⇒ `NGOAI_THOI_GIAN_HOAT_DONG`.
       Không có lịch lần đào (`rule_mining_runs` rỗng) ⇒ không suy được ⇒ chỉ giữ tuần chắc chắn
       thì cũng không có ⇒ mọi dòng sau mốc là `CHUA_XAC_MINH_HOAT_DONG`.
    Trước mốc chắc chắn ⇒ `KHONG_XAC_MINH_DUOC`; khoá không có trong sổ ⇒ `KHONG_RO_LUAT`.

    Quy tắc này khai TRƯỚC khi đo lại (RM-03) — phép đo `_v11195_do_lai_luat.py` đọc nhãn này.
    """
    from bisect import bisect_left, bisect_right

    con.row_factory = sqlite3.Row
    runs = ([r[0] for r in con.execute("SELECT run_date FROM rule_mining_runs ORDER BY run_date")]
            if _bang_co(con, "rule_mining_runs") else [])
    nhat_ky: dict[str, set] = {}
    run_co_nhat_ky: set = set()
    if _bang_co(con, "rule_key_lan_dao"):
        for rd, k in con.execute("SELECT run_date, rule_key FROM rule_key_lan_dao"):
            nhat_ky.setdefault(k, set()).add(rd)
            run_co_nhat_ky.add(rd)

    def lan_dao_truoc(d: str):
        i = bisect_right(runs, d)
        return runs[i - 1] if i else None

    def lan_dao_sau(d: str):
        i = bisect_right(runs, d)
        return runs[i] if i < len(runs) else None

    so = {}
    for r in con.execute("SELECT rule_key, lan_dau_thay, nguon_lan_dau, lan_cuoi_thay, so_lan_dao, "
                         "created_at FROM rule_key_registry"):
        observed = r["nguon_lan_dau"] == "OBSERVED"
        moc = r["lan_dau_thay"] if observed else str(r["created_at"])[:10]
        cuoi = r["lan_cuoi_thay"] or moc
        if observed:
            ky_vong = bisect_right(runs, cuoi) - bisect_left(runs, moc)
        else:  # lần gieo mầm cũng cộng 1 vào so_lan_dao; lần đào tính từ SAU ngày gieo
            ky_vong = 1 + bisect_right(runs, cuoi) - bisect_right(runs, moc)
        so[r["rule_key"]] = {
            "moc": moc,
            "cuoi": cuoi,
            "lien_tuc": bool(runs) and int(r["so_lan_dao"] or 0) == ky_vong,
            "het_tuan_dau": lan_dao_sau(moc),   # lần đào đầu tiên SAU mốc
            "tat_tu": lan_dao_sau(cuoi),        # lần đào đầu tiên SAU lần thấy cuối (None = còn chạy)
        }

    ra = {}
    for r in con.execute("SELECT id, rule_key, date FROM mined_rule_effectiveness"):
        s = so.get(r["rule_key"])
        d = r["date"]
        if not s:
            ra[r["id"]] = NHAN_KHONG_RO
            continue
        if d < s["moc"]:
            ra[r["id"]] = NHAN_TRUOC_MOC
            continue
        rd = lan_dao_truoc(d)
        if rd is not None and rd in run_co_nhat_ky:
            ra[r["id"]] = NHAN_DO_TIEN if rd in nhat_ky.get(r["rule_key"], ()) else NHAN_NGOAI_HOAT_DONG
            continue
        con_chay = s["tat_tu"] is None or d < s["tat_tu"]
        if not runs:
            g = NHAN_CHUA_XAC_MINH
        elif not con_chay:
            g = NHAN_NGOAI_HOAT_DONG
        elif s["lien_tuc"]:
            g = NHAN_DO_TIEN
        elif (s["het_tuan_dau"] is None or d < s["het_tuan_dau"]) or d >= s["cuoi"]:
            g = NHAN_DO_TIEN   # tuần ngay sau lần thấy đầu · tuần ngay sau lần thấy cuối
        else:
            g = NHAN_CHUA_XAC_MINH
        ra[r["id"]] = g
    return ra


def nap_lich_su_lan_dao(con: sqlite3.Connection, ngay_dao: list[str], nguon: str) -> int:
    """V11195 — nạp MỘT LẦN các ngày đào thật đã xảy ra trước khi có `rule_mining_runs`.

    `ngay_dao` phải đến từ bằng chứng (nhật ký `scheduler_logs`), không đoán. Chỉ thêm, không sửa.
    """
    for ddl in DDL_LAN_DAO:
        con.execute(ddl)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    n = 0
    for d in sorted(set(ngay_dao)):
        n += con.execute("INSERT OR IGNORE INTO rule_mining_runs (run_date, so_khoa, nguon, created_at) "
                         "VALUES (?, NULL, ?, ?)", (d, nguon, now)).rowcount or 0
    return n


def phan_loai_giai_doan(con: sqlite3.Connection) -> dict:
    """Gán `giai_doan` cho mọi dòng MRE.

    ═══ VÌ SAO KHÔNG DÙNG `lan_dau_thay` LÀM MỐC ═══

    Bản đầu của hàm này gán `DO_TIEN` khi `date >= lan_dau_thay`. Thử khô cho ra
    **DO_TIEN 2.437 · CHAM_NGUOC 0** — nghe như thắng lớn, nhưng đó là **thắng lợi giả**:
    với khoá gieo mầm, `lan_dau_thay` được lấy bằng CHÍNH ngày chấm sớm nhất trong MRE, nên
    mọi dòng đương nhiên `>=` nó. Phép đo tự khen chính mình.

    Sự thật: với khoá gieo mầm, ta **không chứng minh được** luật đã tồn tại trước ngày đó hay
    được chọn ra bằng chính dữ liệu ngày đó. Bảng lưu luật cũ không tồn tại. Không biết thì phải
    nói là không biết.

    ═══ BA NHÃN ═══

    `DO_TIEN`              ngày chấm >= `moc_chac_chan` — luật CHẮC CHẮN đã tồn tại trước ngày đó
    `KHONG_XAC_MINH_DUOC`  khoá có trong sổ nhưng ngày chấm nằm TRƯỚC mốc chắc chắn ⇒ không có
                           cách nào biết nó là đo tiến hay chấm ngược. **Không được đếm là đo tiến.**
    `KHONG_RO_LUAT`        khoá không còn trong sổ (luật đã biến mất khỏi bộ hiện hành)

    `moc_chac_chan` = ngày mà ta BẮT ĐẦU biết chắc:
      · khoá `OBSERVED`  ⇒ chính `lan_dau_thay` (thấy lần đầu ở một lần đào có thật)
      · khoá `SEED_*`    ⇒ ngày gieo mầm (`created_at`) — từ hôm đó trở đi mới đếm được

    ⇒ Ngay sau khi vá, số ĐO TIẾN sẽ gần **0**. Đó là con số ĐÚNG. Nó bắt đầu tăng từ ngày mai
    và **không bị xoá nữa** — đó mới là thứ phép vá này mua được.

    ═══ V11195 (FU-456) — «date >= mốc» CHƯA ĐỦ ═══
    Mỗi tuần `weekly_rule_miner` chấm bù 112 ngày cho mọi luật đang active. Luật nghỉ vài tuần
    rồi được đào lại thì được chấm bù đúng những ngày nó NGHỈ — những ngày đó nằm trong cửa sổ đã
    dùng để chọn lại nó, nhưng `date >= mốc` vẫn gắn `DO_TIEN`. Kiểm toán V11190: PHẦN 4 nguyên văn
    z +4,9…+8,2, còn trên tập luật chạy liên tục chỉ +1,41 · +1,91 · −0,47. Nay nhãn do
    `tinh_giai_doan()` quyết: chỉ `DO_TIEN` khi luật ĐANG HOẠT ĐỘNG ở ngày đó. Hai nhãn mới:
    `NGOAI_THOI_GIAN_HOAT_DONG` · `CHUA_XAC_MINH_HOAT_DONG`.
    """
    nhan = tinh_giai_doan(con)
    hien = {r[0]: r[1] for r in con.execute("SELECT id, giai_doan FROM mined_rule_effectiveness")}
    ra = {NHAN_DO_TIEN: 0, NHAN_TRUOC_MOC: 0, NHAN_KHONG_RO: 0,
          NHAN_NGOAI_HOAT_DONG: 0, NHAN_CHUA_XAC_MINH: 0, "_doi_nhan": 0}
    for i, g in nhan.items():
        ra[g] = ra.get(g, 0) + 1
        if hien.get(i) != g:
            con.execute("UPDATE mined_rule_effectiveness SET giai_doan=? WHERE id=?", (g, i))
            ra["_doi_nhan"] += 1
    return ra


def noi_lai_rule_id(con: sqlite3.Connection) -> dict:
    """Nối dòng bằng chứng cũ sang `rule_id` MỚI theo khoá bền.

    Đây chính là mục tiêu mà Step 4 cũ muốn đạt — nhưng đạt bằng cách XOÁ rồi chấm lại.
    Nối lại giữ nguyên bằng chứng, kể cả bằng chứng đo tiến.
    """
    con.row_factory = sqlite3.Row
    ban_do = {}
    for r in con.execute("SELECT id, target_region, target_weekday, source_station_slot, "
                         "source_station, source_region, source_offset, prize_keys "
                         "FROM mined_rules WHERE is_active=1").fetchall():
        ban_do[khoa_luat(r["target_region"], r["target_weekday"], r["source_station_slot"],
                         r["source_station"], r["source_region"], r["source_offset"],
                         r["prize_keys"])] = r["id"]
    n = 0
    for k, rid in ban_do.items():
        cur = con.execute("UPDATE mined_rule_effectiveness SET rule_id=? "
                          "WHERE rule_key=? AND rule_id<>?", (rid, k, rid))
        n += cur.rowcount or 0
    return {"dong_noi_lai": n, "khoa_hien_hanh": len(ban_do)}


def thong_ke(con: sqlite3.Connection) -> dict:
    con.row_factory = sqlite3.Row
    r = con.execute("SELECT giai_doan, COUNT(*) n, COUNT(DISTINCT rule_key) k "
                    "FROM mined_rule_effectiveness GROUP BY giai_doan").fetchall()
    ra = {x["giai_doan"] or "(trống)": {"dong": x["n"], "khoa": x["k"]} for x in r}
    du = con.execute("SELECT COUNT(*) FROM (SELECT rule_key FROM mined_rule_effectiveness "
                     "WHERE giai_doan='DO_TIEN' GROUP BY rule_key HAVING COUNT(*)>=20)").fetchone()[0]
    ra["_khoa_du_mau_do_tien_n20"] = du
    ra["_so_khoa_trong_so"] = con.execute("SELECT COUNT(*) FROM rule_key_registry").fetchone()[0]
    return ra
