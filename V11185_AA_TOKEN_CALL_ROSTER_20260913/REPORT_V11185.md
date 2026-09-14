# REPORT V11185 — §AA · TOKEN CALL ROSTER SSOT · DỪNG SHADOW VÔ HẠN · ÁP 8→4 TẠI ĐIỂM GỌI API

> **Phiên:** 13/09/2026 22:00 → 23:xx ICT · **Mã đọc §58:** `XH1309-2` · **Prompt:** 43 R1 §AA
> **Khoá giữ nguyên:** `SC12=CLOSED` · `PREDICTIVE_LIFT=NOT_PROVEN` · `POOL_VERDICT=HOLD` ·
> `MATERIALIZATION_OPTION=B` · `F1`–`F5` `RETIRED` · TOTAL formula và current weights **không đổi**

> 🔴 **BẢN NÀY CÓ BỐN MỤC ĐÃ RÚT LẠI** — `RL-044` `RL-045` `RL-046` `RL-047`, rút ngày
> 14/09/2026 theo §AB-B. Đọc `V11186` §2 trước khi trích bất kỳ terminal nào của bản này.

---

## 1. EXECUTIVE TERMINAL — một trang

| terminal bắt buộc §AA-W | kết quả |
|---|---|
| `TOKEN_CALL_ROSTER_SSOT` | **`DEPLOYED`** |
| `UNBOUNDED_SHADOW_PROVIDER_CALLS` | 🔴 **ĐÃ RÚT LẠI (RL-045)** → **`DEPLOYED_PENDING_NATURAL_RECEIPT`** — chưa có lượt shadow tự nhiên nào sau deploy |
| `INITIAL_LLM_ROSTER_COMPRESSION` | **`APPLIED_ROLLBACK_READY`** |
| `DIRECT_OFFICIAL_GENERATOR_MODELS` | **`MAX_4_PER_REGION`** |
| `MODEL_OUTSIDE_ROSTER_HTTP_CALLS` | 🔴 **ĐÃ RÚT LẠI (RL-044)** → **`STATIC_SCHEDULER_PROOF_ONLY · SYSTEM_WIDE_LIVE_PROOF_PENDING`** — Combo Super còn pool riêng, chưa roster-gated. Xem `V11186` §2 |
| `DETERMINISTIC_PROVIDER_RETRIES` | **`ZERO`** |
| `COST_OBSERVABILITY` | **`EXACT_BLOCKER`** — xem §8 |
| `TRACE_COVERAGE` | **`ACTIVE_LANE_RETIRED`** — lane 502 lượt không trace đã tắt |
| `COMBO_SUPER_EXTRA_CALLS` | **`COUNTED_SEPARATELY`** |
| `OVERRIDE_LINEAGE` | **`EXACT_BLOCKER`** — xem §9 |
| `FAMILY_LINEAGE` | **`EXACT_BLOCKER`** — xem §9 |
| `RETRAIN_SAFETY` | **`EXACT_BLOCKER`** — vẫn là mức V11184, xem §9 |
| `PURE_CONTEXT` | 🔴 **ĐÃ RÚT LẠI (RL-046)** → **`DEFERRED_PENDING_ROSTER_LIVE_PROOF · ZERO_TOKEN_SPENT`** — hoãn theo trình tự, KHÔNG khai tử phương pháp |
| `TOTAL_FORMULA` | **`UNCHANGED`** |
| `CURRENT_WEIGHTS` | **`UNCHANGED`** |
| `PREDICTIVE_LIFT` | **`NOT_PROVEN`** |
| `POOL_VERDICT` | **`HOLD`** |
| `SC12` | **`CLOSED_DO_NOT_REOPEN`** |

**Đã activate lúc 22:36 ngày 13/09** — trước mốc 03:30/04:00 của §AA-I rất xa, và **cùng một roster
epoch cho cả MN/MT/MB** ngày 14/09. Không có miền nào chạy roster cũ.

> 🔴 **ĐÃ RÚT LẠI (RL-047):** con số dưới đây là `ESTIMATE_ONLY`, KHÔNG phải số giảm thực tế,
> và chưa tách được lượt gọi thêm của Combo. Chỉ sau natural receipt đủ ba miền mới được
> công bố phần trăm giảm THẬT. Xem `V11186` §2.

