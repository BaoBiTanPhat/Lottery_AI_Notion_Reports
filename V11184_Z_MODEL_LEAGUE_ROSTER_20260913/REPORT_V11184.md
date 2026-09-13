# REPORT V11184 — §Z · FAST MODEL LEAGUE · DỪNG ĐỐT TOKEN · ĐÓNG KHOẢNG TRỐNG V11183 · CỔNG OPTIMIZER · AN TOÀN RETRAIN · GENERATOR THUẦN NGỮ CẢNH

> **Phiên:** 13/09/2026, 20:44 → 22:xx ICT · **Mã đọc §58:** `XH1309` · **Prompt:** TỔNG LỰC LẦN 43 R1 §Z
> **Khoá Owner mới:** `QD-079 C1+C2+C3 = OWNER_APPROVED` · `WEEKLY_MODEL_LEAGUE = OWNER_APPROVED` ·
> `INITIAL_LLM_ROSTER_COMPRESSION = OWNER_APPROVED` (`QD-080`)
> **Khoá giữ nguyên:** `SC12=CLOSED` · `PREDICTIVE_LIFT=NOT_PROVEN` · `POOL_VERDICT=HOLD` ·
> `MATERIALIZATION_OPTION=B` · `F1`–`F5` `RETIRED`

---

## 1. EXECUTIVE TERMINAL — một trang

| terminal bắt buộc | kết quả |
|---|---|
| `V11183_PRIVATE_PUBLIC_LINEAGE` | **`RECONCILED`** |
| `CURRENT_REGIME_MODEL_LEADERBOARD` | **`PUBLISHED`** — kèm kết luận: Gate 2 **không phân biệt được model nào** |
| `INITIAL_LLM_ROSTER_COMPRESSION` | **`NO_SAFE_CHANGE_WITH_REASON`** — đã tính xong, đã replay, đã có rollback; **chưa lật** vì blocker chính xác ở §6.4 |
| `DIRECT_TOKEN_CALL_CAP` | **`EXACT_BLOCKER`** — chưa đạt `MAX_4`; đã giảm **8 → 6** LLM output-eligible bằng cách ly, chứng minh tại chính điểm gọi |
| `PROVIDER_WASTE` | **`QUARANTINED_NO_RETRY`** |
| `QD079_OPTIMIZER_GATE` | **`DEPLOYED_TESTED`** |
| `RETRAIN_SAFETY` | **`CANDIDATE_PROMOTION_AND_ROLLBACK_READY`** |
| `PURE_CONTEXT_GENERATOR` | **`OFFLINE_PASS_TO_BOUNDED_SHADOW`** |
| `PREDICTIVE_LIFT` | **`NOT_PROVEN`** — không nâng bằng kết quả xanh riêng ngày 13/09 |

**Phát hiện lớn nhất của phiên:** bạch thủ official **không phải** top-1 của phiếu model trong
**16.8%** số ngày. Bốn tầng ghi đè được Owner duyệt (`V10640` MN per-slice · `V10767` MB prev-day ·
`V10789` MB lane · `V10790` MT lane, `main.py:10255/10276/10296/10316`) thay `ranked[0]` bằng số
khác. Trên những ngày đó, câu hỏi *"model nào cứu/phá TOTAL"* **không có nghĩa** — không model nào
quyết cả.

**Một next action duy nhất:** truy đúng call-site dựng `selected_models` cho vòng AI chain hằng
ngày (`scheduler.py` quanh dòng 5897), chứng minh nó lọc theo `allowed_regions`, rồi lật roster
8 → 4. **Hạn: trước 2026-09-20 02:00 ICT.** Tới hạn mà chưa xong ⇒ terminal bắt buộc
`ROSTER_COMPRESSION_RETIRED`, không được gia hạn lần hai.

---

## 2. ĐÃ LÀM GÌ — có bằng chứng, có hash

| # | việc | trạng thái | bằng chứng |
|---|---|---|---|
| 1 | FF `master` để đóng khoảng trống lineage V11183 | XONG | `master`=`origin/master`=`1f0df1e`, fast-forward thuần, không force |
| 2 | `QD-079 C1+C2+C3` | **ĐÃ TRIỂN KHAI** | `weight_optimizer.py` `35bd1fff…`→`4bfcf5fb…` (LF); restart PID `3870722→62494` |
| 3 | Khoá an toàn retrain | **ĐÃ NỐI VÀO** | `_v11184_retrain_an_toan.py` 16/16; checkpoint thật `20260913_210913`, 28 tệp, 52 MB |
| 4 | Cách ly provider, không retry | **ĐÃ TRIỂN KHAI** | `_v11184_cach_ly_provider.py` 23/23; guard tại `gpt_analyzer._invoke_model_api`; restart PID `62494→85063` |
| 5 | Intake model mới có hạn định | XONG | `_v11184_intake_model.py` 19/19 |
| 6 | Leaderboard current-regime | XONG | cổng tái lập **99.38%**, `evidence/z_lb3.py` |
| 7 | Đưa hai tệp canonical VPS-only vào repo | XONG | `_canonical_v11165/` — `.gitignore:126` loại `artifacts/` nên chúng **chưa từng được git theo dõi** |
| 8 | Bộ thử §Z | XONG | **65/65** local và VPS |

