# -*- coding: utf-8 -*-
"""Tái hiện FU-451: nạp v94 rồi v95 trong CÙNG tiến trình (như service lúc 19:18/19:20) rồi print.
    python tai_hien_stdout.py <thư_mục_chứa_hai_tệp>     → in OK_SAU_KHI_NAP hoặc chết (mã thoát ≠ 0)
"""
import gc
import importlib
import sys

sys.path.insert(0, sys.argv[1])
for ten in ("_materialize_v94_safe_batch", "_materialize_v95_data_integrity_audit"):
    importlib.import_module(ten)
    gc.collect()
print("OK_SAU_KHI_NAP — print vẫn sống sau khi nạp cả hai mô-đun")
sys.stdout.flush()
