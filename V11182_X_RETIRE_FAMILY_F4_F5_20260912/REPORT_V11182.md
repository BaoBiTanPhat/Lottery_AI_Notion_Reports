# BÁO CÁO V11182 — §X RETIRE DEAD FAMILY · F4 ĐO LẠI MỘT LẦN · F5 · HARDEN INFRA

> **Phiên:** Prompt TỔNG LỰC 43 R1 §X, bắt đầu 11/09/2026 23:44 → kết 12/09/2026
> **Active Plan:** `PLAN-20260723-lottery-doc-restructure` · không mở Prompt 44 / FU / Plan mới
> **Terminal kỹ thuật:** `RETIRED_FAMILY_CRON_DISABLED_ZERO_OFFICIAL_IMPACT` +
> `REUSABLE_CHALLENGER_INFRA_HARDENED`
> **F4:** `F4_DIGIT_ALGEBRA_RETIRED_AFTER_VALID_MEASUREMENT`
> **F5:** `F5_RETIRED_NO_SIGNAL` · `NO_SUCCESSOR_PASSES_PREDEPLOY_GATE`

---

## 1. Tóm tắt

Tắt cron của family đã chết (4 dòng, comment-out, **0 dòng khác bị động**). Sửa circuit
breaker / retry / validator / canonical lineage. Sửa thước đo: `E[RR]` phải là tổ hợp
**không hoàn lại**, không phải công thức có-hoàn-lại của V11181 (`RL-040`). Đo lại F4
**đúng một lần** với prereg có hash — **117.270 cell, BH-FDR giữ 0**, holdout **không mở**.
Dựng F5 (pooled multivariate logistic ranker) — **trượt cả ba miền và trượt về phía ÂM**.

**Không gọi một lời gọi LM/LLM nào** trong phiên, đúng §X10: F5 chưa pass thì không tiêu
provider.

Official **zero-write** xác minh theo `PRE_X_MANIFEST` · **0 restart** · digest lịch sử
bất biến **không đổi**.

---

## 2. Owner yêu cầu gì — nguyên văn + giờ

**11/09/2026 ~23:44 ICT**, prompt §X:

- *"Cấm: WAIT_DATA chung chung; tiếp tục family đã chết chỉ để có thêm dòng; gọi 19 model mỗi ngày để chứng minh hạ tầng của một family vô tín hiệu."*
- *"F4_DIGIT_ALGEBRA: phép đo trước sai G2; chưa được đánh giá hợp lệ; trạng thái đúng phải là `MEASUREMENT_INVALID_NOT_EVALUATED`; không được gọi `F4_NO_SIGNAL` khi chưa đo lại đúng."*
- *"Không có lần chạy thứ hai bằng cách đổi ngưỡng."*
- *"Nếu deterministic F5 chưa pass: không gọi LM/LLM; không tiêu provider; không dựng prompt giả."*
- *"Không dùng 32 nhãn lo3 lịch sử sai."*
- *"Mọi đo lường phải kết thúc bằng REPAIR, RETIRE, HISTORICAL_GATE_PASS, hoặc BLOCKED_WITH_EXACT_REASONS."*

Đầy đủ ở `docs/SO_TUONG_TAC_OWNER.md` mục 11–12/09 và `QD-078`.

---

## 3. §X0 · PRE_X_MANIFEST

Chụp **trước mọi mutation**, lưu ở `artifacts/v11178/PRE_X_MANIFEST.json`.

| | |
|---|---|
| private | `fu438/admin-only-p0a` @ `302ba45` = `master` = `origin/master`; **0 commit chưa push** |
| public | `main` @ `f8e5e37` = `origin/main`; worktree **SẠCH** |
| worktree riêng | phạm vi `web/backend` + `docs` + `CHANGELOG.md` **SẠCH**; 228 mục untracked đều là `backups/` có sẵn |
| service | PID `3870722` · `NRestarts=0` · `active` · health **200** |
| crontab | 153 dòng · SHA `6e2687eb…` · 4 dòng challenger |
| tiến trình challenger | **(không có)** |
| DB | 849.895.424 byte · 4 bảng `v11178_*` |
| official rows | `predictions` 14.767 · `final_bundles` 588 · `lottery_results` 15.462 · `model_daily_eval` 14.631 · `day_governance` 587 · `shadow_candidates` 39.206 |
| `output_counterfactual_rank NOT NULL` | **0** |
| digest lịch sử bất biến | `day_governance date≤2026-09-09` · 581 dòng · `786e350c…` |