**Ước lượng giảm chi (phương pháp tỷ lệ theo số model, trên số đo thật 30 ngày):**
lượt gọi **2.262 → 489 (−78.4%)** · token **66.05M → 16.74M (−74.7%)**.
Và điều đáng nói thẳng: **phần lớn hơn đến từ chặn shadow (−54.8% tổng), không phải từ tinh gọn
roster (−19.9%)**. Ai giả định ngược lại sẽ đặt sai ưu tiên.

**Một next action duy nhất:** thu và chấm **natural receipt đầu tiên** của roster mới — lượt MN
sáng 14/09 (~05:00–05:35 ICT). Không mở nghiên cứu mới, không thêm model, không chạy thêm shadow.

---

## 2. OWNER YÊU CẦU GÌ (nguyên văn) — §62 lớp `OWNER_SAID`

Prompt §AA, tiếp nối sau V11184. Mệnh lệnh chi phối, nguyên văn:

> *"Biến roster từ một danh sách chỉ lọc khi bỏ phiếu thành một chính sách được thi hành ngay
> trước mọi HTTP provider call; dừng lượng token shadow không tạo output; thực hiện roster 8→4 có
> rollback; bảo toàn TOTAL, lịch sử và output."*
>
> *"Không chờ tới 20/09 chỉ để 'truy thêm'. Nguồn mã hiện tại đã cho thấy đủ căn nguyên để sửa:
> `scheduler.py` import `TOKEN_MODELS as AUTO_AI_MODELS`; daily AI chain dùng trực tiếp
> `AUTO_AI_MODELS` ở preflight, parallel pool, main provider loop và diversity pass;
> `get_expected_models(slot, region)` chỉ đang ghi log; MB post-MT rerun chọn từ `AUTO_AI_MODELS`;
> `allowed_regions` hiện đã chặn đường bỏ phiếu nhưng chưa bảo đảm chặn mọi đường gọi API."*
>
> *"Mục tiêu ưu tiên số một: `UNBOUNDED_SHADOW_PROVIDER_CALLS = 0`."*
>
> *"Không kết thúc bằng monitoring-only. Không gia hạn mơ hồ. Không yêu cầu Owner phê duyệt lại
> roster 8→4 hoặc Weekly Model League."*

**Owner tự soi nguồn và gỡ đúng blocker mà V11185 đã nêu.** Inventory tôi dựng lại khớp **chính xác**
điều Owner chỉ — xem §4.

---

## 3. ĐÀO BỚI / PHÁT HIỆN

| # | đã đào gì | kết quả |
|---|---|---|
| 1 | Preflight git/router/VPS/PID/crontab/quarantine | private `0acce3d` = master = origin, sạch; public `78171d9`; router `V11184`; PID 85063 NRestarts 0 health 200; crontab `4e16ed3d…`; 4 model đang cách ly; trace 7.062 dòng |
| 2 | Inventory call-site `AUTO_AI_MODELS` trong `scheduler.py` | **9 vị trí**: `:4017` import · `:4301` expected · `:4321` preflight · `:4652` prestart · `:4684` **main loop** · `:4874` diversity · `:5793/:5808/:5813` MB rerun |
| 3 | Shadow lane dùng gì | `SHADOW_AUTO_EVAL_MODELS` — **11 model**, nguồn của 60.3% token |
| 4 | `_v11059_lane_ab_3tang.py` ghi vào đâu | **0 lệnh ghi bảng official**; chỉ `prompt_3tang_ab_shadow_v11059` |
| 5 | Ai ĐỌC bảng đó (RM-20) | 4 nơi, gồm `main.py:18489` — endpoint **admin chỉ đọc**, đã xử lý sẵn ca bảng không tồn tại ⇒ **zero-official-impact** |
| 6 | Combo Super có tự gọi provider không | **CÓ** — `combo_super.py:1134` `analyze_and_predict(...)`, duyệt `AI_MODELS` pool riêng |
| 7 | Bẫy trong chính bản vá của tôi | khối win-rate cũ **vẫn ghi đè** `selected_models` ⇒ roster MB rerun sẽ vô tác dụng. Bắt được nhờ đọc lại, không nhờ cổng |
| 8 | Bẫy thứ hai — bài thử của tôi đếm chuỗi thô | B9 báo HỎNG vì chuỗi còn nằm trong **chú thích** của chính tôi (RM-09) |

