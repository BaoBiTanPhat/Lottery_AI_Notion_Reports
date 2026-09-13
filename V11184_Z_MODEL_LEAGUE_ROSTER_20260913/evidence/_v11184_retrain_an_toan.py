# -*- coding: utf-8 -*-
"""V11184 §Z-G — KHOÁ AN TOÀN RETRAIN: checkpoint bất biến · cổng thăng hạng · gỡ về chứng minh được.

VÌ SAO CÓ TỆP NÀY — đo được ngày 13/09/2026 (V11183 §4.4):
  · `training_history.backup_path` RỖNG 12/12 dòng;
  · chỉ `meta_learner_*.pkl` có `.bak`, và bản đó từ 03/07/2026 — KHÔNG phải trạng thái trước 13/09;
  · `random-forest` / `xgboost` / `lstm` KHÔNG có `.bak` nào;
  · 18 artifact bị ghi đè 02:00:33–02:02:54 và prediction 05:00:01 đã chạy trên checkpoint mới.
⇒ Retrain ghi đè TẠI CHỖ, không có bản cũ để quay về. Một lần retrain hỏng là mất vĩnh viễn.

BA ĐIỂM GHI ARTIFACT THẬT (grep, không đoán — RM-10):
  `ml_models.py:364,366`  joblib.dump(model)  + joblib.dump(scaler)
  `lstm_model.py:217`     torch.save({...})
  `meta_learner.py:396`   pickle.dump(model_data, f)
Cả ba module có `MODEL_DIR` hằng số riêng, và dùng nó cho CẢ GHI LẪN ĐỌC.

VÌ SAO KHÔNG "TRAIN VÀO CANDIDATE PATH" NGAY — nói thẳng chứ không giấu:
`MODEL_DIR` phục vụ cả `save()` lẫn `load()`. Đổi nó lúc train sẽ làm chính tiến trình đó đọc
nhầm bản cũ/mới khi so sánh, và ba module lại nằm ở ba tiến trình khác nhau (`_retrain_all.py`
là subprocess, LSTM chạy in-process). Một override nửa vời còn nguy hiểm hơn không override.
TÍNH CHẤT AN TOÀN THẬT SỰ §G cần là «không bao giờ mất đường về», và nó đạt được đầy đủ bằng:
    CHỤP checkpoint bất biến  →  train (đường hiện có)  →  CỔNG trên frozen holdout
                              →  đạt thì giữ, KHÔNG đạt thì TỰ ĐỘNG GỠ VỀ từ checkpoint.
Artifact xấu chỉ sống vài phút rồi bị thu hồi, và mọi bước đều verify bằng SHA256.
Đường tới candidate-path đầy đủ ghi ở `KE_HOACH_CANDIDATE_PATH` cuối tệp.

TỆP NÀY KHÔNG TỰ CHẠY RETRAIN và KHÔNG sửa ba module huấn luyện.
"""
from __future__ import annotations

import glob
import hashlib
import io
import json
import os
import shutil
import sys
import time

BE = os.path.dirname(os.path.abspath(__file__))
GOC = os.path.dirname(os.path.dirname(BE))
MODEL_DIR = GOC + "/data/models"
KHO_CHECKPOINT = GOC + "/data/model_checkpoints"

# Đuôi tệp được coi là artifact model. Lấy từ chính `_v10646_retrain_guard._newest_model_age_days`
# (dòng 70: "*.joblib", "*.pkl", "*.pt") rồi MỞ RỘNG thêm metrics/scaler/config vì §G mục 2 đòi
# checkpoint cả scaler, metrics và config — guard cũ chỉ quét ba đuôi kia để tính tuổi.
DUOI_ARTIFACT = (".joblib", ".pkl", ".pt", ".json")


def bam(p):
    h = hashlib.sha256()
    with io.open(p, "rb") as f:
        for k in iter(lambda: f.read(1 << 20), b""):
            h.update(k)
    return h.hexdigest()


def liet_ke_artifact(thu_muc=MODEL_DIR):
    """Mọi artifact hiện hành + siêu dữ liệu. Bao gồm cả symlink (ghi đích, không ghi hash)."""
    ra = {}
    for p in sorted(glob.glob(thu_muc + "/*")):
        ten = os.path.basename(p)
        if ten.startswith("."):
            continue                      # bỏ marker như .last_optimizer_run
        if not ten.endswith(DUOI_ARTIFACT):
            continue
        st = os.lstat(p)
        la_link = os.path.islink(p)
        ra[ten] = {
            "path": p, "size": st.st_size, "mtime": st.st_mtime,
            "inode": st.st_ino, "la_symlink": la_link,
            "symlink_target": os.readlink(p) if la_link else None,
            "sha256": None if la_link else bam(p),
        }
    return ra


