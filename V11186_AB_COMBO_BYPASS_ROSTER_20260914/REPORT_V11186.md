# REPORT V11186 — §AB · ĐÓNG COMBO ROSTER BYPASS · UỶ QUYỀN TẠI DISPATCHER CUỐI · RECEIPT SỐNG MN

> **Phiên:** 14/09/2026, 12:49 → 13:xx ICT · **Mã đọc §58:** `SC1409` · **Prompt:** 43 R1 §AB
> **Khoá giữ nguyên:** `SC12=CLOSED` · `PREDICTIVE_LIFT=NOT_PROVEN` · `POOL_VERDICT=HOLD` ·
> `MATERIALIZATION_OPTION=B` · `F1`–`F5` `RETIRED` · TOTAL formula và current weights **không đổi**

---

## 1. EXECUTIVE TERMINAL

**Điều phải đọc trước mọi thứ khác: §AB giả định phiên bắt đầu ~00:15 ngày 14/09. Thực tế phiên
bắt đầu lúc 12:49.** Lượt MN sáng 14/09 **đã chạy xong** (05:00–05:17) dưới V11185. Deploy lúc này
sẽ làm **MN một version, MT/MB một version khác trong cùng một ngày** — điều §AB-J cấm tuyệt đối.

⇒ **Quyết định: giữ MỘT epoch V11185 trọn ngày 14/09. Mã §AB đã hoàn tất và STAGED, deploy sau
EOD, effective trước 04:00 ngày 15/09.** Đây đúng là nhánh §AB-V đã định sẵn cho trường hợp không
kịp 03:30.

| terminal §AB-T | kết quả |
|---|---|
| `COMBO_ROSTER_BYPASS` | **`CODE_COMPLETE_STAGED_NOT_DEPLOYED`** — đóng ở CẢ selection lẫn final HTTP dispatch trong mã; chưa deploy vì bảo vệ epoch |
| `ALL_ACTIVE_PROVIDER_CALL_SITES` | **`INVENTORIED`** (24 tệp quét, 7 call-site sống) **`_AND_ROSTER_GATED_IN_STAGED_CODE`** |
| `MODEL_OUTSIDE_ROSTER_HTTP_CALLS` | **`MN_ZERO_LIVE_PROVEN`** · **MT/MB PENDING** |
| `QUARANTINED_MODEL_HTTP_CALLS` | **`MN_ZERO_LIVE_PROVEN`** · MT/MB pending |
| `DETERMINISTIC_PROVIDER_RETRIES` | **`MN_ZERO_LIVE_PROVEN`** · MT/MB pending |
| `UNBOUNDED_SHADOW_PROVIDER_CALLS` | **`PENDING_NATURAL_RECEIPT`** — shadow chạy post-verify, chưa tới |
| `DIRECT_GENERATOR_ROSTER` | **`MN_MAX_4_LIVE_PROVEN`** · MT/MB pending |
| `COMBO_EXTRA_CALLS` | **`DIFFERENT_REQUESTS_COUNTED_SEPARATELY`** — 1 lượt thêm ở MN, **chưa quy được nguồn** |
| `TOKEN_REDUCTION` | **`NOT_YET_MEASURED`** — chỉ có MN, chưa đủ ba miền |
| `COST_OBSERVABILITY` | **`EXACT_BLOCKER`** — mã chuẩn hoá đã staged, chưa deploy |
| `OVERRIDE_LINEAGE` | **`EXACT_BLOCKER`** — không làm trong §AB theo §AB-U |
| `FAMILY_LINEAGE` | **`EXACT_BLOCKER`** — như trên |
| `RETRAIN_SAFETY` | **`EXACT_BLOCKER`** — như trên, hạn 19/09 23:00 |
| `PURE_CONTEXT` | **`DEFERRED_PENDING_ROSTER_LIVE_PROOF`** · **`ZERO_TOKEN_SPENT`** |
| `TOTAL_FORMULA` · `CURRENT_WEIGHTS` | **`UNCHANGED`** |
| `PREDICTIVE_LIFT` · `POOL_VERDICT` · `SC12` | `NOT_PROVEN` · `HOLD` · `CLOSED_DO_NOT_REOPEN` |

**Một next action duy nhất:** thu receipt MT rồi MB (bộ thu nền đã chạy sẵn trên VPS), rồi deploy
gói §AB sau EOD.

---

## 2. ĐÍNH CHÍNH V11185 (§AB-B) — bốn mục, rút tại CHÍNH CHỖ đã công bố

§AB đúng, và tôi chấp nhận. Cả bốn đã ghi vào `docs/SO_RUT_LAI.json` **và** sửa trực tiếp trong
báo cáo V11185 công khai kèm banner đầu bản (`PRJ-RETRACTION-001`).

### RL-044 — `MODEL_OUTSIDE_ROSTER_HTTP_CALLS = ZERO`

