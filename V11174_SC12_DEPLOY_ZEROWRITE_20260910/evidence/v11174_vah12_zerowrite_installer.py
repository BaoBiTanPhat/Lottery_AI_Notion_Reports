# -*- coding: utf-8 -*-
"""V11174 · VA-h12 THAT — KE TOAN CAP/GATE · FINAL_BUNDLES_ZERO_WRITE.

Thay the hoan toan `artifacts/v11165_h12_patch.py` — goi cu KHONG PHAI installer:
`--cai-dat` cua no chi tu chep chinh no len chinh no (DICH == duong dan cua no),
0 dong ghi vao main.py/database.py, va no tu khai "CANDIDATE_KHONG_DEPLOY".
Nhan lai goi cu: VA_H12=DESIGN_HELPER_TESTED · REAL_INSTALLER_MISSING.

===========================================================================
KHOA CANON AP DUNG (Prompt 43 R1 §R muc II)
===========================================================================
FINAL_BUNDLES_ZERO_WRITE          — va nay KHONG ghi/sua final_bundles
OUTPUT_COUNTERFACTUAL_RANK_...    — khong dung toi
SC-12 = MEASUREMENT_ONLY          — chi sua ke toan + taxonomy hien thi
CAM: prediction output · roster/weights · TOTAL · prompt du doan · Combo · FINAL
     · logic 3-cang · 32 nhan lo3

===========================================================================
THIET KE LAI so voi VA-h12 cu — VI SAO BO VA-1/VA-2 GOC
===========================================================================
Goi cu co ba manh:
  VA-1 (main.py ~9823) them tap `_capped_models`      -> chi de nuoi VA-2
  VA-2 (main.py ~10506/10511) GHI 7 khoa moi vao
       final_bundles.source_predictions_json          -> VI PHAM ZERO_WRITE
  VA-3 (database.py classify_day_status) doc so cap    -> DUNG HUONG

Bang chung then chot: metadata can thiet DA CO SAN trong bundle hom nay —
`model_exclusion_reasons` da ghi `reason='max_voters_cap'` cho tung model bi tran
(do 06/09 va 08/09 tren DB that). Vay KHONG can VA-1/VA-2 de tao them du lieu;
chi can DOC cai da co.

=> Ban nay chi con HAI khoi, ca hai deu KHONG ghi final_bundles:

  VA-3' database.py `classify_day_status`
        - doc `model_exclusion_reasons` tu bundle DA TON TAI (SELECT, khong ghi)
        - effective = model_count + so model bi TRAN CO Y
        - phan loai theo `effective` => cap co y khong con bi tinh la thieu hut
        - GHI: CHI `day_governance` (dung bang no von da ghi)
        - `reason` duoc gan o MOI nhanh, ke ca nhanh COMPLETE (goi cu elide dong nay)

  VA-2' main.py `_quality_filtered_models_from_source_meta`
        - SUA O PHIA DOC: bo model co `reason='max_voters_cap'` ra khoi ket qua
        - khoa `wr_gate_filtered` trong DB VAN bi nhiem, nhung nguoi doc khong con
          thay chinh sach CO Y hien ra nhu "model truot cong CHAT LUONG"
        - 0 ghi DB
"""
import sys, io, os, re, json, sqlite3, hashlib, shutil, argparse, datetime

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

PHIEN_BAN = "V11174-VAh12-ZEROWRITE"
MARKER = "V11174"
GOC = "/root/Lottery_AI_Test"
BE = GOC + "/web/backend/"
TEP_DB = BE + "database.py"
TEP_MAIN = BE + "main.py"
DB = "file:" + GOC + "/data/lottery_ai.db?mode=ro"
SL_DB = BE + "database.py.pre_v11174"
SL_MAIN = BE + "main.py.pre_v11174"

