# -*- coding: utf-8 -*-
"""V11188 §AC-E/§AC-F — GROUND TRUTH ngày mục tiêu: kết quả xổ + chấm lại official từ đầu.

CHỈ ĐỌC. Không ghi DB, không gọi provider, không sửa status lịch sử.

VÌ SAO TỰ TRÍCH, KHÔNG DÙNG CỘT CÓ SẴN (RL-042):
  `lottery_results` có sẵn `tail_db` và `tail_g8`, và `backtester.get_actual_tails` từng CỘNG
  hai cột đó vào tập đuôi **trong khi chúng đã nằm sẵn trong `prizes_json`** — đếm hai lần, nền
  ngẫu nhiên phồng lên và lift âm giả. Tệp này trích **chỉ từ `prizes_json`**, mỗi số một lần.

QUY ƯỚC ĐUÔI:
  · đuôi 2 chữ số = hai ký tự cuối của MỌI số giải, tính THEO TỪNG ĐÀI rồi hợp lại thành miền.
  · đuôi 3 chữ số = ba ký tự cuối của mọi số giải có >= 3 chữ số.
  · XIÊN phải cùng xuất hiện **tại cùng MỘT đài** — hợp miền rồi chấm là sai (§AC-F3).

Chạy TRÊN VPS:
    /root/Lottery_AI_Test/venv/bin/python3 _v11188_eod_ground_truth.py [--ngay=YYYY-MM-DD] [--json]
"""
from __future__ import annotations

import io
import json
import os
import sqlite3
import sys

sys.stdout.reconfigure(encoding="utf-8")
BE = os.path.dirname(os.path.abspath(__file__))
GOC = os.path.dirname(os.path.dirname(BE))
DB = os.path.join(GOC, "data", "lottery_ai.db")

NGAY = "2026-09-14"
for a in sys.argv[1:]:
    if a.startswith("--ngay="):
        NGAY = a.split("=", 1)[1]

# Số đài dự kiến theo miền — dùng để phát hiện THIẾU đài, không dùng để đoán tên đài.
DAI_DU_KIEN = {"MN": 3, "MT": 2, "MB": 1}


def _so_trong(v):
    """Duyệt mọi số trong một giá trị prizes_json (chuỗi hoặc danh sách)."""
    if v is None:
        return
    if isinstance(v, (list, tuple)):
        for x in v:
            for y in _so_trong(x):
                yield y
        return
    s = str(v).strip()
    if s and s.isdigit():
        yield s


def _duoi(s, n):
    return s[-n:] if len(s) >= n else None


cn = sqlite3.connect("file:%s?mode=ro" % DB.replace("\\", "/"), uri=True)
cn.row_factory = sqlite3.Row

# ============================================================ 1 · KẾT QUẢ XỔ
mien_data = {}
for r in cn.execute("SELECT id,region,station,prizes_json,tail_db,tail_g8,created_at "
                    "FROM lottery_results WHERE date=? ORDER BY region,id", (NGAY,)):
    mien = r["region"]
    d = mien_data.setdefault(mien, {"dai": [], "loi": []})
    try:
        pz = json.loads(r["prizes_json"])
    except Exception as e:
        d["loi"].append("id=%s station=%s prizes_json hong: %r" % (r["id"], r["station"], e))
        continue
    so = []
    for k, v in pz.items():
        for x in _so_trong(v):
            so.append((k, x))
    d2 = _duoi2 = set()
    d3 = set()
    for _k, x in so:
        t2 = _duoi(x, 2)
        if t2:
            d2.add(t2)
        t3 = _duoi(x, 3)
        if t3:
            d3.add(t3)
    d["dai"].append({
        "id": r["id"], "station": r["station"], "created_at": r["created_at"],
        "so_giai": len(so), "so_khoa": len(pz), "khoa": list(pz.keys()),
        "duoi2": sorted(d2), "duoi3": sorted(d3),
        "tail_db_cot": r["tail_db"], "tail_g8_cot": r["tail_g8"],
        "prizes_json_len": len(r["prizes_json"]),
    })

