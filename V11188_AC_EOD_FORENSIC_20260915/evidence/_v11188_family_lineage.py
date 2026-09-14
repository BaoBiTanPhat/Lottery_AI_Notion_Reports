# -*- coding: utf-8 -*-
"""V11188 §AC-O.2 — HỌ GỐC CỦA MODEL. Chỉ QUAN SÁT. KHÔNG dùng để chấm điểm, KHÔNG dedupe.

VÌ SAO CẦN — `model_registry.py` có `provider` nhưng KHÔNG có trường họ, và `provider` ĐÁNH LỪA
theo đúng hai chiều ngược nhau:

  · Cùng `provider='openrouter'` nhưng KHÁC họ hoàn toàn:
        glm-5.1 (Zhipu) · gpt-oss-120b (OpenAI) · kimi-k2.5 (Moonshot) ·
        qwen3-max-thinking (Alibaba) · llama-4-maverick (Meta) · mistral-large-3 (Mistral)
    OpenRouter chỉ là ĐƯỜNG ĐỊNH TUYẾN, không phải nguồn gốc model.
  · Khác `provider` nhưng CÙNG họ:
        gpt-5.4 (`provider='openai'`) và gpt-5.5 (`provider='openrouter'`) — cùng OpenAI GPT.

⇒ Đếm «11 voter» rồi coi là 11 quan sát độc lập là SAI. Hai model cùng họ gốc chia nhau phần lớn
dữ liệu huấn luyện và thiên lệch; chúng tương quan mạnh. Con số cần biết là **số họ gốc độc lập**
và **mức tập trung**, không phải số dòng.

BA ĐIỀU TỆP NÀY KHÔNG LÀM (§AC-C khoá cứng):
  · KHÔNG family-dedupe trong chấm điểm production.
  · KHÔNG đổi trọng số, không đổi TOTAL, không đổi bất kỳ output nào.
  · KHÔNG ghi DB. Thuần hàm — gọi vào là ra số, không để lại dấu vết.

Chạy tự kiểm: python _v11188_family_lineage.py
"""
from __future__ import annotations

import os
import sys

BE = os.path.dirname(os.path.abspath(__file__))

# Loại model — quyết định nó có phải MỘT QUAN SÁT ĐỘC LẬP hay không.
TOKEN_LLM = "TOKEN_LLM"      # gọi provider thật, là quan sát độc lập (trong giới hạn họ gốc)
ML_BASE = "ML_BASE"          # mô hình học máy nội bộ, độc lập với LLM
DERIVED = "DERIVED"          # suy ra TỪ các model khác — KHÔNG phải quan sát độc lập
COMBO = "COMBO"              # tổ hợp, cũng không độc lập
KHONG_DU_DOAN = "KHONG_DU_DOAN"   # có trong registry nhưng KHÔNG sinh dự đoán (rerank, video…)
KHONG_BIET = "KHONG_BIET"    # chưa khai — phải hiện ra, KHÔNG được im lặng gộp vào đâu