---

## 4. §X1 · CRON RETIREMENT RECEIPT

```
trang_thai : F1_PROVIDER_CRON_DISABLED_RETIRED_NO_SIGNAL
sha before : 6e2687ebfae9b41d0644f01475bc330f28f38a1291dad685259957973ed1945d
sha after  : 4e16ed3d9e1f70e136a8cf1d2ec96cd80ac0f6d86c273305a859d0b97c287488
dòng đang chạy : 97 → 93   (tắt đúng 4)
giảm đúng bằng số tắt : True
đọc lại crontab thật  : khớp · 0 dòng F1 còn chạy
rollback   : crontab /root/Lottery_AI_Test/artifacts/v11178/crontab_before_X1.txt
```

Bốn dòng đã tắt (**comment-out, không xoá**): EOD `5 19` · MT delta `38 16` · MB delta
`33 17` · BASE_D1 `30 13`.

**Không đụng:** scheduler production · `ai_chain` · scraper · `auto_verify` · official
bundle jobs · mọi cron Lottery khác. **Không xoá** source, bảng `v11178_*`,
`shadow_candidates`, freeze packets, lane receipts, historical evidence.

---

## 5. §X2 · CIRCUIT / RETRY — trước / sau

**Sự thật phải đọc mã nguồn mới biết**, và bản đầu của tôi đoán sai (`RM-10`):

| | |
|---|---|
| API thật | `gpt_analyzer._OPENROUTER_CIRCUIT_BREAKER` (dict) · `_openrouter_circuit_check()` |
| tôi đoán | `_circuit_state` / `_CIRCUIT` — **không tồn tại**, cả 4 model trả `UNKNOWN`, adapter **mù hoàn toàn** |
| phạm vi thật | circuit **CHỈ** áp cho tuyến **OpenRouter**; model đi anthropic/google/openai/deepseek **không có circuit** ⇒ `NO_CIRCUIT_FOR_ROUTE`, gọi được bình thường. Trả `UNKNOWN` cho chúng rồi chặn là **tự khoá mình** |
| vòng đời | circuit là bộ nhớ **trong tiến trình** ⇒ challenger khởi động luôn sạch; nó chỉ mở **trong** lượt chạy. Giá trị của §X2 là chặn model **sau** và chặn retry vô ích |

| hành vi | TRƯỚC | SAU |
|---|---|---|
| `BLOCKED…COST_HIGH` | xếp `ERROR` ⇒ **nằm trong danh sách retry** ⇒ retry chắc chắn vô ích | `SKIPPED_CIRCUIT_OPEN`, **không gọi provider**, vẫn có receipt, vẫn trong scheduled denominator |
| 401/403 | retry | `AUTH_ERROR` ⇒ **không** retry |
| thiếu credential | retry | **không** retry |
| 429 còn đủ giờ | retry | retry (đúng) |
| 429 không đủ giờ | retry | **không** — `KHONG_DU_THOI_GIAN:100s<165s` |
| đọc circuit | — | **thuần đọc**: đọc thẳng dict, không gọi `_openrouter_circuit_check()` (hàm đó **xoá** entry hết hạn) — đã kiểm: entry vẫn còn sau khi đọc |

Snapshot trước mỗi lời gọi ghi đủ: `provider_route` · `circuit_state` · `circuit_reason` ·
`circuit_opened_at` · `circuit_next_retry_at` · `credential_available` · `planned_timeout` ·
`target_cutoff` · `execution_class`.

---

## 6. §X3 · VALIDATOR — trước / sau