def chup_checkpoint(nhan="pre_retrain", thu_muc=MODEL_DIR, kho=KHO_CHECKPOINT):
    """Chụp BẤT BIẾN toàn bộ artifact + manifest SHA256. Gọi TRƯỚC khi train.

    Thư mục checkpoint đặt tên theo thời điểm nên KHÔNG BAO GIỜ bị ghi đè — đó là ý nghĩa của
    chữ «bất biến» ở đây. Trả về đường dẫn checkpoint.
    """
    moc = time.strftime("%Y%m%d_%H%M%S")
    dich = "%s/%s__%s" % (kho, moc, nhan)
    if os.path.exists(dich):
        raise IOError("checkpoint da ton tai, tu choi ghi de: %s" % dich)
    os.makedirs(dich, exist_ok=False)

    truoc = liet_ke_artifact(thu_muc)
    for ten, m in truoc.items():
        if m["la_symlink"]:
            continue                       # symlink: chỉ ghi đích vào manifest, không sao chép
        shutil.copy2(m["path"], dich + "/" + ten)

    # Xác minh NGAY: từng tệp chép ra phải khớp hash nguồn. Chép mà không verify thì không phải backup.
    lech = []
    for ten, m in truoc.items():
        if m["la_symlink"]:
            continue
        if bam(dich + "/" + ten) != m["sha256"]:
            lech.append(ten)
    if lech:
        raise IOError("checkpoint HONG, %d tep khong khop hash: %s" % (len(lech), lech[:5]))

    manifest = {
        "artifact": "RETRAIN_CHECKPOINT", "nhan": nhan,
        "chup_luc": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "nguon": thu_muc, "duong_dan": dich,
        "n_tep": len(truoc), "n_tep_da_chep": len([1 for m in truoc.values() if not m["la_symlink"]]),
        "tep": truoc,
    }
    manifest["manifest_sha256"] = hashlib.sha256(
        json.dumps(manifest, sort_keys=True, ensure_ascii=False, default=str).encode()).hexdigest()
    tam = dich + "/_MANIFEST.json.tmp"
    with io.open(tam, "w", encoding="utf-8", newline=chr(10)) as f:
        f.write(json.dumps(manifest, ensure_ascii=False, indent=1, default=str))
        f.flush()
        os.fsync(f.fileno())
    os.replace(tam, dich + "/_MANIFEST.json")
    return dich


def doc_manifest(checkpoint):
    return json.load(io.open(checkpoint + "/_MANIFEST.json", encoding="utf-8"))


def so_sanh_voi_hien_tai(checkpoint, thu_muc=MODEL_DIR):
    """Artifact nào đã ĐỔI so với checkpoint. Đây là bằng chứng retrain thực sự ghi gì."""
    cu = doc_manifest(checkpoint)["tep"]
    moi = liet_ke_artifact(thu_muc)
    ra = {"doi": [], "them": [], "mat": [], "giu_nguyen": []}
    for ten, m in moi.items():
        if ten not in cu:
            ra["them"].append(ten)
        elif m["sha256"] != cu[ten]["sha256"]:
            ra["doi"].append({"ten": ten, "sha_cu": (cu[ten]["sha256"] or "")[:16],
                              "sha_moi": (m["sha256"] or "")[:16],
                              "size_cu": cu[ten]["size"], "size_moi": m["size"]})
        else:
            ra["giu_nguyen"].append(ten)
    for ten in cu:
        if ten not in moi:
            ra["mat"].append(ten)
    return ra


