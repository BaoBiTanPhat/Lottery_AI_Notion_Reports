# -*- coding: utf-8 -*-
"""V11173-r2 · SC-12 muc 3+4 — KHOA COHORT "WR TONG" + LOAI BACKFILL BANG READ SEMANTICS.

TRANG THAI: CANDIDATE cho toi khi chay --cai-dat.
Tep nay nam trong artifacts/, KHONG duoc import boi bat ky tien trinh production nao.

===========================================================================
PHAM VI (owner khoa 09/09/2026) — SC-12 = OWNER_APPROVED · MEASUREMENT_ONLY
===========================================================================
DUOC sua : cach DOC de tinh chi so (daily_evaluation.py)
CAM sua  : ranked/prediction output · roster/model state · model weights/strength
           · TOTAL · prediction SYSTEM_PROMPT / context prompt · Combo/FINAL
           · output_counterfactual_rank production write · lo3_status va goi 32 nhan
           · thuat toan sinh/chon so · moi van de ERP
CAM ghi  : va nay KHONG THEM lenh INSERT/UPDATE/DELETE nao.

    ⚠️ DINH CHINH (phan bien 09/09 bat duoc — ban nhap ghi sai):
    Noi "khong ghi DB" la KHONG CHINH XAC cho toan he. Ham duoc va chi DOC, nhung
    `evaluate_day()` TRONG CUNG TEP (daily_evaluation.py:419) chay
    `INSERT OR REPLACE INTO daily_eval_log` dua tren cohort do ham nay tra ve, va
    `run_daily_eval()` duoc scheduler goi tu dong (scheduler.py:1836 sau MB-verify,
    va :9264 job hang ngay). Nen tu ngay deploy, `daily_eval_log` se nhan GIA TRI MOI.
    Day la THAY DOI DU LIEU, khong chi thay doi cach doc — va rollback CODE KHONG
    hoan tac cac dong da ghi trong thoi gian va dang chay.

===========================================================================
VAN DE (do tren DB production 09/09/2026, khong suy dien)
===========================================================================
daily_evaluation.py `_get_combo_super_predictions(days_back)` dat `LIMIT days_back*3`
SAU menh de WHERE da loai EXCLUDE_PRIMARY/EXCLUDE_ALL.

  MUC 3 — COHORT TRUOT:
    days_back=90 => LIMIT 270 ("3 mien moi ngay"). Do that: 270 dong do trai tu
    2026-03-29 den 2026-09-08 = 156 NGAY rieng biet — voi nguoc 66 ngay so voi nhan
    "90 ngay". Cang nhieu ngay bi loai thi cua so cang dai. `total_predictions` GIAM
    dan theo ngay (V11170 do: 145 -> 144).

  MUC 4 — BACKFILL RO VAO LIVE METRICS:
    final_bundles co 90 dong notes='Phase 1.5 backfill' (2026-02-28..2026-03-29).
    Trong `predictions` chung KHONG co dau rieng (deu run_source='auto_daily') nen
    khong loc duoc neu chi doc mot bang predictions.
    Tac dong THUC theo caller (do that, ghi trung thuc):
      days_back=90   -> loai 0 dong   (moc chan 90 ngay da bo qua backfill 02-03/2026)
      days_back=9999 -> 375 -> 335, loai 40 dong  (evaluate_all_history)

===========================================================================
NGUYEN TAC — r2 lam cung theo Prompt 43 R1 phan Q
===========================================================================
1. CHI DOI CACH DOC. Khong ghi DB, khong doi hanh vi du doan.
2. KHOA COHORT BANG NGAY. LIMIT giu lai lam TRAN AN TOAN (non-binding).
3. GIO VIET NAM (§55). CAM lay moc ngay tu SQLite — no tinh theo UTC, lech 7 gio.
4. r2: DUNG `NOT EXISTS` THAY CHO `LEFT JOIN` (Q phan VII muc 3).
   LEFT JOIN co hai rui ro ma NOT EXISTS khong co:
     (a) nhan ban dong neu mot (date,region) co >1 bundle khop;
     (b) ap va hai lan se chen JOIN doi (SAU_JOIN chua nguyen van TRUOC_JOIN).
   NOT EXISTS la vi tu thuan: khong bao gio doi so dong tra ve.
5. FAIL-SAFE: khong co bundle => NOT EXISTS dung => dong VAN duoc giu.
   Mat mat toi da la giu nguyen hanh vi cu, khong bao gio loai nham.
6. FAIL-CLOSED (Q phan V muc 5): CHi ap len source hash DA DUOC NHAN DIEN;
   dung 1 preimage; dung so lan thay the du kien; marker dung 1 lan;
   cam patch theo so dong mu.
"""
import sys, io, os, re, json, sqlite3, hashlib, shutil, argparse, datetime

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

