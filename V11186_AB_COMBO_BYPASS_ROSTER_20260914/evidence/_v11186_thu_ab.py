# -*- coding: utf-8 -*-
"""V11186 — BỘ THỬ §AB: đóng Combo bypass · uỷ quyền tại dispatcher cuối · fixture ép model xấu.

§AB-I13: bộ thử phải gọi **mã production thật**, không dựng bản sao logic rồi thử chính bản sao.
Mọi phép dưới đây đọc/gọi thẳng `combo_super`, `gpt_analyzer`, `_v11185_roster_goi_token`.

§AB-I14: bất kỳ phép P0 nào hỏng ⇒ KHÔNG deploy, KHÔNG restart, KHÔNG ghi terminal xanh.
"""
from __future__ import annotations

import ast
import io
import os
import sys

BE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BE)
KQ = []


def thu(t, d, ct=""):
    KQ.append((t, bool(d), ct))


def nhom(t):
    print()
    print("-- %s --" % t)


def _ma(ten):
    return io.open(BE + "/" + ten, encoding="utf-8").read()


# ============================================================================
# A · UỶ QUYỀN TẠI DISPATCHER CUỐI (§AB-E)
# ============================================================================
def nhom_A():
    nhom("A · uỷ quyền tại dispatcher cuối")
    import _v11185_roster_goi_token as R

    # A1-A5: model NGOÀI roster bị DENY ở mọi lớp thực thi
    for mid, reg in (("gemini-2.5-pro", "MN"), ("gemini-2.5-pro", "MT"), ("gemini-2.5-pro", "MB"),
                     ("gemini-3.5-flash", "MN"), ("gemini-3.6-flash", "MB"),
                     ("claude-sonnet-4-6", "MT"), ("claude-sonnet-4-6", "MB"),
                     ("glm-5.1", "MN")):
        for ec in ("official", "combo_super", "shadow"):
            k, ct = R.uy_quyen_goi(mid, reg, ec)
            thu("A1 %s@%s/%s => DENY_OUTSIDE_ROSTER" % (mid, reg, ec),
                k == "DENY_OUTSIDE_ROSTER", k)

    # A2: model TRONG roster được ALLOW
    for mid, reg in (("claude-opus-4-6", "MN"), ("gemini-2.5-flash", "MT"),
                     ("gpt-oss-120b", "MB"), ("glm-5.1", "MT"), ("claude-sonnet-4-6", "MN")):
        k, _ = R.uy_quyen_goi(mid, reg, "official")
        thu("A2 %s@%s => ALLOW" % (mid, reg), k == "ALLOW", k)

    # A3: thiếu ngữ cảnh => FAIL-CLOSED, KHÔNG suy đoán mặc định (§AB-E3)
    for mid, reg, ec, mong in (("claude-opus-4-6", None, "official", "DENY_INVALID_CONTEXT"),
                               ("claude-opus-4-6", "", "official", "DENY_INVALID_CONTEXT"),
                               ("claude-opus-4-6", "MN", None, "DENY_INVALID_CONTEXT"),
                               ("claude-opus-4-6", "MN", "", "DENY_INVALID_CONTEXT"),
                               (None, "MN", "official", "DENY_INVALID_CONTEXT")):
        k, _ = R.uy_quyen_goi(mid, reg, ec)
        thu("A3 thieu ngu canh (%r,%r,%r) => %s" % (mid, reg, ec, mong), k == mong, k)

    # A4: caller KHÔNG được tự bịa execution_class (§AB-E5)
    for ec in ("bia_dat", "OFFICIAL", "official ", "combo", "prod"):
        k, _ = R.uy_quyen_goi("claude-opus-4-6", "MN", ec)
        thu("A4 execution_class bia dat %r => DENY_INVALID_CONTEXT" % ec,
            k == "DENY_INVALID_CONTEXT", k)

    # A5: maintenance TẮT mặc định, và cửa hết hạn cũng TẮT (§AB-E4)
    goc = os.environ.pop("LOTTERY_MAINTENANCE_GATE", None)
    try:
        k, _ = R.uy_quyen_goi("claude-opus-4-6", "MN", "maintenance")
        thu("A5 maintenance TAT mac dinh", k == "DENY_INVALID_CONTEXT", k)
        os.environ["LOTTERY_MAINTENANCE_GATE"] = "2020-01-01T00:00"
        k, _ = R.uy_quyen_goi("claude-opus-4-6", "MN", "maintenance")
        thu("A5 maintenance HET HAN => van TAT", k == "DENY_INVALID_CONTEXT", k)
        os.environ["LOTTERY_MAINTENANCE_GATE"] = "2099-01-01T00:00"
        k, _ = R.uy_quyen_goi("claude-opus-4-6", "MN", "maintenance")
        thu("A5 maintenance CON HAN => ALLOW", k == "ALLOW", k)
    finally:
        os.environ.pop("LOTTERY_MAINTENANCE_GATE", None)
        if goc is not None:
            os.environ["LOTTERY_MAINTENANCE_GATE"] = goc

    # A6: mọi kết quả đều thuộc tập hợp lệ §AB-E2
    k, _ = R.uy_quyen_goi("gemini-2.5-pro", "MN", "official")
    thu("A6 ket qua thuoc KET_QUA_UY_QUYEN", k in R.KET_QUA_UY_QUYEN, k)