ket_qua = {}
for mien, d in mien_data.items():
    if not d["dai"]:
        ket_qua[mien] = {"terminal": "RESULT_CONFLICT_NEEDS_REPAIR", "ly_do": "khong co dong nao"}
        continue
    # trùng đài?
    ten = [x["station"] for x in d["dai"]]
    trung = sorted({t for t in ten if ten.count(t) > 1})
    # đủ đài?
    ky_vong = DAI_DU_KIEN.get(mien)
    thieu_dai = (ky_vong is not None and len(d["dai"]) < ky_vong)
    # đài rỗng?
    rong = [x["station"] for x in d["dai"] if x["so_giai"] == 0]
    # ĐB tail kiểm chéo: cột tail_db có khớp hai số cuối của Giải Đặc Biệt không?
    lech_db = []
    for x in d["dai"]:
        pass  # kiểm ở vòng dưới, cần prizes gốc

    hop_duoi2 = set()
    hop_duoi3 = set()
    for x in d["dai"]:
        hop_duoi2 |= set(x["duoi2"])
        hop_duoi3 |= set(x["duoi3"])

    if trung or rong or d["loi"]:
        term = "RESULT_CONFLICT_NEEDS_REPAIR"
    elif thieu_dai:
        term = "RESULT_PARTIAL_EXCLUDED"
    else:
        term = "RESULT_COMPLETE_VALID"

    ket_qua[mien] = {
        "terminal": term,
        "so_dai": len(d["dai"]), "so_dai_du_kien": ky_vong,
        "dai_trung_ten": trung, "dai_rong": rong, "loi_doc": d["loi"],
        "duoi2_mien": sorted(hop_duoi2), "so_duoi2_mien": len(hop_duoi2),
        "duoi3_mien": sorted(hop_duoi3), "so_duoi3_mien": len(hop_duoi3),
        "dai": d["dai"],
    }

# Kiểm chéo cột tail_db/tail_g8 với prizes_json — phát hiện dữ liệu tự mâu thuẫn.
for mien, r in cn.execute("SELECT region,id,station,prizes_json,tail_db,tail_g8 FROM lottery_results "
                          "WHERE date=? ORDER BY region,id", (NGAY,)) and []:
    pass
lech_cot = []
for r in cn.execute("SELECT region,id,station,prizes_json,tail_db,tail_g8 "
                    "FROM lottery_results WHERE date=? ORDER BY region,id", (NGAY,)):
    try:
        pz = json.loads(r["prizes_json"])
    except Exception:
        continue
    db_key = None
    for k in pz:
        if "Đặc Biệt" in k or "DB" == k.upper():
            db_key = k
            break
    db_so = None
    if db_key:
        for x in _so_trong(pz[db_key]):
            db_so = x
            break
    if db_so and r["tail_db"] and _duoi(db_so, 2) != str(r["tail_db"]).zfill(2):
        lech_cot.append({"id": r["id"], "region": r["region"], "station": r["station"],
                         "db_so": db_so, "tail_db_cot": r["tail_db"],
                         "duoi2_tinh_lai": _duoi(db_so, 2)})

# ============================================================ 2 · CHẤM LẠI OFFICIAL
def _ds(v):
    """lo2/lo3/xien2/xien3 lưu dạng chuỗi JSON hoặc chuỗi thường."""
    if v is None:
        return []
    s = str(v).strip()
    if not s:
        return []
    if s.startswith("["):
        try:
            return [str(x).strip() for x in json.loads(s) if str(x).strip()]
        except Exception:
            pass
    return [p.strip() for p in s.replace(",", " ").split() if p.strip()]