# FAIL-CLOSED: chi ap len source DA NHAN DIEN (sha256 full, ban LF tren VPS)
PREIMAGE = {
    "database.py": "fd3d2349ab917c6f36ee8d0a2aa6b82841a963811ba716bc58090c3be566eb16",
    "main.py": "4ed5fd7ebaee8d232177df2e371ca7ad7fc57d829dde503c560ac511a83781cf",
}
# So marker du kien: TINH TU CHINH KHOI VA, khong doan bang tay.
# (Ba lan truoc agent doan sai hang so nay — day la cach dong het cua do.)
def _so_marker_du_kien():
    d = {}
    for _ten, _p, _tr, _sa, _n in KHOI:
        d[_ten] = d.get(_ten, 0) + _sa.count(MARKER) - _tr.count(MARKER)
    return d

# ==========================================================================
# KHOI VA 1/3 — helper doc model bi tran (database.py, chen TRUOC ham)
# ==========================================================================
A_TRUOC = """def classify_day_status(date_str: str, region: str, """

A_SAU = '''def _v11174_capped_models(cursor, date_str: str, region: str) -> list:
    """V11174 SC-12 · doc model bi TRAN CO Y tu bundle DA TON TAI. CHI DOC.

    Nguon: final_bundles.source_predictions_json -> model_exclusion_reasons[]
    voi reason == 'max_voters_cap' (tran top-13 cua MT, V10752, owner duyet 25/06).

    FINAL_BUNDLES_ZERO_WRITE: ham nay chi SELECT, khong bao gio ghi final_bundles.
    FAIL-SAFE: thieu bundle / JSON hong / khong co su kien => tra [] => hanh vi
    quay ve DUNG NHU TRUOC VA (khong bao giờ noi long nham).
    """
    try:
        cursor.execute(
            "SELECT source_predictions_json FROM final_bundles "
            "WHERE date=? AND region=? AND status='ACTIVE'",
            (date_str, (region or "").upper()),
        )
        row = cursor.fetchone()
        if not row:
            return []
        raw = row[0] if not hasattr(row, "keys") else row["source_predictions_json"]
        if not raw:
            return []
        meta = json.loads(raw)
        if not isinstance(meta, dict):
            return []
        events = meta.get("model_exclusion_reasons") or []
        if isinstance(events, dict):
            events = [{"model": m, "reason": r, "active": True} for m, r in events.items()]
        if not isinstance(events, list):
            return []
        out = set()
        for ev in events:
            if not isinstance(ev, dict) or ev.get("active") is False:
                continue
            if str(ev.get("reason") or "").strip().lower() != "max_voters_cap":
                continue
            m = ev.get("model")
            if m:
                out.add(str(m))
        return sorted(out)
    except Exception:
        return []


def classify_day_status(date_str: str, region: str, '''

# ==========================================================================
# KHOI VA 2/3 — tinh effective (database.py)
# ==========================================================================
B_TRUOC = """    expected = EXPECTED_MODEL_COUNT
    quality = classify_bundle_quality(model_count, expected)
    ratio = model_count / expected if expected > 0 else 0
    failed = max(0, expected - model_count)"""

B_SAU = """    # V11174 SC-12: TRAN CO Y KHONG PHAI THIEU HUT.
    # Doc model bi tran tu bundle DA TON TAI (chi SELECT — FINAL_BUNDLES_ZERO_WRITE).
    _v11174_capped = _v11174_capped_models(cursor, date_str, region)
    _v11174_eff = model_count + len(_v11174_capped)
    expected = EXPECTED_MODEL_COUNT
    quality = classify_bundle_quality(_v11174_eff, expected)
    ratio = _v11174_eff / expected if expected > 0 else 0
    failed = max(0, expected - _v11174_eff)"""

# ==========================================================================
# KHOI VA 3/3 — reason gan o MOI nhanh (database.py)
# ==========================================================================
C_TRUOC = """    if quality == 'COMPLETE':
        day_status = 'VALID_LIVE_DAY'
        eval_policy = 'INCLUDE'
        reason = None
    elif quality == 'INCOMPLETE':
        day_status = 'DEGRADED_LIVE_DAY'
        eval_policy = 'EXCLUDE_PRIMARY'
        reason = f'Thiếu {failed} model ({model_count}/{expected})'
    else:  # DEGRADED
        day_status = 'INVALID_FOR_PRIMARY_EVAL'
        eval_policy = 'EXCLUDE_ALL'
        reason = f'Nghiêm trọng: chỉ {model_count}/{expected} model ({ratio:.0%})'"""

