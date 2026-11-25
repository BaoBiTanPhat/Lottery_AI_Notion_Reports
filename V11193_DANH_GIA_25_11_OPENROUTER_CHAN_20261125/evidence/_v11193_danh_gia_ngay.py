# -*- coding: utf-8 -*-
"""V11193 — ĐÁNH GIÁ MỘT NGÀY DỰ ĐOÁN: /du-doan · /choi · từng model. CHỈ ĐỌC (mode=ro).

Owner hỏi 25/11 ~21:35: *"kiểm tra đánh giá việc dự đoán hôm nay sao rồi em"*.

Thước tiền lấy nguyên từ `_v10759_money_board.py` (qua `_v11190_so_bang_choi_du_doan.py`): mỗi số × mỗi đài =
50 điểm · giá 1 điểm MN/MT 18.000đ, MB 27.000đ · mỗi nháy trả 98.000đ/điểm.
Nền (RM-18) tính ĐÚNG NGÀY: m = số đuôi khác nhau về trong ngày ⇒ P(1 số trúng ≥1 nháy) = m/100;
P(≥1 trong 2 số) = 1 − C(100−m,2)/C(100,2).

    venv/bin/python3 web/backend/_v11193_danh_gia_ngay.py 2026-11-25        (chạy TRÊN VPS)
"""
from __future__ import annotations

import json
import sqlite3
import sys
from math import comb

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

DB = "/root/Lottery_AI_Test/data/lottery_ai.db"
PTS, PAY = 50, 98000
COST = {"MN": 18000, "MT": 18000, "MB": 27000}
HE_SO = {"CHƠI": 1.0, "CÂN NHẮC": 0.5, "NGHỈ": 0.0}


def so(x) -> list[str]:
    if x is None:
        return []
    if isinstance(x, str):
        try:
            v = json.loads(x)
        except Exception:
            v = [p for p in x.replace("-", ",").replace(" ", ",").split(",") if p]
    else:
        v = x
    if v is None:
        return []
    if isinstance(v, (int, str)):
        v = [v]
    out = []
    for n in v:
        s = "".join(ch for ch in str(n) if ch.isdigit())
        if s:
            out.append(s[-2:].zfill(2))
    return out


def main() -> int:
    ngay = sys.argv[1] if len(sys.argv) > 1 else "2026-11-25"
    c = sqlite3.connect(f"file:{DB}?mode=ro", uri=True, timeout=60)
    c.row_factory = sqlite3.Row
    print(f"# Đánh giá dự đoán ngày {ngay}\n")
    for mien in ("MN", "MT", "MB"):
        dai = {}
        for r in c.execute("SELECT station, prizes_json FROM lottery_results WHERE date=? AND region=?", (ngay, mien)):
            pj = json.loads(r["prizes_json"] or "{}")
            vals = pj.values() if isinstance(pj, dict) else pj
            t = []
            for v in vals:
                for x in (v if isinstance(v, list) else [v]):
                    s = "".join(ch for ch in str(x) if ch.isdigit())
                    if len(s) >= 2:
                        t.append(s[-2:])
            dai[r["station"]] = t
        tat_ca = [t for tl in dai.values() for t in tl]
        m = len(set(tat_ca))
        nd = len(dai)
        print(f"## {mien} — {nd} đài ({', '.join(dai)}) · {len(tat_ca)} giải · {m} đuôi khác nhau về")
        if not dai:
            print("   (chưa có kết quả)\n")
            continue
        p1 = m / 100
        p2 = 1 - comb(100 - m, 2) / comb(100, 2)

        def nhay(nums):
            return {n: sum(tl.count(n) for tl in dai.values()) for n in nums}

        def pnl(nums, hs=1.0):
            h = nhay(nums)
            von = nd * len(nums) * PTS * COST[mien] * hs
            return sum(h.values()) * PTS * PAY * hs - von, von, h

        def ev(k, hs=1.0):
            return k * (len(tat_ca) / 100 * PTS * PAY - nd * PTS * COST[mien]) * hs

        print(f"   nền ngẫu nhiên hôm nay: 1 số trúng {p1:.0%} · 2 số có ít nhất 1 trúng {p2:.0%}\n")

        fb = c.execute("SELECT * FROM final_bundles WHERE date=? AND region=? AND status='ACTIVE' "
                       "ORDER BY id DESC LIMIT 1", (ngay, mien)).fetchone()
        print("   | bảng | số | trúng (nháy) | lời/lỗ thật | kỳ vọng nếu chọn ngẫu nhiên | vốn | giờ chốt |")
        print("   |---|---|---|---|---|---|---|")
        if fb:
            for ten, nums in (("/du-doan bạch thủ", so(fb["bach_thu"])[:1]), ("/du-doan lô 2 số", so(fb["lo2"])[:2])):
                if nums:
                    p, v, h = pnl(nums)
                    print(f"   | {ten} | {' '.join(nums)} | {h} | {p/1e3:+,.0f}k | {ev(len(nums))/1e3:+,.0f}k | "
                          f"{v/1e3:,.0f}k | {fb['created_at']} |")
            print(f"   | (bundle) | lo3={so(fb['lo3'])} xien2={fb['xien2']} | method={fb['generation_method']} · "
                  f"model_count={fb['model_count']} · fallback={fb['is_fallback']} | | | | |")
        mb = c.execute("SELECT * FROM money_board_log WHERE date=? AND region=?", (ngay, mien)).fetchone()
        if mb:
            nums = so(mb["songthu"])[:2]
            vd = (mb["verdict"] or "").strip().upper()
            if nums:
                p, v, h = pnl(nums)
                print(f"   | /choi đánh đủ | {' '.join(nums)} | {h} | {p/1e3:+,.0f}k | {ev(len(nums))/1e3:+,.0f}k | "
                      f"{v/1e3:,.0f}k | ghi {mb['created_at']} |")
                hs = HE_SO.get(vd, 0.0)
                if hs:
                    p, v, h = pnl(nums, hs)
                    print(f"   | /choi theo khuyến nghị «{vd}» ×{hs} | {' '.join(nums)} | {h} | {p/1e3:+,.0f}k | "
                          f"{ev(len(nums), hs)/1e3:+,.0f}k | {v/1e3:,.0f}k | ⚠ khuyến nghị ghi lúc {mb['created_at'][11:16]} |")
                else:
                    print(f"   | /choi theo khuyến nghị «{vd}» | không đánh | — | 0 | 0 | 0 | |")
            print(f"   /choi: method={mb['method']} · kiểu={mb['play_style']} · stake={mb['stake']}")
        print()
        print("   | model | đường | bạch thủ | trúng BT? | số chọn | trúng / chọn |")
        print("   |---|---|---|---|---|---|")
        n_bt = n_bt_trung = 0
        for r in c.execute("SELECT ai_model, run_source, bt_number, bt_hit, main_numbers, pick_count, hit_count "
                           "FROM model_daily_eval WHERE date=? AND region=? ORDER BY bt_hit DESC, ai_model",
                           (ngay, mien)):
            n_bt += 1
            n_bt_trung += 1 if r["bt_hit"] else 0
            print(f"   | {r['ai_model']} | {r['run_source']} | {r['bt_number']} | {'✓' if r['bt_hit'] else '✗'} | "
                  f"{' '.join(so(r['main_numbers']))} | {r['hit_count']}/{r['pick_count']} |")
        if n_bt:
            print(f"   ⇒ {n_bt_trung}/{n_bt} model trúng bạch thủ · nền {p1:.0%} ⇒ kỳ vọng ngẫu nhiên "
                  f"{n_bt * p1:.1f}/{n_bt}")
        print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