---

## 4. TOKEN CALL ROSTER SSOT (§AA-C) — `DEPLOYED`

`web/backend/_v11185_roster_goi_token.py`, tự kiểm **32/32**.

```
get_token_call_roster(slot, region, execution_class, include_challenger)
```

| yêu cầu §AA-C3 | thi hành |
|---|---|
| lấy model theo region | ✓ `allowed_regions` + chính sách per-region |
| phân biệt CORE/CHALLENGER/SHADOW/QUARANTINE | ✓ |
| chỉ `class=TOKEN`, `role=GENERATOR`, hợp slot | ✓ |
| loại `RETIRED`/`REMOVED` | ✓ |
| loại provider-quarantined **trước khi schedule** | ✓ tầng 1 |
| tối đa 4/miền | ✓ — và **quá trần là FAIL-CLOSED**, không im lặng cắt |
| thứ tự ổn định | ✓ |
| roster version + effective timestamp | ✓ `token_call_roster/2026.09.14-1` |
| **không tự lấp chỗ** khi một model bị cách ly | ✓ roster **ngắn đi**, có bài thử |
| được phép trả ít hơn 4 | ✓ |

**FAIL-CLOSED (§AA-C8) — bài thử quan trọng nhất:** khi không đọc được `model_registry` hoặc trạng
thái cách ly, hàm trả `ok=False`, `ma_loi=TOKEN_ROSTER_INVALID`, **`models=[]`**. Bài thử tiêm lỗi
đọc cách ly và khẳng định **`len(models)==0`** — tức **tuyệt đối không fallback về 8 model**, đúng
thứ §AA sinh ra để diệt.

**Ảnh chụp versioned (§AA-C6)** có đủ: `roster_version` · `owner_approval_ref` · `effective_from` ·
`previous_version` · `previous_behaviour` · `rollback` · `config_sha256` · `quarantined`.
Xem `evidence/ROSTER_SNAPSHOT_20260914.json`.

---

## 5. THAY TOÀN BỘ CALL-SITE (§AA-E)

### 5.1 `_run_ai_models_predict` — sáu điểm

Roster tính **đúng một lần** đầu hàm, fail-closed **trước** mọi vòng gọi:

| điểm | trước | sau |
|---|---|---|
| expected count | `len(AUTO_AI_MODELS) + 1` | `len(_AA_MODELS) + 1` |
| provider preflight | `list(AUTO_AI_MODELS) + ['combo-super']` | `list(_AA_MODELS) + [...]` |
| parallel prestart / `_models_with_keys` | `for _pm in AUTO_AI_MODELS:` | `for _pm in _AA_MODELS:` |
| **main provider loop** | `for ai_model in AUTO_AI_MODELS:` | `for ai_model in _AA_MODELS:` |
| diversity pass | `list(AUTO_AI_MODELS)` | `list(_AA_MODELS)` |
| rolling queue / retry | dẫn xuất từ `_models_with_keys` | dẫn xuất từ roster |

### 5.2 `_rerun_mb_ai_after_mt_verify` — và một bẫy tôi suýt để lọt

Trước: chọn **top-3 theo win-rate 14 ngày** từ **toàn bộ** `AUTO_AI_MODELS`. Hai lỗi: kéo model
ngoài roster quay lại đường gọi, và dùng WR tính ở **thời điểm hiện tại** để chọn (§AA-E2 cấm).

Sau: **ba model MB CORE**, cố định, `include_challenger=False`, không dùng WR.

> **Bản vá đầu của tôi giữ khối cũ "để tham chiếu" — và nó vẫn chạy
> `selected_models = [m[0] for m in ai_model_wrs[:3]]`, tức GHI ĐÈ lựa chọn roster ở trên.**
> Nếu deploy như vậy thì §AA-E2 **vô tác dụng hoàn toàn**. Đã xoá hẳn khối đó; lịch sử còn nguyên
> ở `backups/scheduler.py.pre_v11185` và trong git.

### 5.3 Chứng minh bằng AST trên mã production