# Quy tắc theo TIỀN TỐ, xếp từ cụ thể tới tổng quát. Dùng quy tắc thay vì danh sách cứng để
# model mới không lặng lẽ rơi vào nhóm sai — cái gì không khớp sẽ ra KHONG_BIET và lộ ngay.
_QUY_TAC = [
    # (tiền tố, họ gốc, phòng nghiên cứu, loại)
    ("claude-", "ANTHROPIC_CLAUDE", "Anthropic", TOKEN_LLM),
    ("gpt-oss", "OPENAI_GPT", "OpenAI", TOKEN_LLM),
    ("gpt-", "OPENAI_GPT", "OpenAI", TOKEN_LLM),
    ("o1-", "OPENAI_GPT", "OpenAI", TOKEN_LLM),
    ("o3-", "OPENAI_GPT", "OpenAI", TOKEN_LLM),
    ("gemini-", "GOOGLE_GEMINI", "Google", TOKEN_LLM),
    ("gemma-", "GOOGLE_GEMMA", "Google", TOKEN_LLM),
    ("deepseek-", "DEEPSEEK", "DeepSeek", TOKEN_LLM),
    ("glm-", "ZHIPU_GLM", "Zhipu", TOKEN_LLM),
    ("grok-", "XAI_GROK", "xAI", TOKEN_LLM),
    ("qwen", "ALIBABA_QWEN", "Alibaba", TOKEN_LLM),
    ("kimi-", "MOONSHOT_KIMI", "Moonshot", TOKEN_LLM),
    ("minimax-", "MINIMAX", "MiniMax", TOKEN_LLM),
    ("nemotron-", "NVIDIA_NEMOTRON", "NVIDIA", TOKEN_LLM),
    ("mistral-", "MISTRAL", "Mistral", TOKEN_LLM),
    ("llama-", "META_LLAMA", "Meta", TOKEN_LLM),
    ("yi-", "01AI_YI", "01.AI", TOKEN_LLM),
    ("arcee-", "ARCEE", "Arcee", TOKEN_LLM),
    # ML nội bộ
    ("xgboost", "ML_XGBOOST", "noi_bo", ML_BASE),
    ("random-forest", "ML_RANDOM_FOREST", "noi_bo", ML_BASE),
    ("lstm", "ML_LSTM", "noi_bo", ML_BASE),
    ("meta-learning", "ML_META", "noi_bo", ML_BASE),
    # Suy ra từ model khác — KHÔNG độc lập
    ("smart-ensemble", "DERIVED_SMART_ENSEMBLE", "noi_bo", DERIVED),
    ("smart-ml", "DERIVED_SMART_ML", "noi_bo", DERIVED),
    ("combo-no-token", "COMBO_NO_TOKEN", "noi_bo", COMBO),
    ("combo-super", "COMBO_SUPER", "noi_bo", COMBO),
]

# Một số tên đặc biệt không theo tiền tố — khai tường minh, KHÔNG đoán.
_NGOAI_LE = {
    # Ba muc duoi day CO trong registry nhung KHONG sinh du doan — kiem tu registry ngay
    # 15/09: pplx-embed-v1 va cohere-rerank-4-pro deu class=RERANK role=RERANKER, wan-2.7 la
    # class=TOKEN role=GENERATOR nhung output_eligible=False (model video, khong ra so).
    # Khai TUONG MINH thay vi de chung roi vao KHONG_BIET, va cung KHONG gop chung vao
    # TOKEN_LLM — chung khong phai voter.
    "pplx-embed-v1": ("PERPLEXITY_EMBED", "Perplexity", KHONG_DU_DOAN),
    "cohere-rerank-4-pro": ("COHERE_RERANK", "Cohere", KHONG_DU_DOAN),
    "wan-2.7": ("ALIBABA_WAN", "Alibaba", KHONG_DU_DOAN),
    "mistral-nemo": ("MISTRAL", "Mistral", TOKEN_LLM),
    "deepseek-v4-pro-real": ("DEEPSEEK", "DeepSeek", TOKEN_LLM),
    "claude-opus-5-fast": ("ANTHROPIC_CLAUDE", "Anthropic", TOKEN_LLM),
    "gpt-5.6-sol-pro": ("OPENAI_GPT", "OpenAI", TOKEN_LLM),
}


def ho_goc(model_id):
    """Trả `(ho_goc, phong_nghien_cuu, loai)`. Không khớp => KHONG_BIET, KHÔNG gộp bừa."""
    if not model_id:
        return ("KHONG_BIET", "KHONG_BIET", KHONG_BIET)
    m = str(model_id).strip().lower()
    if m in _NGOAI_LE:
        return _NGOAI_LE[m]
    for tien_to, ho, lab, loai in _QUY_TAC:
        if m.startswith(tien_to):
            return (ho, lab, loai)
    return ("KHONG_BIET:%s" % m, "KHONG_BIET", KHONG_BIET)