C_SAU = """    # V11174: `reason` PHAI duoc gan o MOI nhanh truoc khi ghi degradation_reason.
    # (Goi VA-h12 cu elide dong nay => nhanh COMPLETE se de reason chua gan.)
    _v11174_ghi_cap = ('' if not _v11174_capped else
                       ' · %d model bi TRAN CO Y (V10752), KHONG tinh la thieu: %s'
                       % (len(_v11174_capped), ', '.join(_v11174_capped)))
    if quality == 'COMPLETE':
        day_status = 'VALID_LIVE_DAY'
        eval_policy = 'INCLUDE'
        reason = (None if not _v11174_capped else
                  'Đủ %d/%d model hợp lệ%s' % (_v11174_eff, expected, _v11174_ghi_cap))
    elif quality == 'INCOMPLETE':
        day_status = 'DEGRADED_LIVE_DAY'
        eval_policy = 'EXCLUDE_PRIMARY'
        reason = f'Thiếu {failed} model ({_v11174_eff}/{expected} hợp lệ){_v11174_ghi_cap}'
    else:  # DEGRADED
        day_status = 'INVALID_FOR_PRIMARY_EVAL'
        eval_policy = 'EXCLUDE_ALL'
        reason = (f'Nghiêm trọng: chỉ {_v11174_eff}/{expected} model '
                  f'({ratio:.0%}){_v11174_ghi_cap}')"""

# ==========================================================================
# KHOI VA main.py — SUA PHIA DOC, 0 ghi DB
# ==========================================================================
D_TRUOC = """def _quality_filtered_models_from_source_meta(source_meta: Dict[str, Any]) -> List[str]:
    filtered = set()
    for model in _json_list_or_empty(source_meta.get("wr_gate_filtered")):
        if model:
            filtered.add(str(model))"""

D_SAU = """def _quality_filtered_models_from_source_meta(source_meta: Dict[str, Any]) -> List[str]:
    # V11174 SC-12 · TAXONOMY: `wr_gate_filtered` trong DB dang BI NHIEM — main.py
    # ghi `sorted(filtered_models)` vao do, ma tap ay chua ca model bi TRAN CO Y
    # (max_voters_cap, V10752). Hau qua: mot chinh sach CO Y hien ra tren admin/UI
    # nhu "model truot cong CHAT LUONG".
    # Sua O PHIA DOC (FINAL_BUNDLES_ZERO_WRITE — khong ghi lai final_bundles):
    # loai truoc cac model co reason='max_voters_cap' roi moi gop.
    _v11174_capped = set()
    _v11174_ev = source_meta.get("model_exclusion_reasons") or []
    if isinstance(_v11174_ev, dict):
        _v11174_ev = [{"model": m, "reason": r, "active": True}
                      for m, r in _v11174_ev.items()]
    for _ev in _v11174_ev if isinstance(_v11174_ev, list) else []:
        if not isinstance(_ev, dict) or _ev.get("active") is False:
            continue
        if str(_ev.get("reason") or "").strip().lower() == "max_voters_cap":
            _m = _ev.get("model")
            if _m:
                _v11174_capped.add(str(_m))
    filtered = set()
    for model in _json_list_or_empty(source_meta.get("wr_gate_filtered")):
        if model and str(model) not in _v11174_capped:
            filtered.add(str(model))"""

KHOI = [
    ("database.py", TEP_DB, A_TRUOC, A_SAU, "VA-3a helper doc model bi tran"),
    ("database.py", TEP_DB, B_TRUOC, B_SAU, "VA-3b effective = voters + capped"),
    ("database.py", TEP_DB, C_TRUOC, C_SAU, "VA-3c reason gan o MOI nhanh"),
    ("main.py", TEP_MAIN, D_TRUOC, D_SAU, "VA-2' taxonomy phia DOC"),
]


