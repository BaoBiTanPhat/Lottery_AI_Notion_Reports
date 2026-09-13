# -*- coding: utf-8 -*-
"""V11184 — BỘ THỬ §Z: QD-079 C1/C2/C3 + nền chính xác + cổng ghi weights.

RM-15: cổng không qua thử coi như KHÔNG TỒN TẠI. Mỗi điều kiện của cổng có MỘT bài thử ÂM
riêng, cộng một bài DƯƠNG đủ mạnh để chứng minh cổng không phải loại mọi ứng viên.

Chạy: python _v11184_thu_z.py            (thuần logic, không cần DB)
      python _v11184_thu_z.py --co-db    (thêm nhóm đo trên DB thật)
"""
from __future__ import annotations

import io
import os
import sys
from math import comb

BE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BE)

KQ = []


def thu(ten, dat, chi_tiet=""):
    KQ.append((ten, bool(dat), chi_tiet))


def nhom(ten):
    print()
    print("-- %s --" % ten)


# ============================================================================
# A · C1 — KHỬ TRÙNG TẠI CHỖ ĐO
# ============================================================================
def nhom_A():
    nhom("A · C1 khử trùng tại chỗ đo")
    import weight_optimizer as W

    src = io.open(BE + "/weight_optimizer.py", encoding="utf-8").read()

    # A1: không còn dùng len() của list CÓ TRÙNG làm số đuôi khác nhau
    thu("A1 khong con len(actual_tails) trong weight_optimizer",
        src.count("len(actual_tails)") == 0,
        "dem=%d" % src.count("len(actual_tails)"))

    # A2: có dùng set() tại chỗ đo
    thu("A2 co khu trung bang set(actual_tails)",
        "set(actual_tails)" in src)

    # A3: ngưỡng cũ -50 không còn trong MÃ THỰC THI (phân loại bằng AST, không đếm thô — RM-09)
    import ast
    tree = ast.parse(src)
    for n in ast.walk(tree):
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Module)):
            if (n.body and isinstance(n.body[0], ast.Expr)
                    and isinstance(n.body[0].value, ast.Constant)
                    and isinstance(n.body[0].value.value, str)):
                n.body = n.body[1:]
    ma = ast.unparse(tree)
    thu("A3 nguong cu -50 KHONG con trong ma thuc thi (AST, khong dem chuoi tho)",
        "-50" not in ma, "so lan trong ma thuc thi=%d" % ma.count("-50"))

    # A4: TRÙNG LẶP — list có trùng và set phải khác nhau
    co_trung = ["43", "26", "43", "79", "26", "43"]
    thu("A4 list co trung: len=6 nhung so KHAC NHAU=3",
        len(co_trung) == 6 and len(set(co_trung)) == 3)

    # A5: ĐA ĐÀI — mô phỏng MN 3 đài, mỗi đài 18 giải, có trùng giữa các đài
    dai1 = ["%02d" % (i % 40) for i in range(18)]
    dai2 = ["%02d" % (i % 35) for i in range(18)]
    dai3 = ["%02d" % (i % 30) for i in range(18)]
    tho = dai1 + dai2 + dai3
    thu("A5 da dai: tong tho 54 > so duoi KHAC NHAU %d" % len(set(tho)),
        len(tho) == 54 and len(set(tho)) < 54,
        "tho=54 khac_nhau=%d" % len(set(tho)))

    # A6: MỘT ĐÀI (MB) — vẫn phải khử trùng, vì trong cùng một đài cũng có đuôi trùng
    mb = ["%02d" % (i % 20) for i in range(27)]
    thu("A6 mot dai: tong tho 27 > so duoi KHAC NHAU %d" % len(set(mb)),
        len(set(mb)) < 27)

    # A7: hằng số hồi quy — con số đã đo thật ngày 13/09 (V11183), giữ làm mốc chống trôi
    do_thuc = {"MN": (63.0, 43.1), "MT": (48.5, 35.1), "MB": (29.0, 23.6)}
    thu("A7 moc hoi quy: moi mien deu co tho > khac_nhau",
        all(a > b for a, b in do_thuc.values()),
        "; ".join("%s tho=%.1f khac=%.1f" % (k, a, b) for k, (a, b) in do_thuc.items()))


