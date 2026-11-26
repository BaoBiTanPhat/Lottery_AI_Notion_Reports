# -*- coding: utf-8 -*-
"""Đợt 2 — mỗi script ghi bảng nào, và AI KHÁC đọc bảng đó (grep toàn web/, trừ chính tệp). CHỈ ĐỌC."""
import os
import re
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8")
BE = "/root/Lottery_AI_Test/web/backend"
DS = ["_v10730_pnl_forward_track.py", "_v10733_consensus_freeshadow_shadow.py", "_v10737_output_final_lab_shadow.py",
      "_v10744_rescue_candidate_monitor.py", "_v10789_selector_shadow.py", "_v10801_ml_mark_ab_shadow.py",
      "_v10803_chase_bias_shadow.py", "_v10821_total_v2_shadow.py", "_v10829_rule_cond_shadow.py", "_v10844_mb_whatif.py",
      "_v10984_ghep_lane_official.py", "_v11017_bay_dan_shadow.py", "_v11018_ma_doi_chung.py", "_v11037_g2mb_lane.py",
      "_v11089_cham_lane_tb.py"]
GHI = re.compile(r"(?:INSERT(?:\s+OR\s+\w+)?\s+INTO|REPLACE\s+INTO|CREATE\s+TABLE(?:\s+IF\s+NOT\s+EXISTS)?|UPDATE|DELETE\s+FROM)\s+[\"`]?([A-Za-z_][A-Za-z0-9_]*)", re.I)
BANG_HANG = re.compile(r"^\s*(?:BANG|TABLE|_TABLE|BANG_\w+|\w*_TABLE)\s*=\s*[\"']([A-Za-z_][A-Za-z0-9_]*)[\"']", re.M)
for f in DS:
    p = os.path.join(BE, f)
    if not os.path.exists(p):
        print(f"== {f}: KHÔNG CÓ TỆP")
        continue
    t = open(p, encoding="utf-8", errors="replace").read()
    bang = sorted({m for m in GHI.findall(t)} | set(BANG_HANG.findall(t)))
    bang = [b for b in bang if b.lower() not in ("if", "not", "exists", "set", "table", "or")]
    print(f"== {f}: ghi {bang}")
    for b in bang:
        r = subprocess.run(["grep", "-rlw", b, "--include=*.py", "--include=*.html", "--include=*.js", "--include=*.sh",
                            "/root/Lottery_AI_Test/web/"], capture_output=True, text=True).stdout.split()
        khac = sorted(os.path.relpath(x, "/root/Lottery_AI_Test/web") for x in r
                      if not x.endswith("/" + f) and "__pycache__" not in x and "_staged" not in x)
        print(f"     {b:<42} người khác nhắc: {khac if khac else '— KHÔNG AI'}")