| ca | TRƯỚC | SAU |
|---|---|---|
| `decision=RANKED` + `uncertainty=low` + **toàn bộ confidence=0** | **CHO QUA** — đúng hình dạng `gpt-oss-120b` trả ở cả ba miền ngày 11/09 | `CONTRACT_INVALID_ZERO_CONFIDENCE_RANKED` + `UNCERTAINTY_LOW_BUT_ALL_CONFIDENCE_ZERO` |
| `confidence = NaN / Inf` | không kiểm | `CONFIDENCE_NAN_OR_INF` |
| `confidence` là chuỗi | không kiểm | `CONFIDENCE_LA_CHUOI` |

Regression fixture dựng **đúng hình dạng lỗi của `gpt-oss-120b` ngày 11/09** (test `B-neg`).
Một abstain đội lốt RANKED, nếu lọt, sẽ bị đếm thành tín hiệu khi ai đó chấm "nhóm RANKED".

---

## 7. §X4 · CANONICAL LINEAGE — trước / sau

```
TRƯỚC:  if mong and aid != mong:  bo["khong_phai_canonical"] += 1; continue
        →  canonical_attempt_id NULL  ⇒  MỌI candidate có attempt_id đều LỌT. Cửa sau.

SAU:    if not mong: bo["MISSING_CANONICAL_ATTEMPT_ID"] += 1; continue
        if not aid:  bo["MISSING_CANDIDATE_ATTEMPT_ID"] += 1; continue
        if aid != mong: bo["NON_CANONICAL_ATTEMPT_CANDIDATE"] += 1; continue
        →  KHÔNG có canonical thì FAIL, không phải "có thì mới so".
```

Thêm `kiem_mot_canonical()` — §X4.6: mỗi tuple
`date × region × stage × execution_class × model × method_version` phải có **đúng một**
canonical run; nhiều hơn là hỏng dữ liệu, không phải cảnh báo.

---

## 8. §X6 · THƯỚC ĐO — HIT@K và MRR là HAI thước

**ĐÍNH CHÍNH — `RL-040`. Ba giá trị `E[RR]` mà V11181 công bố ĐÃ RÚT LẠI.** Bảng dưới
nêu chúng **chỉ để đối chiếu**, không phải để dùng lại. V11181 dùng `Σ b(1−b)^(i−1)/i` —
mô hình **có hoàn lại**. Top-K là K đuôi **khác nhau, rút không hoàn lại**. Công thức đúng:

```
Random Hit@K = 1 − C(N−M, K) / C(N, K)
P(R = r)     = [ P(N−M, r−1) / P(N, r−1) ] × M / (N−r+1)
E[RR]        = Σ_{r=1..K} P(R=r) / r
```

Tính bằng `Fraction` (số nguyên chính xác), không float trung gian.

| miền | M | `E[RR]` V11181 | **ĐÚNG** | observed | delta V11181 | **delta ĐÚNG** |
|---|---|---|---|---|---|---|
| MN | 41 | 0,6192 | **0,6207** | 0,1667 | −0,4525 | **−0,4541** |
| MT | 32 | 0,5345 | **0,5367** | 0,2500 | −0,2845 | **−0,2867** |
| MB | 24 | 0,4459 | **0,4487** | 0,5000 | +0,0541 | **+0,0513** |

**Hướng kết luận không đổi.** Tự kiểm **12/12 ĐẠT**, gồm fixture **tính tay**
`N=5, M=2, K=2 → hit@2 = 7/10 · E[RR] = 11/20`, và một phép **chứng minh hai công thức khác
nhau** (0,536686 vs 0,534545) — cột trái của bảng trên là giá trị **ĐÃ RÚT LẠI** theo
`RL-040`, cột phải là giá trị dùng từ nay.

---

## 9. §X5 · MA TRẬN OFFICIAL NGÀY 11/09 — đầy đủ

> **Bảng này là TRẠNG THÁI của MỘT NGÀY (11/09), không phải tuyên bố hiệu quả.** Các ô
> `WIN`/`LOSE`/`PARTIAL` là nhãn kết quả của đúng ngày đó. Mọi phép so với nền ở đây đều
> tính riêng cho ngày đó và **cấm trích** làm bằng chứng về lợi thế. Phép đo nhiều cửa sổ
> của bộ k số (lô2/lô3/xiên) nằm ở `V11086` — xem bảng cửa sổ ở đó, không suy từ bảng này
> (`PRJ-SELECTION-WINDOW-001`).

