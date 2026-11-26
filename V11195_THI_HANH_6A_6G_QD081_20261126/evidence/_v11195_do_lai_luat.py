# -*- coding: utf-8 -*-
"""V11195 — ĐO LẠI luật soi cầu trên nhãn đo tiến ĐÃ SỬA (FU-340 · FU-338 · FU-456). CHỈ ĐỌC.

Owner 26/11/2026 ~10:10: *«6e --> theo khuyến nghị»*. Khuyến nghị V11193: «cho em sửa nhãn rồi đo lại.
Trong lúc chờ, coi là không đạt.»

NHÃN: `_v11025_khoa_luat_ben.tinh_giai_doan()` — dòng (luật, ngày D) là ĐO TIẾN khi luật ĐANG HOẠT ĐỘNG
ở D (có mặt ở lần đào gần nhất ≤ D). Đã qua cổng `_v11195_kiem_nhan_luat.py` (RM-15).

HAI PHÉP (thay PHẦN 4 của `_v11030` và M4 của `_v11028`, giữ đúng thước của chúng):
  P4'  hit_any của bộ k đuôi so với NỀN ĐÚNG `1 − (1−b)^k` (RM-18), b = số đuôi khác nhau về hôm đó /100.
  M4'  McNemar luật THẬT vs luật GIẢ tất định (`sha256(rule_key|date|i)`, cùng k đuôi) trên cùng ngày.
Cả hai tách ĐO TIẾN / TRONG CỬA SỔ CHỌN và báo CẢ HAI (PRJ-SELECTION-WINDOW-001 mục 3). Phép lọc 1–2
của luật cửa sổ chọn: MRE không có `run_source`; thời điểm ghi không quyết định đo tiến (chấm bù ngày
luật đang chạy ra đúng kết quả) — điều quyết định là luật được CHỌN trước ngày đó, chính là nhãn.

PHƯƠNG SAI (RM-21): nhiều luật cùng chấm một ngày-miền nên không độc lập. Không mượn VIF 2,92 của thước
khác — tính z theo CỤM ngày-miền: z = Σ(trúng − nền) / sqrt(Σ_cụm (Σ trong cụm (trúng − nền))²),
và in VIF đo được = phương sai cụm / phương sai nhị thức. M4' cũng vậy: z = (b−c) / sqrt(Σ_cụm (b_d − c_d)²).

NGƯỠNG — KHAI TRƯỚC KHI CHẠY (RM-03), không đổi sau khi thấy số:
  P4'  mỗi miền, phần ĐO TIẾN: n ≥ 100 thì đọc — z ≥ +1,96 «CÓ TÍN HIỆU» · z ≤ −1,96 «KÉM NỀN» ·
       còn lại «KHÔNG CÓ TÍN HIỆU»; n < 100 «CHƯA ĐƯỢC PHÉP KẾT LUẬN» (RM-04).
  M4'  mỗi miền, phần ĐO TIẾN: cặp lệch ≥ 25 thì đọc — z ≥ +1,96 «THẬT HƠN GIẢ» · z ≤ −1,96 «GIẢ HƠN» ·
       còn lại «NGANG NHAU»; < 25 cặp lệch «CHƯA ĐỦ MẪU».
Cửa sổ: 30 / 60 / 90 ngày gần nhất và toàn bộ (từ 07/08) — cấm chọn cửa sổ đẹp (RM-18).

    cd /root/Lottery_AI_Test/web/backend && venv/bin/python3 _v11195_do_lai_luat.py   (TRÊN VPS)
"""
from __future__ import annotations

import hashlib
import json
import math
import os
import sqlite3
import sys
from collections import defaultdict
from datetime import date, timedelta

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
GOC = os.path.abspath(os.path.join(HERE, "..", ".."))
DB = "file:" + os.path.join(GOC, "data", "lottery_ai.db") + "?mode=ro"
TU_NGAY = "2026-08-07"            # V11025 dựng khoá bền — trước đó chưa có nhãn đo tiến nào
MIEN = ("MN", "MT", "MB")
N_TOI_THIEU_P4 = 100
CAP_LECH_TOI_THIEU_M4 = 25
Z = 1.96
CUA_SO = (30, 60, 90, None)

import _v11025_khoa_luat_ben as K  # noqa: E402


def duoi_gia(rule_key: str, ngay: str, so_duoi: int) -> list[str]:
    """Chép NGUYÊN VĂN `_v11028_m4_doi_chung.duoi_gia` — luật giả tất định, không nhìn dữ liệu."""
    ra, i = [], 0
    while len(ra) < so_duoi and i < 400:
        h = hashlib.sha256(f"{rule_key}|{ngay}|{i}".encode()).hexdigest()
        d = f"{int(h[:8], 16) % 100:02d}"
        if d not in ra:
            ra.append(d)
        i += 1
    return ra