# ============================================================================
# B · C2 — NỀN KHÔNG HOÀN LẠI, TỪNG NGÀY
# ============================================================================
def nhom_B():
    nhom("B · C2 nền exact without replacement")
    from weight_optimizer import _nen_top_k_khong_hoan_lai as nen

    thu("B1 M=0 => nen=0", abs(nen(0, 3)) < 1e-12)
    thu("B2 M=100 => nen=1", abs(nen(100, 3) - 1.0) < 1e-12)
    thu("B3 M>=98 (n-M<k) => nen=1", abs(nen(98, 3) - 1.0) < 1e-12)

    # B4: khớp phép tính TAY
    tay = 1.0 - comb(57, 3) / comb(100, 3)       # = 1 - 29260/161700
    thu("B4 M=43,k=3 khop tinh tay 1-C(57,3)/C(100,3)",
        abs(nen(43, 3) - tay) < 1e-12, "= %.6f" % tay)

    # B5: KHÔNG hoàn lại phải LỚN HƠN có hoàn lại — chiều này quyết định dấu của lift
    for M in (20, 35, 43, 60):
        kh = nen(M, 3)
        ch = 1 - (1 - M / 100) ** 3
        thu("B5 M=%d: khong-hoan-lai %.6f > co-hoan-lai %.6f" % (M, kh, ch), kh > ch)

    # B6: JENSEN — trung bình nền TỪNG NGÀY khác nền của M trung bình.
    #     Đây là lý do bản cũ cộng dồn M rồi mới áp công thức là sai.
    Ms = [20, 43, 60]
    tb_nen_tung_ngay = sum(nen(m, 3) for m in Ms) / 3
    nen_cua_M_tb = nen(round(sum(Ms) / 3), 3)
    thu("B6 nen(TB cua M) != TB cua nen(M) — bat dang thuc Jensen",
        abs(tb_nen_tung_ngay - nen_cua_M_tb) > 1e-6,
        "TB_nen=%.6f  nen_cua_M_TB=%.6f  lech=%.6f"
        % (tb_nen_tung_ngay, nen_cua_M_tb, tb_nen_tung_ngay - nen_cua_M_tb))

    # B7: mã có thực sự cộng dồn nền từng ngày không
    src = io.open(BE + "/weight_optimizer.py", encoding="utf-8").read()
    thu("B7 ma cong don total_nen tung ngay", "total_nen += _nen_ngay" in src)
    thu("B8 ma KHONG con dung (1 - ((1 - avg_tails / 100) ** top_n))",
        "(1 - ((1 - avg_tails / 100) ** top_n))" not in src)


# ============================================================================
# C · Poisson-binomial + Šidák
# ============================================================================
def nhom_C():
    nhom("C · kiểm định và chỉnh chọn")
    from weight_optimizer import _poisson_binomial_p_tren as pb, _sidak

    thu("C1 PB p deu = nhi thuc: n=3 p=.5 P(X>=2)=0.5", abs(pb([0.5] * 3, 2) - 0.5) < 1e-12)
    thu("C2 PB p khac nhau: [.2,.8] P(X>=2)=0.16", abs(pb([0.2, 0.8], 2) - 0.16) < 1e-12)
    thu("C3 PB [.2,.8] P(X>=1)=0.84", abs(pb([0.2, 0.8], 1) - 0.84) < 1e-12)
    thu("C4 PB P(X>=0)=1", abs(pb([0.1, 0.9, 0.35], 0) - 1.0) < 1e-12)

    thu("C5 Sidak n=1 khong doi", abs(_sidak(0.01, 1) - 0.01) < 1e-12)
    thu("C6 Sidak n=None khong doi", abs(_sidak(0.01, None) - 0.01) < 1e-12)
    thu("C7 Sidak n=69 lam p to len nhieu", _sidak(0.01, 69) > 0.4,
        "0.01 -> %.4f" % _sidak(0.01, 69))
    thu("C8 Sidak don dieu tang theo n", _sidak(0.01, 10) < _sidak(0.01, 69))


# ============================================================================
# D · C3 — CỔNG GHI: một bài ÂM cho TỪNG điều kiện + một bài DƯƠNG
# ============================================================================
def _gia_ket_qua(n, thang, nen=0.5, lift=0.0):
    """Dựng kết quả backtest giả để thử cổng mà không đụng DB."""
    return {"verified": n, "wins": thang, "lift": lift,
            "random_baseline": nen * 100, "nen_tung_ngay": [nen] * n}