def _doc(p):
    return io.open(p, encoding="utf-8", newline="").read()


def _sha(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def _sha_tep(p):
    return hashlib.sha256(io.open(p, "rb").read()).hexdigest()


def _ap_tep(p):
    s = _doc(p)
    if MARKER in s:
        return s, 0
    n = 0
    for _t, tep, tr, sa, _ten in KHOI:
        if tep != p:
            continue
        if s.count(tr) != 1:
            raise RuntimeError("preimage khop %d lan (phai 1): %s" % (s.count(tr), _ten))
        s = s.replace(tr, sa, 1)
        n += 1
    return s, n


# ==========================================================================
# TEST — goi HAM PRODUCTION THAT, khong copy logic sang helper
# ==========================================================================

def chay_test():
    dat = fail = 0

    def ok(t, c, g=""):
        nonlocal dat, fail
        if c:
            dat += 1; print("  DAT  %s  %s" % (t, g))
        else:
            fail += 1; print("  HONG %s  %s" % (t, g))

    ict = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=7)))
    print("=" * 76)
    print("TEST %s   ICT %s | UTC %s" % (PHIEN_BAN, ict.strftime("%F %T"),
          datetime.datetime.now(datetime.timezone.utc).strftime("%F %T")))
    print("=" * 76)

    print("\n=== A · FAIL-CLOSED: chi ap len source DA NHAN DIEN ===")
    src = {}
    for ten, p in (("database.py", TEP_DB), ("main.py", TEP_MAIN)):
        s = _doc(p); src[ten] = s
        h = _sha(s)
        ok("A-%s hash khop preimage" % ten, h == PREIMAGE[ten], h[:24] + "...")
        ok("A-%s chua tung ap va" % ten, MARKER not in s)
    for ten, tep, tr, _sa, nhan in KHOI:
        ok("A-preimage «%s» khop DUNG 1 lan" % nhan, src[ten].count(tr) == 1,
           "dem=%d" % src[ten].count(tr))
    ok("A KHONG co dau '...' trong bat ky khoi SAU nao",
       all("..." not in sa for _t, _p, _tr, sa, _n in KHOI))

    print("\n=== B · SAU KHI AP ===")
    out = {}
    for ten, p in (("database.py", TEP_DB), ("main.py", TEP_MAIN)):
        s2, n = _ap_tep(p); out[ten] = s2
        try:
            compile(s2, ten, "exec"); cp, loi = True, ""
        except SyntaxError as e:
            cp, loi = False, str(e)
        ok("B-%s AST hop le" % ten, cp, loi)
        ok("B-%s dai ra" % ten, len(s2) > len(src[ten]),
           "%d -> %d" % (len(src[ten]), len(s2)))
        _dk = _so_marker_du_kien()[ten]
        ok("B-%s marker dung so du kien" % ten, s2.count(MARKER) == _dk,
           "dem=%d du kien=%d" % (s2.count(MARKER), _dk))
        ok("B-%s ap lai lan hai KHONG doi" % ten, _ap_tep_str(s2) == s2)
    ok("B so khoi thay the = 4", sum(1 for k in KHOI) == 4)

    print("\n=== C · FINAL_BUNDLES_ZERO_WRITE ===")
    for ten in ("database.py", "main.py"):
        a, b = src[ten], out[ten]
        for tu in ("INSERT INTO final_bundles", "UPDATE final_bundles",
                   "DELETE FROM final_bundles", "REPLACE INTO final_bundles"):
            ok("C-%s KHONG them «%s»" % (ten, tu), a.count(tu) == b.count(tu),
               "%d -> %d" % (a.count(tu), b.count(tu)))
    _khoi_moi = "\n".join(sa for _t, _p, _tr, sa, _n in KHOI)
    ok("C khoi va KHONG chua lenh ghi final_bundles nao",
       not any(x in _khoi_moi for x in ("INSERT INTO final_bundles",
               "UPDATE final_bundles", "REPLACE INTO final_bundles",
               "DELETE FROM final_bundles")))
    ok("C khoi va chi SELECT tu final_bundles",
       _khoi_moi.count("SELECT source_predictions_json FROM final_bundles") == 1)

    print("\n=== D · VUNG CAM (forbidden-surface diff) ===")
    CAM = ("ranked_numbers", "_CANONICAL_OUTPUT_MODELS", "strength_weight",
           "run_combo_super", "SYSTEM_PROMPT", "output_counterfactual_rank",
           "lo3_status", "save_final_bundle", "bach_thu =")
    for ten in ("database.py", "main.py"):
        for tu in CAM:
            ok("D-%s «%s» khong doi" % (ten, tu),
               src[ten].count(tu) == out[ten].count(tu),
               "%d -> %d" % (src[ten].count(tu), out[ten].count(tu)))

    print("\n=== E · reason GAN O MOI NHANH ===")
    kh = C_SAU
    ok("E co 3 nhanh gan reason", kh.count("reason = ") + kh.count("reason = (") >= 3,
       "dem=%d" % (kh.count("reason =")))
    ok("E nhanh COMPLETE co gan reason", "reason = (None if not _v11174_capped" in kh)
    ok("E nhanh INCOMPLETE co gan reason", "reason = f'Thiếu" in kh)
    ok("E nhanh DEGRADED co gan reason", "reason = (f'Nghiêm trọng" in kh)

    print("\n=== F · GOI HAM PRODUCTION THAT tren DB that (CHI DOC) ===")
    try:
        import importlib.util as _iu
        tmp = GOC + "/artifacts/_v11174_db_patched.py"
        io.open(tmp, "w", encoding="utf-8", newline="").write(out["database.py"])
        c = sqlite3.connect(DB, uri=True); c.row_factory = sqlite3.Row
        cur = c.cursor()
        spec = _iu.spec_from_file_location("_v11174_dbp", tmp)
        mod = _iu.module_from_spec(spec)
        sys.path.insert(0, BE)
        spec.loader.exec_module(mod)
        f = getattr(mod, "_v11174_capped_models")
        r1 = f(cur, "2026-09-08", "MT")
        r2 = f(cur, "2026-09-08", "MN")
        r3 = f(cur, "2026-09-06", "MT")
        r4 = f(cur, "1999-01-01", "MT")
        r5 = f(cur, "2026-09-08", "KHONG_CO_MIEN")
        c.close()
        ok("F1 MT 08/09 tra dung 2 model bi tran", len(r1) == 2, str(r1))
        ok("F2 MN 08/09 KHONG co model bi tran", r1 != r2 and len(r2) == 0, str(r2))
        ok("F3 MT 06/09 cung co 2 model (doi theo ngay)", len(r3) == 2, str(r3))
        ok("F4 ngay khong ton tai => [] (fail-safe)", r4 == [], str(r4))
        ok("F5 mien khong ton tai => [] (fail-safe)", r5 == [], str(r5))
        ok("F6 hai ngay khac nhau cat model KHAC nhau", set(r1) != set(r3),
           "%s vs %s" % (r1, r3))
    except Exception as e:
        ok("F* goi ham production that", False, "%s: %s" % (type(e).__name__, e))

    print("\n=== G · TAC DONG PHAN LOAI tren du lieu THAT (chi doc, khong ghi) ===")
    try:
        c = sqlite3.connect(DB, uri=True); c.row_factory = sqlite3.Row
        doi = giu = 0
        chi_tiet = []
        for r in c.execute(
                "SELECT date, region, model_count, source_predictions_json "
                "FROM final_bundles WHERE status='ACTIVE' ORDER BY date DESC LIMIT 400"):
            try:
                meta = json.loads(r["source_predictions_json"] or "{}")
            except Exception:
                meta = {}
            ev = meta.get("model_exclusion_reasons") or []
            cap = {e.get("model") for e in ev if isinstance(e, dict)
                   and e.get("active") is not False
                   and str(e.get("reason") or "").lower() == "max_voters_cap" and e.get("model")}
            mc = r["model_count"] or 0
            if mc < 15 and (mc + len(cap)) >= 15:
                doi += 1
                if len(chi_tiet) < 5:
                    chi_tiet.append("%s %s: %d+%d=15" % (r["date"], r["region"], mc, len(cap)))
            else:
                giu += 1
        c.close()
        print("     doi phan loai: %d · giu nguyen: %d" % (doi, giu))
        for x in chi_tiet:
            print("       %s" % x)
        ok("G1 co ngay doi phan loai (va co tac dung)", doi > 0, "%d ngay" % doi)
        ok("G2 phan lon ngay KHONG doi (khong noi long bua)", giu > doi, "%d giu" % giu)
    except Exception as e:
        ok("G* tac dong", False, "%s: %s" % (type(e).__name__, e))

    print("\n" + "=" * 76)
    print("TONG: %d/%d DAT" % (dat, dat + fail))
    print("=" * 76)
    return fail == 0