def _duoi_ket_qua(con) -> dict:
    ra = defaultdict(set)
    for d, mien, pj in con.execute("SELECT date, region, prizes_json FROM lottery_results WHERE date >= ?",
                                   (TU_NGAY,)):
        try:
            v = json.loads(pj or "{}")
        except Exception:
            continue

        def w(x):
            if isinstance(x, dict):
                [w(i) for i in x.values()]
            elif isinstance(x, list):
                [w(i) for i in x]
            else:
                s = str(x or "").strip()
                if len(s) >= 2 and s[-2:].isdigit():
                    ra[(d, mien)].add(s[-2:])
        w(v)
    return ra


def _z_cum(dong: list[tuple]) -> dict:
    """dong = [(cụm, trúng 0/1, nền p)] ⇒ n, tỉ lệ, nền, chênh, z theo cụm, VIF đo được."""
    n = len(dong)
    if not n:
        return {"n": 0}
    cum = defaultdict(float)
    var_nn = 0.0
    for c, h, p in dong:
        cum[c] += h - p
        var_nn += p * (1 - p)
    tong = sum(cum.values())
    var_cum = sum(v * v for v in cum.values())
    return {"n": n, "so_cum": len(cum), "ti_le": sum(h for _, h, _ in dong) / n,
            "nen": sum(p for _, _, p in dong) / n, "chenh": tong / n,
            "z": tong / math.sqrt(var_cum) if var_cum > 0 else 0.0,
            "vif": var_cum / var_nn if var_nn > 0 else float("nan")}


def _mcnemar_cum(cap: list[tuple]) -> dict:
    """cap = [(cụm, thật trúng, giả trúng)] ⇒ b, c, z thô, z theo cụm."""
    b = sum(1 for _, t, g in cap if t and not g)
    c = sum(1 for _, t, g in cap if g and not t)
    theo = defaultdict(int)
    for k, t, g in cap:
        theo[k] += (1 if t and not g else 0) - (1 if g and not t else 0)
    var_cum = sum(v * v for v in theo.values())
    return {"n": len(cap), "b": b, "c": c, "lech": b + c,
            "z_tho": (b - c) / math.sqrt(b + c) if b + c else 0.0,
            "z": (b - c) / math.sqrt(var_cum) if var_cum > 0 else 0.0}


def doc_p4(s: dict) -> str:
    if s.get("n", 0) < N_TOI_THIEU_P4:
        return "CHƯA ĐƯỢC PHÉP KẾT LUẬN"
    return "CÓ TÍN HIỆU" if s["z"] >= Z else ("KÉM NỀN" if s["z"] <= -Z else "KHÔNG CÓ TÍN HIỆU")


def doc_m4(s: dict) -> str:
    if s.get("lech", 0) < CAP_LECH_TOI_THIEU_M4:
        return "CHƯA ĐỦ MẪU"
    return "THẬT HƠN GIẢ" if s["z"] >= Z else ("GIẢ HƠN" if s["z"] <= -Z else "NGANG NHAU")


