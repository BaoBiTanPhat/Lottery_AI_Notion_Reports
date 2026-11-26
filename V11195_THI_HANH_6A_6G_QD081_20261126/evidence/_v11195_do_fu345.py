# -*- coding: utf-8 -*-
"""V11195 — nghiệm thu FU-345 theo ngưỡng owner duyệt 26/11/2026. CHỈ ĐỌC (đọc prediction_trace.jsonl).

Owner 26/11/2026 ~10:10: *«6f --> theo khuyến nghị chú ý ghi nhận lưu lại backup lại nha em»*.
Khuyến nghị V11193 (việc 6f): «bỏ [ngưỡng ≥10.000 ký tự] cho MT, đóng mục là đạt».

TRƯỚC (FU-345, V11032 08/08): «sau 24h đọc trace: `context_pack_chars` phải > 10.000 ở mọi lượt, và 0 lượt = 64».
SAU  (V11195, owner 26/11):  «0 lượt = 64 ở MỌI miền (dấu vết lỗi gốc) · > 10.000 chỉ áp cho MN và MB ·
                              MT không áp ngưỡng 10.000 — prompt MT vốn ngắn hơn (V11190: p10 9.851)».
Đếm từ 09/08 (ngày đầu sau bản vá 08/08) tới hôm nay.

    cd /root/Lottery_AI_Test/web/backend && venv/bin/python3 _v11195_do_fu345.py     (TRÊN VPS)
"""
from __future__ import annotations

import json
import os
import sys
from collections import defaultdict

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
TRACE = os.path.join(HERE, "prediction_trace.jsonl")
TU_NGAY = "2026-08-09"
LOI_GOC = 64
NGUONG = 10_000
AP_NGUONG = {"MN": True, "MT": False, "MB": True}


def _pct(xs: list[int], q: float) -> int:
    if not xs:
        return 0
    s = sorted(xs)
    return s[min(len(s) - 1, int(q * (len(s) - 1)))]


def main() -> int:
    theo = defaultdict(list)
    loi_goc = defaultdict(int)
    nho = defaultdict(int)
    hong = 0
    with open(TRACE, encoding="utf-8", errors="replace") as fh:
        for dong in fh:
            try:
                r = json.loads(dong)
            except Exception:
                hong += 1
                continue
            d = str(r.get("date") or "")[:10]
            mien = r.get("target_region") or r.get("region")
            c = r.get("context_pack_chars")
            if d < TU_NGAY or mien not in AP_NGUONG or c is None:
                continue
            c = int(c)
            theo[mien].append(c)
            if c == LOI_GOC:
                loi_goc[mien] += 1
            if c < 1000:
                nho[mien] += 1
    print("=" * 96)
    print(f"  V11195 — NGHIỆM THU FU-345 · trace {TU_NGAY} → nay · {sum(len(v) for v in theo.values())} lượt "
          f"(dòng hỏng bỏ qua: {hong})")
    print("=" * 96)
    print(f"  {'miền':5} {'lượt':>6} {'=64 (lỗi gốc)':>14} {'<1.000':>7} {'<10.000':>8} {'p10':>7} {'p50':>7} "
          f"{'nhỏ nhất':>9}  ngưỡng 10.000  kết quả")
    dat = True
    for m in ("MN", "MT", "MB"):
        xs = theo.get(m, [])
        duoi = sum(1 for x in xs if x < NGUONG)
        ok_loi = loi_goc[m] == 0
        ok_nguong = (duoi == 0) if AP_NGUONG[m] else True
        ok = ok_loi and ok_nguong and bool(xs)
        dat &= ok
        print(f"  {m:5} {len(xs):>6} {loi_goc[m]:>14} {nho[m]:>7} {duoi:>8} {_pct(xs, .1):>7} {_pct(xs, .5):>7} "
              f"{min(xs) if xs else 0:>9}  {'ÁP' if AP_NGUONG[m] else 'KHÔNG ÁP (owner 26/11)':<14} "
              f"{'ĐẠT' if ok else 'TRƯỢT'}")
    print("=" * 96)
    print(f"  [do] FU345_V11195={'DAT' if dat else 'TRUOT'}")
    return 0 if dat else 1


if __name__ == "__main__":
    raise SystemExit(main())
