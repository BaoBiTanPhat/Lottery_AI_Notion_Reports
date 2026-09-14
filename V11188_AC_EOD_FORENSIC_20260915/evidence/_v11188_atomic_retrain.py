# -*- coding: utf-8 -*-
"""V11188 §AC-O.3 — ĐƯỜNG CANDIDATE NGUYÊN TỬ CHO RETRAIN. Offline, chưa nối vào production.

BLOCKER ĐƯỢC GHI TỪ V11184, NAY XÁC MINH LẠI NGUYÊN VĂN (RM-10, kiểm 15/09):
    ml_models.py:27   MODEL_DIR = ... / "data" / "models"   -> dùng cho CẢ save lẫn load
    lstm_model.py:29  MODEL_DIR = ... / "data" / "models"   -> :216 save, :248 load
    meta_learner.py:48 MODEL_DIR = ... / "data" / "models"  -> :84 model_path (save+load)
Ba hằng số cấp module này khiến TRAIN GHI ĐÈ THẲNG LÊN BẢN ĐANG PHỤC VỤ. Không có bản ứng viên,
nên không có cách nào so ứng viên với đương kim trên cùng một holdout trước khi thay.
Và `_retrain_all.py` chạy như MỘT TIẾN TRÌNH CON, nên không truyền được bằng biến Python —
phải truyền qua MÔI TRƯỜNG.

BA THƯ MỤC, BA VAI TRÒ:
    ACTIVE      data/models              — bản production ĐANG phục vụ. Train KHÔNG được chạm.
    CANDIDATE   data/models_candidate    — train ghi vào đây.
    CHECKPOINT  data/model_checkpoints   — ảnh chụp bất biến (đã có từ V11184).

HỢP ĐỒNG MÔI TRƯỜNG — mặc định TRÙNG hành vi hôm nay, nên không bật gì thì không đổi gì:
    LOTTERY_ML_WRITE_DIR   nơi train GHI      (không đặt => ACTIVE, y như bây giờ)
    LOTTERY_ML_READ_DIR    nơi suy luận ĐỌC   (không đặt => ACTIVE, y như bây giờ)
Ba module trên sẽ gọi `duong_ghi()` / `duong_doc()` thay cho `MODEL_DIR` — đó là bản vá STAGED,
CHƯA deploy (§AC-M cấm đưa thay đổi vào đường official giữa các lượt ngày 15/09).

KÍCH HOẠT NGUYÊN TỬ — vì sao không chỉ `os.replace` một phát:
  Một model có tới BA tệp (`.joblib` + `_scaler.joblib` + `_metrics.json`). Thay lần lượt mà
  sập giữa chừng sẽ để lại model mới đi với scaler cũ — sai lặng lẽ, tệ hơn hỏng hẳn.
  Nên: (1) chép mọi tệp của một model×miền vào ACTIVE dưới hậu tố `.dang_vao`;
       (2) ghi NHẬT KÝ kích hoạt TRƯỚC khi hoán đổi;
       (3) `os.replace` từng tệp — nguyên tử ở cấp tệp, và cửa sổ rủi ro thu về vài micro giây;
       (4) xoá nhật ký khi xong. Nhật ký còn sót = lần trước sập giữa chừng ⇒ tự sửa được.

CỔNG: theo TỪNG model × TỪNG miền, trên CÙNG MỘT holdout đông cứng. Một model hỏng thì
model đó không lên, KHÔNG kéo theo model khác, và tên module hỏng được ghi CHÍNH XÁC.

Chạy tự kiểm: python _v11188_atomic_retrain.py
"""
from __future__ import annotations

import datetime as dt
import hashlib
import io
import json
import os
import shutil
import sys

BE = os.path.dirname(os.path.abspath(__file__))
GOC = os.path.dirname(os.path.dirname(BE))
ACTIVE = os.path.join(GOC, "data", "models")
CANDIDATE = os.path.join(GOC, "data", "models_candidate")
NHAT_KY = "_kich_hoat_dang_dang.json"

