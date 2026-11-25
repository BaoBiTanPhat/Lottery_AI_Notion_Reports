# -*- coding: utf-8 -*-
"""V11191 — GỌI THỬ SỨC KHOẺ provider sau khi owner nạp tiền; ĐẠT thì NHẢ cách ly kèm bằng chứng.

Owner 25/11/2026 ~13:1x ICT: «deepseek và claude athopic anh đã nạp tiền rồi ah em».
Chạy TRÊN VPS, trong thư mục web/backend (cần .env + DB production):

    ../../venv/bin/python3 _v11191_thu_suc_khoe_provider.py          # CHỈ gọi thử, KHÔNG nhả
    ../../venv/bin/python3 _v11191_thu_suc_khoe_provider.py --nha    # gọi thử; ĐẠT thì nhả

Luật đang hiệu lực (owner 13/09): không gọi khi lỗi tiền còn tồn tại, KHÔNG retry. Owner báo đã
nạp ⇒ đúng MỘT lượt gọi thử cho mỗi model; hỏng thì giữ nguyên cách ly, không gọi lại.

RM-13/RM-14 — đi ĐÚNG đường production, không dựng đường riêng:
  · khoá: `scheduler._get_api_key_for_model` (DB per-model → env per-model → DB chung → env chung);
  · gọi : `gpt_analyzer._call_anthropic` (qua `ANTHROPIC_MODEL_API_MAP`) / `_call_deepseek`,
          y như nhánh `is_claude` / `is_deepseek` của `_invoke_model_api`;
  · nhả : `_v11184_cach_ly_provider.giai_phong(model, bang_chung=…)` — từ chối nếu thiếu bằng chứng.
Không in khoá. Chỉ ghi sha256[:8] của khoá để chứng minh hai lượt dùng CÙNG một khoá.

Phạm vi: CHỈ 4 model của hai hãng owner đã nạp. `gpt-5.4` / `gpt-5-mini` (OpenAI, chưa nạp) KHÔNG đụng.
"""
import hashlib
import json
import os
import sys
import time
from datetime import datetime, timedelta, timezone

try:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (ValueError, AttributeError):
    pass

BE = os.path.dirname(os.path.abspath(__file__))
GOC = os.path.dirname(os.path.dirname(BE))
sys.path.insert(0, BE)
VN = timezone(timedelta(hours=7))

MUC = ["claude-opus-4-6", "claude-sonnet-4-6", "deepseek-reasoner", "deepseek-v4-pro-real"]
KHONG_DUNG = ["gpt-5.4", "gpt-5-mini"]   # OpenAI — owner CHƯA nạp

HE_THONG = "Ban la bo kiem suc khoe API cua he thong. Khong phan tich gi them."
NGUOI_DUNG = 'Tra ve DUNG mot JSON: {"ok": 1}'


def bay_gio():
    return datetime.now(VN).isoformat(timespec="seconds")


def goi_thu(G, S, CL, m):
    """Đúng MỘT lượt. Trả dict kết quả; không bao giờ ném lỗi ra ngoài."""
    kq = {"model": m, "luc": bay_gio()}
    try:
        khoa = S._get_api_key_for_model(m)
    except Exception as e:
        kq.update(dat=False, loi="khong lay duoc khoa: %s" % type(e).__name__)
        return kq
    if not khoa:
        kq.update(dat=False, loi="KHONG_CO_KHOA")
        return kq
    kq["khoa_sha8"] = hashlib.sha256(khoa.encode()).hexdigest()[:8]
    t0 = time.perf_counter()
    try:
        if m.startswith("claude"):
            api_m = G.ANTHROPIC_MODEL_API_MAP.get(m, m)
            kq["model_api"] = api_m
            r = G._call_anthropic(api_m, HE_THONG, NGUOI_DUNG, khoa)
        else:
            route = G.DEEPSEEK_API_ROUTE.get(m) or {}
            kq["model_api"] = route.get("api_model", m)
            r = G._call_deepseek(m, HE_THONG, NGUOI_DUNG, khoa)
    except Exception as e:
        r = {"error": "API invocation wrapper error: %s" % e}
    kq["do_tre_s"] = round(time.perf_counter() - t0, 2)
    if not isinstance(r, dict):
        kq.update(dat=False, loi="ket qua khong phai dict: %r" % type(r).__name__)
        return kq
    if r.get("error"):
        loi = str(r.get("error"))
        kq.update(dat=False, loi=loi[:300], phan_loai=CL.phan_loai_loi(loi))
        return kq
    noi_dung = str(r.get("content") or "")
    kq.update(dat=bool(noi_dung.strip()), tra_loi=noi_dung.strip()[:120],
              tokens=r.get("tokens_used") or r.get("token_count"))
    if not kq["dat"]:
        kq["loi"] = "tra ve rong"
    return kq