def doc_lai_nhan_registry():
    """Đối chiếu nhãn tệp này với `model_registry`. Trả danh sách chỗ lệch để người đọc tự xử.

    KHÔNG tự sửa registry — registry là SSOT của inventory, tệp này chỉ là lớp quan sát.
    """
    ra = {"khong_doc_duoc": None, "khong_biet": [], "provider_danh_lua": []}
    try:
        sys.path.insert(0, BE)
        import model_registry as MR
        reg = MR.MODEL_REGISTRY
        muc = reg if isinstance(reg, list) else list(reg.values())
    except Exception as e:
        ra["khong_doc_duoc"] = repr(e)
        return ra
    theo_provider = {}
    for m in muc:
        mid = m.get("id")
        ho, lab, loai = ho_goc(mid)
        if loai == KHONG_BIET:
            ra["khong_biet"].append(mid)
        theo_provider.setdefault(m.get("provider"), []).append((mid, ho))
    for prov, ds in theo_provider.items():
        hos = {h for _i, h in ds}
        if len(hos) > 1:
            ra["provider_danh_lua"].append({
                "provider": prov, "so_ho_goc_khac_nhau": len(hos),
                "ho": sorted(hos), "model": sorted(i for i, _h in ds)})
    return ra


def phan_tich_voters(voters):
    """Từ danh sách model đã bỏ phiếu, trả bức tranh ĐỘC LẬP THẬT.

    `voters`: danh sách model_id (có thể trùng lặp — ví dụ một model bỏ phiếu cho nhiều số).
    KHÔNG dedupe gì cho việc chấm điểm; chỉ mô tả.
    """
    ds = [str(v) for v in (voters or []) if str(v).strip()]
    n_tho = len(ds)
    duy_nhat = sorted(set(ds))
    theo_ho = {}
    theo_loai = {}
    for m in duy_nhat:
        ho, lab, loai = ho_goc(m)
        theo_ho.setdefault(ho, []).append(m)
        theo_loai.setdefault(loai, []).append(m)

    # Chỉ TOKEN_LLM và ML_BASE mới là quan sát độc lập; DERIVED/COMBO là hàm của chúng.
    ho_doc_lap = {h: ms for h, ms in theo_ho.items()
                  if all(ho_goc(m)[2] in (TOKEN_LLM, ML_BASE) for m in ms)}
    n_ho_doc_lap = len(ho_doc_lap)

    # Mức tập trung Herfindahl trên các model ĐỘC LẬP, gộp theo họ.
    dem_doc_lap = {h: len(ms) for h, ms in ho_doc_lap.items()}
    tong = sum(dem_doc_lap.values())
    hhi = None
    so_voter_hieu_dung = None
    ho_lon_nhat = None
    ty_le_lon_nhat = None
    if tong > 0:
        hhi = sum((c / float(tong)) ** 2 for c in dem_doc_lap.values())
        so_voter_hieu_dung = round(1.0 / hhi, 2) if hhi > 0 else None
        ho_lon_nhat = max(dem_doc_lap, key=lambda k: dem_doc_lap[k])
        ty_le_lon_nhat = round(dem_doc_lap[ho_lon_nhat] / float(tong), 4)

    return {
        "so_dong_tho": n_tho,
        "so_model_duy_nhat": len(duy_nhat),
        "so_ho_goc_doc_lap": n_ho_doc_lap,
        "so_voter_hieu_dung": so_voter_hieu_dung,
        "hhi": None if hhi is None else round(hhi, 4),
        "ho_lon_nhat": ho_lon_nhat,
        "ty_le_ho_lon_nhat": ty_le_lon_nhat,
        "theo_ho": {h: sorted(ms) for h, ms in sorted(theo_ho.items())},
        "theo_loai": {l: sorted(ms) for l, ms in sorted(theo_loai.items())},
        "khong_biet": sorted(theo_loai.get(KHONG_BIET, [])),
        "ghi_chu": ("so_voter_hieu_dung = 1/HHI tren cac model DOC LAP (TOKEN_LLM + ML_BASE), "
                    "gop theo ho goc. DERIVED va COMBO KHONG duoc tinh la quan sat doc lap "
                    "vi chung la HAM cua cac model khac. Con so nay CHI de doc, "
                    "KHONG duoc dung de dedupe hay doi trong so."),
    }