---

## 3. MA TRẬN MODEL 13/09 (§Z-C)

81/81 dòng (27 model × 3 miền), 28/28 trường bắt buộc. Tái lập chính xác **MN 89 · MT 54 · MB 40**,
**0/30 mismatch** trong ranked top — 13/09 là ngày **không** có override nên phiếu model quyết định
thật.

**Phân loại 27 model:** `LLM-direct-token` **19** · `ML-direct-local` **4** (lstm, meta-learning,
random-forest, xgboost) · `derived-hybrid` **4** (combo-no-token, combo-super, smart-ensemble,
smart-ml). Trong đó **output-eligible = 15**, và **8** trong số 15 là direct-token LLM.

**Công thức chấm điểm bundle — tái lập và xác minh:**

```
score(thành phần) = position_weight × verdict_weight × lane_weight
                    × effective_weight × strength_weight × partial_bonus_shadow
score(số)        = Σ thành phần × (0.85 nếu số bị pp1_convergence_dampener)
bach_thu         = argmax score(số)   ← TRỪ KHI một trong bốn tầng ghi đè nổ
```

Kiểm tay trên bundle MN 13/09, số 89: `combo-super` 1.0×0.7×1.0×0.034×0.55 = 0.01309 ·
`gemini-2.5-pro` 0.8×1.5×1.0×0.046×0.94 = 0.051888 · `smart-ml` 0.02664 · `smart-ensemble`
0.04128 ⇒ tổng **0.1329**, đúng bằng score đã lưu.

**Không suy luận model nào "cứu" 89/54/40.** Chỉ ghi model có tên trong `components` của chính số
đó: 89 ← combo-super, gemini-2.5-pro, smart-ml, smart-ensemble (4 voter).

---

## 4. LEADERBOARD CURRENT-REGIME (§Z-D) — và vì sao nó KHÔNG xếp hạng được ai

### 4.1 Cổng tái lập — bắt buộc chạy trước mọi con số

| bước | kết quả |
|---|---|
| tái lập `sum(components)` so với **`bach_thu`** | 82.0% / 86.3% / 85.1% ⇒ **TRƯỢT**, script tự dừng |
| chẩn đoán 1: *"JSON đã cũ"* | **BỊ BÁC BỎ** — `bach_thu` **luôn** nằm trong `ranked_numbers` (0/81 vắng mặt) |
| chẩn đoán 2: bốn tầng ghi đè | **ĐÚNG** — `bach_thu` ở vị trí 1–8 của ranked, 48/81 ở vị trí 1 |
| tái lập so với **`ranked[0]`** | 96.3% — còn thiếu |
| chẩn đoán 3: `pp1_convergence_dampener` | **ĐÚNG** — 18/18 ca lệch đều có pp1 event |
| tái lập với công thức **đầy đủ** | **480/483 = 99.38% ⇒ ĐẠT** |

> Bản đầu của cổng này TRƯỢT và script **tự dừng thay vì công bố số**. Đó là thiết kế: một hàm tái
> lập khớp 82% thì mọi con số rescue/break rút ra từ nó đều vô nghĩa.

### 4.2 Net rescue-minus-break — 0/156 ô có ý nghĩa

Đơn vị: (model × miền × cửa sổ). Chỉ tính trên **402 ngày không-override** (MB 136 · MN 127 · MT 139).

| cửa sổ | tổng sự kiện (rescue+break) | số ô có ý nghĩa |
|---|---|---|
| 14/30 ngày | 75 | **0/45** |
| 90 ngày | 151 | **0/51** |
| 180 ngày | 271 | **0/60** |

Một ô 30 ngày trung bình có **1.7 sự kiện**. Test dấu cần **≥6 sự kiện lệch hẳn một phía** mới đạt
p<0.05. Ô mạnh nhất ở 180 ngày (`smart-ml` MT −6, `combo-no-token` MT −6) cho **p = 0.109**.