PHIEN_BAN = "V11173-r2-SC12-M34"
GOC = "/root/Lottery_AI_Test"
BE = GOC + "/web/backend/"
TEP = BE + "daily_evaluation.py"
DB = "file:" + GOC + "/data/lottery_ai.db?mode=ro"
SAO_LUU = BE + "daily_evaluation.py.pre_v11173"
MARKER = "V11173"

# --- FAIL-CLOSED: chi ap len source DA NHAN DIEN (sha256 full, LF tren VPS) ---
PREIMAGE_SHA256 = {
    "42a7c0fcf04450bdf09c604b8f47bd576abfde413daa3edeb31534cac51ca603":
        "daily_evaluation.py @ VPS 09/09/2026 · 25568 byte · khop kho local HEAD 20140b6 (chuan hoa LF)",
}
SO_THAY_THE_DU_KIEN = 2   # dung 2 khoi: moc cutoff + menh de WHERE
SO_MARKER_SAU_VA = 3      # dem THUC: 1 trong SAU_CUT + 2 trong SAU (chot idempotent)

# ==========================================================================
# PHAN 1 — HAI KHOI VA (TRUOC / SAU) theo §60.4 — KHONG con khoi JOIN
# ==========================================================================

TRUOC_CUT = """    conn = _get_conn()
    # V6.7: Removed verdict='CHOT_HA' filter"""

SAU_CUT = """    conn = _get_conn()
    # V11173 SC-12 muc 3: moc chan cohort tinh bang GIO VIET NAM (§55).
    # Dung dung idiom san co cua tep nay (xem :547-548 va :629-630):
    # tep import `from datetime import datetime, timedelta`, con `timezone` thi
    # import CUC BO. CAM lay moc ngay tu SQLite — no tinh theo UTC, lech 7 gio.
    # Bien: D0 va D89 NAM TRONG, D90 BI LOAI (>= cutoff, cutoff = homnay - 89).
    from datetime import timezone as _v11173_tz
    _v11173_cutoff = (datetime.now(_v11173_tz(timedelta(hours=7)))
                      - timedelta(days=max(0, int(days_back) - 1))
                      ).strftime('%Y-%m-%d')
    # V6.7: Removed verdict='CHOT_HA' filter"""

TRUOC = """        WHERE p.ai_model = 'combo-super'
          AND p.status IN ('WIN', 'LOSE', 'PARTIAL')
          AND COALESCE(dg.evaluation_policy, 'INCLUDE') NOT IN
              ('EXCLUDE_PRIMARY', 'EXCLUDE_ALL')
        ORDER BY p.date DESC
        LIMIT ?
    \"\"\", (days_back * 3,))  # 3 regions per day max"""

SAU = """        WHERE p.ai_model = 'combo-super'
          AND p.status IN ('WIN', 'LOSE', 'PARTIAL')
          AND COALESCE(dg.evaluation_policy, 'INCLUDE') NOT IN
              ('EXCLUDE_PRIMARY', 'EXCLUDE_ALL')
          -- V11173 SC-12 muc 3: KHOA COHORT theo NGAY (gio VN), khong de LIMIT truot.
          AND p.date >= ?
          -- V11173 SC-12 muc 4: loai bundle backfill khoi LIVE metrics (read semantics).
          --   Dung vi tu phu dinh ton tai chu KHONG dung JOIN: khong bao gio nhan ban dong.
          --   Fail-safe: khong co bundle khop => vi tu dung => dong VAN duoc giu.
          AND NOT EXISTS (
                SELECT 1 FROM final_bundles fb
                 WHERE fb.date = p.date
                   AND fb.region = p.target_region
                   AND fb.status = 'ACTIVE'
                   AND COALESCE(fb.notes, '') LIKE '%Phase 1.5 backfill%'
              )
        ORDER BY p.date DESC
        LIMIT ?
    \"\"\", (_v11173_cutoff, days_back * 3))  # LIMIT chi con la TRAN AN TOAN"""