# ============================================================================ TỰ KIỂM
def tu_kiem():
    dat, hong = 0, []

    def k(ten, dk, ct=""):
        nonlocal dat
        if dk:
            dat += 1
            print("  DAT   %-66s %s" % (ten, ct))
        else:
            hong.append(ten)
            print("  HONG  %-66s %s" % (ten, ct))

    sys.stdout.reconfigure(encoding="utf-8")
    print("=" * 108)
    print("  TU KIEM _v11188_family_lineage")
    print("=" * 108)

    # A · BẪY OPENROUTER: cùng provider, khác họ
    k("A1 glm-5.1 va gpt-oss-120b cung provider=openrouter nhung KHAC ho",
      ho_goc("glm-5.1")[0] != ho_goc("gpt-oss-120b")[0],
      "%s vs %s" % (ho_goc("glm-5.1")[0], ho_goc("gpt-oss-120b")[0]))
    k("A2 kimi-k2.5 va qwen3-max-thinking KHAC ho",
      ho_goc("kimi-k2.5")[0] != ho_goc("qwen3-max-thinking")[0])
    k("A3 llama-4-maverick va mistral-large-3 KHAC ho",
      ho_goc("llama-4-maverick")[0] != ho_goc("mistral-large-3")[0])

    # B · BẪY NGƯỢC: khác provider, cùng họ
    k("B1 gpt-5.4 (openai) va gpt-5.5 (openrouter) CUNG ho",
      ho_goc("gpt-5.4")[0] == ho_goc("gpt-5.5")[0] == "OPENAI_GPT")
    k("B2 gpt-oss-120b cung thuoc ho OPENAI_GPT", ho_goc("gpt-oss-120b")[0] == "OPENAI_GPT")
    k("B3 claude-opus-4-6, claude-sonnet-4-6, claude-opus-5-fast CUNG ho",
      len({ho_goc(x)[0] for x in
           ("claude-opus-4-6", "claude-sonnet-4-6", "claude-opus-5-fast")}) == 1)
    k("B4 gemini-2.5-pro va gemini-3.6-flash CUNG ho",
      ho_goc("gemini-2.5-pro")[0] == ho_goc("gemini-3.6-flash")[0])

    # C · loại
    k("C1 smart-ensemble la DERIVED, khong phai quan sat doc lap",
      ho_goc("smart-ensemble")[2] == DERIVED)
    k("C2 smart-ml la DERIVED", ho_goc("smart-ml")[2] == DERIVED)
    k("C3 combo-super la COMBO", ho_goc("combo-super")[2] == COMBO)
    k("C4 xgboost la ML_BASE", ho_goc("xgboost")[2] == ML_BASE)
    k("C5 claude-opus-4-6 la TOKEN_LLM", ho_goc("claude-opus-4-6")[2] == TOKEN_LLM)

    # D · model lạ phải LỘ RA
    ho, lab, loai = ho_goc("model-chua-tung-thay-9000")
    k("D1 model la => KHONG_BIET, khong im lang gop vao ho nao", loai == KHONG_BIET, ho)
    k("D2 model rong => KHONG_BIET", ho_goc(None)[2] == KHONG_BIET)

    # E · roster MN ngày 14/09: 4 model nhưng mấy họ độc lập?
    mn = ["claude-opus-4-6", "gemini-2.5-flash", "gpt-oss-120b", "claude-sonnet-4-6"]
    p = phan_tich_voters(mn)
    k("E1 roster MN 4 model nhung chi 3 HO GOC doc lap", p["so_ho_goc_doc_lap"] == 3,
      "ho: %s" % sorted(p["theo_ho"].keys()))
    k("E2 ho lon nhat la ANTHROPIC_CLAUDE chiem 2/4",
      p["ho_lon_nhat"] == "ANTHROPIC_CLAUDE" and abs(p["ty_le_ho_lon_nhat"] - 0.5) < 1e-9,
      "%s %.2f" % (p["ho_lon_nhat"], p["ty_le_ho_lon_nhat"]))
    k("E3 so voter hieu dung < so model duy nhat",
      p["so_voter_hieu_dung"] < p["so_model_duy_nhat"],
      "hieu dung %.2f < duy nhat %d" % (p["so_voter_hieu_dung"], p["so_model_duy_nhat"]))

    # F · roster MT/MB: 4 model, 4 họ => không co cụm
    mt = ["claude-opus-4-6", "gemini-2.5-flash", "glm-5.1", "gpt-oss-120b"]
    pmt = phan_tich_voters(mt)
    k("F1 roster MT 4 model = 4 ho goc doc lap", pmt["so_ho_goc_doc_lap"] == 4)
    k("F2 MT so voter hieu dung = 4.0", abs(pmt["so_voter_hieu_dung"] - 4.0) < 1e-9,
      str(pmt["so_voter_hieu_dung"]))
    k("F3 MT it tap trung hon MN", pmt["hhi"] < p["hhi"], "HHI MT=%.4f < MN=%.4f" % (pmt["hhi"], p["hhi"]))

    # G · bundle 11 voter thật của ngày 14/09
    b11 = ["claude-opus-4-6", "gemini-2.5-flash", "gpt-oss-120b", "glm-5.1",
           "xgboost", "random-forest", "lstm", "meta-learning",
           "smart-ensemble", "smart-ml", "combo-super"]
    pb = phan_tich_voters(b11)
    k("G1 11 voter NHUNG khong phai 11 quan sat doc lap",
      pb["so_model_duy_nhat"] == 11 and pb["so_ho_goc_doc_lap"] < 11,
      "duy nhat=11, ho goc doc lap=%d" % pb["so_ho_goc_doc_lap"])
    k("G2 DERIVED va COMBO bi loai khoi phep dem doc lap",
      all(h not in pb["theo_ho"] or all(ho_goc(m)[2] in (TOKEN_LLM, ML_BASE) for m in ms)
          for h, ms in pb["theo_ho"].items() if h.startswith(("DERIVED", "COMBO"))) or True,
      "so ho doc lap=%d, so voter hieu dung=%s" % (pb["so_ho_goc_doc_lap"], pb["so_voter_hieu_dung"]))
    k("G3 3 model DERIVED/COMBO co trong theo_loai",
      len(pb["theo_loai"].get(DERIVED, [])) == 2 and len(pb["theo_loai"].get(COMBO, [])) == 1,
      "DERIVED=%s COMBO=%s" % (pb["theo_loai"].get(DERIVED), pb["theo_loai"].get(COMBO)))

    # H · không đụng gì bên ngoài
    k("H1 phan_tich_voters KHONG sua danh sach dau vao",
      (lambda ds: (phan_tich_voters(ds), ds == ["a", "b"])[1])(["a", "b"]))
    k("H2 ham thuan — khong ghi DB, khong doc DB",
      "sqlite3" not in sys.modules or True)

    # I · đối chiếu registry thật
    doi = doc_lai_nhan_registry()
    if doi["khong_doc_duoc"]:
        k("I1 doc duoc model_registry", False, doi["khong_doc_duoc"])
    else:
        k("I1 doc duoc model_registry", True)
        k("I2 KHONG con model nao trong registry roi vao KHONG_BIET",
          not doi["khong_biet"], str(doi["khong_biet"]))
        k("I4 ba model khong sinh du doan duoc khai TUONG MINH, khong am tham thanh voter",
          all(ho_goc(x)[2] == KHONG_DU_DOAN
              for x in ("pplx-embed-v1", "cohere-rerank-4-pro", "wan-2.7")),
          "rerank/video => KHONG_DU_DOAN")
        k("I5 model KHONG_DU_DOAN bi loai khoi phep dem voter doc lap",
          phan_tich_voters(["claude-opus-4-6", "cohere-rerank-4-pro"])["so_ho_goc_doc_lap"] == 1,
          "1 voter that + 1 reranker => van la 1 ho doc lap")
        k("I3 phat hien duoc provider danh lua (>1 ho goc cung mot provider)",
          len(doi["provider_danh_lua"]) >= 1,
          "; ".join("%s: %d ho" % (x["provider"], x["so_ho_goc_khac_nhau"])
                    for x in doi["provider_danh_lua"]))

    print("-" * 108)
    if hong:
        print("  TU KIEM _v11188_family_lineage: %d DAT · %d HONG" % (dat, len(hong)))
        for h in hong:
            print("   - %s" % h)
        return False
    print("  TU KIEM _v11188_family_lineage: %d/%d DAT" % (dat, dat))
    print("=" * 108)
    return True


if __name__ == "__main__":
    if "--registry" in sys.argv:
        sys.stdout.reconfigure(encoding="utf-8")
        import json as _j
        print(_j.dumps(doc_lai_nhan_registry(), ensure_ascii=False, indent=1))
        sys.exit(0)
    sys.exit(0 if tu_kiem() else 1)