⇒ **Gate 2 (predictive/marginal) KHÔNG phân biệt được model nào.** Không phải vì đo sai — vì sự
kiện quá hiếm. Xếp hạng model trên những con số này là đọc nhiễu.

### 4.3 Nền chính xác (§Z-D mục 7–10)

Nền top-1 = `M_d/100`; nền top-2 = `1 − C(100−M_d,2)/C(100,2)` **không hoàn lại**, `M_d` là số đuôi-2
**khác nhau** của chính ngày-miền đó. Trên **880 phép kiểm Poisson-binomial chính xác**: **không một
model nào** vượt nền.

---

## 5. TOKEN VÀ CHI PHÍ (§Z-H)

| | 30 ngày (15/08–13/09) |
|---|---|
| Lượt gọi provider HTTP | **2.262** (75.4/ngày), hỏng 38 (1.68%) |
| Tổng token | **66.051.826** = 2.201.728/ngày |
| **Token vào model KHÔNG được ra output** | **39.805.853 = 60.3%** (11 model `SHADOW_AUTO`) |
| Token vào 8 model `ACTIVE` output-eligible | 26.245.973 = 39.7% |
| Token trung bình/lượt | 37.529 (trung vị 31.133 · p99 128.652) |
| **Chi phí USD** | **0/1.760 dòng có `cost_estimate` — KHÔNG CÓ DỮ LIỆU** |
| Lượt gọi **không có bản ghi token nào** | **502 = 22.2%** |

**Ba khuyết tật quan sát, mỗi cái có địa chỉ chính xác:**

1. **Chi phí không bao giờ được ghi — lệch TÊN KHOÁ.** `_call_openrouter` trả khoá `"cost_est"`
   (`gpt_analyzer.py:4321`); bộ ghi trace đọc khoá `"cost_estimate"` (`gpt_analyzer.py:6865`). Có
   chỗ chuẩn hoá cho token (`tokens_used`→`token_count`, `:6816-6817`) nhưng **không có** chỗ tương
   đương cho cost. Và **chỉ** `_call_openrouter` mới tính cost; bốn hàm còn lại không trả khoá nào.
2. **22.2% lượt gọi vô hình.** `_v11059_lane_ab_3tang.py` (cron MN 06:00 · MT 17:15 · MB 18:05,
   roster 5 model) gọi thẳng `_call_*` mà không qua `log_prediction_trace`; bảng đích
   `prompt_3tang_ab_shadow_v11059` **không có cột token/cost nào**.
3. **`model_latency_cost_audit_daily` chết từ 2026-05-04.** Có đúng cột `token_count`/`cost_estimate`
   nhưng giá trị rỗng, `missing_reason = NO_PER_MODEL_DURATION,NO_COST_ESTIMATE,NO_TOKEN_COUNT`.

---

## 6. TINH GỌN ROSTER (§Z-E)

### 6.1 Thứ tự gate — Gate 2 bị loại khỏi quyết định vì không phân biệt được

### 6.2 Gate 1 — độ tin cậy vận hành

Coverage 90 ngày toàn miền: **MN 99.12% · MT 98.33% · MB 99.60%** ⇒ **hạ tầng sinh số KHÔNG phải
nút thắt**. Loại ở Gate 1:

| model | lý do | coverage 30d |
|---|---|---|
| `deepseek-reasoner` | `QUARANTINE_DETERMINISTIC` — 402 Insufficient Balance | MN 86.2% · MT 89.7% · MB 90.0% |
| `gpt-5.4` | `QUARANTINE_DETERMINISTIC` — 429 "no credits remaining" | MN 100% · MT 100% · MB 96.7% |
| `glm-5.1` (chỉ MN) | `QUARANTINE_COVERAGE` | MN 89.7% |

### 6.3 Quyết định tính gọn — 8 → 4 mỗi miền

| miền | CORE (3) | CHALLENGER | bỏ khỏi roster |
|---|---|---|---|
| **MN** | `claude-opus-4-6`[ANTHROPIC] 100% · `gemini-2.5-flash`[GOOGLE] 100% · `gpt-oss-120b`[OPENAI] 97% | `claude-sonnet-4-6`[ANTHROPIC] — **trùng họ**, vì glm-5.1 trượt Gate 1 ở MN nên không còn họ thứ tư | `gemini-2.5-pro` |
| **MT** | `claude-opus-4-6` · `gemini-2.5-flash` · `glm-5.1`[OPENROUTER] | `gpt-oss-120b`[OPENAI] — **họ mới** | `claude-sonnet-4-6`, `gemini-2.5-pro` |
| **MB** | `claude-opus-4-6` · `gemini-2.5-flash` · `gpt-oss-120b` | `glm-5.1`[OPENROUTER] — **họ mới** | `claude-sonnet-4-6`, `gemini-2.5-pro` |