def _doc():
    return io.open(TEP, encoding="utf-8", newline="").read()


def _sha(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def _sha_tep(p):
    return hashlib.sha256(io.open(p, "rb").read()).hexdigest()


def _ap(s):
    """Ap va — CHOT idempotent bang MARKER, khong replace tho."""
    if MARKER in s:
        return s
    return s.replace(TRUOC_CUT, SAU_CUT, 1).replace(TRUOC, SAU, 1)


# ==========================================================================
# PHAN 2 — DO TAC DONG tren DB THAT (chi doc)
# ==========================================================================

_SEL = "SELECT p.date, p.target_region FROM predictions p "
_JG = ("LEFT JOIN day_governance dg ON p.date = dg.date AND p.target_region = dg.region "
       "WHERE p.ai_model = 'combo-super' AND p.status IN ('WIN','LOSE','PARTIAL') "
       "AND COALESCE(dg.evaluation_policy,'INCLUDE') NOT IN ('EXCLUDE_PRIMARY','EXCLUDE_ALL') ")
_BF = ("AND NOT EXISTS (SELECT 1 FROM final_bundles fb WHERE fb.date=p.date "
       "AND fb.region=p.target_region AND fb.status='ACTIVE' "
       "AND COALESCE(fb.notes,'') LIKE '%Phase 1.5 backfill%') ")


def _cutoff(days_back, as_of=None):
    vn = datetime.timezone(datetime.timedelta(hours=7))
    goc = (datetime.datetime.strptime(as_of, "%Y-%m-%d").replace(tzinfo=vn)
           if as_of else datetime.datetime.now(vn))
    return (goc - datetime.timedelta(days=max(0, int(days_back) - 1))).strftime("%Y-%m-%d")


def do_tac_dong(days_back=90, as_of=None):
    c = sqlite3.connect(DB, uri=True); c.row_factory = sqlite3.Row
    cut = _cutoff(days_back, as_of)
    cu = c.execute(_SEL + _JG + "ORDER BY p.date DESC LIMIT ?", (days_back * 3,)).fetchall()
    moi = c.execute(_SEL + _JG + "AND p.date>=? " + _BF + "ORDER BY p.date DESC LIMIT ?",
                    (cut, days_back * 3)).fetchall()

    def tt(rows):
        ng = sorted({r["date"] for r in rows})
        m = {}
        for r in rows:
            m[r["target_region"]] = m.get(r["target_region"], 0) + 1
        return {"dong": len(rows), "ngay_rieng": len(ng),
                "tu": ng[0] if ng else None, "den": ng[-1] if ng else None, "theo_mien": m}

    r = {"days_back": days_back, "as_of": as_of or "live", "cutoff_VN": cut,
         "TRUOC": tt(cu), "SAU": tt(moi)}
    c.close()
    return r


# ==========================================================================
# PHAN 3 — TEST
# ==========================================================================

def chay_test():
    dat = fail = 0

    def ok(ten, dk, ghi=""):
        nonlocal dat, fail
        if dk:
            dat += 1; print("  DAT  %s  %s" % (ten, ghi))
        else:
            fail += 1; print("  HONG %s  %s" % (ten, ghi))

    print("=" * 74)
    print("TEST %s   (ICT %s)" % (PHIEN_BAN,
          datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=7))).strftime("%Y-%m-%d %H:%M:%S")))
    print("=" * 74)

    s = _doc()
    h = _sha(s)

    print("\n=== A — FAIL-CLOSED: chi ap len source DA NHAN DIEN ===")
    ok("A1 source hash nam trong danh sach cho phep", h in PREIMAGE_SHA256, h[:24] + "...")
    ok("A2 nhan dien dung ban", PREIMAGE_SHA256.get(h, "").startswith("daily_evaluation.py"),
       PREIMAGE_SHA256.get(h, "(khong nhan dien)"))
    ok("A3 preimage CUT khop DUNG 1 lan", s.count(TRUOC_CUT) == 1, "dem=%d" % s.count(TRUOC_CUT))
    ok("A4 preimage WHERE khop DUNG 1 lan", s.count(TRUOC) == 1, "dem=%d" % s.count(TRUOC))
    ok("A5 CHUA tung ap va", MARKER not in s)
    ok("A6 tep dung ten datetime/timedelta DA import",
       bool(re.search(r"^from datetime import datetime, timedelta\s*$", s, re.M)))

    print("\n=== B — SAU KHI AP ===")
    s2 = _ap(s)
    try:
        compile(s2, "daily_evaluation.py", "exec"); cp, loi = True, ""
    except SyntaxError as e:
        cp, loi = False, str(e)
    ok("B1 cu phap Python HOP LE", cp, loi)
    ok("B2 dai ra, khong ngan di", len(s2) > len(s), "%d -> %d byte" % (len(s), len(s2)))
    ok("B3 so lan thay the DUNG du kien",
       (s.count(TRUOC_CUT) - s2.count(TRUOC_CUT)) + (s.count(TRUOC) - s2.count(TRUOC)) == SO_THAY_THE_DU_KIEN,
       "%d" % SO_THAY_THE_DU_KIEN)
    ok("B4 marker xuat hien DUNG so du kien", s2.count(MARKER) == SO_MARKER_SAU_VA,
       "dem=%d (du kien %d)" % (s2.count(MARKER), SO_MARKER_SAU_VA))
    ok("B5 KHONG co JOIN final_bundles nao (r2 dung NOT EXISTS)",
       "JOIN final_bundles" not in s2)
    # Tep GOC da co san 1 chuoi "NOT EXISTS (" o cho khac => phai do DELTA, khong do tuyet doi.
    ok("B6 va THEM DUNG 1 NOT EXISTS", s2.count("NOT EXISTS (") - s.count("NOT EXISTS (") == 1,
       "goc=%d -> sau=%d" % (s.count("NOT EXISTS ("), s2.count("NOT EXISTS (")))
    ok("B7 co moc cutoff VN", "_v11173_cutoff" in s2)
    _sql = s2[s2.index("SELECT p.date, p.target_region"):s2.index("rows = [dict(r)")]
    ok("B8 SQL moi KHONG lay moc ngay tu SQLite",
       ("'now'" not in _sql) and ("CURRENT_DATE" not in _sql) and ("julianday" not in _sql))
    ok("B9 ap lai lan hai KHONG doi gi (chot marker)", _ap(s2) == s2)
    ok("B10 so dong SELECT ... FROM predictions khong doi",
       s2.count("FROM predictions p") == s.count("FROM predictions p"))

    print("\n=== C — BIEN LICH (D0 trong · D89 trong · D90 NGOAI) ===")
    vn = datetime.timezone(datetime.timedelta(hours=7))
    hn = datetime.datetime.now(vn).strftime("%Y-%m-%d")
    ok("C1 cutoff(1) = hom nay ICT", _cutoff(1) == hn, _cutoff(1))
    d0 = datetime.datetime.strptime(hn, "%Y-%m-%d").date()
    c90 = datetime.datetime.strptime(_cutoff(90), "%Y-%m-%d").date()
    ok("C2 cutoff(90) = D-89", (d0 - c90).days == 89, "cach %d ngay" % (d0 - c90).days)
    ok("C3 D0 NAM TRONG (D0 >= cutoff)", hn >= _cutoff(90))
    d89 = (d0 - datetime.timedelta(days=89)).strftime("%Y-%m-%d")
    ok("C4 D89 NAM TRONG", d89 >= _cutoff(90), d89)
    d90 = (d0 - datetime.timedelta(days=90)).strftime("%Y-%m-%d")
    ok("C5 D90 BI LOAI", not (d90 >= _cutoff(90)), d90)
    ok("C6 as_of khoa lai duoc (tai lap)", _cutoff(90, "2026-09-09") == "2026-06-12",
       _cutoff(90, "2026-09-09"))
    ok("C7 days_back=0 khong no", _cutoff(0) == hn)
    ok("C8 days_back=9999 lui rat xa", _cutoff(9999) < "2000-01-01", _cutoff(9999))
    try:
        _cutoff(90, "khong-phai-ngay"); xau = False
    except Exception:
        xau = True
    ok("C9 ngay hong => FAIL-CLOSED (nem loi, khong am tham)", xau)

    print("\n=== D — VUNG CAM (forbidden-surface diff) ===")
    for ten, tu in (("D1 ranked/prediction output", "ranked_numbers"),
                    ("D2 roster/model state", "_CANONICAL_OUTPUT_MODELS"),
                    ("D3 model weights/strength", "strength_weight"),
                    ("D4 TOTAL/Combo", "run_combo_super"),
                    ("D5 prediction SYSTEM_PROMPT", "SYSTEM_PROMPT"),
                    ("D6 output_counterfactual_rank", "output_counterfactual_rank"),
                    ("D7 lo3_status", "lo3_status"),
                    ("D8 FINAL bundle writer", "save_final_bundle")):
        ok(ten, s.count(tu) == s2.count(tu), "so lan %d -> %d" % (s.count(tu), s2.count(tu)))
    ok("D9 KHONG them lenh ghi DB",
       s2.count("INSERT") == s.count("INSERT") and s2.count("UPDATE") == s.count("UPDATE")
       and s2.count("DELETE") == s.count("DELETE"),
       "INSERT %d/%d · UPDATE %d/%d · DELETE %d/%d" % (s.count("INSERT"), s2.count("INSERT"),
       s.count("UPDATE"), s2.count("UPDATE"), s.count("DELETE"), s2.count("DELETE")))
    ok("D10 chi dung MOT ham bi sua", s2.count("def _get_combo_super_predictions") == 1)

    print("\n=== E — CARDINALITY: NOT EXISTS khong doi so dong ===")
    try:
        c = sqlite3.connect(DB, uri=True)
        n_base = c.execute("SELECT COUNT(*) FROM predictions p " + _JG).fetchone()[0]
        n_bf = c.execute("SELECT COUNT(*) FROM predictions p " + _JG + _BF).fetchone()[0]
        n_join = c.execute("SELECT COUNT(*) FROM predictions p LEFT JOIN day_governance dg "
                           "ON p.date=dg.date AND p.target_region=dg.region "
                           "LEFT JOIN final_bundles fb ON fb.date=p.date AND fb.region=p.target_region "
                           "AND fb.status='ACTIVE' WHERE p.ai_model='combo-super' "
                           "AND p.status IN ('WIN','LOSE','PARTIAL') "
                           "AND COALESCE(dg.evaluation_policy,'INCLUDE') NOT IN "
                           "('EXCLUDE_PRIMARY','EXCLUDE_ALL')").fetchone()[0]
        c.close()
        ok("E1 LEFT JOIN khong nhan ban dong (bang chung)", n_join == n_base,
           "join=%d base=%d" % (n_join, n_base))
        ok("E2 NOT EXISTS CHi loai bot, khong bao gio them", n_bf <= n_base,
           "base=%d -> %d" % (n_base, n_bf))
        ok("E3 co dong backfill THAT de loai", n_base - n_bf > 0, "loai %d dong" % (n_base - n_bf))
    except Exception as e:
        ok("E* cardinality", False, "%s: %s" % (type(e).__name__, e))

    print("\n=== F — TAC DONG THAT (as_of=2026-09-09, tai lap so handoff) ===")
    try:
        r = do_tac_dong(90, "2026-09-09")
        t, u = r["TRUOC"], r["SAU"]
        print("     cutoff VN = %s" % r["cutoff_VN"])
        print("     TRUOC: %d dong · %d ngay · %s..%s · %s" % (t["dong"], t["ngay_rieng"], t["tu"], t["den"], t["theo_mien"]))
        print("     SAU  : %d dong · %d ngay · %s..%s · %s" % (u["dong"], u["ngay_rieng"], u["tu"], u["den"], u["theo_mien"]))
        ok("F1 TRUOC vi pham nhan '90 ngay'", t["ngay_rieng"] > 90, "%d ngay" % t["ngay_rieng"])
        ok("F2 SAU nam trong 90 ngay lich", u["ngay_rieng"] <= 90, "%d ngay" % u["ngay_rieng"])
        ok("F3 SAU khong con dong truoc moc chan", (u["tu"] or "9999") >= r["cutoff_VN"], str(u["tu"]))
        ok("F4 SAU khong rong", u["dong"] > 0, "%d dong" % u["dong"])
        r9 = do_tac_dong(9999, "2026-09-09")
        print("     all-history: %d -> %d dong (loai %d)"
              % (r9["TRUOC"]["dong"], r9["SAU"]["dong"], r9["TRUOC"]["dong"] - r9["SAU"]["dong"]))
        ok("F5 all-history loai dung 40 dong backfill",
           r9["TRUOC"]["dong"] - r9["SAU"]["dong"] == 40,
           "loai %d" % (r9["TRUOC"]["dong"] - r9["SAU"]["dong"]))
    except Exception as e:
        ok("F* tac dong", False, "%s: %s" % (type(e).__name__, e))

    print("\n" + "=" * 74)
    print("TONG: %d/%d DAT" % (dat, dat + fail))
    print("=" * 74)
    return fail == 0