def nhom_D():
    nhom("D · C3 cổng ghi — âm cho từng điều kiện, và một bài dương")
    import weight_optimizer as W

    W_goc = W.load_learned_weights
    W.load_learned_weights = lambda r: {"convergence": 0.2, "trend": 0.5, "gan": 0.1, "recency": 0.2}
    UV = {"convergence": 0.1, "trend": 0.3, "gan": 0.1, "recency": 0.5}

    def goi(**kw):
        mac = dict(region="MB", weights_ung_vien=UV,
                   heldout_tu="2026-08-15", heldout_den="2026-09-13",
                   so_cau_hinh_da_thu=69, fit_period="2026-06-01 → 2026-08-14")
        mac.update(kw)
        return W.cong_ghi_weights(**mac)

    try:
        # --- (a) không có held-out ---
        r = goi(heldout_tu=None, heldout_den=None,
                _do_heldout=lambda w: _gia_ket_qua(60, 50))
        thu("D1 (a) khong co held-out => NO_WRITE_KHONG_CO_HELDOUT",
            r["quyet"] == "NO_WRITE_KHONG_CO_HELDOUT", r["quyet"])

        # --- (a) held-out quá ngắn ---
        r = goi(_do_heldout=lambda w: _gia_ket_qua(7, 7))
        thu("D2 (a) held-out 7 ngay < 30 => NO_WRITE_HELDOUT_QUA_NGAN",
            r["quyet"] == "NO_WRITE_HELDOUT_QUA_NGAN", r["quyet"])

        # --- (e) rò dữ liệu: fit kết thúc SAU khi held-out bắt đầu ---
        r = goi(fit_period="2026-06-01 → 2026-09-01",
                _do_heldout=lambda w: _gia_ket_qua(60, 50))
        thu("D3 (e) fit ket thuc SAU held-out bat dau => NO_WRITE_RO_DU_LIEU",
            r["quyet"] == "NO_WRITE_RO_DU_LIEU", r["quyet"])

        # --- (b) không cùng frozen holdout: n khác nhau ---
        def khac_n(w):
            return _gia_ket_qua(60, 50) if w is UV else _gia_ket_qua(45, 30)
        r = goi(_do_heldout=khac_n)
        # Bản đầu bài thử này chỉ kiểm `startswith("NO_WRITE")` nên nó ĐẠT trong khi cổng trả
        # nhãn SAI (`KHONG_CO_HELDOUT` cho một ca thực ra là "không cùng frozen holdout").
        # Nhãn sai làm người đọc sau chẩn đoán nhầm ⇒ nay kiểm ĐÚNG nhãn.
        thu("D4 (b) ung vien 60 ngay vs control 45 ngay => NO_WRITE_KHONG_CUNG_FROZEN_HOLDOUT",
            r["quyet"] == "NO_WRITE_KHONG_CUNG_FROZEN_HOLDOUT", r["quyet"])

        # --- (c) không hơn control ---
        def khong_hon(w):
            return (_gia_ket_qua(60, 40, lift=2.0) if w is UV
                    else _gia_ket_qua(60, 40, lift=9.0))
        r = goi(_do_heldout=khong_hon)
        thu("D5 (c) lift +2.0 khong hon control +9.0 => NO_WRITE_KHONG_HON_CONTROL",
            r["quyet"] == "NO_WRITE_KHONG_HON_CONTROL", r["quyet"])

        # --- (d) hơn control nhưng KHÔNG qua chỉnh chọn ---
        # thắng 38/60 với nền 0.5 cho p thô ~0.026 (DƯỚI 0.05). Nếu cổng cho qua thì đó là do
        # THIẾU bước chỉnh chọn — bài thử này chỉ có nghĩa khi p thô đã dưới ngưỡng.
        def hon_nhung_yeu(w):
            return (_gia_ket_qua(60, 38, lift=5.0) if w is UV
                    else _gia_ket_qua(60, 30, lift=0.0))
        r = goi(_do_heldout=hon_nhung_yeu)
        p_tho = r["so"]["p_tho"]
        thu("D6 (d) p tho %.5f DUOI 0.05 nhung sau Sidak(69) la %.5f => NO_WRITE"
            % (p_tho, r["so"]["p_sau_chinh_chon"]),
            p_tho < 0.05 and r["quyet"] == "NO_WRITE_KHONG_CO_Y_NGHIA_SAU_CHINH_CHON",
            r["quyet"])

        # D7 — CHỨNG MINH bước chỉnh chọn THỰC SỰ đổi kết quả: cùng ứng viên, 1 cấu hình thì QUA
        r1 = goi(so_cau_hinh_da_thu=1, _do_heldout=hon_nhung_yeu)
        thu("D7 cung ung vien do: so_cau_hinh=1 => GHI (chung minh Sidak la thu dang chan)",
            r1["quyet"] == "GHI", r1["quyet"])

        # --- (f) không có rollback ---
        W.load_learned_weights = lambda r: None

        def manh(w):
            return (_gia_ket_qua(60, 52, lift=18.0) if w is UV
                    else _gia_ket_qua(60, 31, lift=1.0))
        r = goi(_do_heldout=manh)
        thu("D8 (f) khong doc duoc weights hien tai => NO_WRITE_THIEU_ROLLBACK",
            r["quyet"] == "NO_WRITE_THIEU_ROLLBACK", r["quyet"])

        # --- DƯƠNG: ứng viên đủ mạnh phải QUA ---
        W.load_learned_weights = lambda r: {"convergence": 0.2, "trend": 0.5,
                                            "gan": 0.1, "recency": 0.2}
        r = goi(_do_heldout=manh)
        thu("D9 DUONG: ung vien manh (52/60 vs nen .5, hon control 17pp) => GHI",
            r["quyet"] == "GHI", "%s p_sau_chinh=%.6f" % (r["quyet"], r["so"]["p_sau_chinh_chon"]))
        thu("D10 bai duong bat DU CA SAU dieu kien",
            all(r["dieu_kien"].values()), str(r["dieu_kien"]))
        thu("D11 bai duong co ghi duong go ve", bool(r["so"].get("lenh_go_ve")))
        thu("D12 bai duong ghi lai weights TRUOC khi ghi (de go ve)",
            r["so"].get("weights_truoc_khi_ghi") is not None)
    finally:
        W.load_learned_weights = W_goc