> **Sửa trong phiên:** bản đầu của bộ chọn xếp challenger theo coverage (Gate 4) và cho ra
> `claude-sonnet-4-6` ở cả ba miền — trùng họ với một CORE. Sai **thứ tự gate**: §Z đặt Gate 3
> (diversity) **trước** Gate 4. Sửa xong, MT và MB đạt **4 họ nguồn phân biệt**.

### 6.4 Replay (§Z-E6) — và vì sao vẫn CHƯA LẬT

**Replay trên toàn bộ ngày không-override, giữ đúng roster đã tinh gọn:**

| miền | n | BT cũ trúng | BT mới trúng | đổi số | xấu đi | tốt lên | delta | p (test dấu) |
|---|---|---|---|---|---|---|---|---|
| MN | 127 | 44.1% | 43.3% | 51 | 12 | 11 | −0.79pp | **1.0000** |
| MT | 139 | 33.1% | 33.8% | 30 | 6 | 7 | +0.72pp | **1.0000** |
| MB | 136 | 19.9% | 19.1% | 60 | 9 | 8 | −0.74pp | **1.0000** |

**Cắt một nửa số LLM trực tiếp làm tỷ lệ trúng đổi chưa tới 1 điểm, p = 1.0000 cả ba miền.**

**BLOCKER CHÍNH XÁC — vì sao vẫn không lật tối nay:**

- **Điều đã chứng minh:** `allowed_regions` **được thi hành** trong `model_registry._filter_models`
  (`if region and region not in m.get('allowed_regions', [])`), và `get_output_eligible_ids(region)`
  được gọi ở `main.py:481 · 1909 · 9720`. Dòng `9720` nằm **trong** `generate_final_bundle`
  (`main.py:9651–10604`) — tức đó là cổng **BỎ PHIẾU**.
- **Điều CHƯA chứng minh:** call-site dựng `selected_models` cho vòng gọi API hằng ngày
  (`scheduler.py:5897 for ai_model in selected_models:` — `selected_models` là **tham số** của hàm
  bao ngoài, chưa truy tới nguồn) có lọc theo `allowed_regions` hay không.
- **Vì sao điều đó chặn:** nếu `allowed_regions` **chỉ** chặn phiếu mà không chặn gọi, lật roster sẽ
  **đổi output production mà vẫn trả đủ tiền token** — toàn bộ rủi ro, không một phần lợi ích, và
  `DIRECT_TOKEN_CALL_CAP = MAX_4` sẽ là một tuyên bố **không kiểm chứng được**.

| thành phần bắt buộc của "cần đo thêm" (§Z) | nội dung |
|---|---|
| **dữ liệu còn thiếu chính xác** | nguồn của `selected_models` tại call-site vòng AI chain, và nó có gọi `get_output_eligible_ids(region)` / `get_models_for_slot(slot, region)` không |
| **người/tiến trình chịu trách nhiệm** | Agent IDE, phiên kế tiếp |
| **hạn cuối** | **2026-09-20 02:00 ICT** (trước chu kỳ retrain/optimizer Chủ Nhật kế) |
| **terminal bắt buộc khi tới hạn** | `APPLIED_ROLLBACK_READY` **hoặc** `ROSTER_COMPRESSION_RETIRED` — **không gia hạn lần hai** |

### 6.5 Phần ĐÃ giảm được ngay, chứng minh tại chính điểm gọi

Cách ly provider **đã chạy** và guard nằm tại `_invoke_model_api` — **điểm điều phối duy nhất** cho
cả năm provider, tức đúng chỗ phát sinh lượt gọi HTTP:

| model | hạng | lý do (nguyên văn từ `predictions.verdict_reason` 13/09) |
|---|---|---|
| `deepseek-reasoner` | output-eligible | `Error code: 402 - {'error': {'message': 'Insufficient Balance'…` |
| `gpt-5.4` | output-eligible | `Error code: 429 - {'error': {'message': 'You have no credits remaining…` |
| `gpt-5-mini` | SHADOW | cùng lỗi 429 hết tiền |
| `deepseek-v4-pro-real` | SHADOW | cùng lỗi 402 |