def go_ve(checkpoint, thu_muc=MODEL_DIR, chi_cac_tep=None):
    """Khôi phục artifact từ checkpoint và XÁC MINH BẰNG HASH.

    `chi_cac_tep` cho phép gỡ về có chọn lọc (ví dụ chỉ model×miền trượt cổng).
    Trả về báo cáo; ném IOError nếu có tệp khôi phục xong mà hash không khớp.
    """
    man = doc_manifest(checkpoint)
    bc = {"checkpoint": checkpoint, "da_go": [], "bo_qua": [], "khong_khop": []}
    for ten, m in man["tep"].items():
        if m.get("la_symlink"):
            bc["bo_qua"].append({"ten": ten, "vi_sao": "symlink, chi ghi dich trong manifest"})
            continue
        if chi_cac_tep and ten not in chi_cac_tep:
            continue
        nguon = checkpoint + "/" + ten
        if not os.path.exists(nguon):
            bc["bo_qua"].append({"ten": ten, "vi_sao": "khong co trong checkpoint"})
            continue
        dich = thu_muc + "/" + ten
        tam = dich + ".rollback_tmp"
        shutil.copy2(nguon, tam)
        os.replace(tam, dich)              # thay thế NGUYÊN TỬ, không để trạng thái nửa vời
        sha_sau = bam(dich)
        if sha_sau != m["sha256"]:
            bc["khong_khop"].append({"ten": ten, "mong_doi": m["sha256"][:16],
                                     "thuc_te": sha_sau[:16]})
        else:
            bc["da_go"].append(ten)
    if bc["khong_khop"]:
        raise IOError("GO VE HONG: %d tep khong khop hash sau khoi phuc: %s"
                      % (len(bc["khong_khop"]), bc["khong_khop"][:3]))
    return bc


# ============================================================================
# CỔNG THĂNG HẠNG — §G mục 4 và 5
# ============================================================================
def cong_thang_hang(diem_cu, diem_moi, n_holdout, toi_thieu_ngay=30,
                    ten_thuoc="auc", cho_phep_bang=False):
    """Có được GIỮ model mới không, hay phải GỠ VỀ bản cũ?

    §G mục 4 bắt: cùng frozen holdout, KHÔNG dịch cửa sổ giữa hai model, chấm riêng từng
    model×miền, TÁCH thước AUC khỏi thước BT, và CẤM thăng hạng bằng thước không tương thích.

    Đây chính là chỗ 13/09 đã hỏng: `auc` và `old_auc` trong `training_history` đo trên HAI
    holdout LỆCH NHAU 7 NGÀY ⇒ `METRIC_NOT_COMPARABLE`, dấu của delta KHÔNG đọc được.
    Hàm này TỪ CHỐI kết luận khi thước không so được, thay vì đoán bừa.
    """
    ra = {"thuoc": ten_thuoc, "diem_cu": diem_cu, "diem_moi": diem_moi,
          "n_holdout": n_holdout, "quyet": None, "ly_do": ""}

    if diem_cu is None or diem_moi is None:
        ra["quyet"] = "GO_VE_THUOC_KHONG_SO_DUOC"
        ra["ly_do"] = ("thieu diem cho mot ben (cu=%r moi=%r) — khong so duoc thi KHONG duoc "
                       "thang hang (day la loi METRIC_NOT_COMPARABLE cua 13/09)"
                       % (diem_cu, diem_moi))
        return ra

    if n_holdout is None or n_holdout < toi_thieu_ngay:
        ra["quyet"] = "GO_VE_HOLDOUT_QUA_NGAN"
        ra["ly_do"] = ("holdout %r ngay < %d — chua duoc phep ket luan (RM-04)"
                       % (n_holdout, toi_thieu_ngay))
        return ra

    if diem_moi > diem_cu or (cho_phep_bang and diem_moi == diem_cu):
        ra["quyet"] = "GIU_MODEL_MOI"
        ra["ly_do"] = "%s moi %.4f %s cu %.4f tren CUNG frozen holdout %d ngay" % (
            ten_thuoc, diem_moi, ">=" if cho_phep_bang else ">", diem_cu, n_holdout)
    else:
        ra["quyet"] = "GO_VE_MODEL_CU"
        ra["ly_do"] = "%s moi %.4f KHONG hon cu %.4f tren cung holdout %d ngay" % (
            ten_thuoc, diem_moi, diem_cu, n_holdout)
    return ra


def don_checkpoint_cu(giu=6, kho=KHO_CHECKPOINT):
    """Giữ `giu` checkpoint mới nhất, xoá phần cũ hơn.

    VÌ SAO CẦN: mỗi checkpoint ~52 MB; retrain hàng tuần ⇒ ~2,7 GB/năm nếu không dọn, trên một
    đĩa vốn đã dùng 39% và KHÔNG có backup ra ngoài máy (nợ P0 còn mở). Giữ 6 bản ≈ 6 tuần
    ≈ 312 MB — đủ để quay về nhiều vòng retrain mà không ăn đĩa.
    XOÁ CÓ CHỦ Ý và chỉ trong thư mục checkpoint của chính module này; KHÔNG bao giờ đụng
    `data/models/`.
    """
    if not os.path.isdir(kho):
        return {"da_xoa": [], "con_lai": 0}
    ds = sorted(d for d in glob.glob(kho + "/*") if os.path.isdir(d))
    xoa = ds[:-giu] if len(ds) > giu else []
    for d in xoa:
        if os.path.realpath(d).startswith(os.path.realpath(kho) + os.sep):
            shutil.rmtree(d, ignore_errors=True)
    return {"da_xoa": [os.path.basename(d) for d in xoa], "con_lai": len(ds) - len(xoa)}


