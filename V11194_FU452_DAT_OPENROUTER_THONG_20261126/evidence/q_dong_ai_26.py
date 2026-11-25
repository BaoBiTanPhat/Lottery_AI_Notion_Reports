import sqlite3, sys, hashlib
sys.stdout.reconfigure(encoding="utf-8")
c = sqlite3.connect("file:/root/Lottery_AI_Test/data/lottery_ai.db?mode=ro", uri=True, timeout=60)
for m, reg, nums, at, rj, rt in c.execute("SELECT ai_model, target_region, main_numbers, analysis_text, reasoning_json, reasoning_tokens FROM predictions WHERE date='2026-11-26' AND ai_model IN ('gpt-oss-120b','gemini-2.5-flash','claude-opus-4-6','claude-sonnet-4-6')"):
    at = at or ""
    print(f"{m:18} {reg} {nums} len={len(at)} sha8={hashlib.sha256(at.encode()).hexdigest()[:8]} rtok={rt}")
    print("   ", at[:220].replace("\n", " "))
print("--- 25/11 vs 24/11 dong co so theo model (MN/MT/MB):")
for d in ("2026-11-24", "2026-11-25", "2026-11-26"):
    for m in ("gpt-oss-120b", "glm-5.1"):
        n = c.execute("SELECT COUNT(*) FROM predictions WHERE date=? AND ai_model=? AND main_numbers NOT IN ('', '[]', 'null') AND main_numbers IS NOT NULL", (d, m)).fetchone()[0]
        t = c.execute("SELECT COUNT(*) FROM predictions WHERE date=? AND ai_model=?", (d, m)).fetchone()[0]
        print(f"   {d} {m:14} co so {n}/{t}")