def _ap_tep_str(s):
    if MARKER in s:
        return s
    for _t, _p, tr, sa, _n in KHOI:
        if s.count(tr) == 1:
            s = s.replace(tr, sa, 1)
    return s


# ==========================================================================
# CAI DAT / GO VE
# ==========================================================================

def cai_dat():
    for ten, p in (("database.py", TEP_DB), ("main.py", TEP_MAIN)):
        s = _doc(p)
        if MARKER in s:
            print("  ! %s DA AP VA — bo qua" % ten); continue
        if _sha(s) != PREIMAGE[ten]:
            print("  ! HUY (fail-closed): %s hash KHONG khop preimage" % ten)
            print("    hien tai:", _sha(s)); return 1
    for ten, p, sl in (("database.py", TEP_DB, SL_DB), ("main.py", TEP_MAIN, SL_MAIN)):
        s = _doc(p)
        if MARKER in s:
            continue
        s2, n = _ap_tep(p)
        _dk = _so_marker_du_kien()[ten]
        if s2.count(MARKER) != _dk:
            print("  ! HUY: %s marker=%d du kien=%d" % (ten, s2.count(MARKER), _dk)); return 1
        compile(s2, ten, "exec")
        shutil.copy2(p, sl)
        io.open(p, "w", encoding="utf-8", newline="").write(s2)
        print("  %s: %d khoi · %d -> %d byte" % (ten, n, len(s), len(s2)))
        print("     PRE :", _sha(s))
        print("     POST:", _sha_tep(p))
        print("     sao luu:", sl)
    return 0