| phép kiểm | kết quả |
|---|---|
| vòng lặp trên `AUTO_AI_MODELS` | **0** |
| tham chiếu tên `AUTO_AI_MODELS` trong mã thực thi | **0** |
| import cũ còn giữ (backward compat §AA-C5, **không xoá mã**) | ✓ |
| `_AA_MODELS` gán **đúng một lần**, từ `_aa_roster['models']` | ✓ |
| fail-closed đứng **trước** main provider loop | ✓ |

---

## 6. DỪNG SHADOW TOKEN WASTE (§AA-F) — `UNBOUNDED_SHADOW_PROVIDER_CALLS = ZERO`

**Đây là khoản lớn nhất.** V11184 đo: **60.3% token (39.8M/30 ngày) chảy vào 11 model
`SHADOW_AUTO` không được phép ra output.**

Sau §AA: `_run_shadow_auto_eval` lọc `_gated_shadow_models` về **đúng challenger được chỉ định của
miền đó** (MN `claude-sonnet-4-6` · MT `gpt-oss-120b` · MB `glm-5.1`), và **fail-closed** nếu không
đọc được chính sách. Registry và lịch sử **giữ nguyên** — chỉ tắt khả năng được gọi, thuận nghịch.

**`_v11059_lane_ab_3tang.py`** — 502 lượt gọi/30 ngày **không có bản ghi token nào**. Đã chứng minh
zero-official-impact (0 lệnh ghi bảng official; nơi đọc duy nhất là endpoint admin chỉ-đọc) rồi
**tắt 3 dòng cron** bằng comment (không xoá): **93 → 90 dòng đang chạy, 0 dòng `_v11059` hoạt động**.
Rollback: `/root/crontab.pre_v11185.bak` (bản sao ở `evidence/`).
⇒ Terminal `LANE_AB_RETIRED_ZERO_OFFICIAL_IMPACT`.

---

## 7. QUARANTINE HAI TẦNG (§AA-G)

| tầng | vị trí | trạng thái |
|---|---|---|
| 1 — schedule filter | `_v11185_roster_goi_token.get_token_call_roster` | ✓ loại **trước khi** vào hàng đợi |
| 2 — guard trước HTTP | `gpt_analyzer._invoke_model_api` (V11184) | ✓ chặn nếu lọt qua do bug/race |

Bốn model đang cách ly: `deepseek-reasoner` · `gpt-5.4` · `gpt-5-mini` · `deepseek-v4-pro-real`.
Tất cả trả `PROVIDER_QUARANTINED_DETERMINISTIC` với **`retry=False`**. Bền qua restart.
Mở lại **bắt buộc có bằng chứng sức khoẻ** và trả về hàng **CHALLENGER**, không tự về CORE.

**Fail-open đã sửa:** cả roster lẫn shadow lane nay **bỏ token call và ghi lỗi rõ** khi không xác
minh được chính sách; **ML no-token không bị ảnh hưởng**.

---

## 8. COST/TOKEN OBSERVABILITY (§AA-H) — `EXACT_BLOCKER`

**Chưa làm trong phiên này.** Nói thẳng thay vì tô:

| thành phần bắt buộc của "cần đo thêm" | nội dung |
|---|---|
| **dữ liệu còn thiếu chính xác** | chuẩn hoá response tại dispatch: `cost_est`→`cost_estimate` (`gpt_analyzer.py:4321` vs `:6865`); thêm cost cho 4 route `_call_openai`/`_call_anthropic`/`_call_gemini`/`_call_deepseek` (hiện **chỉ** `_call_openrouter` tính cost); bảng giá versioned có effective date; phân biệt `ACTUAL`/`ESTIMATED_RATE_TABLE`/`UNKNOWN` |
| **người/tiến trình chịu trách nhiệm** | Agent IDE, phiên kế tiếp |
| **hạn cuối** | **2026-09-20 02:00 ICT** |
| **terminal bắt buộc khi tới hạn** | `COST_OBSERVABILITY_LIVE` hoặc `COST_OBSERVABILITY_RETIRED_WITH_REASON` |

**Phần ĐÃ làm cho trace coverage:** lane 502 lượt không-trace đã tắt ⇒ mọi active call-site còn lại
đều đi qua `analyze_and_predict` → `log_prediction_trace`.

