# -*- coding: utf-8 -*-
"""V11195 — phép máy cho QD-081 (owner 26/11/2026 ~10:10 duyệt 6a–6g «theo khuyến nghị»). Chỉ đọc MÃ.

Mỗi vế kiểm trên mã/cấu hình thật (không cần DB, chạy được ở máy dev và trên VPS):
  6a  glm-5.1 vẫn là CORE của MT trong roster (`_v11185_roster_goi_token._CHINH_SACH`) — không bị gỡ
  6b  (giữ trọng số chọn số) — không có phép máy riêng: «giữ nguyên» = không đổi mã; ghi ở ghi_chu QD-081
  6c  lớp ghi đè V10640 MN vẫn bật (`OVERRIDE_CONFIG['MN']['enabled'] is True`)
  6d  học thuyết anti-trap vẫn trong prompt (`gpt_analyzer.py` có «OWNER ANTI-TRAP DOCTRINE»)
  6e  nhãn đo tiến mới có mặt và qua cổng thử chặn (`_v11195_kiem_nhan_luat.py` thoát 0)
  6f  ngưỡng FU-345 mới: MT không áp 10.000 ký tự, MN/MB vẫn áp (`_v11195_do_fu345.AP_NGUONG`)
  6g  chỗ còn lại đã chặn biên và cổng biên anchor ĐẠT (`_v11050_kiem_bien_anchor.py` thoát 0)

    python web/backend/_v11195_kiem_qd081.py     → in QD081_V11195=DAT và thoát 0 khi mọi vế đúng
"""
from __future__ import annotations

import ast
import os
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8")
H = os.path.dirname(os.path.abspath(__file__))


def _doc(ten: str) -> str:
    with open(os.path.join(H, ten), encoding="utf-8", errors="replace") as fh:
        return fh.read()


def _gia_tri(ten_tep: str, bien: str):
    for n in ast.parse(_doc(ten_tep)).body:
        if isinstance(n, ast.Assign) and any(getattr(t, "id", "") == bien for t in n.targets):
            return n.value
    return None


def _chay(tep: str) -> int:
    return subprocess.run([sys.executable, os.path.join(H, tep)], capture_output=True, text=True,
                          encoding="utf-8", errors="replace", timeout=240).returncode


def main() -> int:
    ket = []
    nut = _gia_tri("_v11185_roster_goi_token.py", "_CHINH_SACH")
    mt_core = []
    if isinstance(nut, ast.Dict):
        for k, v in zip(nut.keys, nut.values):
            if isinstance(k, ast.Constant) and k.value == "MT":
                mt_core = ast.literal_eval(v).get("CORE", [])
    ket.append(("6a", "glm-5.1 vẫn CORE MT", "glm-5.1" in mt_core, f"MT CORE = {mt_core}"))

    cfg = _gia_tri("_v10640_official_perslice_override.py", "OVERRIDE_CONFIG")
    mn = ast.literal_eval(cfg).get("MN", {}).get("enabled") if cfg is not None else None
    ket.append(("6c", "ghi đè V10640 MN vẫn bật", mn is True, f"OVERRIDE_CONFIG['MN']['enabled'] = {mn}"))

    ket.append(("6d", "anti-trap còn trong prompt", "OWNER ANTI-TRAP DOCTRINE" in _doc("gpt_analyzer.py"),
                "gpt_analyzer.py có «OWNER ANTI-TRAP DOCTRINE»"))

    co_ham = "def tinh_giai_doan(" in _doc("_v11025_khoa_luat_ben.py")
    rc = _chay("_v11195_kiem_nhan_luat.py") if co_ham else -1
    ket.append(("6e", "nhãn đo tiến mới qua cổng", co_ham and rc == 0, f"tinh_giai_doan có mặt · cổng thoát {rc}"))

    ap = _gia_tri("_v11195_do_fu345.py", "AP_NGUONG")
    ap = ast.literal_eval(ap) if ap is not None else {}
    ket.append(("6f", "MT không áp 10.000, MN/MB vẫn áp", ap == {"MN": True, "MT": False, "MB": True},
                f"AP_NGUONG = {ap}"))

    # Chuỗi tách đôi để chính cổng biên anchor không đọc dòng này thành một truy vấn (RM-09).
    va = ("anchor_date " + "<= date(?, '-1 day') AND region = ?") in _doc("_v104_shadow_prompt_injection.py")
    rc2 = _chay("_v11050_kiem_bien_anchor.py")
    ket.append(("6g", "chỗ còn lại đã chặn biên", va and rc2 == 0, f"đã vá {va} · cổng biên anchor thoát {rc2}"))

    print("=" * 92)
    print("  V11195 — PHÉP MÁY QD-081 (6a–6g theo khuyến nghị, owner 26/11/2026)")
    print("=" * 92)
    for ma, mo_ta, ok, chi_tiet in ket:
        print(f"  {'✓' if ok else '✗'} {ma}  {mo_ta:<36} {chi_tiet}")
    print("  · 6b  giữ trọng số chọn số — không có phép máy riêng (giữ nguyên = không đổi mã)")
    dat = all(k[2] for k in ket)
    print("=" * 92)
    print(f"  {'✓' if dat else '✗'} [cong] QD081_V11195={'DAT' if dat else 'TRUOT'}")
    return 0 if dat else 1


if __name__ == "__main__":
    raise SystemExit(main())