**Đây là trạng thái của MỘT NGÀY (hôm nay 11/09) — CẤM trích riêng làm bằng chứng hiệu quả
(`PRJ-SELECTION-WINDOW-001`).**

| trạng thái **một ngày** (CẤM trích riêng) | MN | MT | MB |
|---|---|---|---|
| đài mong đợi / có mặt | 3/3 | 2/2 | 1/1 |
| completeness | `COMPLETE` | `COMPLETE` | `COMPLETE` |
| đuôi trúng (union) | 41 | 32 | 24 |
| `bach_thu` (status) | `95` (LOSE) | `92` (LOSE) | `95` (LOSE) |
| `lo2` — nhãn **một ngày** | `95,35` (LOSE) | `92,42` (LOSE) | `95,53` (**PARTIAL**) |
| `lo3` = 3-càng — nhãn **một ngày** | `095` (LOSE) | `892` (LOSE) | `695` (LOSE) |
| `xien2` / `xien3` — nhãn **một ngày**, CẤM trích riêng | LOSE / LOSE | LOSE / LOSE | LOSE / LOSE |
| `ranked[0]` | `95` | `92` | `95` |
| `bach_thu == ranked[0]` | **True** | **True** | **True** |
| hạng trúng đầu tiên | 6 | 4 | 2 |
| `observed RR` vs nền EXACT | 0,1667 vs 0,6207 | 0,2500 vs 0,5367 | 0,5000 vs 0,4487 |
| **stage forensic** | `RANKER_MISS` | `RANKER_MISS` | `RANKER_MISS` |

**Không có `SELECTOR_MISS`**: `bach_thu == ranked[0]` ở cả ba miền ⇒ lớp chọn **không**
đổi số. **Không có `GENERATOR_MISS`**: đuôi trúng **có** trong candidate universe. Nguyên
nhân ở **tầng xếp hạng** — đuôi trúng có mặt nhưng không được đẩy lên hạng 1.

### 3-càng — SCORABLE, và lineage khớp

`lo3` **chính là** 3-càng. Đo được: **588/588 bundle** có `len(lo3)=3` **và** `lo3` luôn
kết thúc bằng `bach_thu` ⇒ `lo3 = prefix + lane-specific final BT`, đúng kiến trúc đã khoá.

| | MN | MT | MB |
|---|---|---|---|
| `lo3` | `095` | `892` | `695` |
| prefix | `0` | `8` | `6` |
| lineage khớp BT | ✓ | ✓ | ✓ |
| 3-càng thật trong ngày | 50 | 34 | 22 |
| trúng | — | — | — |

### 32 nhãn `lo3 WIN` sai — xác định ĐÚNG dòng nào, không ghi DB

V11166 phát hiện 57 lưu / 25 thật / **32 sai** nhưng ghi là **BỊ CHẶN** vì phải ghi
production DB. Phiên này **chấm lại đọc-thuần** từ `lottery_results`:

```
WIN trong DB = 57 · WIN THẬT = 25 · WIN SAI = 32 · theo tháng = {'2026-03': 32}
```

**Khớp chính xác V11166 qua một đường mã hoàn toàn khác.** 32 dòng nay có `rowid` cụ thể
(vd `rowid=5 2026-03-01 MN lo3=571 bt=71`) và được loại khỏi mọi cohort **mà không ghi DB**.

---

## 10. §X7 · MA TRẬN 19 MODEL — không một mean duy nhất

| execution class | miền | scheduled | scoreable | coverage | `conditional_MRR` | `all_scheduled_MRR` | `provider_healthy_MRR` | nền EXACT |
|---|---|---|---|---|---|---|---|---|
| `BASE_D1_LIVE` | MN | 19 | **0** | 0,000 | — | 0,000 | — | 0,6207 |
| `BASE_D1_LIVE` | MT | 19 | **0** | 0,000 | — | 0,000 | — | 0,5367 |
| `BASE_D1_LIVE` | MB | 19 | **0** | 0,000 | — | 0,000 | — | 0,4487 |
| `MT_DELTA_LIVE` | MT | 19 | 15 | **0,789** | 0,2852 | **0,2251** | 0,2852 | 0,5367 |
| `MB_DELTA_LIVE` | MB | 19 | 11 | **0,579** | 0,2954 | **0,1711** | 0,2954 | 0,4487 |