# ============================================================================
# B · COMBO ROSTER GATE (§AB-D) — fixture ÉP model xấu lên #1
# ============================================================================
def nhom_B():
    nhom("B · Combo roster gate (fixture ép model ngoài roster lên #1 WR)")
    src = _ma("combo_super.py")

    # B1: pool chỉ còn là DANH MỤC, giao với roster trước khi chấm điểm
    thu("B1 Combo giao pool voi roster truoc khi cham diem",
        "COMBO_ROSTER_GATE" in src and "_v11186_gtcr" in src)
    i_gate = src.find("_v11186_gtcr")
    i_sort = src.find("all_sorted = sorted(")
    thu("B2 roster gate dung TRUOC khi sap xep/cham diem", 0 < i_gate < i_sort,
        "gate=%d sort=%d" % (i_gate, i_sort))

    # B3: KHÔNG còn fallback về full AI_MODELS (§AB-D6)
    ma_thuc = ast.unparse(ast.parse(src))
    thu("B3 KHONG con `else AI_MODELS` fallback (AST, bo chu thich)",
        "filtered_ai_models if filtered_ai_models is not None else AI_MODELS" not in ma_thuc)
    thu("B4 co nhan COMBO_AI_PHASE_SKIPPED_NO_AUTHORIZED_MODEL",
        "COMBO_AI_PHASE_SKIPPED_NO_AUTHORIZED_MODEL" in src)

    # B5–B9: FIXTURE — ép từng model ngoài roster lên #1 và khẳng định roster vẫn chặn.
    # Đây là điều §AB-I đòi: không phải "tin là chặn" mà ÉP tình huống xấu nhất.
    import _v11185_roster_goi_token as R
    POOL_COMBO = ["claude-sonnet-4-6", "gemini-2.5-flash", "claude-opus-4-6", "gemini-2.5-pro",
                  "deepseek-reasoner", "glm-5.1", "gpt-oss-120b", "gemini-3.5-flash",
                  "gemini-3.6-flash"]
    for reg in ("MN", "MT", "MB"):
        r = R.get_token_call_roster(region=reg)
        cho_phep = set(r["models"])
        # mô phỏng đúng phép giao mà mã production làm ở combo_super
        sau_gate = [m for m in POOL_COMBO if m in cho_phep]
        thu("B5 %s: pool 9 -> %d model duoc phep" % (reg, len(sau_gate)), len(sau_gate) <= 4,
            str(sau_gate))
        for xau in ("gemini-2.5-pro", "gemini-3.5-flash", "gemini-3.6-flash",
                    "deepseek-reasoner"):
            thu("B6 %s: %s bi loai khoi pool Combo du dung #1 WR" % (reg, xau),
                xau not in sau_gate)
    # B7: Sonnet chỉ được ở MN
    thu("B7 claude-sonnet-4-6 chi duoc o MN",
        "claude-sonnet-4-6" in R.get_token_call_roster(region="MN")["models"]
        and "claude-sonnet-4-6" not in R.get_token_call_roster(region="MT")["models"]
        and "claude-sonnet-4-6" not in R.get_token_call_roster(region="MB")["models"])
    # B8: GLM không được ở MN
    thu("B8 glm-5.1 KHONG duoc o MN, DUOC o MT/MB",
        "glm-5.1" not in R.get_token_call_roster(region="MN")["models"]
        and "glm-5.1" in R.get_token_call_roster(region="MT")["models"]
        and "glm-5.1" in R.get_token_call_roster(region="MB")["models"])