# Ba module huấn luyện phải fail-closed RIÊNG — tên dùng đúng như trong mã.
MODULE_HUAN_LUYEN = ("ml_models", "lstm_model", "meta_learner")

# Hậu tố tệp của từng loại model. KHÔNG đoán: đọc từ chính `data/models` hiện có.
HAU_TO = {
    "xgboost": ("{m}_{r}.joblib", "{m}_{r}_scaler.joblib", "{m}_{r}_metrics.json"),
    "random-forest": ("{m}_{r}.joblib", "{m}_{r}_scaler.joblib", "{m}_{r}_metrics.json"),
    "lstm": ("lstm_{r}.pt", "lstm_{r}_metrics.json"),
    "meta-learning": ("meta_learner_{r}.pkl",),
}
MIEN = ("MN", "MT", "MB")


# ============================================================================ đường đọc/ghi
def duong_ghi():
    """Nơi train GHI. Không đặt biến => ACTIVE, tức đúng hành vi hôm nay."""
    return os.environ.get("LOTTERY_ML_WRITE_DIR") or ACTIVE


def duong_doc():
    """Nơi suy luận ĐỌC. Không đặt biến => ACTIVE, tức đúng hành vi hôm nay."""
    return os.environ.get("LOTTERY_ML_READ_DIR") or ACTIVE


def moi_truong_train_vao_candidate(thu_muc=None):
    """Biến môi trường để truyền cho TIẾN TRÌNH CON `_retrain_all.py`.

    Ghi vào CANDIDATE nhưng vẫn ĐỌC từ ACTIVE — đó là điều kiện để so ứng viên với đương kim.
    """
    return {"LOTTERY_ML_WRITE_DIR": thu_muc or CANDIDATE,
            "LOTTERY_ML_READ_DIR": ACTIVE}


# ============================================================================ tiện ích
def _bam(p):
    try:
        return hashlib.sha256(io.open(p, "rb").read()).hexdigest()
    except Exception:
        return None


def tep_cua(model, mien):
    mau = HAU_TO.get(model)
    if not mau:
        return None
    return [t.format(m=model, r=mien) for t in mau]


def liet_ke(thu_muc):
    ra = {}
    if not os.path.isdir(thu_muc):
        return ra
    for t in sorted(os.listdir(thu_muc)):
        p = os.path.join(thu_muc, t)
        if os.path.isfile(p):
            ra[t] = {"bytes": os.path.getsize(p), "sha256": _bam(p)}
    return ra


# ============================================================================ cổng per model×miền
def cong_kich_hoat(model, mien, diem_ung_vien, diem_duong_kim, holdout_id_ung_vien,
                   holdout_id_duong_kim, n_holdout, toi_thieu_holdout=30,
                   module_loi=None, tep_ung_vien_du=True):
    """Cổng cho ĐÚNG MỘT model × MỘT miền. Trả `(cho_len, ma, ly_do)`.

    Fail-closed ở mọi nhánh không chắc chắn. Một model trượt KHÔNG kéo model khác xuống.
    """
    if module_loi:
        return (False, "KHONG_LEN_MODULE_LOI",
                "module %s bao loi khi huan luyen %s@%s" % (module_loi, model, mien))
    if not tep_ung_vien_du:
        return (False, "KHONG_LEN_THIEU_TEP_UNG_VIEN",
                "thieu tep ung vien cho %s@%s" % (model, mien))
    if holdout_id_ung_vien is None or holdout_id_duong_kim is None:
        return (False, "KHONG_LEN_KHONG_CO_HOLDOUT", "thieu dinh danh holdout")
    if holdout_id_ung_vien != holdout_id_duong_kim:
        return (False, "KHONG_LEN_KHAC_HOLDOUT",
                "ung vien do tren %s, duong kim do tren %s — khong so duoc"
                % (holdout_id_ung_vien, holdout_id_duong_kim))
    if n_holdout is None or n_holdout < toi_thieu_holdout:
        return (False, "KHONG_LEN_HOLDOUT_QUA_NGAN",
                "n=%s < %d" % (n_holdout, toi_thieu_holdout))
    if diem_ung_vien is None or diem_duong_kim is None:
        return (False, "KHONG_LEN_THIEU_DIEM", "thieu diem de so")
    if not (diem_ung_vien > diem_duong_kim):
        return (False, "KHONG_LEN_KHONG_HON_DUONG_KIM",
                "ung vien %.6f khong hon duong kim %.6f" % (diem_ung_vien, diem_duong_kim))
    return (True, "LEN", "ung vien %.6f > duong kim %.6f tren cung holdout %s (n=%d)"
            % (diem_ung_vien, diem_duong_kim, holdout_id_ung_vien, n_holdout))