def roster_hien_tai(R):
    ra = {}
    for mien in ("MN", "MT", "MB"):
        try:
            r = R.get_token_call_roster(region=mien, execution_class="official",
                                        include_challenger=True)
            ra[mien] = {"core": r.get("core"), "challenger": r.get("challenger"),
                        "loai_bo": [(x.get("model"), x.get("vi_sao")) for x in r.get("loai_bo") or []]}
        except Exception as e:
            ra[mien] = {"loi": repr(e)[:160]}
    return ra


def main():
    nha = "--nha" in sys.argv
    import gpt_analyzer as G
    import scheduler as S
    import _v11184_cach_ly_provider as CL
    import _v11185_roster_goi_token as R

    ev = {"version": "V11191", "bat_dau": bay_gio(), "che_do": "THU+NHA" if nha else "CHI_THU",
          "cach_ly_truoc": sorted(CL.danh_sach().keys()), "roster_truoc": roster_hien_tai(R),
          "ket_qua": [], "da_nha": [], "giu_cach_ly": []}

    print("=" * 92)
    print("  V11191 — gọi thử sức khoẻ provider · %s · chế độ %s" % (ev["bat_dau"], ev["che_do"]))
    print("  cách ly TRƯỚC:", ", ".join(ev["cach_ly_truoc"]) or "(trống)")
    print("=" * 92)

    dang_cach_ly = CL.danh_sach()
    for m in MUC:
        if m not in dang_cach_ly:
            print("  -  %-22s không bị cách ly — bỏ qua, không gọi" % m)
            ev["ket_qua"].append({"model": m, "bo_qua": "khong bi cach ly"})
            continue
        kq = goi_thu(G, S, CL, m)
        ev["ket_qua"].append(kq)
        if kq.get("dat"):
            print("  ✓  %-22s ĐẠT · %-18s · %5.2fs · tokens %s · khoá %s · «%s»"
                  % (m, kq.get("model_api"), kq["do_tre_s"], kq.get("tokens"),
                     kq.get("khoa_sha8"), kq.get("tra_loi", "")[:40]))
            if nha:
                bc = {"luot_goi_that": "OK", "luc": kq["luc"], "model_api": kq.get("model_api"),
                      "do_tre_s": kq["do_tre_s"], "tokens": kq.get("tokens"),
                      "khoa_sha8": kq.get("khoa_sha8"), "phien_ban": "V11191",
                      "can_cu": "owner bao da nap tien 25/11/2026 ~13:1x ICT"}
                r = CL.giai_phong(m, bang_chung=bc)
                if r.get("ok"):
                    ev["da_nha"].append(m)
                    print("       → ĐÃ NHẢ cách ly")
                else:
                    ev["giu_cach_ly"].append(m)
                    print("       → giai_phong TỪ CHỐI: %s" % r)
        else:
            ev["giu_cach_ly"].append(m)
            print("  ✗  %-22s HỎNG · %s · %s — GIỮ cách ly, KHÔNG gọi lại"
                  % (m, kq.get("phan_loai", "-"), str(kq.get("loi"))[:110]))

    for m in KHONG_DUNG:
        print("  ·  %-22s KHÔNG gọi (OpenAI chưa nạp) — giữ nguyên cách ly" % m)

    ev["cach_ly_sau"] = sorted(CL.danh_sach().keys())
    ev["roster_sau"] = roster_hien_tai(R)
    ev["ket_thuc"] = bay_gio()
    print("-" * 92)
    print("  cách ly SAU :", ", ".join(ev["cach_ly_sau"]) or "(trống)")
    for mien in ("MN", "MT", "MB"):
        a, b = ev["roster_truoc"][mien], ev["roster_sau"][mien]
        print("  roster %s  TRƯỚC core=%s ch=%s" % (mien, a.get("core"), a.get("challenger")))
        print("            SAU   core=%s ch=%s · loại=%s"
              % (b.get("core"), b.get("challenger"), b.get("loai_bo")))

    d = os.path.join(GOC, "artifacts", "v11191")
    os.makedirs(d, exist_ok=True)
    p = os.path.join(d, "thu_suc_khoe_%s.json" % ("nha" if nha else "thu"))
    with open(p, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(ev, fh, ensure_ascii=False, indent=1)
    print("  bằng chứng:", p)
    print("=" * 92)
    return 0 if not ev["giu_cach_ly"] else 1


if __name__ == "__main__":
    sys.exit(main())