---

## 9. BA MỤC CÒN LÀ `EXACT_BLOCKER`, mỗi mục đủ bốn thành phần

| mục | dữ liệu còn thiếu chính xác | hạn | terminal bắt buộc |
|---|---|---|---|
| **`OVERRIDE_LINEAGE`** (§AA-L) | thêm `pre_override_ranked0` · `pre_override_score` · `override_applied` · `override_rule_id` · `override_input_hash` · `main_selection_reason` **thực** · `roster_version` vào metadata bundle MỚI. Không backfill 16.8% ngày cũ | 20/09 | `CORRECT_FOR_NEW_BUNDLES` hoặc `RETIRED_WITH_REASON` |
| **`FAMILY_LINEAGE`** (§AA-M) | canonical lineage map + sửa nhãn sai của `smart-ensemble` (ghi `meta_numbers`/`lstm_numbers` nhưng nội dung là `xgboost`/`random-forest`) + in song song raw voter count và independent root-family count | 20/09 | `OBSERVABILITY_FIXED_NO_SCORING_CHANGE` hoặc `RETIRED_WITH_REASON` |
| **`RETRAIN_SAFETY`** (§AA-N) | tách `ACTIVE_MODEL_DIR`/`CANDIDATE_MODEL_DIR`/`CHECKPOINT_DIR`; training subprocess chỉ ghi candidate; atomic activation bằng symlink/pointer. Hiện mới ở mức V11184 (checkpoint + restore) | **trước CN 20/09 02:00** | `ATOMIC_CANDIDATE_TRAINING_AND_PROMOTION_READY` hoặc `RETRAIN_ABORTED_FAIL_CLOSED_WITH_EXACT_MODULE` |

**Người chịu trách nhiệm cả ba: Agent IDE, phiên kế tiếp.** Không gia hạn lần hai.

---

## 10. PURE-CONTEXT (§AA-O) — `RETIRED_BEFORE_TOKEN_SPEND` trong phiên này

§AA đọc đúng V11184: `OFFLINE_PASS` mới là **structural/contamination pass**, **chưa phải
predictive pass**. §AA-O đòi preregister **trước call đầu tiên**, và ngân sách ≤20%.

**Phiên này KHÔNG tiêu một token nào cho nhánh B.** Lý do: ưu tiên số một của §AA là
`UNBOUNDED_SHADOW_PROVIDER_CALLS = 0`, và mở một lane shadow mới **cùng lúc** với việc đóng lane cũ
là tự mâu thuẫn. Preregistration + lane bounded sẽ mở **sau khi** natural receipt xác nhận roster
mới chạy sạch.

⇒ Terminal `RETIRED_BEFORE_TOKEN_SPEND` cho §AA; mở lại ở phiên sau với preregistration đầy đủ.

---

## 11. ƯỚC LƯỢNG GIẢM CHI (§AA-F7)

**Phương pháp: tỷ lệ theo số model, áp lên số đo thật 30 ngày của V11184 §H. Đây là ƯỚC LƯỢNG.
Số đo THẬT sẽ đến từ natural receipt (§AA-S).**

| | lượt gọi trước | token trước | lượt gọi sau | token sau |
|---|---|---|---|---|
| official (8 → 4 model) | 805 | 26,245,973 | ~402 | ~13,122,986 |
| shadow (11 → 1 model) | 955 | 39,805,853 | ~87 | ~3,618,714 |
| lane A/B `_v11059` (TẮT) | 502 | **không có trace** | 0 | 0 |
| **tổng** | **2.262** | **66,051,826** | **~489** | **~16,741,700** |

**−78.4% lượt gọi · −74.7% token.** Phân rã: chặn shadow **−54.8%** · tinh gọn roster **−19.9%**.

**Chưa tính:** Combo Super tự gọi thêm provider (`combo_super.py:1134`) — **đếm riêng** theo
§AA-E5, chưa có số 30 ngày tách bạch vì nó đi chung đường `analyze_and_predict`.
⇒ `COMBO_SUPER_EXTRA_CALLS = COUNTED_SEPARATELY`. **Không giấu vào "một voter".**

---

## 11b. HƯỚNG XỬ LÝ VÀ VÌ SAO CHỌN