# ============================================================================ kích hoạt nguyên tử
def _duong_nhat_ky(thu_muc_active):
    return os.path.join(thu_muc_active, NHAT_KY)


def con_nhat_ky_sot(thu_muc_active=None):
    """Nhật ký còn sót = lần kích hoạt trước SẬP GIỮA CHỪNG. Trả nội dung hoặc None."""
    p = _duong_nhat_ky(thu_muc_active or ACTIVE)
    if not os.path.exists(p):
        return None
    try:
        return json.loads(io.open(p, encoding="utf-8").read())
    except Exception as e:
        return {"hong": repr(e), "duong": p}


def kich_hoat_nguyen_tu(model, mien, thu_muc_candidate=None, thu_muc_active=None):
    """Đưa một model × miền từ CANDIDATE lên ACTIVE, nguyên tử theo đơn vị model.

    Trả dict. KHÔNG raise. Nếu hỏng giữa chừng, nhật ký còn lại để `tu_sua()` dọn.
    """
    cand = thu_muc_candidate or CANDIDATE
    act = thu_muc_active or ACTIVE
    ra = {"model": model, "mien": mien, "ok": False, "da_thay": [], "ly_do": None}
    ten = tep_cua(model, mien)
    if not ten:
        ra["ly_do"] = "KHONG_BIET_LOAI_MODEL:%s" % model
        return ra
    try:
        thieu = [t for t in ten if not os.path.exists(os.path.join(cand, t))]
        if thieu:
            ra["ly_do"] = "THIEU_TEP_UNG_VIEN:%s" % thieu
            return ra
        os.makedirs(act, exist_ok=True)

        # (1) chép sang ACTIVE dưới hậu tố tạm — chưa ai nhìn thấy
        tam = []
        for t in ten:
            dich = os.path.join(act, t + ".dang_vao")
            shutil.copy2(os.path.join(cand, t), dich)
            tam.append((dich, os.path.join(act, t)))

        # (2) ghi nhật ký TRƯỚC khi hoán đổi
        nk = {"model": model, "mien": mien, "tep": ten,
              "bat_dau": dt.datetime.now().isoformat(timespec="seconds")}
        with io.open(_duong_nhat_ky(act), "w", encoding="utf-8", newline="\n") as f:
            f.write(json.dumps(nk, ensure_ascii=False))
            f.flush()
            os.fsync(f.fileno())

        # (3) hoán đổi từng tệp — os.replace nguyên tử ở cấp tệp
        for nguon, dich in tam:
            os.replace(nguon, dich)
            ra["da_thay"].append(os.path.basename(dich))

        # (4) xoá nhật ký
        try:
            os.remove(_duong_nhat_ky(act))
        except Exception:
            pass
        ra["ok"] = True
        return ra
    except Exception as e:
        ra["ly_do"] = "LOI:%r" % e
        return ra