`BASE_D1_LIVE` scoreable = **0** vì 414 dòng của lượt unfrozen thiếu `attempt_id` ⇒ bị luật
§X4 loại — **đúng thiết kế, không phải lỗi**.

Khoảng cách giữa `conditional_MRR` và `all_scheduled_MRR` chính là survivorship bias:
MT **0,2852 → 0,2251**; MB **0,2954 → 0,1711**. Báo một con số duy nhất sẽ giấu mất
21% và 42% phần thiếu. **Cả hai đều dưới nền EXACT.**

Đơn vị bằng chứng là **ngày × miền**, không phải 15 hay 11 quan sát độc lập — các model
dùng chung payload và candidate.

---

## 11. §X8 · F4 — ĐO ĐÚNG MỘT LẦN

Prereg `F4_DIGIT_ALGEBRA_PREREG.json`, hash `ac7a05c035899dbf…`, sinh **trước** khi chạy.

Họ = năm ánh xạ đại số chữ số trên đuôi nguồn `(a,b)`:
`D1_sum_prod` · `D2_diff_sum` · `D3_sum_double` · `D4_prod_diff` · `D5_swap_sum`.

**Nền in cạnh nhau** (§X8.A.3) — chính chỗ phép đo cũ đã ngã:

| miền | nền per-station | nền gộp miền | lệch | cell | du support |
|---|---|---|---|---|---|
| MN | 0,165936 | 0,431167 | **2,60×** | 56.070 | 56.070 |
| MT | 0,164772 | 0,351667 | **2,13×** | 43.380 | 43.380 |
| MB | 0,238239 | 0,238239 | **1,00×** | 17.820 | 17.820 |

**Hiệu chỉnh trên cả ba miền một lần:**

```
tổng cell        : 117.270
log₁₀ p tốt nhất : −4,8445          (p ≈ 1,4e-05)
ngưỡng Bonferroni: −6,3702
BH-FDR α=0,10 giữ: 0
```

Ô mạnh nhất `MT thứ 4 · Gia Lai ← MN/Đồng Nai Giải nhất[0] lag=2 D3_sum_double`:
`14/26 = 53,85%` vs nền `16,48%`, lift **+37,37pp**. Nghe rất to — nhưng với 117.270 phép
thử, kỳ vọng thuần ngẫu nhiên là `117270 × 1,4e-05 ≈ 1,7` ô như thế, và support chỉ **26**
(`RM-04`: n nhỏ là *chưa được phép kết luận*).

⇒ **`F4_DIGIT_ALGEBRA_RETIRED_AFTER_VALID_MEASUREMENT`. Holdout KHÔNG mở.** Dừng vĩnh viễn
theo `stop_rule` đã đăng ký. **Không có lần chạy thứ hai bằng cách đổi ngưỡng.**

---

## 12. §X9 · F5 — POOLED MULTIVARIATE CONTEXT RANKER

Prereg `F5_PREREG.json`, hash `53518dd8181d93fb…`, seed `20260912`, sklearn 1.7.2.

- **Trục khác hẳn F1–F4**: không phải ánh xạ ô-nguồn → đuôi-đích, mà là *"với ngữ cảnh trước
  cutoff, đuôi nào ở đài này có xác suất cao hơn"* — **một** mô hình, **một** bộ tham số.
- **Đơn vị mẫu**: `date × region × station × tail(00–99)`; **đơn vị bằng chứng**: `(ngày × đài)`.
  100 đuôi cùng ngày dùng chung ngữ cảnh và bị ràng buộc đúng M đuôi trúng — coi là 100 quan
  sát độc lập sẽ phóng đại cỡ mẫu ~100 lần.
- **12 feature**, tất cả chỉ dùng ngày **trước** ngày đích (cửa sổ 90 ngày) + upstream cùng
  ngày theo chiều `MT←MN`, `MB←MN,MT`.