def go_ve():
    rc = 0
    for ten, p, sl in (("main.py", TEP_MAIN, SL_MAIN), ("database.py", TEP_DB, SL_DB)):
        if not os.path.exists(sl):
            print("  ! khong co sao luu", sl); rc = 1; continue
        shutil.copy2(sl, p)
        h = _sha_tep(p)
        print("  %s go ve · sha256 %s · khop preimage: %s" % (ten, h[:24] + "...", h == PREIMAGE[ten]))
        if h != PREIMAGE[ten]:
            rc = 1
    return rc


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--test", action="store_true")
    ap.add_argument("--cai-dat", action="store_true")
    ap.add_argument("--rollback", action="store_true")
    ap.add_argument("--out", default=GOC + "/artifacts/v11174_vah12_kq.json")
    a = ap.parse_args()
    if a.rollback:
        return go_ve()
    if a.cai_dat:
        return cai_dat()
    ok = chay_test()
    try:
        io.open(a.out, "w", encoding="utf-8", newline="\n").write(json.dumps(
            {"phien_ban": PHIEN_BAN, "dat": ok,
             "ICT": datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=7))).isoformat(),
             "preimage": {k: _sha(_doc(v)) for k, v in
                          (("database.py", TEP_DB), ("main.py", TEP_MAIN))}},
            ensure_ascii=False, indent=1))
        print("GHI:", a.out)
    except Exception as e:
        print("khong ghi duoc artifact:", e)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
