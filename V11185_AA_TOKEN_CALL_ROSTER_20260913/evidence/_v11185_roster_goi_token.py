# -*- coding: utf-8 -*-
"""V11185 §AA-C — TOKEN CALL ROSTER SSOT: chính sách được thi hành NGAY TRƯỚC mọi HTTP provider call.

VÌ SAO CÓ TỆP NÀY — đo được và Owner tự soi nguồn xác nhận (§AA):
  `scheduler.py:4017` `from model_registry import TOKEN_MODELS as AUTO_AI_MODELS`, rồi dùng THẲNG
  danh sách tĩnh đó ở SÁU chỗ quyết định gọi API:
      :4301 expected count · :4321 provider preflight · :4652 parallel prestart ·
      :4684 MAIN PROVIDER LOOP · :4874 diversity pass · :5793/:5808/:5813 MB rerun post-MT
  `get_expected_models(slot, region)` chỉ đang GHI LOG, không chặn gì.
  `allowed_regions` chặn được đường BỎ PHIẾU (`main.py:9720`) nhưng KHÔNG chặn đường GỌI.
⇒ Roster trước §AA là «danh sách chỉ lọc khi bỏ phiếu». Tệp này biến nó thành CHÍNH SÁCH GỌI.

NGUYÊN TẮC CỨNG:
  · `model_registry.MODEL_REGISTRY` vẫn là SSOT của INVENTORY (model nào tồn tại, thuộc tính gì).
    Tệp này là SSOT của CHÍNH SÁCH GỌI (model nào ĐƯỢC GỌI, ở miền nào, slot nào).
  · FAIL-CLOSED: đọc không được chính sách hoặc trạng thái cách ly ⇒ **KHÔNG gọi token nào**,
    ghi `TOKEN_ROSTER_INVALID`. TUYỆT ĐỐI KHÔNG fallback về toàn bộ 8 model — đó chính là hành vi
    §AA sinh ra để diệt.
  · KHÔNG tự lấp chỗ: một model bị cách ly thì roster miền đó NGẮN ĐI, không kéo model ngoài
    roster vào thế chỗ.
  · Historical-safe: đổi chính sách hôm nay KHÔNG được đổi cách đọc ngày cũ. Mọi bản ghi mới mang
    `roster_version`; replay lịch sử phải dùng snapshot đúng ngày, không dùng roster «hôm nay».
"""
from __future__ import annotations

import io
import json
import os
import sys

BE = os.path.dirname(os.path.abspath(__file__))
GOC = os.path.dirname(os.path.dirname(BE))

TOKEN_ROSTER_INVALID = "TOKEN_ROSTER_INVALID"
TRAN_MOI_MIEN = 4          # §AA khoá: tối đa 3 CORE + 1 CHALLENGER

# ============================================================================
# CHÍNH SÁCH — Owner duyệt §Z 13/09/2026 20:44 ICT, tái khẳng định §AA mục D
# ============================================================================
ROSTER_VERSION = "token_call_roster/2026.09.14-1"

_CHINH_SACH = {
    "_meta": {
        "roster_version": ROSTER_VERSION,
        "owner_approval_ref": "QD-080 · §Z khoá 2-6 (13/09/2026 20:44 ICT) · §AA mục D",
        "effective_from": "2026-09-14T00:00:00+07:00",
        "previous_version": None,          # đây là bản ĐẦU TIÊN của cơ chế này
        "previous_behaviour": ("model_registry.TOKEN_MODELS (8 direct-token LLM output-eligible) "
                               "dung THANG o moi call-site scheduler.py"),
        "rollback": ("python web/backend/_v11185_roster_goi_token.py --go-ve  "
                     "(dat _KHAN_CAP_DUNG_TOKEN_MODELS=1, khoi phuc hanh vi truoc §AA)"),
        "ghi_chu_bang_chung": ("replay V11184 tren cohort dong bang, loai ngay override: "
                               "MN -0.79pp · MT +0.72pp · MB -0.74pp, p=1.0000 ca ba. "
                               "DOC DUNG: cat mot nua direct LLM KHONG lam phat hien thay doi "
                               "chat luong — KHONG phai 'roster moi tot hon'."),
    },
    "MN": {
        "CORE": ["claude-opus-4-6", "gemini-2.5-flash", "gpt-oss-120b"],
        "CHALLENGER": ["claude-sonnet-4-6"],
    },
    "MT": {
        "CORE": ["claude-opus-4-6", "gemini-2.5-flash", "glm-5.1"],
        "CHALLENGER": ["gpt-oss-120b"],
    },
    "MB": {
        "CORE": ["claude-opus-4-6", "gemini-2.5-flash", "gpt-oss-120b"],
        "CHALLENGER": ["glm-5.1"],
    },
}