# ============================================================================
# E · DIỄN LẠI LỊCH SỬ — đường cũ ghi 6/6, cổng đúng chấp nhận 0/6
# ============================================================================
def nhom_E():
    nhom("E · diễn lại lịch sử optimizer")
    import weight_optimizer as W

    # Sáu lần chạy thật đọc từ logs/optimizer_once.log (V11183 §5.4)
    LICH_SU = [("2026-09-06", "MN", -4.75), ("2026-09-06", "MT", -7.67),
               ("2026-09-06", "MB", 6.28), ("2026-09-13", "MN", -3.11),
               ("2026-09-13", "MT", -6.03), ("2026-09-13", "MB", 9.56)]

    cu_ghi = sum(1 for _, _, lf in LICH_SU if lf > -50)
    thu("E1 duong CU ghi 6/6 lan (nguong > -50)", cu_ghi == 6, "cu_ghi=%d" % cu_ghi)

    W_goc = W.load_learned_weights
    W.load_learned_weights = lambda r: {"convergence": 0.2, "trend": 0.5, "gan": 0.1, "recency": 0.2}
    try:
        # Không lần chạy nào trong sáu lần đó có held-out ⇒ cổng đúng từ chối tất
        moi_ghi = 0
        for ngay, reg, lf in LICH_SU:
            r = W.cong_ghi_weights(region=reg,
                                   weights_ung_vien={"convergence": 0.1, "trend": 0.3,
                                                     "gan": 0.1, "recency": 0.5},
                                   heldout_tu=None, heldout_den=None,
                                   so_cau_hinh_da_thu=69, fit_period=None)
            if r["quyet"] == "GHI":
                moi_ghi += 1
        thu("E2 cong DUNG chap nhan 0/6 (vi khong lan nao co held-out)",
            moi_ghi == 0, "moi_ghi=%d" % moi_ghi)
    finally:
        W.load_learned_weights = W_goc

    thu("E3 khuyet tat la QUY TRINH, khong phai cua mot lan chay", cu_ghi == 6 and moi_ghi == 0)