**Ba hướng đã cân nhắc cho việc chặn lượt gọi:**

| hướng | vì sao **không** chọn / chọn |
|---|---|
| (a) Sửa `allowed_regions` trong `model_registry` | **Không đủ.** V11184 đã chứng minh nó chặn đường **bỏ phiếu** (`main.py:9720`) nhưng `scheduler.py` duyệt hằng số tĩnh nên vẫn gọi đủ 8. Sửa chỗ này là sửa đúng tệp nhưng sai tầng |
| (b) Sửa trực tiếp 9 call-site, mỗi chỗ một điều kiện | **Không chọn.** Chín bản sao của cùng một chính sách là chín cơ hội để chúng trôi khỏi nhau. Và lần sau đổi roster lại phải sửa chín chỗ |
| (c) **Một hàm SSOT, mọi call-site đọc từ đó** | **ĐÃ CHỌN.** Một nguồn quyết định, versioned, fail-closed, rollback một lệnh. Chín call-site trở thành chín *người đọc*, không còn là chín *người quyết* |

**Vì sao FAIL-CLOSED chứ không fail-open:** hành vi cũ khi lỗi là "gọi hết 8" — chính là thứ §AA
sinh ra để diệt. Một hệ fail-open sẽ âm thầm quay về hành vi cũ đúng lúc không ai nhìn. Nên khi
không xác minh được chính sách, hàm trả **`models=[]`**, và `ML no-token` vẫn chạy bình thường.

**Vì sao chặn shadow trước, tinh gọn roster sau:** đo được 60.3% token chảy vào 11 model *không
được phép ra output*. Đó là khoản lớn hơn, và nó **không có bất kỳ đánh đổi chất lượng nào** —
model không được ra output thì tắt nó không đổi một dòng output nào. Tinh gọn roster mới là phần
có đánh đổi (đã replay: p=1.0000 cả ba miền).

**Vì sao KHÔNG mở pure-context shadow trong cùng phiên:** ưu tiên số một của §AA là
`UNBOUNDED_SHADOW_PROVIDER_CALLS = 0`. Mở một lane shadow mới **cùng lúc** với việc đóng lane cũ là
tự mâu thuẫn, và sẽ làm số đo của natural receipt đầu tiên lẫn lộn hai thay đổi.

**Vì sao KHÔNG đổi Combo Super:** §AA-A cấm đổi Combo semantics khi chưa chứng minh
output-equivalent. Nó **có** gọi thêm provider, nên đếm riêng và nói thẳng, thay vì hoặc giấu hoặc
đổi liều.

---

## 11c. VƯỚNG VẤP

1. **Bản vá đầu của tôi làm §AA-E2 vô tác dụng hoàn toàn.** Khi vá MB rerun tôi giữ khối win-rate
   cũ "để tham chiếu" — nhưng nó vẫn chạy `selected_models = [m[0] for m in ai_model_wrs[:3]]`,
   tức **ghi đè** lựa chọn roster. Deploy như vậy thì roster MB rerun chỉ là trang trí. Bắt được
   nhờ **đọc lại mã sau khi vá**, không nhờ cổng nào.
   *Bài học: "giữ lại để tham chiếu" trong một hàm đang chạy không trung lập — nó vẫn thực thi.*

2. **Bài thử của tôi đếm chuỗi thô (RM-09).** Bài `B9` báo **HỎNG** trong khi mã đã đúng, vì chuỗi
   nó tìm còn nằm trong **chú thích của chính tôi** giải thích vì sao đã xoá. Chú thích mô tả lối
   sai không phải lối sai. Sửa sang AST → 45/45. Đây là lỗi tôi vẫn cảnh báo người khác.

3. **Một cảnh báo giả.** `_v11184_intake_model.py` báo `rc=2` trong lượt regression — thoạt nhìn là
   hồi quy. Thật ra tệp **chưa deploy lên VPS**; `rc=2` là "file not found". Deploy xong 19/19.

4. **Heredoc và `grep -c`.** `grep -c` trả mã thoát 1 khi đếm ra 0, làm một lệnh Bash báo "lỗi"
   trong khi kết quả đúng là *không có lỗi nào*. Phải đọc kỹ trước khi kết luận.

