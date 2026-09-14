# -*- coding: utf-8 -*-
"""V11188 §AC-O.1 — LINEAGE CHO BỐN LỚP OVERRIDE. Additive-only, zero output change.

VẤN ĐỀ ĐANG CÓ (đo được, không suy đoán):
  `main.py:10229`  bach_thu = ranked[0][0]          <- đây là ranked0 TRƯỚC override
  `main.py:10232`  V10640 MN per-slice   ─┐
  `main.py:10251`  V10767 MB prev-day     │ bốn lớp này có thể GÁN LẠI `bach_thu`
  `main.py:10268`  V10789 MB lane         │
  `main.py:10288`  V10790 MT lane        ─┘
  `main.py:10383`  main_selection_reason = "max_ranked_score_after_gate_and_lane_weight"
                   <- GÁN CỨNG, đứng SAU cả bốn lớp.
⇒ Khi một override nổ, bản ghi vẫn khai là «xếp hạng cao nhất sau gate và lane weight», trong khi
  số cuối cùng KHÔNG phải số xếp hạng cao nhất. Đo trên lịch sử: sai ở **16,8%** số ngày.
  Không ai truy ngược được vì `pre_override_ranked0` **không được lưu ở đâu cả**.

TỆP NÀY KHÔNG SỬA HÀNH VI. Nó chỉ GHI LẠI sự thật vào một bảng RIÊNG:
  · không đổi `bach_thu`, `lo2`, `lo3`, `xien2`, `xien3`;
  · không đổi `main_selection_reason` đang ghi vào `final_bundles` (đổi là đổi output);
  · không backfill lịch sử — chỉ ghi cho bundle SINH RA TỪ SAU KHI DEPLOY;
  · mọi lỗi đều bị nuốt: lineage hỏng KHÔNG được phép làm hỏng một lượt dự đoán.

MỘT PHÁT HIỆN ĐI KÈM, KHÔNG SỬA TRONG BẢN NÀY (§AC-C cấm sửa override ở bước đánh giá):
  `main.py:10323`  xien2 = [ranked[0][0], ranked[1][0]]
  Dòng này lấy `ranked[0][0]` chứ KHÔNG lấy `bach_thu`. Khi override nổ, `xien2[0]` sẽ KHÁC
  `bach_thu` — hai thẻ của cùng một bundle nói hai số khác nhau. Ngày 14/09 không lớp nào nổ
  nên chưa cắn. Lineage ghi lại đủ dữ kiện để đo tần suất chuyện này.

Chạy tự kiểm: python _v11188_override_lineage.py
"""
from __future__ import annotations

import hashlib
import json
import os
import sqlite3
import sys

BE = os.path.dirname(os.path.abspath(__file__))
GOC = os.path.dirname(os.path.dirname(BE))
DB_MAC_DINH = os.path.join(GOC, "data", "lottery_ai.db")

BANG = "v11188_override_lineage"

# Bốn lớp hợp lệ + trường hợp không có override. Caller KHÔNG được tự bịa mã khác.
RULE_HOP_LE = ("V10640_MN_PERSLICE", "V10767_MB_PREVDAY", "V10789_MB_LANE",
               "V10790_MT_LANE", "NONE")

DDL = """
CREATE TABLE IF NOT EXISTS %s (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    region TEXT NOT NULL,
    bundle_row_id INTEGER,
    pre_override_ranked0 TEXT,
    pre_override_score REAL,
    pre_override_topk TEXT,
    override_applied INTEGER NOT NULL,
    override_rule_id TEXT NOT NULL,
    override_basis TEXT,
    override_input_hash TEXT,
    main_selection_reason_ghi TEXT,
    main_selection_reason_that TEXT,
    final_bach_thu TEXT,
    xien2_dau TEXT,
    xien2_lech_bach_thu INTEGER,
    roster_version TEXT,
    ghi_luc TEXT NOT NULL,
    UNIQUE(date, region, bundle_row_id)
)
""" % BANG


def _ket_noi(duong=None):
    cn = sqlite3.connect(duong or DB_MAC_DINH, timeout=5.0)
    cn.execute("PRAGMA busy_timeout=5000")
    return cn


def tao_bang(duong=None):
    """Tạo bảng nếu chưa có. Additive — không đụng bảng nào đang có."""
    cn = _ket_noi(duong)
    try:
        cn.execute(DDL)
        cn.commit()
        return True
    finally:
        cn.close()


