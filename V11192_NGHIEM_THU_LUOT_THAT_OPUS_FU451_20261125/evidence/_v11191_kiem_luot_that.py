# -*- coding: utf-8 -*-
"""V11191 — kiểm LƯỢT THẬT sau khi nhả cách ly Claude (FU-452) + nghiệm thu vá stdout (FU-451a). CHỈ ĐỌC.

Chạy TRÊN VPS:  /root/Lottery_AI_Test/venv/bin/python3 web/backend/_v11191_kiem_luot_that.py [YYYY-MM-DD]

FU-452  ĐẠT khi mỗi dòng `predictions` của Claude trong ngày có số và KHÔNG mang lỗi
        (`PERSISTED_DIAGNOSTIC_EMPTY` / `ERROR`), và Claude không bị cách ly lại.
FU-451a ĐẠT khi `scheduler_logs` có `SHADOW-PROMOTION-SCORECARD <miền> <ngày>: inserted=` cho cả ba miền
        và không có `closed file` kể từ 04:30 VN hôm đó.
⚠ `scheduler_logs.log_time` lưu UTC naive (CLAUDE.md §55 quy ước thứ tư) ⇒ cộng 7 giờ khi đọc.
"""
import json
import os
import sqlite3
import sys
from datetime import datetime, timedelta

try:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (ValueError, AttributeError):
    pass

GOC = "/root/Lottery_AI_Test"
DB = "file:%s/data/lottery_ai.db?mode=ro" % GOC
CACH_LY = GOC + "/data/provider_quarantine.json"


def main():
    ngay = sys.argv[1] if len(sys.argv) > 1 else datetime.now().strftime("%Y-%m-%d")
    c = sqlite3.connect(DB, uri=True)
    dat_452, dat_451 = True, True

    print("=" * 92)
    print("  V11191 — kiểm lượt thật ngày %s (chạy lúc %s, giờ máy VPS)" % (ngay, datetime.now().strftime("%H:%M")))
    print("=" * 92)

    print("\n[FU-452] Dòng predictions của Claude trong ngày")
    dong = list(c.execute(
        """SELECT substr(created_at,12,5), target_region, ai_model, COALESCE(run_source,'-'),
                  COALESCE(main_numbers,''), COALESCE(verdict_reason,''), COALESCE(status,'-')
             FROM predictions WHERE ai_model LIKE 'claude%' AND date = ? ORDER BY created_at""", (ngay,)))
    if not dong:
        print("  (chưa có dòng nào)")
        dat_452 = False
    for hm, reg, m, rs, so, ly_do, st in dong:
        loi = ("PERSISTED_DIAGNOSTIC_EMPTY" in ly_do) or ly_do.startswith("ERROR") or ("ERROR:" in ly_do[:60])
        ok = bool(so.strip()) and so.strip() not in ("[]", "null") and not loi
        dat_452 = dat_452 and ok
        print("  %s %s  %s %-18s %-11s %-8s số=%-22s %s" % ("✓" if ok else "✗", hm, reg, m, rs, st, so[:22],
                                                         ("" if ok else ly_do[:70])))

    print("\n[FU-452] Model AI trong predictions theo miền (đếm model, không đếm dòng)")
    for reg, n, ds in c.execute(
            """SELECT target_region, count(DISTINCT ai_model), group_concat(DISTINCT ai_model)
                 FROM predictions WHERE date = ? AND (ai_model LIKE 'claude%' OR ai_model LIKE 'gemini%'
                      OR ai_model LIKE 'gpt%' OR ai_model LIKE 'glm%' OR ai_model LIKE 'deepseek%')
                GROUP BY 1 ORDER BY 1""", (ngay,)):
        print("  %s  %d model: %s" % (reg, n, ds))

    try:
        cl = json.load(open(CACH_LY, encoding="utf-8"))
    except Exception as e:
        cl = {"_loi_doc": repr(e)}
    claude_lai = [m for m in cl if m.startswith("claude")]
    print("\n[FU-452] Cách ly hiện tại:", ", ".join(sorted(cl)) or "(trống)")
    if claude_lai:
        dat_452 = False
        print("  ✗ Claude BỊ CÁCH LY LẠI:", claude_lai, "—", str(cl[claude_lai[0]].get("ly_do"))[:120])

    print("\n[FU-451a] SHADOW-PROMOTION-SCORECARD (log_time UTC → +7)")
    tu_utc = (datetime.strptime(ngay, "%Y-%m-%d") - timedelta(hours=7) + timedelta(hours=4, minutes=30))
    tu = tu_utc.strftime("%Y-%m-%d %H:%M:%S")
    co_mien = set()
    for lt, msg in c.execute(
            """SELECT log_time, message FROM scheduler_logs WHERE message LIKE '%SHADOW-PROMOTION-SCORECARD%'
                  AND log_time >= ? ORDER BY id""", (tu,)):
        vn = (datetime.strptime(lt[:19], "%Y-%m-%d %H:%M:%S") + timedelta(hours=7)).strftime("%H:%M")
        print("  %s VN  %s" % (vn, msg[:120]))
        for reg in ("MN", "MT", "MB"):
            if (" %s %s" % (reg, ngay)) in msg and "inserted=" in msg:
                co_mien.add(reg)
    thieu = [r for r in ("MN", "MT", "MB") if r not in co_mien]
    if thieu:
        dat_451 = False
        print("  ✗ thiếu miền:", thieu)
    n_closed = c.execute("""SELECT count(*) FROM scheduler_logs WHERE message LIKE '%closed file%'
                              AND log_time >= ?""", (tu,)).fetchone()[0]
    print("  'closed file' trong scheduler_logs từ 04:30 VN: %d" % n_closed)
    if n_closed:
        dat_451 = False

    print("\n" + "=" * 92)
    print("  FU-452  Claude chạy lại thật : %s" % ("ĐẠT" if dat_452 else "CHƯA ĐẠT"))
    print("  FU-451a scorecard + stdout   : %s" % ("ĐẠT" if dat_451 else "CHƯA ĐẠT"))
    print("=" * 92)
    return 0 if (dat_452 and dat_451) else 1


if __name__ == "__main__":
    sys.exit(main())