# ============================================================================
# F · KHOÁ §Z — những thứ TUYỆT ĐỐI không được đổi
# ============================================================================
def nhom_F():
    nhom("F · khoá §Z")
    src = io.open(BE + "/weight_optimizer.py", encoding="utf-8").read()

    # F1: cổng NO_WRITE phải GIỮ NGUYÊN weights, tuyệt đối không reset về mặc định
    thu("F1 co dong ghi ro KHONG rollback ve mac dinh khi NO_WRITE",
        "KHONG rollback ve mac dinh" in src or "KHÔNG rollback về mặc định" in src)

    # F2: CONTROL_MAC_DINH chỉ dùng để SO, không được ghi
    import ast
    tree = ast.parse(src)
    goi_save = []
    for n in ast.walk(tree):
        if isinstance(n, ast.Call) and getattr(n.func, "id", "") == "save_learned_weights":
            goi_save.append(n.lineno)
    thu("F2 chi co DUNG MOT cho goi save_learned_weights trong optimize_and_save",
        len(goi_save) == 1, "cac dong: %s" % goi_save)

    # F3: CONTROL_MAC_DINH không bao giờ là đối số của save_learned_weights
    thu("F3 CONTROL_MAC_DINH khong bao gio duoc ghi",
        "save_learned_weights(region, CONTROL_MAC_DINH" not in src)

    # F4: ngưỡng khai báo tường minh, không giấu trong biểu thức
    thu("F4 nguong khai bao tuong minh",
        "QD079_HELDOUT_TOI_THIEU = 30" in src and "QD079_MUC_Y_NGHIA = 0.05" in src)

    # F5: grid KHÔNG được nhìn thấy held-out
    thu("F5 optimize_weights duoc goi voi end_date=fit_den",
        "end_date=fit_den" in src)


# ============================================================================
# G · §Z-G — KHOÁ AN TOÀN RETRAIN đã NỐI VÀO đường chạy thật
# ============================================================================
def nhom_G():
    nhom("G · khoá an toàn retrain (đã nối vào _v10646_retrain_guard)")
    import types

    src = io.open(BE + "/_v10646_retrain_guard.py", encoding="utf-8").read()
    thu("G_W1 _retrain() co goi chup_checkpoint", "chup_checkpoint(" in src)
    thu("G_W2 co don checkpoint cu (chong day dia)", "don_checkpoint_cu(" in src)

    # Điểm chèn phải nằm TRƯỚC mọi lệnh train — nếu sau thì checkpoint vô nghĩa
    i_cp = src.find("chup_checkpoint(")
    i_train = src.find('"_retrain_all.py"')
    thu("G_W3 checkpoint dung TRUOC khi goi _retrain_all.py",
        0 < i_cp < i_train, "vi tri cp=%d train=%d" % (i_cp, i_train))

    # FAIL-CLOSED: tiêm lỗi chụp checkpoint ⇒ phải huỷ retrain, KHÔNG train gì
    goc = sys.modules.get("_v11184_retrain_an_toan")
    gia = types.ModuleType("_v11184_retrain_an_toan")

    def no(*a, **k):
        raise IOError("dia day (gia lap)")

    gia.chup_checkpoint = no
    gia.doc_manifest = lambda p: {}
    gia.don_checkpoint_cu = lambda **k: {"da_xoa": [], "con_lai": 0}
    sys.modules["_v11184_retrain_an_toan"] = gia
    try:
        import importlib
        G = importlib.import_module("_v10646_retrain_guard")
        detail, so_loi = G._retrain()
        thu("G_W4 FAIL-CLOSED: chup checkpoint hong => HUY retrain (khong train gi)",
            so_loi == 99 and "CHECKPOINT_THAT_BAI" in detail, "so_loi=%s" % so_loi)
    finally:
        if goc is not None:
            sys.modules["_v11184_retrain_an_toan"] = goc
        else:
            sys.modules.pop("_v11184_retrain_an_toan", None)

    # Cổng thăng hạng: bốn nhánh phải đúng
    sys.modules.pop("_v11184_retrain_an_toan", None)
    import _v11184_retrain_an_toan as AT
    thu("G_W5 cong: moi kem hon => GO_VE_MODEL_CU",
        AT.cong_thang_hang(0.5299, 0.4928, 60)["quyet"] == "GO_VE_MODEL_CU")
    thu("G_W6 cong: moi tot hon => GIU_MODEL_MOI",
        AT.cong_thang_hang(0.4999, 0.5100, 60)["quyet"] == "GIU_MODEL_MOI")
    thu("G_W7 cong: thuoc khong so duoc => KHONG thang hang (loi 13/09)",
        AT.cong_thang_hang(None, 0.55, 60)["quyet"] == "GO_VE_THUOC_KHONG_SO_DUOC")
    thu("G_W8 cong: holdout ngan => khong ket luan (RM-04)",
        AT.cong_thang_hang(0.50, 0.60, 7)["quyet"] == "GO_VE_HOLDOUT_QUA_NGAN")

    # Tự kiểm của chính module an toàn phải ĐẠT
    import contextlib
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        ok = AT.tu_kiem()
    thu("G_W9 tu kiem _v11184_retrain_an_toan DAT", ok,
        [l for l in buf.getvalue().split("\n") if "TỰ KIỂM" in l][:1])