# ==========================================================================
# PHAN 4 — CAI DAT / GO VE (fail-closed)
# ==========================================================================

def cai_dat():
    s = _doc(); h = _sha(s)
    if MARKER in s:
        print("  ! DA AP VA — khong ap lai (idempotent). sha256 hien tai:", _sha_tep(TEP)); return 0
    if h not in PREIMAGE_SHA256:
        print("  ! HUY (fail-closed): source hash KHONG nam trong danh sach nhan dien"); print("    ", h); return 1
    if s.count(TRUOC_CUT) != 1 or s.count(TRUOC) != 1:
        print("  ! HUY: preimage khop sai so lan  CUT=%d WHERE=%d" % (s.count(TRUOC_CUT), s.count(TRUOC))); return 1
    s2 = _ap(s)
    if s2.count(MARKER) != SO_MARKER_SAU_VA:
        print("  ! HUY: marker sau va = %d, du kien %d" % (s2.count(MARKER), SO_MARKER_SAU_VA)); return 1
    if "JOIN final_bundles" in s2 or (s2.count("NOT EXISTS (") - s.count("NOT EXISTS (")) != 1:
        print("  ! HUY: cau truc SQL sau va khong dung"); return 1
    compile(s2, "daily_evaluation.py", "exec")
    shutil.copy2(TEP, SAO_LUU)
    print("  sao luu :", SAO_LUU, "· sha256", _sha_tep(SAO_LUU)[:24] + "...")
    io.open(TEP, "w", encoding="utf-8", newline="").write(s2)
    print("  DA AP VA · %d -> %d byte" % (len(s), len(s2)))
    print("  PREIMAGE  sha256:", h)
    print("  POSTIMAGE sha256:", _sha_tep(TEP))
    return 0