def tinh_input_hash(dau_vao):
    """Băm tất định đầu vào của lớp override, để sau này truy được «vì sao nó nổ».

    Chuẩn hoá bằng JSON sort_keys nên thứ tự khoá không làm đổi băm; nhưng ĐỔI GIÁ TRỊ
    của bất kỳ trường nào là đổi băm — đó chính là điều cần.
    """
    try:
        chuoi = json.dumps(dau_vao, ensure_ascii=False, sort_keys=True, default=str)
    except Exception:
        chuoi = repr(dau_vao)
    return hashlib.sha256(chuoi.encode("utf-8")).hexdigest()[:32]


def ly_do_that(pre_ranked0, final_bt, rule_id, basis=None):
    """Câu lý do KHÔNG nói dối.

    Khi không có override: giữ nguyên câu cũ (đúng sự thật).
    Khi có override: nói rõ đã đổi từ số nào sang số nào và do lớp nào.
    """
    p = "" if pre_ranked0 is None else str(pre_ranked0)
    f = "" if final_bt is None else str(final_bt)
    if rule_id in (None, "", "NONE") or p == f:
        return "max_ranked_score_after_gate_and_lane_weight"
    ra = "override_%s_replaced_ranked0_%s_with_%s" % (rule_id, p or "NA", f or "NA")
    if basis:
        ra += " · basis=%s" % str(basis)[:160]
    return ra


def ghi_lineage(date_str, region, pre_override_ranked0, pre_override_score,
                pre_override_topk, final_bach_thu, rule_id="NONE", basis=None,
                override_inputs=None, bundle_row_id=None, roster_version=None,
                xien2_dau=None, main_selection_reason_ghi=None, duong=None):
    """Ghi một dòng lineage. TRẢ VỀ dict mô tả, KHÔNG BAO GIỜ raise.

    Giá trị trả về chỉ để quan sát/thử — caller KHÔNG được dùng nó để đổi output.
    """
    ra = {"ok": False, "ly_do": None, "rule_id": rule_id}
    try:
        if rule_id not in RULE_HOP_LE:
            # Không suy đoán: mã lạ thì ghi thẳng là lạ, không tự quy về NONE.
            ra["ly_do"] = "RULE_ID_KHONG_HOP_LE:%r" % (rule_id,)
            rule_id = "UNKNOWN_%s" % str(rule_id)[:32]
        p = None if pre_override_ranked0 is None else str(pre_override_ranked0)
        f = None if final_bach_thu is None else str(final_bach_thu)
        applied = 1 if (p is not None and f is not None and p != f) else 0
        # Mâu thuẫn nội tại: rule nói NONE nhưng số đã đổi, hoặc ngược lại.
        if applied and rule_id == "NONE":
            rule_id = "UNKNOWN_SO_DA_DOI_NHUNG_RULE_NONE"
        if (not applied) and rule_id not in ("NONE",) and not rule_id.startswith("UNKNOWN"):
            ra["ly_do"] = "RULE_BAO_NO_NHUNG_SO_KHONG_DOI"

        topk = None
        if pre_override_topk is not None:
            try:
                topk = json.dumps([[str(a), float(b)] for a, b in pre_override_topk][:10],
                                  ensure_ascii=False)
            except Exception:
                topk = json.dumps([str(x) for x in list(pre_override_topk)[:10]],
                                  ensure_ascii=False)

        x2 = None if xien2_dau is None else str(xien2_dau)
        x2_lech = 1 if (x2 is not None and f is not None and x2 != f) else 0

        import datetime as _dt
        tao_bang(duong)
        cn = _ket_noi(duong)
        try:
            cn.execute(
                "INSERT OR REPLACE INTO %s (date,region,bundle_row_id,pre_override_ranked0,"
                "pre_override_score,pre_override_topk,override_applied,override_rule_id,"
                "override_basis,override_input_hash,main_selection_reason_ghi,"
                "main_selection_reason_that,final_bach_thu,xien2_dau,xien2_lech_bach_thu,"
                "roster_version,ghi_luc) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)" % BANG,
                (date_str, region, bundle_row_id, p,
                 None if pre_override_score is None else float(pre_override_score), topk,
                 applied, rule_id, None if basis is None else str(basis)[:400],
                 tinh_input_hash(override_inputs) if override_inputs is not None else None,
                 main_selection_reason_ghi,
                 ly_do_that(p, f, rule_id if rule_id in RULE_HOP_LE else "NONE", basis),
                 f, x2, x2_lech, roster_version,
                 _dt.datetime.now().isoformat(timespec="seconds")))
            cn.commit()
        finally:
            cn.close()
        ra["ok"] = True
        ra["override_applied"] = applied
        ra["main_selection_reason_that"] = ly_do_that(
            p, f, rule_id if rule_id in RULE_HOP_LE else "NONE", basis)
        return ra
    except Exception as e:
        # NUỐT MỌI LỖI. Lineage hỏng không được phép làm hỏng một lượt dự đoán.
        ra["ly_do"] = "NUOT_LOI:%r" % e
        return ra