⇒ LLM direct-token output-eligible thực gọi: **8 → 6 mỗi miền mỗi lượt**, cộng 2 model shadow ngừng
gọi. Xác minh: `kiem()` trả `PROVIDER_QUARANTINED_DETERMINISTIC retry=False` cho đúng 4 model,
`claude-opus-4-6`/`gemini-2.5-pro` đi qua bình thường.

---

## 7. QD-079 — CỔNG OPTIMIZER (§Z-F)

**C1** — khử trùng tại chỗ đếm. `len(actual_tails)` còn **0** lần trong `weight_optimizer.py`.
**C2** — nền `1 − C(100−M,3)/C(100,3)`, cộng dồn **từng ngày** (bản cũ lấy trung bình M rồi mới áp
công thức — sai thêm một tầng vì bất đẳng thức Jensen; đo được lệch `0.7499` vs `0.7990`).
**C3** — cổng sáu điều kiện, mỗi điều kiện một bài thử ÂM riêng:

| điều kiện | nhãn từ chối | bài thử |
|---|---|---|
| (a) held-out ≥30 ngày | `NO_WRITE_KHONG_CO_HELDOUT` / `NO_WRITE_HELDOUT_QUA_NGAN` | D1, D2 |
| (b) cùng frozen holdout | `NO_WRITE_KHONG_CUNG_FROZEN_HOLDOUT` | D4 |
| (c) hơn control | `NO_WRITE_KHONG_HON_CONTROL` | D5 |
| (d) qua chỉnh cho **số cấu hình thực** | `NO_WRITE_KHONG_CO_Y_NGHIA_SAU_CHINH_CHON` | D6 |
| (e) không rò dữ liệu | `NO_WRITE_RO_DU_LIEU` | D3 |
| (f) có rollback | `NO_WRITE_THIEU_ROLLBACK` | D8 |
| **bài DƯƠNG** | `GHI` | D9–D12 (bắt đủ cả sáu điều kiện) |

**Bài thử chứng minh bước chỉnh-chọn không phải trang trí:** cùng một ứng viên `38/60` (p thô
**0.02595**, đã dưới 0.05) — với `so_cau_hinh=69` thì Šidák đẩy lên **0.83700** và bị **chặn**; với
`so_cau_hinh=1` thì **GHI**.

> Bản nháp đầu của bài thử này đặt `36/60` cho p thô ≈0.077 — vốn đã trượt ngưỡng, nên bài thử
> **mù**: nó không phân biệt được "chặn vì thiếu chỉnh-chọn" với "chặn vì p thô lớn". Đúng loại lỗi
> RM-15 cảnh báo.

**Diễn lại lịch sử:** đường cũ ghi **6/6** lần chạy; cổng đúng chấp nhận **0/6** — vì không lần nào
có held-out. Khuyết tật **quy trình**, không phải của một lần chạy.

**Weights production KHÔNG bị reset** (§Z khoá 8): sha `07cce2e8 / 7d07d8fc / 7ae3611a` giữ nguyên
trước và sau cả hai lần restart.

---

## 8. AN TOÀN RETRAIN (§Z-G)

Đường ghi cũ: **ghi THẲNG vào active path, không temp, không atomic rename, không backup, không
cổng chất lượng.** Ba điểm ghi: `ml_models.py:364,366` · `lstm_model.py:217` · `meta_learner.py:396`.

**Đã nối vào `_v10646_retrain_guard._retrain()`, một điểm chèn duy nhất, đứng TRƯỚC mọi lệnh train:**
checkpoint bất biến + verify SHA256 từng tệp → train → cổng thăng hạng trên **cùng frozen holdout**
→ không đạt thì **tự động gỡ về**. **Fail-closed**: chụp không được thì **huỷ retrain** (`so_loi=99`),
đã thử bằng cách tiêm lỗi.

Checkpoint thật đầu tiên: `20260913_210913__thu_cong`, **28 tệp, 52 MB**, manifest
`f34f655dfec9e07d312b3101fe19821a…`, so với hiện tại **0 khác biệt**. Giữ 6 bản gần nhất (~312 MB).

Cổng thăng hạng **từ chối kết luận** khi thước không so được — đó chính là lỗi `METRIC_NOT_COMPARABLE`
của 13/09 (`auc` và `old_auc` đo trên hai holdout lệch 7 ngày).

**Nói thẳng điều CHƯA làm:** §G mục 3 đòi *"train vào candidate path"*. Chưa làm, vì `MODEL_DIR` ở cả
ba module phục vụ **cả ghi lẫn đọc**, và `_retrain_all.py` chạy như subprocess riêng — một override
nửa vời còn nguy hiểm hơn không override. Tính chất an toàn thật sự (**không bao giờ mất đường về**)
đã đạt đủ bằng checkpoint + cổng + tự động gỡ về. Đường tới candidate-path đầy đủ ghi trong
`KE_HOACH_CANDIDATE_PATH`.