def tu_sua(thu_muc_active=None, kho_checkpoint=None):
    """Dọn hậu quả một lần kích hoạt bị sập giữa chừng.

    Không đoán: nếu còn nhật ký thì xoá mọi tệp `.dang_vao` còn sót và BÁO CÁO để người
    vận hành quyết định gỡ về từ checkpoint nào. KHÔNG tự gỡ về.
    """
    act = thu_muc_active or ACTIVE
    nk = con_nhat_ky_sot(act)
    ra = {"co_nhat_ky_sot": nk is not None, "nhat_ky": nk, "da_don": []}
    if not os.path.isdir(act):
        return ra
    for t in sorted(os.listdir(act)):
        if t.endswith(".dang_vao"):
            try:
                os.remove(os.path.join(act, t))
                ra["da_don"].append(t)
            except Exception:
                pass
    if nk is not None:
        ra["khuyen_nghi"] = ("Mot lan kich hoat da SAP GIUA CHUNG voi %s@%s. Kiem sha cua %s "
                             "roi go ve tu checkpoint gan nhat neu lech."
                             % (nk.get("model"), nk.get("mien"), nk.get("tep")))
        try:
            os.remove(_duong_nhat_ky(act))
        except Exception:
            pass
    return ra


# ============================================================================ smoke sau kích hoạt
def khoi_smoke(model, mien, thu_muc_active=None, ham_kiem=None):
    """Chạy smoke sau khi kích hoạt. `ham_kiem` do caller truyền vào để tệp này không phải
    import torch/sklearn. Thiếu `ham_kiem` => trả về KHONG_KIEM_DUOC, KHÔNG coi là đạt."""
    act = thu_muc_active or ACTIVE
    ten = tep_cua(model, mien) or []
    thieu = [t for t in ten if not os.path.exists(os.path.join(act, t))]
    if thieu:
        return {"dat": False, "ma": "THIEU_TEP_SAU_KICH_HOAT", "chi_tiet": thieu}
    if ham_kiem is None:
        return {"dat": False, "ma": "KHONG_KIEM_DUOC",
                "chi_tiet": "chua truyen ham_kiem — KHONG duoc coi la dat"}
    try:
        ok = bool(ham_kiem(model, mien, act))
        return {"dat": ok, "ma": "SMOKE_DAT" if ok else "SMOKE_TRUOT"}
    except Exception as e:
        return {"dat": False, "ma": "SMOKE_NEM_LOI", "chi_tiet": repr(e)}


# ============================================================================ bản vá STAGED
BAN_VA_BA_MODULE = """
BẢN VÁ CHO BA MODULE — STAGED, CHƯA ÁP (§AC-M cấm đưa vào official path giữa các lượt 15/09).

Mỗi module thay HẰNG SỐ cấp module bằng HAI HÀM, và mặc định KHÔNG đặt biến môi trường thì
đường ghi = đường đọc = `data/models`, tức hành vi byte-identical với hôm nay.

  ml_models.py     (hiện: :27 MODEL_DIR, dùng ở :86 :90 :94 save/load, :362 mkdir)
      from _v11188_atomic_retrain import duong_ghi, duong_doc
      # save -> Path(duong_ghi()) / ...      ; load -> Path(duong_doc()) / ...
  lstm_model.py    (hiện: :29 MODEL_DIR, :215-216 :314 :318 save, :248 load)
      save_path   = Path(duong_ghi()) / f"lstm_{region}.pt"
      checkpoint  = torch.load(str(Path(duong_doc()) / f"lstm_{region}.pt"), ...)
  meta_learner.py  (hiện: :48 MODEL_DIR, :84 model_path dùng cho CẢ save lẫn load)
      self.model_path_ghi = Path(duong_ghi()) / f"meta_learner_{region}.pkl"
      self.model_path_doc = Path(duong_doc()) / f"meta_learner_{region}.pkl"

  `_retrain_all.py` chạy như TIẾN TRÌNH CON ⇒ truyền qua môi trường:
      env = {**os.environ, **moi_truong_train_vao_candidate()}

TRÌNH TỰ MỘT VÒNG RETRAIN AN TOÀN:
  1. `_v11184_retrain_an_toan.chup_checkpoint("pre_retrain")`  (đã có, đang chạy fail-closed)
  2. train với env ghi->CANDIDATE, đọc->ACTIVE
  3. chấm ứng viên và đương kim trên CÙNG một holdout đông cứng
  4. `cong_kich_hoat()` cho TỪNG model × miền
  5. `kich_hoat_nguyen_tu()` cho những cái qua cổng
  6. `khoi_smoke()`; trượt thì gỡ về ngay từ checkpoint bước 1
  7. `tu_sua()` ở lần khởi động kế tiếp để bắt trường hợp sập giữa chừng
"""