# Model CÓ trong registry nhưng KHÔNG được gọi tự động nữa (§AA mục D + F).
# Giữ nguyên registry và lịch sử — chỉ tắt khả năng ĐƯỢC GỌI, thuận nghịch.
NGOAI_ROSTER_GOI = {
    "gemini-2.5-pro": "khong con trong active call roster o bat ky mien nao (§AA D)",
    "claude-sonnet-4-6@MT": "chi la CHALLENGER cua MN",
    "claude-sonnet-4-6@MB": "chi la CHALLENGER cua MN",
    "glm-5.1@MN": "Gate 1 coverage 89.7% < 90 o MN; la CORE cua MT va CHALLENGER cua MB",
}

# Cửa chạy ngoại lệ — CHỈ để gỡ về khẩn cấp, mặc định TẮT.
_KHAN_CAP_DUNG_TOKEN_MODELS = os.getenv("LOTTERY_ROSTER_KHAN_CAP", "0") == "1"


def _doc_cach_ly():
    """Trạng thái cách ly provider. Trả `(tap_model, loi)` — `loi` khác None là FAIL-CLOSED."""
    try:
        sys.path.insert(0, BE)
        import _v11184_cach_ly_provider as CL
        return set(CL.danh_sach().keys()), None
    except Exception as e:
        return set(), "khong doc duoc trang thai cach ly: %r" % e


def _doc_registry():
    """Thuộc tính model từ inventory SSOT. `loi` khác None là FAIL-CLOSED."""
    try:
        sys.path.insert(0, BE)
        from model_registry import MODEL_REGISTRY
        return {m["id"]: m for m in MODEL_REGISTRY if isinstance(m, dict) and m.get("id")}, None
    except Exception as e:
        return {}, "khong doc duoc model_registry: %r" % e


def _hop_le_de_goi(mid, reg, slot, inv):
    """Model này có đủ tư cách được GỌI ở miền/slot này không? Trả `(bool, ly_do)`."""
    m = inv.get(mid)
    if not m:
        return False, "khong co trong model_registry"
    if m.get("status") in ("RETIRED", "REMOVED"):
        return False, "status=%s" % m.get("status")
    if m.get("class") != "TOKEN":
        return False, "class=%s (khong phai TOKEN)" % m.get("class")
    if m.get("role") != "GENERATOR":
        return False, "role=%s (khong phai GENERATOR)" % m.get("role")
    ar = m.get("allowed_regions") or []
    if reg and ar and reg not in ar:
        return False, "khong thuoc allowed_regions=%s" % ar
    if slot:
        ss = m.get("schedule_slots") or []
        if ss and slot not in ss:
            return False, "slot %r khong thuoc schedule_slots=%s" % (slot, ss)
    return True, "ok"