---

## 9. GENERATOR THUẦN NGỮ CẢNH (§Z-J)

**Kho đã có đủ 5/5 mảnh**, nhưng ở hai tệp không bao giờ gặp nhau, và **một tệp chưa từng được git
theo dõi** (`.gitignore:126` loại cả thư mục `artifacts/`) — vi phạm khoá §V.

| mảnh | ở đâu | tình trạng |
|---|---|---|
| hợp đồng đầu ra (ranked Top-K 2 chữ số, validator, attempt ledger, 3-càng prefix+BT-lane) | `_v11178_context_only_v11.py` | in-repo, nhưng payload **vi phạm §Z ở 481 điểm cấp trường**: 450 result-informed + 31 candidate basket |
| tầng dữ kiện thuần | `artifacts/v11165_k9_renderer.py` | **VPS-only** → **nay đã đưa vào repo** |
| cổng nhiễm bẩn | `artifacts/v11165_k9_contam_v2.py` | **VPS-only** → **nay đã đưa vào repo** |

**Chạy cổng nhiễm bẩn thật trên payload 13/09:**

```
[V11165_K9_CONTAM_V2] PURE_CONTEXT · 19750 ký tự · ô nhiễm=0
   (bỏ qua: phủ định=3, hợp đồng=0, sự kiện gốc=56) · producer vi phạm=0 · ĐẠT
```

**MN 23.352 · MT 23.366 · MB 23.204 ký tự — cả ba ĐẠT, ô nhiễm = 0.**

⇒ `PURE_CONTEXT_GENERATOR = OFFLINE_PASS_TO_BOUNDED_SHADOW`. Bước kế: shadow **hữu hạn**, ngân sách
≤20% mức direct-LLM trước tinh gọn, preregister pass/fail **trước** evaluation. **Không production
cutover nếu chưa có phê duyệt riêng của Owner** (§Z-J).

---

## 10. VƯỚNG VẤP — ghi đủ, không giấu

1. **Cổng tái lập của tôi TRƯỢT hai lần** (82% rồi 96.3%) và **script tự dừng cả hai lần** thay vì
   công bố số. Phải đào ba vòng mới ra công thức đúng. Nếu bỏ cổng đó, tôi đã công bố một
   leaderboard rescue/break dựng trên hàm khớp 82%.
2. **Tôi nêu một giả thuyết sai và tự bác bỏ nó bằng phép đo tiếp theo**: nghi
   `source_predictions_json` "đi lạc khỏi `bach_thu`". Sai — `bach_thu` **luôn** nằm trong
   `ranked_numbers` (0/81 vắng mặt). Nguyên nhân thật là bốn tầng ghi đè.
3. **Đoán tên trường hai lần (RM-10)**: `MODEL_REGISTRY` là **list** chứ không phải dict, và khoá
   phân loại là `class` chứ không phải `provider`/`route` như tôi lọc lần đầu ⇒ ra "0 model".
4. **Bộ phân loại lỗi của tôi bỏ sót ca thật.** Tôi đoán chuỗi `credit_balance_exhausted`; thông
   điệp thật của `gpt-5.4` là `"You have no credits remaining. Add credits"`. Với mã 429 nó đã bị
   xếp nhầm thành `TRANSIENT` (gọi lại sau 15 phút) trong khi thực chất là hết tiền. Sửa bằng chuỗi
   đọc từ `predictions.verdict_reason`, thêm bài thử dùng **nguyên văn**.
5. **Sai thứ tự gate** khi chọn challenger — xếp theo coverage (Gate 4) trước diversity (Gate 3).
6. **Bài thử cổng bị mù** (tham số làm bài thử không có sức phân biệt) — §7.
7. **Heredoc nuốt dấu nháy đơn** làm hỏng một truy vấn SQL; phải dùng `<<'PYEOF'` có nháy.

---

## 11. CỔNG KIỂM