# ============================================================================ TỰ KIỂM
def tu_kiem():
    import tempfile
    dat, hong = 0, []

    def k(ten, dk, ct=""):
        nonlocal dat
        if dk:
            dat += 1
            print("  DAT   %-64s %s" % (ten, ct))
        else:
            hong.append(ten)
            print("  HONG  %-64s %s" % (ten, ct))

    sys.stdout.reconfigure(encoding="utf-8")
    print("=" * 106)
    print("  TU KIEM _v11188_atomic_retrain")
    print("=" * 106)

    goc = tempfile.mkdtemp(prefix="_v11188_ar_")
    act = os.path.join(goc, "models")
    cand = os.path.join(goc, "models_candidate")
    os.makedirs(act)
    os.makedirs(cand)

    def viet(thu_muc, ten, noi_dung):
        with io.open(os.path.join(thu_muc, ten), "w", encoding="utf-8", newline="\n") as f:
            f.write(noi_dung)

    # A · mặc định KHÔNG đổi hành vi
    for b in ("LOTTERY_ML_WRITE_DIR", "LOTTERY_ML_READ_DIR"):
        os.environ.pop(b, None)
    k("A1 khong dat bien => duong ghi = ACTIVE (hanh vi hom nay)", duong_ghi() == ACTIVE)
    k("A2 khong dat bien => duong doc = ACTIVE", duong_doc() == ACTIVE)
    k("A3 duong ghi va duong doc TRUNG nhau khi chua bat", duong_ghi() == duong_doc())
    mt = moi_truong_train_vao_candidate()
    k("A4 moi truong train: GHI candidate nhung DOC active",
      mt["LOTTERY_ML_WRITE_DIR"] == CANDIDATE and mt["LOTTERY_ML_READ_DIR"] == ACTIVE)
    os.environ["LOTTERY_ML_WRITE_DIR"] = cand
    os.environ["LOTTERY_ML_READ_DIR"] = act
    k("A5 dat bien => hai duong TACH RA", duong_ghi() == cand and duong_doc() == act)

    # B · tên tệp lấy đúng, không đoán
    k("B1 xgboost co DU 3 tep (model + scaler + metrics)",
      tep_cua("xgboost", "MN") == ["xgboost_MN.joblib", "xgboost_MN_scaler.joblib",
                                   "xgboost_MN_metrics.json"], str(tep_cua("xgboost", "MN")))
    k("B2 lstm co 2 tep", len(tep_cua("lstm", "MB")) == 2, str(tep_cua("lstm", "MB")))
    k("B3 meta-learning co 1 tep", tep_cua("meta-learning", "MT") == ["meta_learner_MT.pkl"])
    k("B4 model la => None, khong doan ten tep", tep_cua("khong-ton-tai", "MN") is None)

    # C · cổng per model×miền
    c = cong_kich_hoat("xgboost", "MN", 0.60, 0.55, "H1", "H1", 60)
    k("C1 hon duong kim tren cung holdout => LEN", c[0] and c[1] == "LEN", c[2])
    c = cong_kich_hoat("xgboost", "MN", 0.60, 0.55, "H1", "H2", 60)
    k("C2 KHAC holdout => KHONG LEN", (not c[0]) and c[1] == "KHONG_LEN_KHAC_HOLDOUT", c[2])
    c = cong_kich_hoat("xgboost", "MN", 0.60, 0.55, "H1", "H1", 10)
    k("C3 holdout qua ngan => KHONG LEN", (not c[0]) and c[1] == "KHONG_LEN_HOLDOUT_QUA_NGAN", c[2])
    c = cong_kich_hoat("xgboost", "MN", 0.55, 0.55, "H1", "H1", 60)
    k("C4 BANG duong kim => KHONG LEN (khong thay khi khong hon)",
      (not c[0]) and c[1] == "KHONG_LEN_KHONG_HON_DUONG_KIM", c[2])
    c = cong_kich_hoat("lstm", "MB", 0.9, 0.1, "H1", "H1", 60, module_loi="lstm_model")
    k("C5 module huan luyen loi => KHONG LEN du diem cao",
      (not c[0]) and c[1] == "KHONG_LEN_MODULE_LOI", c[2])
    k("C6 va ly do neu DUNG TEN MODULE hong", "lstm_model" in c[2])
    c = cong_kich_hoat("lstm", "MB", 0.9, 0.1, "H1", "H1", 60, tep_ung_vien_du=False)
    k("C7 thieu tep ung vien => KHONG LEN", (not c[0]) and c[1] == "KHONG_LEN_THIEU_TEP_UNG_VIEN")
    c = cong_kich_hoat("xgboost", "MN", None, 0.55, "H1", "H1", 60)
    k("C8 thieu diem => KHONG LEN (fail-closed)", (not c[0]) and c[1] == "KHONG_LEN_THIEU_DIEM")
    c = cong_kich_hoat("xgboost", "MN", 0.6, 0.5, None, "H1", 60)
    k("C9 thieu dinh danh holdout => KHONG LEN", (not c[0]) and c[1] == "KHONG_LEN_KHONG_CO_HOLDOUT")

    # D · một model trượt KHÔNG kéo model khác xuống
    kq = {}
    for m, diem, loi in (("xgboost", 0.60, None), ("random-forest", 0.50, None),
                         ("lstm", 0.99, "lstm_model")):
        kq[m] = cong_kich_hoat(m, "MN", diem, 0.55, "H1", "H1", 60, module_loi=loi)
    k("D1 xgboost LEN", kq["xgboost"][0])
    k("D2 random-forest KHONG len (khong hon)", not kq["random-forest"][0])
    k("D3 lstm KHONG len (module loi)", not kq["lstm"][0])
    k("D4 ba ket qua DOC LAP — mot cai truot khong keo cai khac",
      kq["xgboost"][0] and not kq["random-forest"][0] and not kq["lstm"][0])

    # E · kích hoạt nguyên tử
    for t in tep_cua("xgboost", "MN"):
        viet(act, t, "BAN_CU")
        viet(cand, t, "BAN_MOI")
    r = kich_hoat_nguyen_tu("xgboost", "MN", cand, act)
    k("E1 kich hoat thanh cong", r["ok"], str(r.get("ly_do") or ""))
    k("E2 thay DU CA BA tep", len(r["da_thay"]) == 3, str(r["da_thay"]))
    noi = {t: io.open(os.path.join(act, t), encoding="utf-8").read()
           for t in tep_cua("xgboost", "MN")}
    k("E3 ca ba tep deu la BAN MOI — khong con lai bo mix",
      all(v == "BAN_MOI" for v in noi.values()), str(noi))
    k("E4 khong con tep .dang_vao sot lai",
      not [t for t in os.listdir(act) if t.endswith(".dang_vao")])
    k("E5 nhat ky da duoc xoa sau khi xong", con_nhat_ky_sot(act) is None)

    # F · thiếu tệp ứng viên thì KHÔNG đụng gì vào ACTIVE
    for t in tep_cua("random-forest", "MN"):
        viet(act, t, "BAN_CU_RF")
    viet(cand, "random-forest_MN.joblib", "BAN_MOI_RF")   # cố ý thiếu scaler + metrics
    r2 = kich_hoat_nguyen_tu("random-forest", "MN", cand, act)
    k("F1 thieu tep ung vien => TU CHOI kich hoat", not r2["ok"],
      str(r2.get("ly_do"))[:70])
    con = {t: io.open(os.path.join(act, t), encoding="utf-8").read()
           for t in tep_cua("random-forest", "MN")}
    k("F2 ACTIVE GIU NGUYEN ban cu, khong bi dung toi",
      all(v == "BAN_CU_RF" for v in con.values()), str(con))

    # G · sập giữa chừng: mô phỏng nhật ký + tệp .dang_vao còn sót
    viet(act, "lstm_MB.pt.dang_vao", "NUA_CHUNG")
    with io.open(_duong_nhat_ky(act), "w", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps({"model": "lstm", "mien": "MB",
                            "tep": ["lstm_MB.pt", "lstm_MB_metrics.json"]}))
    s = con_nhat_ky_sot(act)
    k("G1 phat hien duoc nhat ky sot", s is not None and s.get("model") == "lstm", str(s))
    d = tu_sua(act)
    k("G2 tu_sua don sach tep .dang_vao", "lstm_MB.pt.dang_vao" in d["da_don"], str(d["da_don"]))
    k("G3 tu_sua BAO CAO chu KHONG tu go ve", "khuyen_nghi" in d and "go ve" in d["khuyen_nghi"])
    k("G4 sau tu_sua khong con nhat ky", con_nhat_ky_sot(act) is None)

    # H · smoke
    s1 = khoi_smoke("xgboost", "MN", act)
    k("H1 khong truyen ham_kiem => KHONG duoc coi la dat",
      s1["dat"] is False and s1["ma"] == "KHONG_KIEM_DUOC", s1["ma"])
    s2 = khoi_smoke("xgboost", "MN", act, ham_kiem=lambda m, r, d: True)
    k("H2 ham_kiem tra True => SMOKE_DAT", s2["dat"] and s2["ma"] == "SMOKE_DAT")
    s3 = khoi_smoke("xgboost", "MN", act, ham_kiem=lambda m, r, d: False)
    k("H3 ham_kiem tra False => SMOKE_TRUOT", (not s3["dat"]) and s3["ma"] == "SMOKE_TRUOT")

    def _nem(m, r, d):
        raise RuntimeError("model hong")
    s4 = khoi_smoke("xgboost", "MN", act, ham_kiem=_nem)
    k("H4 ham_kiem nem loi => SMOKE_NEM_LOI, khong lam sap tien trinh",
      (not s4["dat"]) and s4["ma"] == "SMOKE_NEM_LOI")
    s5 = khoi_smoke("lstm", "MB", act, ham_kiem=lambda m, r, d: True)
    k("H5 thieu tep sau kich hoat => KHONG dat du ham_kiem tra True",
      (not s5["dat"]) and s5["ma"] == "THIEU_TEP_SAU_KICH_HOAT")

    # I · không raise ra ngoài trong mọi nhánh
    r3 = kich_hoat_nguyen_tu("khong-biet-la-gi", "MN", cand, act)
    k("I1 model la => tra ve loi, KHONG raise",
      r3["ok"] is False and str(r3["ly_do"]).startswith("KHONG_BIET_LOAI_MODEL"))
    r4 = kich_hoat_nguyen_tu("xgboost", "MN", "/khong/ton/tai", act)
    k("I2 thu muc candidate khong ton tai => tra ve loi, KHONG raise", r4["ok"] is False)

    # J · ba module fail-closed riêng biệt, tên đúng
    k("J1 khai du ba module huan luyen, dung ten trong ma",
      MODULE_HUAN_LUYEN == ("ml_models", "lstm_model", "meta_learner"))

    for b in ("LOTTERY_ML_WRITE_DIR", "LOTTERY_ML_READ_DIR"):
        os.environ.pop(b, None)
    k("K1 khoi phuc nguyen trang bien moi truong sau bo thu",
      os.environ.get("LOTTERY_ML_WRITE_DIR") is None
      and os.environ.get("LOTTERY_ML_READ_DIR") is None)
    shutil.rmtree(goc, ignore_errors=True)

    print("-" * 106)
    if hong:
        print("  TU KIEM _v11188_atomic_retrain: %d DAT · %d HONG" % (dat, len(hong)))
        for h in hong:
            print("   - %s" % h)
        return False
    print("  TU KIEM _v11188_atomic_retrain: %d/%d DAT" % (dat, dat))
    print("=" * 106)
    return True


if __name__ == "__main__":
    if "--ban-va" in sys.argv:
        sys.stdout.reconfigure(encoding="utf-8")
        print(BAN_VA_BA_MODULE)
        sys.exit(0)
    sys.exit(0 if tu_kiem() else 1)