def get_token_call_roster(slot=None, region=None, execution_class="official",
                          include_challenger=True):
    """API canonical DUY NHẤT quyết định model nào được gọi provider.

    Trả dict:
        ok                bool — False nghĩa là FAIL-CLOSED, KHÔNG được gọi token nào
        ma_loi            `TOKEN_ROSTER_INVALID` khi ok=False
        models            [str] — danh sách ĐƯỢC GỌI, thứ tự ỔN ĐỊNH, tối đa 4, có thể ÍT HƠN
        core / challenger [str]
        loai_bo           [{model, vi_sao}] — vì sao từng model bị loại
        quarantined       [str]
        roster_version / effective_from / slot / region / execution_class

    KHÔNG BAO GIỜ trả về toàn bộ `TOKEN_MODELS` khi có lỗi. Thà không gọi còn hơn gọi bừa.
    """
    ra = {"ok": False, "ma_loi": None, "models": [], "core": [], "challenger": [],
          "loai_bo": [], "quarantined": [], "roster_version": ROSTER_VERSION,
          "effective_from": _CHINH_SACH["_meta"]["effective_from"],
          "slot": slot, "region": region, "execution_class": execution_class}

    if _KHAN_CAP_DUNG_TOKEN_MODELS:
        # Cửa gỡ về khẩn cấp. Ghi RÕ để không ai tưởng đây là hành vi bình thường.
        try:
            sys.path.insert(0, BE)
            from model_registry import TOKEN_MODELS
            ra.update({"ok": True, "models": list(TOKEN_MODELS), "core": list(TOKEN_MODELS),
                       "roster_version": "KHAN_CAP_PRE_AA",
                       "canh_bao": "LOTTERY_ROSTER_KHAN_CAP=1 — dang chay hanh vi TRUOC §AA"})
            return ra
        except Exception as e:
            ra["ma_loi"] = TOKEN_ROSTER_INVALID
            ra["ly_do"] = "khan cap nhung khong doc duoc TOKEN_MODELS: %r" % e
            return ra

    reg = (region or "").upper()
    if reg not in ("MN", "MT", "MB"):
        ra["ma_loi"] = TOKEN_ROSTER_INVALID
        ra["ly_do"] = "region %r khong hop le" % region
        return ra

    inv, loi_inv = _doc_registry()
    if loi_inv:
        ra["ma_loi"] = TOKEN_ROSTER_INVALID
        ra["ly_do"] = loi_inv
        return ra

    cl, loi_cl = _doc_cach_ly()
    if loi_cl:
        # FAIL-CLOSED: không xác minh được chính sách cách ly ⇒ không gọi token.
        ra["ma_loi"] = TOKEN_ROSTER_INVALID
        ra["ly_do"] = loi_cl
        return ra
    ra["quarantined"] = sorted(cl)

    cs = _CHINH_SACH.get(reg)
    if not cs or not cs.get("CORE"):
        ra["ma_loi"] = TOKEN_ROSTER_INVALID
        ra["ly_do"] = "khong co chinh sach roster cho mien %s" % reg
        return ra

    def _loc(ds, hang):
        giu = []
        for mid in ds:
            if mid in cl:
                ra["loai_bo"].append({"model": mid, "hang": hang,
                                      "vi_sao": "PROVIDER_QUARANTINED"})
                continue
            ok, ly_do = _hop_le_de_goi(mid, reg, slot, inv)
            if not ok:
                ra["loai_bo"].append({"model": mid, "hang": hang, "vi_sao": ly_do})
                continue
            if mid in giu:
                ra["loai_bo"].append({"model": mid, "hang": hang, "vi_sao": "TRUNG_LAP"})
                continue
            giu.append(mid)
        return giu

    core = _loc(list(cs.get("CORE") or []), "CORE")
    ch = _loc(list(cs.get("CHALLENGER") or []), "CHALLENGER") if include_challenger else []
    ch = [m for m in ch if m not in core]

    models = core + ch
    if len(models) > TRAN_MOI_MIEN:
        # KHÔNG im lặng cắt — đây là lỗi cấu hình, phải fail-closed.
        ra["ma_loi"] = TOKEN_ROSTER_INVALID
        ra["ly_do"] = ("chinh sach cho mien %s co %d model > tran %d — cau hinh SAI"
                       % (reg, len(models), TRAN_MOI_MIEN))
        return ra

    ra.update({"ok": True, "models": models, "core": core, "challenger": ch})
    return ra


def kiem_mot_model(model_id, region, slot=None, execution_class="official"):
    """Model này có được phép gọi ở miền/slot này không? Dùng làm tầng chặn thứ hai."""
    r = get_token_call_roster(slot=slot, region=region, execution_class=execution_class)
    if not r["ok"]:
        return False, r.get("ly_do") or TOKEN_ROSTER_INVALID
    if model_id in r["models"]:
        return True, "trong roster"
    return False, "NGOAI_ROSTER (roster %s = %s)" % (r["roster_version"], r["models"])