KE_HOACH_CANDIDATE_PATH = """
ĐƯỜNG TỚI CANDIDATE-PATH ĐẦY ĐỦ (§G mục 3) — chưa làm, và vì sao:
  Ba module ghi artifact đều dùng hằng số `MODEL_DIR` ở cấp module cho CẢ `save()` LẪN `load()`:
    ml_models.py:27 · lstm_model.py:29 · meta_learner.py:48
  Muốn train vào candidate path thì phải cho phép GHI sang thư mục khác mà vẫn ĐỌC bản hiện hành
  để so sánh. Việc đó đòi tách `DUONG_GHI` khỏi `DUONG_DOC` ở cả ba module, và `_retrain_all.py`
  chạy như SUBPROCESS RIÊNG nên còn phải truyền qua môi trường.
  Đó là ba sửa đổi trên đường huấn luyện production — cần dry-run một vòng retrain đầy đủ trước
  khi bật. Trong khi chờ, checkpoint + cổng + tự động gỡ về đã loại bỏ rủi ro MẤT ĐƯỜNG VỀ,
  là rủi ro thật sự của 13/09.
"""


# ============================================================================
# TỰ KIỂM — RM-15, gồm một bài GỠ VỀ THẬT
# ============================================================================
def tu_kiem():
    import tempfile
    kq = []

    def thu(ten, dat, ct=""):
        kq.append((ten, bool(dat), ct))

    tam = tempfile.mkdtemp(prefix="thu_retrain_")
    md = tam + "/models"
    kho = tam + "/checkpoints"
    os.makedirs(md)

    # dựng artifact giả đủ ba loại đuôi + một tệp metrics
    noi_goc = {}
    for ten, noi in (("xgboost_MB.joblib", b"MODEL-CU-XGB"),
                     ("xgboost_MB_scaler.joblib", b"SCALER-CU"),
                     ("lstm_MB.pt", b"MODEL-CU-LSTM"),
                     ("meta_learner_MB.pkl", b"MODEL-CU-META"),
                     ("xgboost_MB_metrics.json", b'{"auc": 0.51}')):
        io.open(md + "/" + ten, "wb").write(noi)
        noi_goc[ten] = noi

    # G1 liệt kê
    ds = liet_ke_artifact(md)
    thu("G1 liet ke du 5 artifact", len(ds) == 5, "thay %d" % len(ds))

    # G2 chụp checkpoint + verify
    cp = chup_checkpoint("thu", thu_muc=md, kho=kho)
    thu("G2 chup checkpoint thanh cong", os.path.isdir(cp))
    man = doc_manifest(cp)
    thu("G3 manifest ghi du 5 tep kem sha256",
        man["n_tep"] == 5 and all(v["sha256"] for v in man["tep"].values()))

    # G4 checkpoint là BẤT BIẾN — chụp lại cùng tên phải bị từ chối
    try:
        os.makedirs(cp, exist_ok=False)
        thu("G4 checkpoint bat bien (tu choi ghi de)", False, "khong tu choi")
    except OSError:
        thu("G4 checkpoint bat bien (tu choi ghi de)", True)

    # G5 chưa đổi gì thì so sánh phải cho 0 thay đổi
    ss = so_sanh_voi_hien_tai(cp, md)
    thu("G5 chua train: 0 doi, 5 giu nguyen",
        len(ss["doi"]) == 0 and len(ss["giu_nguyen"]) == 5)

    # --- MÔ PHỎNG RETRAIN GHI ĐÈ (đúng cách production đang làm) ---
    io.open(md + "/xgboost_MB.joblib", "wb").write(b"MODEL-MOI-XAU")
    io.open(md + "/lstm_MB.pt", "wb").write(b"MODEL-MOI-TOT")

    ss = so_sanh_voi_hien_tai(cp, md)
    thu("G6 phat hien DUNG 2 artifact bi ghi de",
        len(ss["doi"]) == 2 and {d["ten"] for d in ss["doi"]} ==
        {"xgboost_MB.joblib", "lstm_MB.pt"},
        str([d["ten"] for d in ss["doi"]]))

    # G7 cổng: model mới XẤU hơn ⇒ phải GỠ VỀ
    c = cong_thang_hang(diem_cu=0.5299, diem_moi=0.4928, n_holdout=60)
    thu("G7 model moi kem hon => GO_VE_MODEL_CU", c["quyet"] == "GO_VE_MODEL_CU", c["quyet"])

    # G8 cổng: model mới TỐT hơn ⇒ giữ
    c = cong_thang_hang(diem_cu=0.4999, diem_moi=0.5100, n_holdout=60)
    thu("G8 model moi tot hon => GIU_MODEL_MOI", c["quyet"] == "GIU_MODEL_MOI", c["quyet"])

    # G9 cổng: thước không so được ⇒ KHÔNG thăng hạng (lỗi 13/09)
    c = cong_thang_hang(diem_cu=None, diem_moi=0.55, n_holdout=60)
    thu("G9 thieu diem mot ben => GO_VE_THUOC_KHONG_SO_DUOC",
        c["quyet"] == "GO_VE_THUOC_KHONG_SO_DUOC", c["quyet"])

    # G10 cổng: holdout quá ngắn ⇒ không kết luận
    c = cong_thang_hang(diem_cu=0.50, diem_moi=0.60, n_holdout=7)
    thu("G10 holdout 7 ngay => GO_VE_HOLDOUT_QUA_NGAN",
        c["quyet"] == "GO_VE_HOLDOUT_QUA_NGAN", c["quyet"])

    # --- G11 GỠ VỀ THẬT: khôi phục đúng artifact trượt cổng, giữ nguyên artifact đạt cổng ---
    bc = go_ve(cp, md, chi_cac_tep=["xgboost_MB.joblib"])
    thu("G11 go ve dung 1 tep", bc["da_go"] == ["xgboost_MB.joblib"], str(bc["da_go"]))
    thu("G12 noi dung xgboost DA QUAY VE ban cu",
        io.open(md + "/xgboost_MB.joblib", "rb").read() == noi_goc["xgboost_MB.joblib"])
    thu("G13 lstm (dat cong) VAN LA BAN MOI",
        io.open(md + "/lstm_MB.pt", "rb").read() == b"MODEL-MOI-TOT")

    ss = so_sanh_voi_hien_tai(cp, md)
    thu("G14 sau go ve chi con 1 artifact khac checkpoint",
        len(ss["doi"]) == 1 and ss["doi"][0]["ten"] == "lstm_MB.pt", str(ss["doi"]))

    # --- G15 GỠ VỀ TOÀN BỘ phải đưa mọi thứ về đúng trạng thái checkpoint ---
    go_ve(cp, md)
    ss = so_sanh_voi_hien_tai(cp, md)
    thu("G15 go ve toan bo => 0 khac biet, 5 giu nguyen",
        len(ss["doi"]) == 0 and len(ss["giu_nguyen"]) == 5, str(ss["doi"]))

    # --- G16 phát hiện checkpoint HỎNG: sửa tệp trong checkpoint thì go_ve phải NÉM LỖI ---
    io.open(cp + "/meta_learner_MB.pkl", "wb").write(b"CHECKPOINT-DA-BI-SUA")
    try:
        go_ve(cp, md, chi_cac_tep=["meta_learner_MB.pkl"])
        thu("G16 checkpoint bi sua => go_ve phai nem loi", False, "khong nem loi")
    except IOError:
        thu("G16 checkpoint bi sua => go_ve nem loi (khong im lang chap nhan)", True)

    shutil.rmtree(tam, ignore_errors=True)

    dat = sum(1 for _, v, _ in kq if v)
    print("=" * 92)
    print("  TỰ KIỂM _v11184_retrain_an_toan: %d/%d" % (dat, len(kq)))
    print("=" * 92)
    for ten, v, ct in kq:
        print("  %s  %-62s %s" % ("DAT " if v else "HONG", ten, ct[:30]))
    print("=" * 92)
    return dat == len(kq)


def main():
    ok = tu_kiem()
    print(KE_HOACH_CANDIDATE_PATH)
    if "--chup-that" in sys.argv:
        cp = chup_checkpoint("thu_cong")
        man = doc_manifest(cp)
        print("DA CHUP CHECKPOINT THAT: %s" % cp)
        print("  %d tep, manifest sha256 = %s" % (man["n_tep"], man["manifest_sha256"][:32]))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
