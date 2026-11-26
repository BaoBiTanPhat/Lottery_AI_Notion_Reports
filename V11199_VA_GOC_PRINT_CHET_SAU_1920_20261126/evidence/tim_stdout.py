# -*- coding: utf-8 -*-
"""Tìm chỗ gán `sys.stdout = ...` CHẠY LÚC IMPORT (cấp mô-đun, kể cả trong try/if cấp mô-đun; KHÔNG tính trong def/class
và trong khối `if __name__ == "__main__"`)."""
import ast
import sys

sys.stdout.reconfigure(encoding="utf-8")


def la_main_guard(node) -> bool:
    t = getattr(node, "test", None)
    return (isinstance(node, ast.If) and isinstance(t, ast.Compare) and isinstance(t.left, ast.Name)
            and t.left.id == "__name__")


def duyet(nodes, ra):
    for n in nodes:
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            continue
        if la_main_guard(n):
            continue
        if isinstance(n, ast.Assign):
            for tg in n.targets:
                if (isinstance(tg, ast.Attribute) and tg.attr in ("stdout", "stderr")
                        and isinstance(tg.value, ast.Name) and tg.value.id == "sys"):
                    ra.append((n.lineno, tg.attr))
        for f in ("body", "orelse", "finalbody", "handlers"):
            con = getattr(n, f, None)
            if isinstance(con, list):
                duyet(con, ra)


for p in sys.argv[1:]:
    src = open(p, encoding="utf-8", errors="replace").read()
    ra = []
    duyet(ast.parse(src).body, ra)
    print(f"{p}: {'GAN LUC IMPORT dong ' + str(ra) if ra else 'khong gan luc import'}")