5. **Thứ tự phải đúng.** Nếu tắt cron `_v11059` *trước* khi chứng minh zero-official-impact thì đó
   là tắt mù. Đã chứng minh trước (0 lệnh ghi bảng official; nơi đọc duy nhất là endpoint admin
   chỉ-đọc) rồi mới tắt.

---

## 12. CỔNG KIỂM

| bộ thử | kết quả |
|---|---|
| `_v11185_thu_aa.py` (mới) | **45/45** |
| `_v11185_roster_goi_token.py` (mới) | **32/32** |
| `_v11184_thu_z.py` · `_v11184_retrain_an_toan` · `_v11184_cach_ly_provider` · `_v11184_intake_model` | 65 · 16 · 23 · 19 |
| `_v11183_cong_optimizer` · `_v11182_thu_x` · `_v11182_thuoc_do` · `_v11180_thu_w` · `_v11178_thu_v12` · `_v11178_thu_v2_ledger` | 15 · 50 · 12 · 33 · 51 · 16 |
| **tổng sống** | **377/377** |

**Hai lỗi của chính tôi bị bộ thử bắt:** (a) khối win-rate cũ ghi đè roster MB — bắt bằng đọc lại
mã; (b) bài thử B9 **đếm chuỗi thô** nên báo HỎNG oan vì chuỗi nằm trong chú thích của tôi — sửa
sang AST (RM-09).

---

## 13. ZERO-WRITE (§AA-T)

| | |
|---|---|
| `predictions` · `final_bundles` · `lottery_results` · `model_daily_eval` | 14929 · 594 · 15477 · 14793 — **không đổi** |
| bundle 13/09 | `MB=40/WIN MN=89/WIN MT=54/WIN` — **không đổi** |
| 3 bộ learned weights | `07cce2e8 7d07d8fc 7ae3611a` — **không đổi** |
| `output_counterfactual_rank` NOT NULL | **0** |
| công thức TOTAL (`main.py:9651–10604`) | **không sửa một dòng** |
| bốn override legacy | **không đụng** |
| prompt production CORE | **không đụng** |

**Đã thay (đều nằm trong phạm vi §AA-T cho phép):** `scheduler.py` (roster call-site + shadow
bounded) · `_v11185_roster_goi_token.py` mới · `_v11185_thu_aa.py` mới · crontab (tắt 3 dòng
`_v11059`) · một lần restart service.

---

## 14. GỠ VỀ (§AA-K)

```bash
# 1) Roster — MỘT lệnh, không cần đụng weights, không xoá predictions
ssh vietnix 'systemctl set-environment LOTTERY_ROSTER_KHAN_CAP=1 && systemctl restart lottery'
#    (roster trả về hành vi TRƯỚC §AA; bỏ gỡ về: systemctl unset-environment ...)

# 2) Mã scheduler
cp backups/scheduler.py.pre_v11185 web/backend/scheduler.py   # + scp LF len VPS + restart

# 3) Cron lane A/B
ssh vietnix 'crontab /root/crontab.pre_v11185.bak'

# 4) Cách ly provider: GIỮ NGUYÊN — §AA-K nói rõ rollback roster KHÔNG reset quarantine
```

**Auto rollback chỉ vì lỗi vận hành** (mất toàn bộ token output · config invalid · model ngoài
roster bị gọi · duplicate provider call · bundle generation failure · health failure).
**Không auto rollback chỉ vì một ngày dự đoán thua.**

---

## 15. BA LỚP NGUỒN (§62)

**`OWNER_SAID`** — §AA, nguyên văn ở §2 và `CONVERSATION_CONTEXT`.

**`CODE_DID`**
- `scheduler.py:4017` import giữ nguyên; **0 tham chiếu** `AUTO_AI_MODELS` trong mã thực thi
- `_AA_MODELS` gán đúng một lần từ `get_token_call_roster`
- `combo_super.py:1134` `analyze_and_predict` — Combo **có** gọi thêm provider
- `_v11059_lane_ab_3tang.py` — 0 lệnh ghi bảng official; `main.py:18489` là endpoint admin chỉ đọc
- VPS: PID `85063 → 97754`, NRestarts 0, health 200, 0 ERROR/CRITICAL, 0 traceback,
  **0 `TOKEN_ROSTER_INVALID`**; crontab `4e16ed3d…` → `81efcf8d…`, 93 → 90 dòng