bundles = {}
for r in cn.execute("SELECT * FROM final_bundles WHERE date=? AND status='ACTIVE' "
                    "ORDER BY region", (NGAY,)):
    mien = r["region"]
    kq = ket_qua.get(mien)
    if not kq or kq["terminal"] == "RESULT_CONFLICT_NEEDS_REPAIR":
        bundles[mien] = {"terminal": "UNSCORABLE_MISSING_RESULT"}
        continue
    d2_mien = set(kq["duoi2_mien"])
    d3_mien = set(kq["duoi3_mien"])
    d2_theo_dai = {x["station"]: set(x["duoi2"]) for x in kq["dai"]}

    bt = str(r["bach_thu"]).strip() if r["bach_thu"] is not None else ""
    bt_win = bool(bt) and bt in d2_mien

    lo2 = _ds(r["lo2"])
    lo2_hit = [x for x in lo2 if x in d2_mien]
    if not lo2:
        lo2_st = "KHONG_CO"
    elif len(lo2_hit) == len(lo2):
        lo2_st = "WIN"
    elif lo2_hit:
        lo2_st = "PARTIAL"
    else:
        lo2_st = "LOSE"

    lo3 = _ds(r["lo3"])
    lo3_hit = [x for x in lo3 if x in d3_mien]
    lo3_st = ("KHONG_CO" if not lo3 else
              "WIN" if len(lo3_hit) == len(lo3) else
              "PARTIAL" if lo3_hit else "LOSE")

    def cham_xien(ds):
        """XIÊN: mọi số phải cùng về tại CÙNG MỘT đài (§AC-F3)."""
        if not ds:
            return "KHONG_CO", None, []
        dai_trung = [dai for dai, tap in d2_theo_dai.items() if all(x in tap for x in ds)]
        if dai_trung:
            return "WIN", dai_trung, ds
        # số nào về ở đâu — để thấy rõ bẫy "gộp miền thành WIN"
        o_dau = {x: sorted([dai for dai, tap in d2_theo_dai.items() if x in tap]) for x in ds}
        ve_du_nhung_khac_dai = all(o_dau[x] for x in ds)
        return ("LOSE_KHAC_DAI" if ve_du_nhung_khac_dai else "LOSE"), None, o_dau

    x2 = _ds(r["xien2"])
    x3 = _ds(r["xien3"])
    x2_st, x2_dai, x2_ct = cham_xien(x2)
    x3_st, x3_dai, x3_ct = cham_xien(x3)

    bundles[mien] = {
        "row_id": r["id"], "bundle_version": r["bundle_version"],
        "created_at": r["created_at"], "verified_at": r["verified_at"],
        "policy_version_ref": r["policy_version_ref"],
        "generation_method": r["generation_method"],
        "consensus_level": r["consensus_level"], "model_count": r["model_count"],
        "top_score": r["top_score"], "is_fallback": r["is_fallback"], "notes": r["notes"],
        "bach_thu": bt, "bt_tinh_lai": "WIN" if bt_win else "LOSE",
        "bt_luu": r["bach_thu_status"],
        "lo2": lo2, "lo2_hit": lo2_hit, "lo2_tinh_lai": lo2_st, "lo2_luu": r["lo2_status"],
        "lo3": lo3, "lo3_hit": lo3_hit, "lo3_tinh_lai": lo3_st, "lo3_luu": r["lo3_status"],
        "xien2": x2, "xien2_tinh_lai": x2_st, "xien2_dai": x2_dai, "xien2_chi_tiet": x2_ct,
        "xien2_luu": r["xien2_status"],
        "xien3": x3, "xien3_tinh_lai": x3_st, "xien3_dai": x3_dai, "xien3_chi_tiet": x3_ct,
        "xien3_luu": r["xien3_status"],
    }

# ============================================================ 3 · LỆCH stored vs tính lại
def _chuan(v):
    if v is None:
        return "NULL"
    s = str(v).strip().upper()
    return s if s else "RONG"


lech_cham = []
for mien, b in bundles.items():
    if b.get("terminal") == "UNSCORABLE_MISSING_RESULT":
        continue
    for truong in ("bt", "lo2", "lo3", "xien2", "xien3"):
        luu = _chuan(b.get(truong + "_luu"))
        moi = _chuan(b.get(truong + "_tinh_lai"))
        if luu in ("NULL", "RONG"):
            lech_cham.append({"mien": mien, "truong": truong, "luu": luu, "tinh_lai": moi,
                              "loai": "CHUA_CHAM"})
        elif luu != moi and not (luu.startswith("LOSE") and moi.startswith("LOSE")):
            lech_cham.append({"mien": mien, "truong": truong, "luu": luu, "tinh_lai": moi,
                              "loai": "LECH"})

cn.close()

ra = {"ngay": NGAY, "ket_qua_xo": ket_qua, "lech_cot_tail_db": lech_cot,
      "official": bundles, "lech_cham": lech_cham}

if "--json" in sys.argv:
    print(json.dumps(ra, ensure_ascii=False, indent=1))
    sys.exit(0)