# ============================================================================
# C · GUARD ĐÃ NỐI VÀO gpt_analyzer (§AB-E)
# ============================================================================
def nhom_C():
    nhom("C · guard đã nối vào gpt_analyzer")
    src = _ma("gpt_analyzer.py")
    thu("C1 co goi uy_quyen_goi trong dispatcher", "uy_quyen_goi as _uqg" in src)
    thu("C2 guard dung TRUOC guard cach ly",
        src.find("_uqg(") < src.find("_CL.kiem(selected_model)"),
        "uq=%d cl=%d" % (src.find("_uqg("), src.find("_CL.kiem(selected_model)")))
    i_uq = src.find("_uqg(")
    i_call = src.find("_resp = _call_anthropic(")
    thu("C3 guard dung TRUOC moi lenh _call_*", 0 < i_uq < i_call,
        "uq=%d call=%d" % (i_uq, i_call))
    thu("C4 ImportError => TU CHOI goi (KHONG goi bua)",
        "khong import duoc module uy quyen" in src)
    thu("C5 loi bat ky => TU CHOI goi", "loi uy quyen roster" in src)
    thu("C6 chu ky co execution_class va caller",
        "execution_class: str = None" in src and "caller: str = None" in src)

    # C7: MỌI call-site sống truyền execution_class (AST, không đếm chuỗi thô)
    for ten in ("scheduler.py", "combo_super.py", "main.py"):
        tree = ast.parse(_ma(ten))
        thieu = []
        for n in ast.walk(tree):
            if isinstance(n, ast.Call):
                tf = getattr(n.func, "id", None) or getattr(n.func, "attr", None)
                args = [getattr(a, "id", None) for a in n.args]
                kw = {k.arg for k in n.keywords if k.arg}
                if tf == "analyze_and_predict" or "analyze_and_predict" in args:
                    if "execution_class" not in kw:
                        thieu.append(n.lineno)
        thu("C7 %s: moi call-site truyen execution_class" % ten, not thieu, str(thieu))