- **Blocked time split**, `StandardScaler` fit **chỉ trên train**, nested blocked validation
  trong discovery, holdout mở **đúng một lần**.
- **Kiểm định Poisson-binomial chính xác** (mỗi ngày-đài có nền riêng vì M khác nhau).

| miền | train | holdout | n (ngày×đài) | Hit@10 | nền EXACT | **effect** | Wilson95 lower | p |
|---|---|---|---|---|---|---|---|---|
| MN | 56.600 | 18.800 | 188 | 0,8032 | 0,8481 | **−4,49pp** | 0,7405 < nền | 0,962 |
| MT | 43.800 | 14.500 | 145 | 0,8138 | 0,8514 | **−3,76pp** | 0,7426 < nền | 0,915 |
| MB | 17.600 | 6.000 | 60 | 0,8833 | 0,9410 | **−5,77pp** | 0,7782 < nền | 0,976 |

**Nhánh đối chứng — baseline tần suất đơn giản** (§X9): −3,42 / −1,00 / −0,77 pp so với
ngẫu nhiên, tức **xấp xỉ ngẫu nhiên**. Đó vừa là yêu cầu hợp đồng vừa là **phép kiểm chính
đường ống**: nếu nó ra cao bất thường thì phải nghi rò rỉ; nó không.

Và mô hình học được **thua cả baseline**: −1,06 / −2,76 / −5,00 pp.

⇒ **`F5_RETIRED_NO_SIGNAL`** · **`NO_SUCCESSOR_PASSES_PREDEPLOY_GATE`**.

**Một phát hiện dùng lại được:** mọi ranker **tập trung** vào đuôi tần suất cao / vừa ra gần
đây đều **mất độ phủ** so với Top-10 trải đều — vì tập trúng gần như đồng đều. Đó là lý do
cả F5 lẫn baseline tần suất đều **âm**, không phải do lỗi cài đặt.

### §X10 — LM/LLM

F5 chưa pass ⇒ **không gọi một lời gọi LM/LLM nào**, không tiêu provider, không dựng prompt
giả. Đúng hợp đồng.

---

## 13. §X11 · TEST

| bộ | kết quả |
|---|---|
| `_v11178_thu_v12.py` | **51/51 ĐẠT** |
| `_v11178_thu_v2_ledger.py` | **16/16 ĐẠT** (DB thật) |
| `_v11180_thu_w.py` | **33/33 ĐẠT** |
| `_v11182_thu_x.py` (§X11) | **50/50 ĐẠT** |
| `_v11182_thuoc_do.py --tu-kiem` | **12/12 ĐẠT** |
| `_v11180_lich_dai.py` | **ĐẠT** |

Mỗi test semantic có fixture **dương** và **âm**. Hai phép trong `_v11180_thu_w.py` phải
sửa vì brittle theo ngày (tìm gói freeze của *hôm nay*, mà family đã retire nên không còn
sinh gói) và một phép khẳng định **hình dạng code cũ** mà §X4 vừa siết — đã sửa, không nới.

---

## 14. §X12 · ZERO-WRITE

So với `PRE_X_MANIFEST`:

| bảng | trước | sau | |
|---|---|---|---|
| `predictions` | 14.767 | 14.767 | **OK** |
| `final_bundles` | 588 | 588 | **OK** |
| `lottery_results` | 15.462 | 15.462 | **OK** |
| `model_daily_eval` | 14.631 | 14.631 | **OK** |
| `day_governance` | 587 | 587 | **OK** |
| `shadow_candidates` | 39.206 | 39.206 | **OK** |
| `output_counterfactual_rank NOT NULL` | 0 | 0 | **OK** |
| 7 tệp official (`main.py`, `scheduler.py`, `database.py`, `gpt_analyzer.py`, `model_registry.py`, `combo_super.py`, `daily_evaluation.py`) | — | — | **KHÔNG ĐỔI** |
| digest lịch sử bất biến (581 dòng) | `786e350c…` | `786e350c…` | **KHÔNG ĐỔI** |
| service | PID `3870722` · `NRestarts=0` · health 200 | như trước | **KHÔNG RESTART** |