| phần | nội dung |
|---|---|
| **chỗ gốc** | `V11185 REPORT §1` + `NOTION_SYNC_DELTA_PACKET §A`, công bố 13/09 ~23:20 ICT |
| **nguyên văn câu sai** | *"`MODEL_OUTSIDE_ROSTER_HTTP_CALLS` \| **`ZERO`** (chứng minh tĩnh + guard hai tầng; số đo sống ở §AA-S)"* |
| **điều đúng** | `STATIC_SCHEDULER_PROOF_ONLY · SYSTEM_WIDE_LIVE_PROOF_PENDING`. V11185 chỉ đóng đường gọi trong `scheduler.py`. `combo_super.py` **vẫn** giữ pool `AI_MODELS` riêng 9 model, trong đó **bốn** ngoài roster hoặc bị cách ly, và Combo tự chấm WR rồi gọi `analyze_and_predict` (`combo_super.py:1134`) — một đường **hoàn toàn không qua roster**. Thêm nữa `_invoke_model_api` lúc đó **chỉ** có guard cách ly, **chưa** có guard uỷ quyền roster, nên model **khoẻ nhưng ngoài roster** vẫn ra được HTTP |
| **phép đo tái lập** | `evidence/ab_replay_combo.py`; và receipt MN 14/09 cho thấy trace **không ghi** `caller`/`execution_class` nên không quy được lượt gọi thêm |
| **quyết định đã dựa trên số sai** | **Không có quyết định production nào.** Nhưng câu sai **đã vào báo cáo công khai và gói Notion**, nên người đọc sau có thể tưởng toàn hệ thống đã được chứng minh — đó chính là tác hại |

### RL-045 — `UNBOUNDED_SHADOW_PROVIDER_CALLS = ZERO`
Đúng: `DEPLOYED_PENDING_NATURAL_RECEIPT`. Deploy 22:36 ngày 13/09, báo cáo viết ~23:20 **cùng
ngày** — chưa có một lượt shadow tự nhiên nào. Viết `ZERO` là nâng từ `DEPLOYED` lên `LIVE_PROVEN`,
đúng lỗi RM-12 cấm.

### RL-046 — `PURE_CONTEXT = RETIRED_BEFORE_TOKEN_SPEND`
Đúng: `DEFERRED_PENDING_ROSTER_LIVE_PROOF · ZERO_TOKEN_SPENT`. `RETIRED` nghĩa là **khai tử về
phương pháp**. Thực tế pure-context **đã đạt** cổng nhiễm bẩn offline cả ba miền; không chạy chỉ là
quyết định **trình tự**. Ghi `RETIRED` có thể khiến phiên sau bỏ hẳn một nhánh còn nguyên giá trị.

### RL-047 — `−74,7% token`
Đúng: `ESTIMATE_ONLY`. Suy ra bằng tỷ lệ theo số model, **chưa tách lượt gọi thêm của Combo**.
V11185 **có** dán nhãn "ước lượng" ở thân báo cáo, nhưng đặt nó trong bảng EXECUTIVE TERMINAL ngang
hàng các terminal đã chứng minh làm người đọc lướt hiểu thành số đo.

---

## 2b. OWNER YÊU CẦU GÌ (nguyên văn) — §62 lớp `OWNER_SAID`

Prompt §AB, mức thực thi *"CỰC GẮT · CỰC MẠNH · KHÔNG TÔ XANH · KHÔNG ĐOÁN · KHÔNG GIA HẠN MƠ HỒ"*.
Owner **tự soi nguồn** và chỉ đúng sáu điểm V11185 chưa đóng:

> *"V11185 đã đóng scheduler chính nhưng chưa chứng minh toàn hệ thống vì:
> 1. `combo_super.py` còn pool `AI_MODELS` riêng.
> 2. Combo tự chọn Top-N và gọi `analyze_and_predict`.
> 3. Pool Combo còn model ngoài roster từng miền.
> 4. `gpt_analyzer._invoke_model_api` hiện có quarantine guard nhưng chưa có roster authorization
>    bắt buộc cho model khỏe nhưng ngoài roster.
> 5. Ước lượng giảm 74,7% chưa tách đầy đủ Combo calls.
> 6. Natural receipt chưa xảy ra.
>
> Do đó, trước khi có §AB: `MODEL_OUTSIDE_ROSTER_HTTP_CALLS=ZERO` chỉ là PREDEPLOY/STATIC CLAIM,
> chưa phải runtime fact toàn hệ thống."*

Mệnh lệnh chi phối phiên, nguyên văn:

> *"Biến roster từ một danh sách chỉ lọc khi bỏ phiếu thành một chính sách được thi hành ngay
> trước mọi HTTP provider call."*
>
> *"Không được để tài liệu dẫn người sau đọc sai."* (§AB-B — đính chính **trước khi làm tiếp**)
>
> *"Không được coi việc 'đếm Combo riêng' là đủ. Đếm riêng không thay thế việc tuân thủ roster."*
>
> *"Không được gọi provider tay để tạo bằng chứng."* (§AB-K)
>
> *"Nếu thiếu `target_region` hoặc `execution_class`: fail closed; không suy đoán mặc định;
> không gọi HTTP."* (§AB-E3)
>
> *"Nếu không đạt trước 03:30: không deploy patch nửa vời; không thay code giữa MN/MT/MB; giữ
> V11185 cho toàn ngày 14/09... Cấm: MN một version, MT/MB version khác."* (§AB-J)

Và §AB-U cấm kết thúc kiểu cũ, trong đó có: *"«AST sạch nên live sạch»"* · *"«ước lượng token
giảm» viết thành số thật"* · *"«MN pass» viết thành ba miền pass"* · *"thiếu data viết thành
zero"* · *"static proof viết thành runtime proof"* · *"pure-context chưa chạy viết thành retired"*.