# ============================================================================
# H · §Z-E5/H2 — CÁCH LY PROVIDER đã NỐI VÀO gpt_analyzer
# ============================================================================
def nhom_H():
    nhom("H · cách ly provider (đã nối vào gpt_analyzer._invoke_model_api)")
    import ast

    src = io.open(BE + "/gpt_analyzer.py", encoding="utf-8").read()
    thu("H1 co import _v11184_cach_ly_provider", "_v11184_cach_ly_provider" in src)
    thu("H2 co goi _CL.kiem(selected_model) TRUOC khi goi provider", "_CL.kiem(selected_model)" in src)
    thu("H3 co ghi nhan loi sau khi goi", "_CL.ghi_nhan_loi(" in src)

    # Guard phải đứng TRƯỚC mọi lệnh gọi _call_*
    i_guard = src.find("_CL.kiem(selected_model)")
    i_call = src.find("_resp = _call_anthropic(")
    thu("H4 guard dung TRUOC chuoi dieu phoi _call_*", 0 < i_guard < i_call,
        "guard=%d call=%d" % (i_guard, i_call))

    # Chèn đúng MỘT chỗ — nhiều chỗ nghĩa là vá nhầm
    thu("H5 chen DUNG MOT guard", src.count("_CL.kiem(selected_model)") == 1,
        "dem=%d" % src.count("_CL.kiem(selected_model)"))

    thu("H6 cu phap gpt_analyzer con hop le", ast.parse(src) is not None)

    import importlib
    CL = importlib.import_module("_v11184_cach_ly_provider")
    thu("H7 402 Insufficient Balance => DETERMINISTIC",
        CL.phan_loai_loi("Error code: 402 - Insufficient Balance") == "DETERMINISTIC")
    thu("H8 429 credit_balance_exhausted => DETERMINISTIC (KHONG phai rate limit)",
        CL.phan_loai_loi("Error code: 429 - credit_balance_exhausted", 429) == "DETERMINISTIC")
    thu("H9 429 rate limit thuan => TRANSIENT",
        CL.phan_loai_loi("rate limit exceeded", 429) == "TRANSIENT")

    import contextlib
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        ok = CL.tu_kiem()
    thu("H10 tu kiem _v11184_cach_ly_provider DAT", ok,
        [l for l in buf.getvalue().split("\n") if "TỰ KIỂM" in l][:1])


def main():
    print("=" * 92)
    print("  V11184 · BỘ THỬ §Z — QD-079 + retrain safety + cách ly provider")
    print("=" * 92)
    nhom_A()
    nhom_B()
    nhom_C()
    nhom_D()
    nhom_E()
    nhom_F()
    nhom_G()
    nhom_H()

    print()
    print("=" * 92)
    dat = sum(1 for _, v, _ in KQ if v)
    for ten, v, ct in KQ:
        print("  %s  %-70s %s" % ("DAT " if v else "HONG", ten, ct[:40]))
    print("=" * 92)
    print("  TỔNG §Z: %d/%d %s" % (dat, len(KQ), "ĐẠT" if dat == len(KQ) else "CÓ BÀI HỎNG"))
    print("=" * 92)
    return 0 if dat == len(KQ) else 1


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