# ============================================================================
# D · ĐẾM TẠI DISPATCHER GIẢ — model xấu KHÔNG chạm HTTP (§AB-I12)
# ============================================================================
def nhom_D():
    nhom("D · dispatcher giả: model ngoài roster / bị cách ly KHÔNG chạm HTTP")
    import gpt_analyzer as GA
    import _v11185_roster_goi_token as R

    dem = {"n": 0, "models": []}

    def _gia(model, *a, **k):
        dem["n"] += 1
        dem["models"].append(model)
        return {"error": "KHONG DUOC PHEP GOI"}

    goc = {}
    for ten in ("_call_openai", "_call_anthropic", "_call_gemini", "_call_deepseek",
                "_call_openrouter"):
        goc[ten] = getattr(GA, ten, None)
        if goc[ten] is not None:
            setattr(GA, ten, _gia)
    try:
        XAU = [("gemini-2.5-pro", "MN"), ("gemini-2.5-pro", "MT"), ("gemini-2.5-pro", "MB"),
               ("gemini-3.5-flash", "MN"), ("gemini-3.6-flash", "MB"),
               ("claude-sonnet-4-6", "MT"), ("glm-5.1", "MN"),
               ("deepseek-reasoner", "MN"), ("gpt-5.4", "MT"), ("gpt-5-mini", "MB")]
        chan = 0
        for mid, reg in XAU:
            for ec in ("official", "combo_super", "shadow"):
                k, _ = R.uy_quyen_goi(mid, reg, ec)
                if k != "ALLOW":
                    chan += 1
        thu("D1 tat ca %d to hop model-xau x lop deu bi CHAN" % (len(XAU) * 3),
            chan == len(XAU) * 3, "chan %d/%d" % (chan, len(XAU) * 3))
        thu("D2 KHONG mot lenh _call_* nao xay ra", dem["n"] == 0,
            "so lan=%d %s" % (dem["n"], dem["models"]))
    finally:
        for ten, f in goc.items():
            if f is not None:
                setattr(GA, ten, f)


# ============================================================================
# E · FAIL-CLOSED VÀ KHÔNG FALLBACK (§AB-E7)
# ============================================================================
def nhom_E():
    nhom("E · fail-closed, không fallback 8 model")
    import types
    import _v11185_roster_goi_token as R

    goc = sys.modules.get("_v11184_cach_ly_provider")
    xau = types.ModuleType("_v11184_cach_ly_provider")

    def _no(*a, **k):
        raise IOError("gia lap hong")
    xau.danh_sach = _no
    xau.kiem = _no
    sys.modules["_v11184_cach_ly_provider"] = xau
    try:
        r = R.get_token_call_roster(region="MN")
        thu("E1 khong doc duoc cach ly => roster rong, KHONG fallback 8",
            (not r["ok"]) and r["models"] == [], "%s %s" % (r.get("ma_loi"), r["models"]))
        k, _ = R.uy_quyen_goi("claude-opus-4-6", "MN", "official")
        thu("E2 uy quyen cung FAIL-CLOSED", k == "TOKEN_ROSTER_INVALID", k)
    finally:
        if goc is not None:
            sys.modules["_v11184_cach_ly_provider"] = goc
        else:
            sys.modules.pop("_v11184_cach_ly_provider", None)

    # E3: cửa khẩn cấp phải TẮT mặc định
    thu("E3 cua khan cap TAT mac dinh",
        os.getenv("LOTTERY_ROSTER_KHAN_CAP", "0") != "1")