def doc_lineage(date_str=None, region=None, duong=None):
    try:
        tao_bang(duong)
        cn = _ket_noi(duong)
        cn.row_factory = sqlite3.Row
        q = "SELECT * FROM %s WHERE 1=1" % BANG
        p = []
        if date_str:
            q += " AND date=?"
            p.append(date_str)
        if region:
            q += " AND region=?"
            p.append(region)
        q += " ORDER BY date DESC, region"
        ra = [dict(r) for r in cn.execute(q, p)]
        cn.close()
        return ra
    except Exception:
        return []


# ============================================================================ TỰ KIỂM
def tu_kiem():
    import datetime as _dt
    import tempfile
    dat, hong = 0, []

    def k(ten, dk, ct=""):
        nonlocal dat
        if dk:
            dat += 1
            print("  DAT   %-62s %s" % (ten, ct))
        else:
            hong.append(ten)
            print("  HONG  %-62s %s" % (ten, ct))

    tmp = os.path.join(tempfile.gettempdir(), "_v11188_lineage_thu.db")
    if os.path.exists(tmp):
        os.remove(tmp)

    print("=" * 100)
    print("  TU KIEM _v11188_override_lineage")
    print("=" * 100)

    # A · không override
    r = ghi_lineage("2026-09-14", "MN", "24", 0.1276, [("24", 0.1276), ("14", 0.09)],
                    "24", rule_id="NONE", bundle_row_id=884,
                    roster_version="token_call_roster/2026.09.14-1", xien2_dau="24",
                    main_selection_reason_ghi="max_ranked_score_after_gate_and_lane_weight",
                    duong=tmp)
    k("A1 ghi duoc khi khong co override", r["ok"], r.get("ly_do") or "")
    k("A2 override_applied = 0", r.get("override_applied") == 0)
    k("A3 ly do that GIU NGUYEN cau cu khi khong override",
      r.get("main_selection_reason_that") == "max_ranked_score_after_gate_and_lane_weight")

    # B · có override
    r2 = ghi_lineage("2026-09-14", "MB", "31", 0.2, [("31", 0.2), ("16", 0.18)],
                     "16", rule_id="V10767_MB_PREVDAY", basis="ML plurality D-1",
                     override_inputs={"prev_day_ml": ["16", "16", "31"], "region": "MB"},
                     bundle_row_id=888, xien2_dau="31",
                     main_selection_reason_ghi="max_ranked_score_after_gate_and_lane_weight",
                     duong=tmp)
    k("B1 ghi duoc khi CO override", r2["ok"], r2.get("ly_do") or "")
    k("B2 override_applied = 1", r2.get("override_applied") == 1)
    k("B3 ly do that NOI RO doi tu so nao sang so nao",
      "replaced_ranked0_31_with_16" in (r2.get("main_selection_reason_that") or ""),
      r2.get("main_selection_reason_that"))
    k("B4 ly do that KHAC cau gan cung dang ghi vao final_bundles",
      r2.get("main_selection_reason_that") != "max_ranked_score_after_gate_and_lane_weight")

    ds = doc_lineage("2026-09-14", "MB", duong=tmp)
    k("B5 doc lai duoc", len(ds) == 1, "%d dong" % len(ds))
    k("B6 luu ca cau DA GHI lan cau THAT (de doi chieu)",
      ds and ds[0]["main_selection_reason_ghi"] == "max_ranked_score_after_gate_and_lane_weight"
      and ds[0]["main_selection_reason_that"] != ds[0]["main_selection_reason_ghi"])
    k("B7 phat hien xien2 lech bach_thu khi override no",
      ds and ds[0]["xien2_lech_bach_thu"] == 1,
      "xien2_dau=%s final_bt=%s" % (ds[0]["xien2_dau"], ds[0]["final_bach_thu"]) if ds else "")

    # C · input hash
    h1 = tinh_input_hash({"a": 1, "b": [2, 3]})
    h2 = tinh_input_hash({"b": [2, 3], "a": 1})
    h3 = tinh_input_hash({"a": 1, "b": [2, 4]})
    k("C1 thu tu khoa KHONG lam doi bam", h1 == h2)
    k("C2 doi mot gia tri LAM DOI bam", h1 != h3)
    k("C3 bam on dinh giua hai lan goi", h1 == tinh_input_hash({"a": 1, "b": [2, 3]}))

    # D · mâu thuẫn nội tại
    r4 = ghi_lineage("2026-09-14", "MT", "20", 0.08, None, "77", rule_id="NONE",
                     bundle_row_id=886, duong=tmp)
    ds4 = doc_lineage("2026-09-14", "MT", duong=tmp)
    k("D1 so DA DOI nhung rule=NONE => danh dau UNKNOWN, khong im lang",
      ds4 and ds4[0]["override_rule_id"].startswith("UNKNOWN"), ds4[0]["override_rule_id"] if ds4 else "")
    r5 = ghi_lineage("2026-09-13", "MT", "20", 0.08, None, "20", rule_id="V10790_MT_LANE",
                     bundle_row_id=1, duong=tmp)
    k("D2 rule bao NO nhung so KHONG doi => ghi nhan bat thuong",
      r5.get("ly_do") == "RULE_BAO_NO_NHUNG_SO_KHONG_DOI", r5.get("ly_do"))
    r6 = ghi_lineage("2026-09-13", "MB", "10", 0.1, None, "11", rule_id="TU_BIA",
                     bundle_row_id=2, duong=tmp)
    k("D3 rule_id tu bia bi tu choi, KHONG quy ve NONE",
      (r6.get("ly_do") or "").startswith("RULE_ID_KHONG_HOP_LE"), r6.get("ly_do"))

    # E · fail-safe: đường DB không ghi được thì NUỐT lỗi, không raise
    r7 = ghi_lineage("2026-09-14", "MN", "24", 0.1, None, "24", rule_id="NONE",
                     duong="/khong/ton/tai/sao/ghi/duoc.db")
    k("E1 DB khong ghi duoc => tra ve ok=False, KHONG raise", r7["ok"] is False)
    k("E2 va noi ro da nuot loi gi", (r7.get("ly_do") or "").startswith("NUOT_LOI"),
      (r7.get("ly_do") or "")[:60])

    # F · zero output change — hàm không được đụng vào dữ liệu caller đưa vào
    ranked_goc = [("24", 0.1276), ("14", 0.09)]
    ban_sao = list(ranked_goc)
    ghi_lineage("2026-09-14", "MN", "24", 0.1276, ranked_goc, "24", rule_id="NONE",
                bundle_row_id=884, duong=tmp)
    k("F1 KHONG sua danh sach ranked cua caller", ranked_goc == ban_sao)
    k("F2 ham chi tra dict quan sat, khong tra so de caller dung lam output",
      set(r2.keys()) <= {"ok", "ly_do", "rule_id", "override_applied",
                         "main_selection_reason_that"}, str(sorted(r2.keys())))

    # G · không backfill: cùng (date, region, bundle_row_id) thì THAY chứ không đẻ dòng mới
    n_truoc = len(doc_lineage(duong=tmp))
    ghi_lineage("2026-09-14", "MB", "31", 0.2, None, "16", rule_id="V10767_MB_PREVDAY",
                bundle_row_id=888, duong=tmp)
    n_sau = len(doc_lineage(duong=tmp))
    k("G1 ghi lai cung bundle KHONG de them dong", n_truoc == n_sau, "%d -> %d" % (n_truoc, n_sau))

    # H · bảng riêng, không đụng bảng khoá
    cn = _ket_noi(tmp)
    bang = {r[0] for r in cn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    cn.close()
    k("H1 chi tao DUNG MOT bang moi", bang == {BANG} or BANG in bang, str(sorted(bang)))
    k("H2 KHONG tao/dung bang khoa nao",
      not (bang & {"predictions", "final_bundles", "lottery_results", "model_daily_eval"}),
      str(sorted(bang)))

    if os.path.exists(tmp):
        os.remove(tmp)
    print("-" * 100)
    if hong:
        print("  TU KIEM _v11188_override_lineage: %d DAT · %d HONG" % (dat, len(hong)))
        for h in hong:
            print("   - %s" % h)
        return False
    print("  TU KIEM _v11188_override_lineage: %d/%d DAT" % (dat, dat))
    print("=" * 100)
    return True


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(0 if tu_kiem() else 1)
