# -*- coding: utf-8 -*-
"""V11193 — ỨNG VIÊN THẾ CHỖ hai model OpenRouter (bị OpenRouter chặn từ 25/11). CHỈ ĐỌC.

Thước: bạch thủ (`model_daily_eval.bt_hit`) so với NỀN ĐÚNG NGÀY (RM-18): p = m/100, m = số đuôi khác nhau
về trong ngày-miền. Chỉ lượt THẬT của đường chính (loại dòng rỗng, loại `shadow%`). Cửa sổ: tính theo ngày HOẠT ĐỘNG
gần nhất của từng model, đo ĐỦ BỘ cửa sổ 14/30/90/180 ngày hoạt động (PRJ-SELECTION-WINDOW-001, thước TW-001 —
đã từng đổi dấu giữa các cửa sổ) — các model dừng ở các thời điểm khác nhau nên chênh so với nền mới so được.
n nhỏ ⇒ ghi «chưa được phép kết luận» (RM-04).

    venv/bin/python3 web/backend/_v11193_ung_vien_the_cho.py      (chạy TRÊN VPS)
"""
import json
import math
import sqlite3
import sys
from collections import defaultdict

sys.stdout.reconfigure(encoding="utf-8")
DB = "file:/root/Lottery_AI_Test/data/lottery_ai.db?mode=ro"
MODELS = ["claude-opus-4-6", "claude-sonnet-4-6", "gemini-2.5-flash", "gemini-2.5-pro", "deepseek-reasoner",
          "gpt-oss-120b", "glm-5.1"]
RONG = "(main_numbers IS NULL OR main_numbers IN ('', '[]', 'null'))"


def main():
    c = sqlite3.connect(DB, uri=True, timeout=60)
    nen = {}
    for d, reg, pj in c.execute("SELECT date, region, prizes_json FROM lottery_results WHERE date >= '2026-06-01'"):
        try:
            v = json.loads(pj or "{}")
        except Exception:
            continue
        vals = v.values() if isinstance(v, dict) else v
        s = nen.setdefault((d, reg), set())
        for x in vals:
            for y in (x if isinstance(x, list) else [x]):
                t = "".join(ch for ch in str(y) if ch.isdigit())
                if len(t) >= 2:
                    s.add(t[-2:])
    CUA_SO = (14, 30, 90, 180)
    print("| model | miền | " + " | ".join(f"{w} ngày: chênh ±2σ (n)" for w in CUA_SO) + " | đọc |")
    print("|---|---|" + "---|" * len(CUA_SO) + "---|")
    for m in MODELS:
        ngay_hd = [r[0] for r in c.execute(
            f"SELECT DISTINCT date FROM model_daily_eval WHERE ai_model=? AND NOT {RONG} "
            "AND COALESCE(run_source,'') NOT LIKE 'shadow%' ORDER BY date DESC LIMIT 180", (m,))]
        if not ngay_hd:
            print(f"| {m} | — | " + " | ".join("—" for _ in CUA_SO) + " | không có lượt thật |")
            continue
        theo = defaultdict(list)  # reg -> [(date, hit, base)]
        for d, reg, hit in c.execute(
                f"SELECT date, region, bt_hit FROM model_daily_eval WHERE ai_model=? AND NOT {RONG} "
                "AND COALESCE(run_source,'') NOT LIKE 'shadow%' AND date >= ?", (m, min(ngay_hd))):
            if (d, reg) in nen and nen[(d, reg)]:
                theo[reg].append((d, 1 if hit else 0, len(nen[(d, reg)]) / 100))
        for reg in ("MN", "MT", "MB"):
            if not theo.get(reg):
                continue
            o, doc_cuoi = [], ""
            for w in CUA_SO:
                if len(ngay_hd) < w:
                    o.append("chưa có đủ ngày")
                    continue
                moc = ngay_hd[w - 1]
                xs = [(h, b) for d, h, b in theo[reg] if d >= moc]
                n = len(xs)
                if not n:
                    o.append("—")
                    continue
                chenh = sum(h for h, _ in xs) / n - sum(b for _, b in xs) / n
                se = math.sqrt(sum(b * (1 - b) for _, b in xs)) / n
                o.append(f"{chenh*100:+.1f} ±{2*se*100:.1f} ({n})")
                if n >= 30:
                    doc_cuoi = ("hơn nền" if chenh > 2 * se else ("kém nền" if chenh < -2 * se else "không khác nền"))
            print(f"| {m} | {reg} | " + " | ".join(o) + f" | {doc_cuoi or 'chưa được phép kết luận (n<30)'} (cửa sổ dài nhất có n≥30) |")
    return 0


if __name__ == "__main__":
    sys.exit(main())
