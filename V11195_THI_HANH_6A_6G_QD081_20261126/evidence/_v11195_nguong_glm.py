# -*- coding: utf-8 -*-
"""V11195 — ngưỡng gỡ `glm-5.1` khỏi official (FU-195) theo cách đo owner duyệt 26/11/2026. CHỈ ĐỌC.

Owner 26/11/2026 ~10:10: *«6a --> theo khuyến nghị»*. Khuyến nghị V11193 (việc 6a): «giữ [glm-5.1]» — lựa
chọn «giữ và sửa cách đo dài hơn», vì 2/28 = 7,1% vượt 6% nhưng 42% khả năng chỉ do ngẫu nhiên; «xét lại
khi OpenRouter chạy lại».

TRƯỚC (FU-195, owner 31/07): gỡ nếu «tỉ lệ lỗi >6% trong 14 ngày, HOẶC làm MT lỡ mốc 16:58 từ 2 ngày trở lên».
SAU  (V11195 — khai TRƯỚC khi đọc số mới, RM-03):
  · cửa sổ 28 ngày (dài gấp đôi) tính theo NGÀY CÓ CHẠY của glm-5.1 ở official (MT/MB);
  · KHÔNG tính ngày nhà cung cấp hỏng toàn phần — mọi dòng của mọi model đi qua OpenRouter trong ngày đều
    rỗng (≥ 3 dòng) — theo QD-080 mục 6 (lỗi auth/billing/circuit-open/model unavailable không tính vào hiệu năng);
  · gỡ nếu tỉ lệ lỗi > 6% VÀ xác suất do ngẫu nhiên < 5% (nhị thức một phía, giả thuyết gốc «lỗi thật ≤ 6%»);
  · HOẶC MT khoá bundle sau 16:58 từ 2 ngày trở lên trong cửa sổ (giữ nguyên vế này).
«Lỗi» = dòng `predictions` của glm-5.1 không có số (`main_numbers` rỗng).

    cd /root/Lottery_AI_Test/web/backend && venv/bin/python3 _v11195_nguong_glm.py [YYYY-MM-DD]   (TRÊN VPS)
"""
from __future__ import annotations

import math
import os
import sqlite3
import sys
from collections import defaultdict
from datetime import date, timedelta

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
DB = "file:" + os.path.abspath(os.path.join(HERE, "..", "..", "data", "lottery_ai.db")) + "?mode=ro"
MODEL = "glm-5.1"
QUA_OPENROUTER = ("glm-5.1", "gpt-oss-120b")
NGUONG = 0.06
ALPHA = 0.05
CUA_SO = 28
MOC_MT = "16:58:00"
RONG = "(main_numbers IS NULL OR main_numbers IN ('', '[]', 'null'))"


def p_mot_phia(x: int, n: int, p: float) -> float:
    """P(X ≥ x) với X ~ Nhị thức(n, p)."""
    return sum(math.comb(n, k) * p ** k * (1 - p) ** (n - k) for k in range(x, n + 1))


def main() -> int:
    con = sqlite3.connect(DB, uri=True, timeout=60)
    den = sys.argv[1] if len(sys.argv) > 1 else date.today().isoformat()
    tu_28 = (date.fromisoformat(den) - timedelta(days=CUA_SO - 1)).isoformat()
    tu_14 = (date.fromisoformat(den) - timedelta(days=13)).isoformat()

    ngay_hong = defaultdict(lambda: [0, 0])          # ngày → [số dòng OpenRouter, số dòng rỗng]
    for d, rong in con.execute(
            f"SELECT date, {RONG} FROM predictions WHERE ai_model IN ({','.join('?' * len(QUA_OPENROUTER))}) "
            "AND COALESCE(run_source,'') NOT LIKE 'shadow%' AND date >= date(?, '-150 days') AND date <= ?",
            (*QUA_OPENROUTER, den, den)):
        ngay_hong[d][0] += 1
        ngay_hong[d][1] += 1 if rong else 0
    loai = sorted(d for d, (n, r) in ngay_hong.items() if n >= 3 and r == n)

    dong = list(con.execute(
        f"SELECT date, target_region, {RONG} FROM predictions WHERE ai_model=? AND target_region IN ('MT','MB') "
        "AND COALESCE(run_source,'') NOT LIKE 'shadow%' AND date >= date(?, '-150 days') AND date <= ? ORDER BY date",
        (MODEL, den, den)))

    def dem(tu, toi, bo_loai=True):
        xs = [r for r in dong if tu <= r[0] <= toi and not (bo_loai and r[0] in loai)]
        return len(xs), sum(1 for r in xs if r[2])

    n28, x28 = dem(tu_28, den)
    n14_cu, x14_cu = dem(tu_14, den, bo_loai=False)
    nen_tu = (date.fromisoformat(tu_28) - timedelta(days=90)).isoformat()
    nen_toi = (date.fromisoformat(tu_28) - timedelta(days=1)).isoformat()
    n_nen, x_nen = dem(nen_tu, nen_toi)
    tre_mt = [r for r in con.execute(
        "SELECT date, created_at FROM final_bundles WHERE region='MT' AND date BETWEEN ? AND ? ORDER BY date",
        (tu_28, den)) if str(r[1])[11:19] > MOC_MT]
    p = p_mot_phia(x28, n28, NGUONG) if n28 else 1.0
    ti_le = x28 / n28 if n28 else 0.0
    go = (ti_le > NGUONG and p < ALPHA) or len(tre_mt) >= 2

    print("=" * 96)
    print(f"  V11195 — NGƯỠNG GỠ glm-5.1 (FU-195) · cửa sổ 28 ngày {tu_28} → {den} · DB production (mode=ro)")
    print("=" * 96)
    print(f"  ngày OpenRouter hỏng toàn phần (không tính, QD-080 mục 6): {', '.join(loai) or 'không có'}")
    print(f"  CÁCH CŨ  (14 ngày, không loại ngày hỏng): {x14_cu}/{n14_cu} = "
          f"{(x14_cu / n14_cu * 100 if n14_cu else 0):.1f}% → {'VƯỢT 6%' if n14_cu and x14_cu / n14_cu > NGUONG else 'không vượt'}")
    print(f"  CÁCH MỚI (28 ngày, loại ngày hỏng)     : {x28}/{n28} = {ti_le * 100:.1f}% · "
          f"xác suất do ngẫu nhiên nếu lỗi thật ≤ 6%: {p:.3f}")
    print(f"  nền lỗi 90 ngày trước cửa sổ ({nen_tu} → {nen_toi}): {x_nen}/{n_nen} = "
          f"{(x_nen / n_nen * 100 if n_nen else 0):.1f}%")
    print(f"  MT khoá bundle sau {MOC_MT[:5]} trong cửa sổ: {len(tre_mt)} ngày "
          f"{[(d, str(t)[11:16]) for d, t in tre_mt] if tre_mt else ''}")
    print("-" * 96)
    print(f"  ngưỡng (khai trước): gỡ nếu (tỉ lệ > 6% VÀ xác suất < {ALPHA}) HOẶC MT trễ ≥ 2 ngày")
    print(f"  [do] FU195_V11195={'GO' if go else 'GIU'}")
    print("=" * 96)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