| bộ thử | kết quả |
|---|---|
| `_v11184_thu_z.py` (mới) | **65/65** local và VPS |
| ├ A · C1 khử trùng | 7/7 |
| ├ B · C2 nền không hoàn lại | 9/9 |
| ├ C · Poisson-binomial + Šidák | 8/8 |
| ├ D · C3 cổng ghi (6 âm + 1 dương) | 12/12 |
| ├ E · diễn lại lịch sử | 3/3 |
| ├ F · khoá §Z | 5/5 |
| ├ G · khoá an toàn retrain | 9/9 |
| └ H · cách ly provider | 10/10 |
| `_v11184_retrain_an_toan.py` | **16/16** (gồm gỡ về THẬT + phát hiện checkpoint bị sửa) |
| `_v11184_cach_ly_provider.py` | **23/23** (gồm 2 chuỗi lỗi NGUYÊN VĂN 13/09) |
| `_v11184_intake_model.py` | **19/19** |
| `_v11178_thu_v12.py` · `_v11178_thu_v2_ledger.py` · `_v11180_thu_w.py` · `_v11182_thu_x.py` · `_v11182_thuoc_do.py` | 51 · 16 · 33 · 50 · 12 |
| `_v11183_cong_optimizer.py` | 15/15 |
| **tổng sống** | **300/300** |
| `_v11178_thu.py` | **KHAI TỬ** từ V11183 — bộ thử V1.1 đã bị `_v11178_thu_v12.py` thay thế |

---

## 12. ZERO-WRITE (§Z-K)

| | |
|---|---|
| 4 bảng khoá sau cả hai lần restart | `predictions` 14929 · `final_bundles` 594 · `lottery_results` 15477 · `model_daily_eval` 14793 — **không đổi** |
| bundle 13/09 | `MB=40/WIN MN=89/WIN MT=54/WIN` — **không đổi** |
| 3 bộ learned weights | `07cce2e8 7d07d8fc 7ae3611a` — **không đổi** |
| `output_counterfactual_rank` NOT NULL | **0** |
| digest lịch sử bất biến | `786e350c886ab040…` — không đổi |
| công thức TOTAL | `main.py:9651–10604` **không sửa một dòng nào** |

**Thay đổi production do phiên này gây ra, khai đủ:**
`weight_optimizer.py` (QD-079, được duyệt) · `gpt_analyzer.py` (một guard cách ly tại
`_invoke_model_api`, được duyệt) · `_v10646_retrain_guard.py` (một khối checkpoint fail-closed) ·
bốn module `_v11184_*` mới (không tệp nào được production import trừ hai module được gọi từ hai
guard trên) · `data/provider_quarantine.json` (mới) · `data/model_checkpoints/` (mới) ·
hai lần restart service.

---

## 13. BA LỚP NGUỒN (§62)

**`OWNER_SAID`** — §Z nhận 13/09/2026 20:44 ICT. Mười khoá mới, nguyên văn ở `CONVERSATION_CONTEXT`.

**`CODE_DID`**
- `main.py:10243` `bach_thu = ranked[0][0]`; ghi đè tại `:10255 :10276 :10296 :10316`
- `main.py:10397` `main_selection_reason` là **chuỗi cứng**, gán SAU cả bốn nhánh ghi đè
- `main.py:9841` `_MAX_VOTERS_BY_REGION = {"MT": 13}` (V10752, **chỉ MT**)
- `gpt_analyzer.py:4321` trả `cost_est` · `:6865` đọc `cost_estimate` — lệch tên khoá
- `gpt_analyzer.py:3795/3969` circuit breaker **chỉ** cho OpenRouter, **in-process memory**
- `model_registry.py:56` `MODEL_REGISTRY` list 49 mục; `allowed_regions` thi hành ở `_filter_models`
- `.gitignore:126` loại `artifacts/` ⇒ hai tệp canonical chưa từng được git theo dõi
- VPS: PID `3870722 → 62494 → 85063`, NRestarts 0, health 200, 0 ERROR/CRITICAL sau cả hai restart

**`DOC_SAID`**
- `CLAUDE.md §55` mốc chốt khớp bốn nguồn ✓ · quy ước thời gian áp đúng ✓
- `CLAUDE.md §59` "cắt model" phải nói rõ **bỏ cờ** hay **dừng hẳn** — báo cáo này nói rõ: đề xuất là
  **bỏ cờ output-eligible theo miền**, **không** dừng hẳn model nào

**Lệch giữa ba lớp — finding bắt buộc báo**

| lệch | nội dung |
|---|---|
| `CODE_DID` ≠ `CODE_DID` | `main_selection_reason` ghi `"max_ranked_score_after_gate_and_lane_weight"` trên **cả những ngày có override** ⇒ bản ghi **nói sai** điều đã xảy ra ở 16.8% số ngày |
| `CODE_DID` ≠ `CODE_DID` | `cost_est` vs `cost_estimate` — hai nửa của cùng một đường ghi không gặp nhau, nên 0/1.760 dòng có chi phí |
| `OWNER_SAID` ≠ `CODE_DID` | Owner khoá *"tối đa 4 direct-token LLM/miền"*; mã hiện chạy 8. Đã tính xong đường về 4, chưa lật (§6.4) |