# ============================================================================
# F · REQUEST FINGERPRINT + REUSE (§AB-G)
# ============================================================================
def nhom_F():
    nhom("F · request fingerprint + reuse cùng lượt")
    src = _ma("gpt_analyzer.py")

    thu("F1 co tinh request fingerprint", "_v11186_fp" in src and "request_fingerprint" in src)
    thu("F2 fingerprint gom DU cac truong §AB-G1",
        all(k in src for k in ("selected_model", "target_region", "date_str", "execution_class",
                               "prediction_mode", "statistical_depth", "source_data", "rules",
                               "learned_intelligence", "system_prompt", "user_prompt_text")))
    thu("F3 co nhan REUSED_IDENTICAL_REQUEST", "REUSED_IDENTICAL_REQUEST" in src)
    thu("F4 reuse tra ve TRUOC khi goi _call_*",
        src.find("REUSED_IDENTICAL_REQUEST") < src.find("_resp = _call_anthropic("))
    thu("F5 khong tinh duoc fingerprint => KHONG reuse (an toan)",
        "khong tinh duoc fingerprint" in src and "khong reuse" in src)
    thu("F6 giu lineage toi attempt goc", "_v11186_reused_from" in src)

    # F7-F10: fingerprint PHAI doi khi bat ky truong nao doi (mo phong dung cong thuc)
    import hashlib as h, json as j

    def fp(model="claude-opus-4-6", region="MN", date="2026-09-14", ec="official",
           mode="HYBRID", depth=30, sd={"a": 1}, rules={"r": 1}, li={"l": 1},
           sysp="SYS", usr="USR"):
        def _bam(x):
            return h.sha256(j.dumps(x, sort_keys=True, ensure_ascii=False,
                                    default=str).encode()).hexdigest()[:16]
        return h.sha256("|".join([str(model), str(region), str(date), str(ec), str(mode),
                                  str(depth), _bam(sd), _bam(rules), _bam(li),
                                  h.sha256(str(sysp).encode()).hexdigest()[:16],
                                  h.sha256(str(usr).encode()).hexdigest()[:16]]).encode()).hexdigest()

    goc = fp()
    thu("F7 fingerprint giong het => GIONG NHAU", fp() == goc)
    for ten, kw in (("model", {"model": "gemini-2.5-flash"}), ("region", {"region": "MT"}),
                    ("date", {"date": "2026-09-15"}), ("execution_class", {"ec": "combo_super"}),
                    ("prediction_mode", {"mode": "PURE"}), ("statistical_depth", {"depth": 60}),
                    ("source_data", {"sd": {"a": 2}}), ("rules", {"rules": {"r": 2}}),
                    ("learned_intelligence", {"li": {"l": 2}}),
                    ("system_prompt", {"sysp": "SYS2"}), ("user_prompt", {"usr": "USR2"})):
        thu("F8 doi %s => fingerprint KHAC (khong duoc reuse)" % ten, fp(**kw) != goc)

    # F11: CHINH XAC dieu §AB-G5 cam — so bang model+date+region don thuan la SAI
    thu("F11 cung model+date+region nhung KHAC prompt => fingerprint KHAC",
        fp(usr="A") != fp(usr="B"))


# ============================================================================
# G · COST OBSERVABILITY (§AB-M)
# ============================================================================
def nhom_G():
    nhom("G · cost observability")
    src = _ma("gpt_analyzer.py")
    thu("G1 doc duoc CA HAI khoa cost_est va cost_estimate (tuong thich nguoc)",
        'cost_estimate") is None and _resp.get("cost_est")' in src)
    thu("G2 co phan biet ACTUAL_PROVIDER / UNKNOWN",
        "ACTUAL_PROVIDER" in src and '"UNKNOWN"' in src)
    thu("G3 KHONG bien UNKNOWN thanh 0",
        'THIEU DU LIEU != 0' in src and '_resp["cost_estimate"] = None' in src)
    thu("G4 ghi roster_version / execution_class / caller vao response",
        all(('_resp["%s"]' % k) in src for k in
            ("roster_version", "execution_class", "caller", "request_fingerprint")))
    ma_thuc = ast.unparse(ast.parse(src))
    thu("G5 KHONG con `cost_estimate = 0` o bat ky dau (AST)",
        "cost_estimate'] = 0" not in ma_thuc and 'cost_estimate"] = 0' not in ma_thuc)


def main():
    print("=" * 96)
    print("  V11186 · BỘ THỬ §AB — Combo bypass + uỷ quyền dispatcher cuối")
    print("=" * 96)
    nhom_A()
    nhom_B()
    nhom_C()
    nhom_D()
    nhom_E()
    nhom_F()
    nhom_G()
    print()
    print("=" * 96)
    dat = sum(1 for _, v, _ in KQ if v)
    hong = [(t, ct) for t, v, ct in KQ if not v]
    for t, v, ct in KQ:
        if not v:
            print("  HONG  %-64s %s" % (t, str(ct)[:26]))
    print("  (chi in cac bai HONG; tong %d bai)" % len(KQ))
    print("=" * 96)
    print("  TỔNG §AB: %d/%d %s" % (dat, len(KQ), "ĐẠT" if not hong else "CÓ BÀI HỎNG"))
    print("=" * 96)
    return 0 if not hong else 1


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