def anh_chup():
    """Ảnh chụp đầy đủ chính sách — để ghi vào manifest/trace và để gỡ về."""
    ra = {"_meta": dict(_CHINH_SACH["_meta"]), "mien": {}}
    for reg in ("MN", "MT", "MB"):
        r = get_token_call_roster(region=reg)
        ra["mien"][reg] = {"ok": r["ok"], "models": r["models"], "core": r["core"],
                           "challenger": r["challenger"], "loai_bo": r["loai_bo"]}
    ra["ngoai_roster_goi"] = dict(NGOAI_ROSTER_GOI)
    ra["quarantined"] = sorted(_doc_cach_ly()[0])
    import hashlib
    ra["config_sha256"] = hashlib.sha256(
        json.dumps(_CHINH_SACH, sort_keys=True, ensure_ascii=False).encode()).hexdigest()
    return ra


# ============================================================================
# TỰ KIỂM — RM-15
# ============================================================================
def tu_kiem():
    kq = []

    def thu(t, d, ct=""):
        kq.append((t, bool(d), ct))

    # R1-R3: thành viên đúng từng miền
    mong = {"MN": ["claude-opus-4-6", "gemini-2.5-flash", "gpt-oss-120b", "claude-sonnet-4-6"],
            "MT": ["claude-opus-4-6", "gemini-2.5-flash", "glm-5.1", "gpt-oss-120b"],
            "MB": ["claude-opus-4-6", "gemini-2.5-flash", "gpt-oss-120b", "glm-5.1"]}
    for reg, ms in mong.items():
        r = get_token_call_roster(region=reg)
        thu("R_%s thanh vien dung va DU 4" % reg, r["ok"] and r["models"] == ms,
            str(r["models"]))

    # R4: trần 4
    for reg in ("MN", "MT", "MB"):
        r = get_token_call_roster(region=reg)
        thu("R_tran_%s <= 4" % reg, len(r["models"]) <= TRAN_MOI_MIEN, str(len(r["models"])))

    # R5: thứ tự ỔN ĐỊNH
    a = get_token_call_roster(region="MN")["models"]
    b = get_token_call_roster(region="MN")["models"]
    thu("R_thu_tu_on_dinh", a == b)

    # R6: model NGOÀI roster bị từ chối
    for mid, reg in (("gemini-2.5-pro", "MN"), ("gemini-2.5-pro", "MT"),
                     ("gemini-2.5-pro", "MB"), ("claude-sonnet-4-6", "MT"),
                     ("claude-sonnet-4-6", "MB"), ("glm-5.1", "MN")):
        ok, ly = kiem_mot_model(mid, reg)
        thu("R_ngoai_roster %s@%s bi tu choi" % (mid, reg), not ok, ly[:38])

    # R7: model bị cách ly KHÔNG xuất hiện
    cl, _ = _doc_cach_ly()
    for reg in ("MN", "MT", "MB"):
        r = get_token_call_roster(region=reg)
        thu("R_cach_ly_%s khong lot" % reg, not (set(r["models"]) & cl),
            str(sorted(set(r["models"]) & cl)))

    # R8: region sai => FAIL-CLOSED, KHÔNG trả danh sách nào
    for bad in ("XX", "", None, "mn "):
        r = get_token_call_roster(region=bad)
        thu("R_region_sai %r => fail-closed, models rong" % bad,
            (not r["ok"]) and r["ma_loi"] == TOKEN_ROSTER_INVALID and r["models"] == [])

    # R9: include_challenger=False => chỉ CORE
    r = get_token_call_roster(region="MN", include_challenger=False)
    thu("R_chi_CORE tra 3 model", r["ok"] and len(r["models"]) == 3
        and "claude-sonnet-4-6" not in r["models"], str(r["models"]))

    # R10: ĐIỀU QUAN TRỌNG NHẤT — lỗi đọc cách ly phải FAIL-CLOSED, KHÔNG fallback 8 model
    goc = sys.modules.get("_v11184_cach_ly_provider")
    import types
    xau = types.ModuleType("_v11184_cach_ly_provider")

    def _no(*a, **k):
        raise IOError("gia lap hong")
    xau.danh_sach = _no
    sys.modules["_v11184_cach_ly_provider"] = xau
    try:
        r = get_token_call_roster(region="MN")
        thu("R_fail_closed khi khong doc duoc cach ly",
            (not r["ok"]) and r["ma_loi"] == TOKEN_ROSTER_INVALID and r["models"] == [],
            "%s models=%s" % (r["ma_loi"], r["models"]))
        thu("R_fail_closed KHONG fallback ve 8 model", len(r["models"]) == 0)
    finally:
        if goc is not None:
            sys.modules["_v11184_cach_ly_provider"] = goc
        else:
            sys.modules.pop("_v11184_cach_ly_provider", None)

    # R11: KHÔNG tự lấp chỗ khi một model bị cách ly
    import copy
    goc_cs = copy.deepcopy(_CHINH_SACH)
    try:
        globals()["_CHINH_SACH"]["MB"]["CORE"] = ["claude-opus-4-6", "deepseek-reasoner",
                                                 "gemini-2.5-flash"]
        r = get_token_call_roster(region="MB")
        thu("R_khong_lap_cho: mat 1 model thi roster NGAN DI (3 thay vi 4)",
            r["ok"] and len(r["models"]) == 3 and "deepseek-reasoner" not in r["models"],
            str(r["models"]))
        thu("R_khong_lap_cho: ghi ly do loai bo",
            any(x["model"] == "deepseek-reasoner" and x["vi_sao"] == "PROVIDER_QUARANTINED"
                for x in r["loai_bo"]))
        # R12: cấu hình quá trần => FAIL-CLOSED
        globals()["_CHINH_SACH"]["MB"]["CORE"] = ["claude-opus-4-6", "gemini-2.5-flash",
                                                  "gpt-oss-120b", "claude-sonnet-4-6"]
        globals()["_CHINH_SACH"]["MB"]["CHALLENGER"] = ["glm-5.1"]
        r = get_token_call_roster(region="MB")
        thu("R_qua_tran => fail-closed (KHONG im lang cat)",
            (not r["ok"]) and r["ma_loi"] == TOKEN_ROSTER_INVALID, str(r.get("ly_do"))[:44])
    finally:
        globals()["_CHINH_SACH"] = goc_cs

    # R13: ảnh chụp có đủ siêu dữ liệu bắt buộc (§AA C6)
    ac = anh_chup()
    for k in ("roster_version", "owner_approval_ref", "effective_from", "previous_version",
              "rollback"):
        thu("R_anh_chup co %s" % k, k in ac["_meta"])
    thu("R_anh_chup co config_sha256", bool(ac.get("config_sha256")))

    dat = sum(1 for _, v, _ in kq if v)
    print("=" * 96)
    print("  TỰ KIỂM _v11185_roster_goi_token: %d/%d" % (dat, len(kq)))
    print("=" * 96)
    for t, v, ct in kq:
        print("  %s  %-58s %s" % ("DAT " if v else "HONG", t, str(ct)[:32]))
    print("=" * 96)
    return dat == len(kq)


def main():
    if "--anh-chup" in sys.argv:
        print(json.dumps(anh_chup(), ensure_ascii=False, indent=1))
        return 0
    if "--go-ve" in sys.argv:
        print("GO VE: dat bien moi truong LOTTERY_ROSTER_KHAN_CAP=1 roi restart service.")
        print("  systemctl set-environment LOTTERY_ROSTER_KHAN_CAP=1 && systemctl restart lottery")
        print("Khi do roster tra ve hanh vi TRUOC §AA (toan bo TOKEN_MODELS).")
        print("Bo go ve: systemctl unset-environment LOTTERY_ROSTER_KHAN_CAP && systemctl restart lottery")
        return 0
    return 0 if tu_kiem() else 1


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