# ============================================================ IN
print("=" * 104)
print("  §AC-E · KET QUA XO NGAY %s" % NGAY)
print("=" * 104)
for mien in ("MN", "MT", "MB"):
    k = ket_qua.get(mien)
    if not k:
        print("  %s  KHONG CO DU LIEU  -> UNSCORABLE_MISSING_RESULT" % mien)
        continue
    print("  %s  %s  · %s/%s dai · %d duoi2 · %d duoi3"
          % (mien, k["terminal"], k["so_dai"], k["so_dai_du_kien"],
             k["so_duoi2_mien"], k["so_duoi3_mien"]))
    for x in k["dai"]:
        print("       %-16s id=%-6s %d so · DB-tail(cot)=%s G8/G7(cot)=%s"
              % (x["station"], x["id"], x["so_giai"], x["tail_db_cot"], x["tail_g8_cot"]))
    if k["dai_trung_ten"]:
        print("       !! DAI TRUNG TEN: %s" % k["dai_trung_ten"])
    if k["dai_rong"]:
        print("       !! DAI RONG: %s" % k["dai_rong"])
    print("       duoi2: %s" % " ".join(k["duoi2_mien"]))
print("-" * 104)
print("  kiem cheo cot tail_db vs prizes_json: %s"
      % ("KHOP tat ca" if not lech_cot else "LECH %d dong: %s" % (len(lech_cot), lech_cot)))

print()
print("=" * 104)
print("  §AC-F · CHAM LAI OFFICIAL TU GROUND TRUTH")
print("=" * 104)
print("  %-4s %-6s %-9s %-22s %-9s %-16s %-9s" %
      ("mien", "BT", "BT-stat", "lo2", "lo2-stat", "lo3", "lo3-stat"))
for mien in ("MN", "MT", "MB"):
    b = bundles.get(mien)
    if not b:
        print("  %-4s (khong co bundle ACTIVE)" % mien)
        continue
    if b.get("terminal"):
        print("  %-4s %s" % (mien, b["terminal"]))
        continue
    print("  %-4s %-6s %-9s %-22s %-9s %-16s %-9s"
          % (mien, b["bach_thu"], b["bt_tinh_lai"], ",".join(b["lo2"]), b["lo2_tinh_lai"],
             ",".join(b["lo3"]), b["lo3_tinh_lai"]))
print()
for mien in ("MN", "MT", "MB"):
    b = bundles.get(mien)
    if not b or b.get("terminal"):
        continue
    print("  --- %s  row=%s  ver=%s  tao=%s  verified=%s" %
          (mien, b["row_id"], b["bundle_version"], b["created_at"], b["verified_at"]))
    print("      policy=%s  method=%s  consensus=%s  model_count=%s  top_score=%s  fallback=%s"
          % (b["policy_version_ref"], b["generation_method"], b["consensus_level"],
             b["model_count"], b["top_score"], b["is_fallback"]))
    print("      BT   %-5s tinh_lai=%-5s  luu=%s" % (b["bach_thu"], b["bt_tinh_lai"], b["bt_luu"]))
    print("      lo2  %-20s hit=%-12s tinh_lai=%-8s luu=%s"
          % (",".join(b["lo2"]), ",".join(b["lo2_hit"]), b["lo2_tinh_lai"], b["lo2_luu"]))
    print("      lo3  %-20s hit=%-12s tinh_lai=%-8s luu=%s"
          % (",".join(b["lo3"]), ",".join(b["lo3_hit"]), b["lo3_tinh_lai"], b["lo3_luu"]))
    print("      xien2 %-18s tinh_lai=%-14s dai=%s" % (",".join(b["xien2"]), b["xien2_tinh_lai"], b["xien2_dai"]))
    if b["xien2_tinh_lai"].startswith("LOSE") and isinstance(b["xien2_chi_tiet"], dict):
        print("            chi tiet (so -> dai ve): %s" % b["xien2_chi_tiet"])
    print("      xien3 %-18s tinh_lai=%-14s dai=%s" % (",".join(b["xien3"]), b["xien3_tinh_lai"], b["xien3_dai"]))
    if b["xien3_tinh_lai"].startswith("LOSE") and isinstance(b["xien3_chi_tiet"], dict):
        print("            chi tiet (so -> dai ve): %s" % b["xien3_chi_tiet"])

print("-" * 104)
if lech_cham:
    print("  !! LECH giua status DA LUU va status TINH LAI — %d truong:" % len(lech_cham))
    for x in lech_cham:
        print("     %s.%s  luu=%s  tinh_lai=%s  (%s)" % (x["mien"], x["truong"], x["luu"],
                                                         x["tinh_lai"], x["loai"]))
    print("  => xet LIVE_SCORING_DEFECT neu loai=LECH (loai=CHUA_CHAM chi la chua verify)")
else:
    print("  stored status vs tinh lai: KHOP toan bo")
print("=" * 104)