**Không có yêu cầu rời nào giữa phiên.**

**Điều Owner yêu cầu mà phiên CỐ Ý không làm, kèm lý do:** deploy (§AB-J cấm phá epoch — xem §1);
override lineage · family lineage · retrain atomic (§AB-U: *"Nếu P0 chưa đóng: không mở việc
nghiên cứu khác"*); pure-context (§AB-Q: chỉ activate **sau** `ROSTER_SYSTEM_WIDE_LIVE_PROOF_OK`).

---

## 3. ĐÀO BỚI / PHÁT HIỆN

| # | đã đào gì | kết quả |
|---|---|---|
| 1 | Preflight §AB-C1 | private `e2e0357`=master=origin sạch; public `a86bcd5`; router `V11185`; PID 97754 NRestarts 0 health 200; crontab `81efcf8d…` 90 dòng; trace 7.067 dòng; 4 model cách ly |
| 2 | **Thời điểm thật** | **12:49 ngày 14/09**, không phải ~00:15 như §AB giả định ⇒ MN đã chạy, deploy hôm nay là vi phạm §AB-J |
| 3 | Inventory provider call-site toàn repo | 24 tệp có gọi provider; **0 tệp** trong số đó được cron gọi trực tiếp; **7 call-site sống** của `analyze_and_predict` |
| 4 | Pool `AI_MODELS` của Combo | **9 model**, trong đó **4 ngoài roster/cách ly**: `gemini-2.5-pro`, `deepseek-reasoner`, `gemini-3.5-flash`, `gemini-3.6-flash` |
| 5 | Fallback nguy hiểm | `combo_super.py:1115` `else AI_MODELS` — không có danh sách đã lọc thì chạy **toàn bộ 9 model** |
| 6 | Lịch sử 30 ngày: model ngoài roster có mặt trong bundle | MN `gemini-2.5-pro` **29/30 ngày** · MT 28 · MB 27 · `deepseek-reasoner` MB 27/MT 26/MN 24 · `glm-5.1`@MN 24 · `claude-sonnet-4-6`@MT 23/@MB 17 |
| 7 | **§AA đã đóng được tới đâu trên thực tế** | 13/09 (trước): MB có 2 LLM ngoài roster, MN có 1. **14/09 (sau): MN có 0** |
| 8 | Receipt MN 14/09 | 5 lượt HTTP, đúng 4 model roster, **0 ngoài roster, 0 cách ly**; `claude-opus-4-6` **2 lượt** |
| 9 | `main._make_prediction` là gì | Đường dự đoán **LIVE** (7 nơi gọi, gồm MT sau MN và MB sau MN+MT) ⇒ lớp `official`, **không** phải route bảo trì |
| 10 | Cost trong trace 14/09 | **0/5 dòng có `cost_estimate`** — xác nhận lại khuyết tật lệch tên khoá |

---

## 4. RECEIPT SỐNG MN — `MN_ROSTER_LIVE_PROOF_OK` (10/10)

Thu bằng `_v11186_receipt_roster.py`, **chỉ đọc**, không gọi provider, append vào
`artifacts/v11178/ROSTER_RECEIPTS.jsonl`.

| phép §AB-K | kết quả |
|---|---|
| model chạm HTTP | `claude-opus-4-6`×2 · `claude-sonnet-4-6` · `gemini-2.5-flash` · `gpt-oss-120b` |
| **outside-roster HTTP** | **0** ✓ |
| **quarantined HTTP** | **0** ✓ |
| model duy nhất ≤ 4 | 4 ✓ |
| dòng sau cutoff | 0 ✓ |
| bundle sinh được | `bach_thu=24` ✓ |
| `TOKEN_ROSTER_INVALID` · ERROR/CRITICAL · traceback | 0 · 0 · 0 ✓ |
| health | 200 ✓ |
| token | 151.015 |
| **thiếu cost** | **5/5** ✗ (blocker đã biết) |

**Điểm mở duy nhất — và tôi KHÔNG đoán:** `claude-opus-4-6` gọi **2 lượt**. `prediction_trace.jsonl`
**không ghi** `caller`, `execution_class`, `request_fingerprint`, nên **không quy được** lượt thêm
cho scheduler hay Combo. Receipt ghi đúng nhãn `LUOT_THEM_CHUA_QUY_DUOC_NGUON`. Chính §AB-G/E sinh
ra để lấp chỗ này — sau khi deploy, mọi lượt sẽ mang `caller` + `execution_class` + fingerprint.

> **Bộ thu của tôi ban đầu báo FAIL OAN 3 phép**: `grep -c` trả mã thoát 1 khi đếm ra 0 nên
> `... || echo 0` làm **cả hai** cùng chạy, cho ra chuỗi hai dòng. Sửa bằng `; true` + ép `int`,
> và **−1 nghĩa là KHÔNG ĐỌC ĐƯỢC** (khác hẳn 0) để không bao giờ biến "thiếu dữ liệu" thành "sạch".

**MT và MB chưa chạy.** Bộ thu nền đã khởi động trên VPS (PID 140302), tự đợi bundle từng miền rồi
thu receipt, ghi vào `artifacts/v11178/receipt_watch.log`.

---

## 4b. ĐÃ LÀM GÌ — danh mục thay đổi (§57.3 mục 5)

**Không có một byte nào lên VPS trong phiên này**, trừ 5 tệp backup gỡ về (phần 9 dưới đây) —
thứ chỉ thêm vào, không đụng tiến trình đang chạy. PID 97754 · NRestarts 0 · health 200 giữ nguyên
từ đầu tới cuối phiên.

| # | thay đổi | tệp | trạng thái |
|---|---|---|---|
| 1 | Combo giao pool với roster **trước khi chấm điểm** (thuật toán top-N giữ nguyên) | `web/backend/combo_super.py:1270` | `STAGED` |
| 2 | Đóng fallback `else AI_MODELS` — trước đây không có danh sách lọc thì chạy **cả 9 model** | `web/backend/combo_super.py:1115` | `STAGED` |
| 3 | `uy_quyen_goi()` — 7 kết quả §AB-E2, fail-closed khi thiếu `target_region`/`execution_class` | `web/backend/_v11185_roster_goi_token.py` | `STAGED` |
| 4 | Cắm guard uỷ quyền **trước** cả guard cách ly và mọi `_call_*` | `web/backend/gpt_analyzer.py::_invoke_model_api` | `STAGED` |
| 5 | Truyền `execution_class` + `caller` từ **cả 7 call-site sống** (xác minh AST) | `scheduler.py` · `combo_super.py` · `main.py` | `STAGED` |
| 6 | Request fingerprint 11 trường + reuse chỉ khi **giống hệt** | `gpt_analyzer.py` | `STAGED` |
| 7 | Chuẩn hoá cost: đọc **cả** `cost_est` (`:4321`) và `cost_estimate` (`:6865`), phân biệt `ACTUAL_PROVIDER`/`UNKNOWN`, **không** biến UNKNOWN thành 0 | `gpt_analyzer.py` | `STAGED` |
| 8 | **CẤP 2 gỡ về có expiry 24 h + ALERT stderr** (V11186b) — trước đó bật là giữ mãi | `_v11185_roster_goi_token.py` | `STAGED` |
| 9 | **CẤP 1 gỡ về: lập 5 tệp `.pre_v11186` trên VPS**, sha256 khớp bản đang chạy cả 5 (V11186b) | `/root/Lottery_AI_Test/backups/` | **`ĐÃ LÀM TRÊN VPS`** (additive, không restart) |
| 10 | Bộ thu receipt **chỉ đọc**, ghi `ROSTER_RECEIPTS.jsonl` | `web/backend/_v11186_receipt_roster.py` | `ĐÃ DEPLOY` (đã có từ đầu phiên) |
| 11 | Hai tệp trạng thái runtime vào `.gitignore` (`provider_quarantine.json`, `roster_khan_cap.json`) | `.gitignore` | `ĐÃ LÀM` |
| 12 | Đính chính bốn terminal V11185 tại **chính chỗ đã công bố** + `SO_RUT_LAI.json` | repo công khai | `ĐÃ LÀM` |
| 13 | Bộ thử mới: `_v11186_thu_ab.py` **102/102** · `_v11186_thu_khan_cap.py` **45/45** | `web/backend/` | `ĐÃ LÀM` |

**Commit:** `0a8d7f6` (V11186a) · `2d20f74` (bốn mặt quản trị, `governance_seq → 501`) ·
`0ea1439` (V11186b). Cả ba **đều là `STAGED`** về mặt runtime.

---

## 5. ĐÓNG COMBO BYPASS (§AB-D) — mã hoàn tất, staged

| điểm | trước | sau |
|---|---|---|
| `combo_super.py:1270` dựng ứng viên | `all_ai_ids = [m['id'] for m in AI_MODELS]` (9 model) | **giao với roster TRƯỚC khi chấm điểm** |
| `combo_super.py:1115` fallback | `filtered_ai_models if ... else AI_MODELS` | **không có danh sách đã lọc ⇒ KHÔNG gọi AI nào** |
| nhãn khi pool rỗng | `"Unified pool không chọn AI model nào"` | `COMBO_AI_PHASE_SKIPPED_NO_AUTHORIZED_MODEL` |

**Thuật toán chọn top-N và scoring của Combo GIỮ NGUYÊN** (§AB-D4) — nó chỉ không còn *nhìn thấy*
model không được phép. Roster gate đặt **trước** `all_sorted = sorted(...)`, có bài thử vị trí.

**Pool sau gate, theo miền:**

| miền | được phép (từ 9) | bị loại |
|---|---|---|
| MN | `claude-sonnet-4-6` `gemini-2.5-flash` `claude-opus-4-6` `gpt-oss-120b` | `gemini-2.5-pro` `deepseek-reasoner` `glm-5.1` `gemini-3.5-flash` `gemini-3.6-flash` |
| MT | `gemini-2.5-flash` `claude-opus-4-6` `glm-5.1` `gpt-oss-120b` | `claude-sonnet-4-6` `gemini-2.5-pro` `deepseek-reasoner` `gemini-3.5-flash` `gemini-3.6-flash` |
| MB | `gemini-2.5-flash` `claude-opus-4-6` `glm-5.1` `gpt-oss-120b` | như MT |

---

## 6. UỶ QUYỀN TẠI DISPATCHER CUỐI (§AB-E) — mã hoàn tất, staged

`uy_quyen_goi(model, target_region, execution_class, slot, caller, request_fingerprint)` trong
module SSOT. Bảy kết quả đúng §AB-E2.

Guard đặt trong `gpt_analyzer._invoke_model_api`, **trước cả guard cách ly và mọi `_call_*`**.

| yêu cầu §AB-E | thi hành |
|---|---|
| thiếu `target_region` ⇒ fail-closed, không suy đoán | ✓ `DENY_INVALID_CONTEXT` |
| thiếu `execution_class` ⇒ fail-closed | ✓ |
| caller không được tự bịa `execution_class` | ✓ chỉ 5 giá trị hợp lệ; sai chính tả (`OFFICIAL`, `official `) cũng bị DENY |
| ngoại lệ bảo trì có env gate + expiry, mặc định TẮT | ✓ hết hạn cũng TẮT, có bài thử |
| ImportError / lỗi bất kỳ ⇒ từ chối gọi | ✓ |
| không đọc được policy ⇒ token=0, ML vẫn chạy | ✓ |

**Ngữ cảnh truyền từ entry point canonical (§AB-E5)** — cả 7 call-site sống, xác minh bằng AST:

| call-site | `execution_class` |
|---|---|
| `scheduler` parallel prestart · rolling queue · **main loop** · MB rerun | `official` |
| `scheduler` shadow auto-eval | `shadow` |
| `combo_super._run_ai_models` | `combo_super` |
| `main._make_prediction` | `official` (đã xác minh bằng AST là đường LIVE, 7 nơi gọi) |

---

## 7. REQUEST FINGERPRINT + REUSE (§AB-G) — mã hoàn tất, staged

Fingerprint gồm **đủ 11 trường** §AB-G1: model · region · date · execution_class · prediction_mode ·
statistical_depth · hash(source_data) · hash(rules) · hash(learned_intelligence) ·
hash(system_prompt) · hash(user_prompt).

- Fingerprint **giống hệt** ⇒ reuse frozen same-run result, **HTTP mới = 0**, ghi
  `REUSED_IDENTICAL_REQUEST`, giữ lineage tới attempt gốc.
- **Đổi bất kỳ một trường nào** ⇒ fingerprint khác ⇒ **không reuse** (11 bài thử, mỗi trường một bài).
- Không tính được fingerprint ⇒ **không reuse** (an toàn), vẫn gọi bình thường.
- Bài thử riêng cho điều §AB-G5 cấm: **cùng model+date+region nhưng khác prompt ⇒ fingerprint khác**.

---

## 8. COST OBSERVABILITY (§AB-M) — mã hoàn tất, staged

Chuẩn hoá tại điểm dispatch duy nhất: đọc **cả hai** khoá `cost_est` (`gpt_analyzer.py:4321`) và
`cost_estimate` (`:6865`) — tương thích ngược. Phân biệt `ACTUAL_PROVIDER` / `UNKNOWN`.
**Không bao giờ biến UNKNOWN thành 0** — có bài thử AST khẳng định không còn `cost_estimate = 0` ở
bất kỳ đâu. Response nay mang thêm `roster_version` · `execution_class` · `caller` ·
`request_fingerprint`.

⇒ Terminal vẫn là `EXACT_BLOCKER` **cho tới khi deploy**, vì §AB-T cấm dùng chữ `LIVE` khi chưa có
bằng chứng đúng tầng.

---

## 9. CỔNG KIỂM

| bộ thử | kết quả |
|---|---|
| `_v11186_thu_ab.py` (mới) | **102/102** trên mã đã vá |
| ├ A uỷ quyền dispatcher (24 ca DENY + 5 ALLOW + ngữ cảnh thiếu + bịa lớp + maintenance) | ✓ |
| ├ B Combo gate + **fixture ép model ngoài roster lên #1 WR** | ✓ |
| ├ C guard đã nối + AST mọi call-site truyền `execution_class` | ✓ |
| ├ D dispatcher giả: 30 tổ hợp model-xấu × lớp đều bị chặn, **0 lệnh `_call_*`** | ✓ |
| ├ E fail-closed, không fallback 8 model | ✓ |
| ├ F fingerprint (11 trường, mỗi trường một bài) | ✓ |
| └ G cost (không biến UNKNOWN thành 0) | ✓ |
| `_v11186_thu_khan_cap.py` (mới, V11186b) | **45/45** — cửa gỡ về CẤP 2 có expiry + alert |
| 377 bộ thử V11185 | **đo lại trên trạng thái cách ly SỐNG**: §AA 44/44 · §Z 65/65 · roster tự-kiểm 32/32 · cách ly 23/23 · retrain 16/16 · intake 19/19 |

> `_v11186_thu_ab.py` **chưa chạy được trên VPS** vì VPS còn V11185 — đó chính là **bằng chứng
> patch chưa deploy**, đúng ý đồ. Sau deploy sẽ chạy và phải đạt 102/102 trước khi restart.

---

## 10. ZERO-WRITE (§AB-T)

| | |
|---|---|
| `predictions` · `final_bundles` · `lottery_results` · `model_daily_eval` | **không đổi** bởi phiên này |
| 3 bộ learned weights | `07cce2e8 7d07d8fc 7ae3611a` — **không đổi** |
| công thức TOTAL · bốn override · prompt CORE · 3-càng | **không đụng** |
| `output_counterfactual_rank` NOT NULL | **0** |
| **VPS** | **KHÔNG deploy gì trong phiên này** — vẫn V11185, PID 97754, NRestarts 0 |

**Đã thay (đều trong phạm vi §AB-T cho phép):** `combo_super.py` · `gpt_analyzer.py` ·
`scheduler.py` · `main.py` · `_v11185_roster_goi_token.py` (thêm `uy_quyen_goi`) ·
hai module `_v11186_*` mới — **tất cả chỉ trong repo, chưa lên VPS**.
Trên VPS chỉ thêm: `_v11186_receipt_roster.py` (chỉ đọc) và một script thu receipt nền.

---

## 11. HƯỚNG XỬ LÝ VÀ VÌ SAO CHỌN

**Vì sao KHÔNG deploy hôm nay dù mã đã xong:** §AB-J cấm "MN một version, MT/MB version khác".
MN đã chạy 05:00. Deploy lúc 13:xx sẽ tạo đúng tình trạng đó. §AB-V đã định sẵn nhánh này: giữ một
epoch, thu receipt, deploy sau EOD. **Mã xong sớm không phải lý do để phá epoch.**

**Vì sao giao pool ở `:1270` chứ không lọc ở `:1364`:** lọc ở `:1364` là sau khi đã chấm điểm và
chọn top-3 — model ngoài roster vẫn tham gia cuộc đua và có thể đẩy model hợp lệ ra. Giao ở `:1270`
làm thuật toán chọn **giữ nguyên** mà chỉ thấy tập hợp lệ.

**Vì sao guard tầng 2 vẫn cần dù tầng 1 đã chặn:** tầng 1 có thể sập vì bug, race giữa lúc đổi
roster và lúc hàng đợi đã xếp, một script import danh sách cũ, hay một đường gọi chưa ai kiểm kê.
Tầng 2 ở ngay trước `_call_*` là chỗ cuối cùng còn chặn được.

**Vì sao KHÔNG làm override lineage / family lineage / retrain trong §AB:** §AB-U nói rõ *"Nếu P0
chưa đóng: không mở việc nghiên cứu khác... xử lý đúng Combo + final dispatch cho tới khi có
terminal."* P0 chưa deploy ⇒ chưa đóng ⇒ ba mục kia giữ `EXACT_BLOCKER` có hạn.

---

## 12. VƯỚNG VẤP

1. **Prompt giả định sai thời điểm.** §AB viết cho ~00:15; phiên chạy 12:49. Nếu tôi làm theo chữ
   ("deploy trước 04:00") mà không kiểm đồng hồ, tôi đã phá epoch ngày 14/09. **Luôn chạy `date`
   trước khi tin mốc giờ trong prompt.**
2. **Bộ thu receipt của tôi báo FAIL oan 3 phép** — `grep -c` trả mã thoát 1 khi đếm 0. Sửa, và
   thêm `−1 = không đọc được` để không biến thiếu dữ liệu thành sạch.
3. **Script sửa của tôi hỏng vì `\n` trong chú thích tiếng Việt** bị diễn giải trong heredoc. Tệp
   không bị ghi (ast.parse chặn trước). Làm lại không dùng escape.
4. **Tôi viết `"_ct_uq" in dir()`** để lấy `roster_version` — mong manh và khó đọc. Sửa thành biến
   khai trước.
5. **Lệnh kiểm của tôi in "?"** cho `cost_source` và `request_fingerprint` — nhưng đó là **kỳ vọng
   tôi đoán trong lệnh kiểm**, không phải yêu cầu. 2 lần mỗi cái là đúng.
6. **Đường gỡ về tôi tự công bố ở §15 KHÔNG chạy được** (phát hiện V11186b, cùng ngày). §15 bảo
   `cp backups/<tệp>.pre_v11186 …` trong khi **`/root/Lottery_AI_Test/backups/` không tồn tại trên
   VPS** — 0 tệp. Tôi viết một runbook gỡ về mà **chưa bao giờ kiểm nó thực thi được**; đó đúng là
   RM-15 (*"cổng không qua thử coi như KHÔNG TỒN TẠI"*) áp vào chính đường thoát hiểm. Đã lập 5 tệp
   `.pre_v11186`, đối chiếu sha256 từng tệp với bản **đang chạy**: khớp cả 5.
7. **Tôi suýt đọc nhầm một sai lệch môi trường thành hồi quy.** Sau khi vá `_v11185_roster_goi_token.py`,
   `_v11185_thu_aa` ra **38/40** và tự-kiểm roster ra **30/32**. Nguyên nhân **không** phải bản vá:
   máy local **không hề có** `data/provider_quarantine.json` (0 model cách ly) trong khi VPS có 4 —
   hai bài đó đo đúng thứ phụ thuộc trạng thái runtime. Đồng bộ bản sống về ⇒ **44/44** và **32/32**
   (RM-13). Bài học: đo lại trên nguồn sống **trước** khi gọi một con số là hồi quy.
8. **Phép đếm CR của tôi đếm chữ cái `r`, không đếm ký tự CR.** `grep -c` với mẫu CR viết
   bằng escape shell không được diễn giải, nên nó đếm mọi dòng có chữ `r` — báo
   `combo_super.py CR=2804` trong khi tệp thật có **CR=0**. Đếm lại bằng `b.count()` trên byte
   trong Python. Cùng họ RM-09 với mục 2, và lần này nó suýt làm tôi "sửa" một vấn đề không tồn tại.
9. **Chính dòng mục 8 ở trên từng bị hỏng khi tôi viết nó.** Escape CR trong heredoc bị diễn giải
   thành **ký tự CR thật**, cắt cụt dòng trong báo cáo công khai. Tôi đã có ghi nhớ đúng về bẫy này
   và vẫn vấp. Viết lại bằng script ra tệp thay vì heredoc.
10. **Bản đầu của báo cáo này qua cổng §57.3 nhờ một TAI NẠN.** Cổng nhận diện 9 phần bằng **tiêu
   đề**, nhưng nó đọc cả dòng bắt đầu bằng `#` **nằm trong khối code**. Phần *"đã làm gì"* của bản
   đầu được khớp bởi dòng chú thích bash `# Sau khi deploy (15/09), gỡ về CẤP 1…` — không phải bởi
   một mục thật nào. Viết lại §15 làm dòng đó biến mất và cổng **lập tức báo thiếu**. Báo cáo khi ấy
   **thật sự thiếu** mục 5 của khung; nay đã có §4b. Ghi lại vì đây là **cổng báo xanh cho một thứ
   không tồn tại** — đúng họ RM-15, và lần này nạn nhân là chính bộ kiểm.

---

## 13. BA LỚP NGUỒN (§62)

**`OWNER_SAID`** — §AB, nguyên văn ở `CONVERSATION_CONTEXT`. Điểm quan trọng nhất: Owner **tự soi
nguồn** và chỉ đúng chỗ V11185 báo quá.

**`CODE_DID`**
- `combo_super.py:74` `AI_MODELS` 9 model · `:1115` fallback · `:1134` `analyze_and_predict` · `:1270` ứng viên
- `gpt_analyzer.py:4321` `cost_est` vs `:6865` `cost_estimate`
- `main.py` `_make_prediction` (7308–8918), 7 nơi gọi ⇒ đường LIVE
- VPS 14/09: MN 12 dòng predictions, 4 direct-token LLM, trace 5 lượt, 151.015 token, 0 cost
- Bundle 14/09 MN: **0 LLM ngoài roster** (13/09 MN có 1, MB có 2)

**`DOC_SAID`**
- `CLAUDE.md §55` quy ước thời gian — áp đúng
- `CLAUDE.md §60.3` quét ngược phải **phân loại** — đã dùng AST ở mọi phép kiểm

**Lệch:** `OWNER_SAID` (§AB: mọi provider call phải tuân roster) ≠ `CODE_DID` **đang chạy** (Combo
vẫn có pool riêng) — **mã sửa đã xong và staged**, sẽ khớp sau deploy EOD.

---

## 14. THEO DÕI TIẾP

| # | việc | hạn | terminal bắt buộc |
|---|---|---|---|
| 1 | Thu receipt MT rồi MB (bộ thu nền đang chạy) | 14/09 EOD | `MT/MB_ROSTER_LIVE_PROOF_OK/FAIL` |
| 2 | **Deploy gói §AB** + chạy 102/102 trên VPS + restart | trước 04:00 **15/09** | `DEPLOYED_PENDING_NATURAL_PROOF` |
| 3 | Receipt ba miền ngày 15/09 | 15/09 EOD | `ROSTER_SYSTEM_WIDE_LIVE_PROOF_OK` hoặc `AUTO_ROLLBACK_WITH_EXACT_REASON` |
| 4 | Công bố token/cost **THẬT** (sau khi có ba miền) | 15/09 EOD | `TOKEN_REDUCTION = ACTUAL_MEASURED` |
| 5 | Override lineage (additive, bundle mới) | 20/09 | `CORRECT_FOR_NEW_BUNDLES` hoặc `STAGED_NOT_DEPLOYED_WITH_REASON` |
| 6 | Family lineage observability | 20/09 | `OBSERVABILITY_FIXED_NO_SCORING_CHANGE` |
| 7 | Retrain atomic candidate path | **19/09 23:00** | `ATOMIC_..._READY` hoặc `RETRAIN_ABORTED_FAIL_CLOSED_WITH_EXACT_MODULE` |
| 8 | Pure-context preregistration + activate | sau `ROSTER_SYSTEM_WIDE_LIVE_PROOF_OK` | `BOUNDED_SHADOW_PREREGISTERED` |
| 9 | Auto-rollback hai cấp (§AB-L) | ~~cùng lúc deploy~~ | **`ĐÃ LÀM` (V11186b)** — CẤP 1 backup thật trên VPS (5 tệp, sha khớp); CẤP 2 có expiry 24 h + alert stderr, **45/45** bài thử |
| 10 | **Cổng `_v10921_report_gate` đọc dòng `#` trong khối code như tiêu đề** ⇒ có thể báo đủ 9 phần cho báo cáo thật sự thiếu | chưa đặt hạn — **không mở FU mới** theo khoá §AB | `GATE_HEADING_FALSE_POSITIVE_GHI_NHAN` |

---

## 15. GỠ VỀ

> **Sửa tại chính chỗ đã công bố (V11186b, 14/09).** Bản đầu của mục này bảo
> `cp backups/<tệp>.pre_v11186 …` trong khi **thư mục `backups/` không tồn tại trên VPS**. Thủ tục
> đó **không thực thi được**. Dưới đây là bản đã lập và đã đối chiếu sha.

**Hiện trạng (14/09):** mã §AB **chưa deploy** — gỡ về chỉ là bỏ commit:
```bash
git revert 0a8d7f6 0ea1439      # V11186a + V11186b, đều STAGED
```

**Sau khi deploy (15/09) — CẤP 1, mặc định, GIỮ trần 4:**
```bash
ssh root@14.225.224.89 'cd /root/Lottery_AI_Test
for f in combo_super.py gpt_analyzer.py scheduler.py main.py _v11185_roster_goi_token.py; do
  cp -p backups/$f.pre_v11186 web/backend/$f
done
systemctl restart lottery'
# -> về V11185: roster 4 GIỮ · shadow bounded GIỮ · cách ly GIỮ · KHÔNG biến nào phải đặt
```

| tệp `.pre_v11186` trên VPS | sha256 (16) | đối chiếu bản đang chạy |
|---|---|---|
| `combo_super.py` | `47047b1dc0b7e0b9` | **khớp** |
| `gpt_analyzer.py` | `20f3bb5305ad13d2` | **khớp** |
| `scheduler.py` | `732e302a57e299fb` | **khớp** |
| `main.py` | `d59a6ae94f9c3666` | **khớp** |
| `_v11185_roster_goi_token.py` | `294ec64572e5cd9d` | **khớp** |

**CẤP 2 DISASTER — CHỈ khi roster 4 không ra output VÀ ML-only cũng hỏng:**
```bash
ssh root@14.225.224.89 'systemctl set-environment LOTTERY_ROSTER_KHAN_CAP=1 && systemctl restart lottery'
# -> hành vi TRƯỚC §AA (toàn bộ TOKEN_MODELS, 8 model)
```

Cấp 2 **có hạn và có alert** (§AB-L, làm ở V11186b):

| | |
|---|---|
| hạn mặc định | **24 giờ**, đo từ **lần bật đầu tiên** (`data/roster_khan_cap.json`) ⇒ restart **không** làm đồng hồ chạy lại |
| đổi hạn | `LOTTERY_ROSTER_KHAN_CAP_GIO=<số giờ>` hoặc `LOTTERY_ROSTER_KHAN_CAP_HET_HAN=<ISO>` |
| viết sai hai biến trên | **TỪ CHỐI mở cửa** — §AB-E3, không suy đoán mặc định |
| hết hạn | **tự động quay về roster bình thường (trần 4)**, *không* fail-closed — cửa này sinh ra để cứu lúc roster 4 không ra output, chặn sạch còn tệ hơn |
| cờ còn bật sau khi hết hạn | chạy roster bình thường **nhưng** để lại `canh_bao_khan_cap` + **ALERT stderr** — im lặng ở đây mới là nguy hiểm |
| alert | `[ROSTER_KHAN_CAP] …` ra stderr (journal), một lần mỗi tiến trình |
| tắt gỡ về | `systemctl unset-environment LOTTERY_ROSTER_KHAN_CAP && systemctl restart lottery` |

```bash
python web/backend/_v11185_roster_goi_token.py --go-ve   # in đủ hai cấp + trạng thái hiện tại
python web/backend/_v11186_thu_khan_cap.py               # 45/45 — RM-15
```

**Sau receipt MN pass, roster 4 là `provisional last-known-good`.** Sau full EOD pass ba miền, nó
trở thành **canonical last-known-good** và rollback mặc định **không được vượt trần 4** (§AB-L).

---

## 16. KHÔNG ÁP DỤNG

- **§52 (panel UI)** — không tạo bảng shadow mới.
- **Notion** — chỉ đọc (§57.1); gói delta ở `NOTION_SYNC_DELTA_PACKET.md`, **không tự tuyên bố đã sync**.
- **§AB-H replay Combo output-equivalent** — không áp dụng phần "loại model ngoài roster phải
  output-equivalent", vì §AB-H3 nói rõ thay candidate eligibility là **hệ quả được phép** của roster
  policy đã được Owner duyệt. Phần bắt buộc output-equivalent 100% là **exact-fingerprint reuse**,
  và nó đã có 11 bài thử.

---

**TanPhatAI cần làm:** ghi **bốn mục rút lại `RL-044`–`RL-047`** vào sổ và **đừng sync** các terminal
đã gạch của V11185; ghi rõ mã §AB là **`STAGED_NOT_DEPLOYED`**, VPS vẫn chạy V11185; ghi receipt
**`MN_ROSTER_LIVE_PROOF_OK`** nhưng **KHÔNG** được suy thành ba miền; **đừng ghi**
`TOKEN_REDUCTION` bằng bất kỳ con số nào — nó là `NOT_YET_MEASURED`; thêm **9 việc treo ở §14** kèm
hạn và terminal. **Code đi trước tài liệu** ở `_v11186_*` và bốn tệp đã vá; mục sổ tương ứng là
`docs/SO_TUONG_TAC_OWNER.md` phiên 14/09/2026. Giữ nguyên `SC12=CLOSED` ·
`PREDICTIVE_LIFT=NOT_PROVEN` · `POOL_VERDICT=HOLD`.