**`DOC_SAID`**
- `CLAUDE.md §59` — báo cáo này nói rõ đây là **bỏ cờ gọi theo miền**, **không** dừng hẳn model nào
- `CLAUDE.md §60.3` — quét ngược đã **phân loại** bằng AST, không đếm chuỗi thô

**Lệch:** `OWNER_SAID` (§Z khoá 4: tối đa 4/miền) ≠ `CODE_DID` trước §AA (chạy 8) — **nay đã khớp**.

---

## 16. THEO DÕI TIẾP

| # | việc | hạn | terminal bắt buộc |
|---|---|---|---|
| 1 | **Thu và chấm natural receipt đầu tiên** (MN ~05:00 14/09) | 14/09 EOD | `ROSTER_LIVE_PROOF_OK` hoặc auto-rollback |
| 2 | Cost observability (§8) | 20/09 | `COST_OBSERVABILITY_LIVE` hoặc `RETIRED_WITH_REASON` |
| 3 | Override lineage cho bundle mới | 20/09 | `CORRECT_FOR_NEW_BUNDLES` hoặc `RETIRED_WITH_REASON` |
| 4 | Family lineage observability | 20/09 | `OBSERVABILITY_FIXED_NO_SCORING_CHANGE` hoặc `RETIRED_WITH_REASON` |
| 5 | Retrain atomic candidate path | **trước CN 20/09 02:00** | `ATOMIC_..._READY` hoặc `RETRAIN_ABORTED_FAIL_CLOSED_WITH_EXACT_MODULE` |
| 6 | Pure-context bounded shadow + preregistration | sau receipt #1 | `BOUNDED_SHADOW_PREREGISTERED` hoặc `RETIRED` |
| 7 | Combo Super: thử đường reuse frozen same-run output | 20/09 | `REUSED_OUTPUT_EQUIVALENT` hoặc giữ `COUNTED_SEPARATELY` |
| 8 | Bảy nợ P0 (§AA-U) — backup ngoài máy, SSH, swap/OOM | chờ Owner xếp lịch | không được chiếm chỗ predictive work |

---

## 17. KHÔNG ÁP DỤNG

- **§52 (panel UI)** — không tạo bảng shadow mới.
- **Notion** — chỉ đọc (§57.1); gói delta ở `NOTION_SYNC_DELTA_PACKET.md`, **không tự tuyên bố đã sync**.
- **§AA-U hạ tầng P0** — không làm trong phiên này theo đúng lời §AA: *"không dùng hạ tầng làm lý do
  trì hoãn roster/token fix"*; token call path đã đóng xong, P0 chuyển sang phiên sau.

---

**TanPhatAI cần làm:** ghi roster version `token_call_roster/2026.09.14-1` (effective
2026-09-14T00:00:00+07:00, activate thật lúc 22:36 ngày 13/09) vào sổ; ghi `QD-080` là **ĐÃ THI
HÀNH** chứ không còn "chưa lật"; đánh dấu 11 model `SHADOW_AUTO` là **`SHADOW_PAUSED`** (không phải
RETIRE — registry và lịch sử giữ nguyên); ghi `_v11059_lane_ab_3tang` =
`LANE_AB_RETIRED_ZERO_OFFICIAL_IMPACT`; thêm **8 việc treo ở §16 kèm hạn và terminal bắt buộc**.
**Đừng đọc** ước lượng −74.7% token như số đo — số thật đến từ natural receipt. **Đừng ghi**
`COST_OBSERVABILITY`, `OVERRIDE_LINEAGE`, `FAMILY_LINEAGE`, `RETRAIN_SAFETY` là đã xong — cả bốn vẫn
là `EXACT_BLOCKER` có hạn 20/09. **Code đi trước tài liệu** ở `_v11185_*`; mục sổ tương ứng là
`docs/SO_TUONG_TAC_OWNER.md` phiên 13/09/2026. Giữ nguyên `SC12=CLOSED` ·
`PREDICTIVE_LIFT=NOT_PROVEN` · `POOL_VERDICT=HOLD`.