def go_ve():
    if not os.path.exists(SAO_LUU):
        print("  ! khong co ban sao luu", SAO_LUU); return 1
    shutil.copy2(SAO_LUU, TEP)
    h = _sha_tep(TEP)
    print("  DA GO VE tu", SAO_LUU); print("  sha256:", h)
    print("  khop preimage goc:", h in PREIMAGE_SHA256)
    return 0 if h in PREIMAGE_SHA256 else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--test", action="store_true")
    ap.add_argument("--do", action="store_true", help="chi do tac dong, khong sua gi")
    ap.add_argument("--as-of", default=None)
    ap.add_argument("--cai-dat", action="store_true")
    ap.add_argument("--rollback", action="store_true")
    ap.add_argument("--out", default=GOC + "/artifacts/v11173_sc12_m34_kq.json")
    a = ap.parse_args()
    if a.rollback:
        return go_ve()
    if a.cai_dat:
        return cai_dat()
    if a.do:
        print(json.dumps({"90": do_tac_dong(90, a.as_of), "9999": do_tac_dong(9999, a.as_of)},
                         ensure_ascii=False, indent=1)); return 0
    ok = chay_test()
    try:
        io.open(a.out, "w", encoding="utf-8", newline="\n").write(json.dumps(
            {"phien_ban": PHIEN_BAN, "dat": ok,
             "ICT": datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=7))).isoformat(),
             "UTC": datetime.datetime.now(datetime.timezone.utc).isoformat(),
             "preimage_sha256": _sha(_doc()),
             "tac_dong_as_of_20260909": do_tac_dong(90, "2026-09-09")},
            ensure_ascii=False, indent=1))
        print("GHI:", a.out)
    except Exception as e:
        print("khong ghi duoc artifact:", e)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