def main() -> int:
    con = sqlite3.connect(DB, uri=True, timeout=60)
    con.row_factory = sqlite3.Row
    nhan = K.tinh_giai_doan(con)
    trong_db = {r[0]: r[1] for r in con.execute("SELECT id, giai_doan FROM mined_rule_effectiveness")}
    khop = sum(1 for i, g in nhan.items() if trong_db.get(i) == g)
    kq = _duoi_ket_qua(con)
    hom_qua = (date.today() - timedelta(days=1)).isoformat()

    dong = []
    for r in con.execute("SELECT id, date, target_region, rule_key, tails_produced FROM mined_rule_effectiveness "
                         "WHERE date >= ? AND date <= ? AND rule_key IS NOT NULL", (TU_NGAY, hom_qua)):
        k_dq = kq.get((r["date"], r["target_region"]))
        if not k_dq:
            continue
        try:
            duoi = sorted(set(json.loads(r["tails_produced"] or "[]")))
        except Exception:
            continue
        if not duoi:
            continue
        b = len(k_dq) / 100.0
        nen = 1 - (1 - b) ** len(duoi)
        that = 1 if any(d in k_dq for d in duoi) else 0
        gia = 1 if any(d in k_dq for d in duoi_gia(r["rule_key"], r["date"], len(duoi))) else 0
        nhom = "DO_TIEN" if nhan.get(r["id"]) == K.NHAN_DO_TIEN else "TRONG_CUA_SO"
        dong.append({"ngay": r["date"], "mien": r["target_region"], "nhom": nhom, "nhan": nhan.get(r["id"]),
                     "that": that, "gia": gia, "nen": nen})

    ngay_cuoi = max((x["ngay"] for x in dong), default=hom_qua)
    print("=" * 112)
    print(f"  V11195 — ĐO LẠI LUẬT TRÊN NHÃN ĐÃ SỬA · {TU_NGAY} → {ngay_cuoi} · DB production (mode=ro)")
    print("=" * 112)
    phan_bo = defaultdict(int)
    for x in dong:
        phan_bo[x["nhan"]] += 1
    print(f"  nhãn tính lại khớp cột giai_doan trong DB: {khop}/{len(nhan)} dòng "
          f"({'ĐÃ ÁP' if khop == len(nhan) else 'CHƯA ÁP — số dưới đây dùng nhãn tính lại'})")
    print(f"  dòng đo được (có kết quả, có đuôi): {len(dong)} · theo nhãn: {dict(sorted(phan_bo.items()))}")

    def loc(m, nhom, so_ngay):
        moc = (date.fromisoformat(ngay_cuoi) - timedelta(days=so_ngay - 1)).isoformat() if so_ngay else TU_NGAY
        return [x for x in dong if x["mien"] == m and x["nhom"] == nhom and x["ngay"] >= moc]

    print("\n  P4' — hit_any của bộ k đuôi so với nền 1−(1−b)^k · z theo CỤM ngày-miền · VIF đo cho chính thước này")
    print(f"  {'miền':5} {'nhóm':<13} {'cửa sổ':>8} {'n':>6} {'cụm':>5} {'trúng':>7} {'nền':>7} {'chênh':>7} "
          f"{'z':>7} {'VIF':>6}  đọc (ngưỡng khai trước)")
    ket_p4 = {}
    for m in MIEN:
        for nhom in ("DO_TIEN", "TRONG_CUA_SO"):
            for w in CUA_SO:
                s = _z_cum([((x["ngay"], x["mien"]), x["that"], x["nen"]) for x in loc(m, nhom, w)])
                ten_w = f"{w} ngày" if w else "toàn bộ"
                if not s["n"]:
                    print(f"  {m:5} {nhom:<13} {ten_w:>8} {0:>6}   (không có dòng)")
                    continue
                doc = doc_p4(s) if nhom == "DO_TIEN" else "— (trong cửa sổ chọn: không dùng làm bằng chứng)"
                if nhom == "DO_TIEN" and w is None:
                    ket_p4[m] = (s, doc)
                print(f"  {m:5} {nhom:<13} {ten_w:>8} {s['n']:>6} {s['so_cum']:>5} {s['ti_le']*100:>6.1f}% "
                      f"{s['nen']*100:>6.1f}% {s['chenh']*100:>+6.1f} {s['z']:>+7.2f} {s['vif']:>6.2f}  {doc}")
        print()

    print("  M4' — McNemar luật THẬT vs luật GIẢ tất định, cùng ngày · z theo CỤM ngày-miền")
    print(f"  {'miền':5} {'nhóm':<13} {'cửa sổ':>8} {'n':>6} {'b thật hơn':>11} {'c giả hơn':>10} {'lệch':>5} "
          f"{'z thô':>7} {'z cụm':>7}  đọc (ngưỡng khai trước)")
    ket_m4 = {}
    for m in MIEN:
        for nhom in ("DO_TIEN", "TRONG_CUA_SO"):
            for w in CUA_SO:
                s = _mcnemar_cum([((x["ngay"], x["mien"]), x["that"], x["gia"]) for x in loc(m, nhom, w)])
                ten_w = f"{w} ngày" if w else "toàn bộ"
                if not s["n"]:
                    print(f"  {m:5} {nhom:<13} {ten_w:>8} {0:>6}   (không có dòng)")
                    continue
                doc = doc_m4(s) if nhom == "DO_TIEN" else "—"
                if nhom == "DO_TIEN" and w is None:
                    ket_m4[m] = (s, doc)
                print(f"  {m:5} {nhom:<13} {ten_w:>8} {s['n']:>6} {s['b']:>11} {s['c']:>10} {s['lech']:>5} "
                      f"{s['z_tho']:>+7.2f} {s['z']:>+7.2f}  {doc}")
        print()

    print("  KẾT LUẬN THEO NGƯỠNG KHAI TRƯỚC (phần ĐO TIẾN, toàn bộ từ 07/08):")
    for m in MIEN:
        p4 = ket_p4.get(m, ({"n": 0}, "CHƯA ĐƯỢC PHÉP KẾT LUẬN"))
        m4 = ket_m4.get(m, ({"lech": 0}, "CHƯA ĐỦ MẪU"))
        print(f"    {m}: P4' {p4[1]} (n={p4[0].get('n', 0)}) · M4' {m4[1]} (cặp lệch={m4[0].get('lech', 0)})")
    co = any(v[1] == "CÓ TÍN HIỆU" for v in ket_p4.values()) or any(v[1] == "THẬT HƠN GIẢ" for v in ket_m4.values())
    print(f"  [do] LUAT_DO_TIEN_V11195={'CO_TIN_HIEU_O_IT_NHAT_MOT_MIEN' if co else 'KHONG_DAT'}")
    print("=" * 112)
    con.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