Bảng challenger cũng **không đổi** (149 / 124 / 27 / 3) vì cron đã tắt và không lượt nào chạy.

---

## 15. §X14 · TERMINAL

```
TECHNICAL : RETIRED_FAMILY_CRON_DISABLED_ZERO_OFFICIAL_IMPACT
          + REUSABLE_CHALLENGER_INFRA_HARDENED
F4        : F4_DIGIT_ALGEBRA_RETIRED_AFTER_VALID_MEASUREMENT
F5        : F5_RETIRED_NO_SIGNAL
          + NO_SUCCESSOR_PASSES_PREDEPLOY_GATE

PREDICTIVE_LIFT = NOT_PROVEN
POOL_VERDICT    = HOLD
SC12            = CLOSED · DO_NOT_REOPEN
```

---

## 16. Vướng vấp

1. **`RM-10` — đoán tên circuit API.** `_circuit_state`/`_CIRCUIT` không tồn tại; adapter trả `UNKNOWN` cho **cả 4** model thử, tức mù hoàn toàn, và vì `UNKNOWN` bị xử như `OPEN` nên nó sẽ **chặn mọi lời gọi**. Tên thật: `_OPENROUTER_CIRCUIT_BREAKER` + `_openrouter_circuit_check`.
2. **`RL-041` — hai kết luận sai cùng một gốc.** So `lo3` (3 chữ số) với đuôi 2 chữ số ⇒ `57/57 nhãn sai`; và đi tìm cột tên `"cang"/"prefix"` ⇒ `NOT_SCORABLE_MISSING_PREFIX_LINEAGE`. Bị bắt vì `57/57` quá cực đoan và mâu thuẫn V11166.
3. **`RM-09` lần thứ tư.** Test `F-pos` quét `"shuffle" not in src5` trên cả tệp — chữ đó nằm trong chính câu *"KHONG shuffle"* của tôi. Sửa: phân tích AST, soi **danh sách hàm được gọi**.
4. **Test brittle theo ngày.** Hai phép tìm gói freeze của *hôm nay*; qua nửa đêm + family retire ⇒ trượt. Sửa: tìm gói **hợp lệ bất kỳ**.
5. **Crontab SHA hai giá trị.** `crontab -l | sha256sum` (có newline cuối) = `6e2687eb…`; băm chuỗi đã strip = `8b7c84ea…`. Cả hai đúng trong phương pháp của nó; đã thống nhất dùng một cách.

---

## 17. Gỡ về

```bash
crontab /root/Lottery_AI_Test/artifacts/v11178/crontab_before_X1.txt   # bật lại 4 dòng F1
# Không có mutation nào khác cần gỡ: phiên này KHÔNG ghi DB, KHÔNG restart service,
# KHÔNG sửa tệp official nào.
```

---

## §62 · NGUỒN BA LỚP

### `OWNER_SAID`
- 11/09 ~23:44 — *"Cấm… gọi 19 model mỗi ngày để chứng minh hạ tầng của một family vô tín hiệu."*
- 11/09 ~23:44 — *"Không được gọi `F4_NO_SIGNAL` khi chưa đo lại đúng."*
- 11/09 ~23:44 — *"Nếu deterministic F5 chưa pass: không gọi LM/LLM; không tiêu provider."*

### `CODE_DID`
- `crontab -l` sau thao tác: **0 dòng** `_v11178_(lane|eod)` đang chạy; 97 → 93 dòng.
- `artifacts/v11178/F4_DISCOVERY_RESULT.json` — `n_cell_hieu_chinh=117270`, `n_qua_fdr=0`, `holdout_da_mo=false`.
- `artifacts/v11178/F5_RESULT.json` — `mien_dat_gate=[]`, `terminal=F5_RETIRED_NO_SIGNAL`.
- `v11178_attempts` 149 → 149: **0 lời gọi provider** trong phiên.

### `DOC_SAID`
- `REPORT_V11181.md` mục 12 — `E[RR]` **đã rút** (`RL-040`), giá trị đúng ở ĐÍNH CHÍNH X-1.
- `REPORT_V11166.md` — *"32 nhãn lo3 WIN sai, P1 bị chặn vì phải ghi production DB"* ⇒ nay **xác định được đúng 32 dòng mà không cần ghi**.