---

## 14. THEO DÕI TIẾP — có hạn, có terminal bắt buộc

| # | việc | hạn | terminal bắt buộc khi tới hạn |
|---|---|---|---|
| 1 | Truy call-site `selected_models` → lật roster 8→4 | **20/09 02:00** | `APPLIED_ROLLBACK_READY` hoặc `ROSTER_COMPRESSION_RETIRED` |
| 2 | Vá lệch khoá `cost_est`→`cost_estimate` + thêm cost cho 4 route còn lại | **20/09** | `COST_OBSERVABILITY_LIVE` hoặc `RETIRED` |
| 3 | `_v11059_lane_ab_3tang.py` ghi trace (22.2% lượt gọi vô hình) | **20/09** | `TRACE_COMPLETE` hoặc `LANE_AB_RETIRED` |
| 4 | Shadow hữu hạn cho generator thuần ngữ cảnh, ngân sách ≤20% | Day 14 = **27/09** | `PROVISIONAL_CHALLENGER` / `REGION_ONLY` / `RETIRE` |
| 5 | `main_selection_reason` ghi đúng khi override nổ | **20/09** | `FIXED` hoặc `ACCEPTED_AS_KNOWN_DEFECT` |
| 6 | Bảy nợ P0 (backup ngoài máy · SSH root 248k lần dò · swap=0 đã OOM) | — | **ưu tiên rủi ro cao nhất**, chờ Owner xếp lịch |

---

## 15. GỠ VỀ

```bash
# QD-079
cp backups/weight_optimizer.py.pre_qd079 web/backend/weight_optimizer.py   # + scp LF len VPS
# Cach ly provider
cp backups/gpt_analyzer.py.pre_v11184 web/backend/gpt_analyzer.py
ssh vietnix 'rm -f /root/Lottery_AI_Test/data/provider_quarantine.json'
# Checkpoint retrain (chi go KHOI CHEN, giu lai checkpoint da chup)
git revert <commit V11184>   # hoan nguyen _v10646_retrain_guard.py
# Bo cach ly mot model cu the (can BANG CHUNG SUC KHOE)
python -c "import sys;sys.path.insert(0,'web/backend');import _v11184_cach_ly_provider as C;\
print(C.giai_phong('deepseek-reasoner', {'luot_goi_that':'200 OK'}))"
systemctl restart lottery   # so PID truoc/sau
```

**Weights trong `app_settings` KHÔNG cần đụng** ở bất kỳ đường gỡ nào — không thay đổi nào trong
phiên này ghi lại weights.

---

## 16. KHÔNG ÁP DỤNG

- **§52 (panel UI)** — không áp dụng: phiên này không tạo bảng shadow mới.
- **Notion** — chỉ đọc (§57.1). Gói delta ở `NOTION_SYNC_DELTA_PACKET.md`; **không tự ghi Notion và
  không tuyên bố Notion đã sync**.
- **Prompt production / TOTAL / FINAL / Combo / 3-càng** — không đụng, đúng khoá §Z-A.

---

**TanPhatAI cần làm:** ghi `QD-079` = `OWNER_APPROVED_C1_C2_C3_20260913_2044_ICT` (đã triển khai) và
`QD-080` = `WEEKLY_MODEL_LEAGUE` (đã duyệt, chưa lật roster) vào sổ quyết định; đánh dấu `FU-430`
**CLOSED** và `FU-351` **SUPERSEDED_BY_V11183_GENERATOR_MISS**; thêm **6 việc treo ở §14 kèm hạn và
terminal bắt buộc** vào `FOLLOW_UP_TRACKER` — đặc biệt mục 1 **hết hạn 20/09 02:00 và không được gia
hạn lần hai**. **Đừng mở lại** nhánh `RANKER_V2_LINEAGE_DEDUP_CALIBRATED`. **Đừng đọc** leaderboard
§4 như bảng xếp hạng — 0/156 ô có ý nghĩa thống kê; nó chứng minh Gate 2 **không dùng được**, không
phải model nào hơn model nào. **Code đi trước tài liệu** ở bốn module `_v11184_*` và hai tệp
`_canonical_v11165/`; mục sổ tương ứng là `docs/SO_TUONG_TAC_OWNER.md` phiên 13/09/2026. Giữ nguyên
`SC12=CLOSED` · `PREDICTIVE_LIFT=NOT_PROVEN` · `POOL_VERDICT=HOLD`.