**LỆCH BA LỚP:**
1. `DOC_SAID` ≠ `CODE_DID`: V11181 công bố `E[RR]` bằng công thức có-hoàn-lại ⇒ `RL-040`, sửa công thức, giữ hướng kết luận.
2. `DOC_SAID` ≠ `CODE_DID`: V11166 ghi việc chấm lại 32 nhãn là **bị chặn**; đo lại đọc-thuần cho thấy **không cần ghi DB** mới xác định được ⇒ việc đó **mở lại được**.
3. `OWNER_SAID` = `CODE_DID`: *"không tiêu provider"* — `v11178_attempts` không tăng một dòng.

---

TanPhatAI cần làm: ghi **`V11182`** — `governance_seq 497`, công khai bản này cùng `CONVERSATION_CONTEXT_V11182_20260912.md` và `evidence/`. Ghi **TERMINAL KỸ THUẬT `RETIRED_FAMILY_CRON_DISABLED_ZERO_OFFICIAL_IMPACT` + `REUSABLE_CHALLENGER_INFRA_HARDENED`**; **F4 `F4_DIGIT_ALGEBRA_RETIRED_AFTER_VALID_MEASUREMENT`** (117.270 cell, BH-FDR giữ **0**, **holdout không mở**); **F5 `F5_RETIRED_NO_SIGNAL` + `NO_SUCCESSOR_PASSES_PREDEPLOY_GATE`** (effect **−4,49 / −3,76 / −5,77 pp**, đều ÂM; baseline tần suất ≈ ngẫu nhiên nên đường ống đo đúng; mô hình thua cả baseline). Ghi **cron family F1 đã tắt**: 4 dòng comment-out, dòng đang chạy **97→93**, 0 dòng F1 còn chạy, rollback `crontab_before_X1.txt`. Ghi **KHÔNG gọi một lời gọi LM/LLM nào** trong phiên (`v11178_attempts` 149→149) — đúng §X10. Ghi **`RL-040`**: `E[RR]` của V11181 dùng công thức **có hoàn lại**, giá trị đúng là **0,6207 / 0,5367 / 0,4487**, delta đúng **−0,4541 / −0,2867 / +0,0513**, **hướng kết luận không đổi**. Ghi **`RL-041`**: hai kết luận sai cùng một gốc — `57/57 nhãn lo3 sai` (so 3 chữ số với đuôi 2 chữ số) và `NOT_SCORABLE_MISSING_PREFIX_LINEAGE` (đi tìm cột tên "cang"/"prefix"); **3-càng CHÍNH LÀ cột `lo3`**, đo được **588/588** bundle có `len(lo3)=3` và luôn kết thúc bằng `bach_thu`. Ghi **32 nhãn `lo3 WIN` sai nay xác định được ĐÚNG dòng nào** (kèm rowid, toàn bộ tháng 03/2026) bằng phép chấm lại **đọc thuần** — khớp chính xác V11166 qua đường mã khác, và **không cần ghi DB** như V11166 từng lo. Ghi **stage forensic 11/09 = `RANKER_MISS` cả ba miền** (`bach_thu == ranked[0]` ⇒ không phải `SELECTOR_MISS`; đuôi trúng có trong universe ⇒ không phải `GENERATOR_MISS`). Ghi **survivorship bias đo được**: `conditional_MRR` → `all_scheduled_MRR` là **0,2852→0,2251** (MT) và **0,2954→0,1711** (MB). Ghi **ZERO-WRITE**: 6 bảng + 7 tệp official + digest lịch sử **không đổi**, **0 restart**, health 200. Ghi **README và READ_THIS_FIRST đã sửa** (từ `V10861` và `V74` → `V11182`; link org `irissnss` → `BaoBiTanPhat` ở router gốc; thân báo cáo cũ **giữ nguyên làm bản ghi**). **Không mở Prompt 44. Không mở FU mới. Không mở Plan mới. Không trộn ERP. CHƯA sync Notion.**
