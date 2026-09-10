# V11178 — CONTEXT_ONLY_CHALLENGER V1.1 · LIVE RANKED OUTPUT

> `SOURCE_TIMESTAMP` **2026-09-11 01:18 → 02:25 ICT** · `AUTHORITY` Prompt 43 R1 **§U**
> `PLAN` `PLAN-20260723-lottery-doc-restructure` · **Không mở Prompt 44 / FU / Plan mới**
> `PRODUCTION_MUTATIONS` **0 tệp official** · `DEPLOY/RESTART` **0**
> `DB MUTATIONS` **shadow-only**: 27 dòng `v11178_challenger_runs` + 114 dòng `shadow_candidates`
> **0 ghi `final_bundles` · 0 ghi `predictions` · 0 ghi `output_counterfactual_rank`**

---

## 1 · TÓM TẮT — 12 CÂU TRẢ LỜI (§U14)

| # | câu hỏi | trả lời |
|---|---|---|
| **1** | H1–H7 đúng/sai thế nào | **H1 ✅CONFIRMED · H2 ✅CONFIRMED · H3 ✅CONFIRMED · H4 ❌REFUTED · H5 ✅CONFIRMED · H6 🟡PARTIAL · H7 ✅CONFIRMED** |
| **2** | Claim "ready" của V11177 có bị hạ không | **CÓ.** → `CONTEXT_ONLY_STRUCTURAL_PROTOTYPE · LIVE_PREDICTIVE_OUTPUT_NOT_PROVEN`, đính chính **append-only**, `RL-035` |
| **3** | Payload V1.1 có observed values thật chưa | **CÓ. 486 live facts** với `observed_raw_value` · `observed_tail` · `available_at` · `source_row_id`. V11177 có **0** |
| **4** | Bao nhiêu model LM/LLM trong roster | **8**, đọc từ `model_registry` (V11177 hardcode 4) |
| **5** | Mỗi miền bao nhiêu valid/abstain/error/timeout | MN **6 ABSTAIN · 1 RANKED · 1 ERROR** · MT **6 ABSTAIN · 2 ERROR** · MB **6 ABSTAIN · 2 ERROR** — **24/24 có receipt, 0 im lặng** |
| **6** | Có diagnostic Top-K thật không | **CÓ. 99 dòng** `diagnostic_ranked_topk` + **15 dòng** `deterministic_ranked_topk` |
| **7** | Output seal lúc nào so với cutoff | **Tất cả `completed_before_cutoff = 1`**; chạy ~01:55–02:15 vs cutoff MN 15:40 · MT 16:55 · MB 17:55 |
| **8** | Chạy lại có duplicate không | **KHÔNG.** Thử hai lần: `runs 1→1`, `rows 10→10`, fingerprint **giống hệt**, exit 0, không sập |
| **9** | Official tables có đổi không | **KHÔNG.** `final_bundles=585` · `predictions=14686` · `day_governance=584` · `ocr NOT NULL=0` |
| **10** | V11176 row-ID mismatch đã giải quyết chưa | **RỒI.** SQL: **860 / 862 / 864**. Evidence JSON **ĐÚNG**, báo cáo **chép sai** → `RL-036` |
| **11** | 11/09 challenger và official ra gì | Challenger **đã có output**; **official chưa sinh bundle 11/09** lúc 02:25 ⇒ so sánh ba nhánh **chưa đủ** |
| **12** | Terminal status | **B · `ACTION_ABSTAIN_WITH_DIAGNOSTIC_RANKING`** |

---

## 2 · OWNER YÊU CẦU GÌ — NGUYÊN VĂN + GIỜ

| giờ ICT | NGUYÊN VĂN | loại | agent đã làm gì | trạng thái |
|---|---|---|---|---|
| **11/09 ~01:18** | *«[CONTINUATION · §U] [REPAIR REAL CONTEXT-ONLY CHALLENGER · LIVE RANKED OUTPUT · STOP EMPTY-ABSTAIN LOOP]» · «Tiếp tục tổng lực mạnh tay hơn nữa, đừng chần chừ»* | `YÊU_CẦU` | §U0→§U14 | `ĐÃ_LÀM` |

---

## 3 · ĐÀO BỚI / PHÁT HIỆN

### 3.1 · BẢY NGHI VẤN — kết luận kèm bằng chứng

| # | kết luận | bằng chứng |
|---|---|---|
| **H1** | 🔴 **CONFIRMED** | `conditions[0]` của payload V11177 **không có** `source_date` / `observed_raw_value` / `observed_tail` / `available_at` / `source_row_id` |
| **H2** | 🔴 **CONFIRMED** | **không trường nào** tên `*tail*`/`*value*`/`*observ*`/`*number*` ⇒ **không thể ánh xạ sang 00–99** |
| **H3** | 🔴 **CONFIRMED** | `shadow_candidates` có **đúng 1 dòng** V11177: `2026-09-11 \| MB \| deepseek-chat \| abstain` |
| **H4** | 🟢 **REFUTED** | cron **CÓ** `--models deepseek-chat,gemini-2.5-flash --regions MN,MT,MB`. Nhưng **thiếu lock/timeout/deadline** — đã bổ sung ở V1.1 |
| **H5** | 🔴 **CONFIRMED** | MN **3 đài** (An Giang, Bình Thuận, Tây Ninh) · MT **3 đài** (Bình Định, Quảng Bình, Quảng Trị) — `station_set="ALL"` xoá identity |
| **H6** | 🟡 **PARTIAL** | UNIQUE **chặn được trùng** (1→1) nhưng `INSERT` thuần ⇒ `IntegrityError` **không bắt** ⇒ script **sập**, miền sau không chạy |
| **H7** | 🔴 **CONFIRMED** | `grep holdout\|train_start\|validation` → **0 dòng**; cửa sổ 28/56/84/140 **lồng nhau**; nhiều đếm trong cùng ngày đích **không độc lập** |

### 3.2 · SAI LẦM CHÍ MẠNG CỦA V11177 — và vì sao cách diễn giải cũ CÓ LỢI CHO AGENT

V11177 kết luận: *«model correctly abstains vì không đủ bằng chứng»*.

Sự thật: **model không thể làm gì khác**. Payload nói *«ô `MT.Đà Nẵng.Giải sáu[1]` lag=1 có
stability 0,45 trên 40 mẫu»* nhưng **không bao giờ nói SỐ NÀO đã ra ở ô đó**. Ngay cả một điều
kiện `z=10` cũng không giúp model gọi tên một đuôi.

⇒ `abstain` là **hệ quả của payload thiếu cấu trúc**, không phải **lựa chọn dựa trên bằng chứng**.
Cách diễn giải cũ biến một **khiếm khuyết thiết kế** thành một **«kết luận trung thực»** — nó
**có lợi cho chính agent**. `RL-035`.

---

## 4 · HƯỚNG XỬ LÝ VÀ VÌ SAO CHỌN

**Ba lớp tách bạch (§U2)** — thứ V11177 thiếu là **LỚP B**:

| lớp | nội dung | V11177 | V1.1 |
|---|---|---|---|
| **A · CONDITION CATALOG** | cấu trúc + bằng chứng lịch sử, `train_start/end`, `holdout` | có (thiếu holdout) | **có, discovery/holdout tách** |
| **B · LIVE FACTS** | `observed_raw_value` · `observed_tail` · `available_at` · `source_row_id` | **KHÔNG CÓ** | **486 fact** |
| **C · CANDIDATE DERIVATION** | `condition × live_fact × transform → derived_tail` | **KHÔNG CÓ** | **có, ánh xạ 00–99** |

**Transform đóng băng trước khi đọc holdout (§U8):** `T1_identity` · `T2_reverse` ·
`T3_complement` · `T4_plus1`, khoá lúc `2026-09-11T01:45:00+07:00`. **Cấm thêm transform vì đã
biết kết quả một ngày cụ thể.**

**Thống kê sửa (§U8):** discovery `2026-01-14 → 2026-07-12` · holdout `2026-07-13 → 2026-09-10`
— **không chồng lấn**; BH-FDR **chỉ ở discovery**; holdout **không** dùng để chọn điều kiện.

**Vì sao terminal là B chứ không A:** mọi tiền đề kỹ thuật của A **đều đạt** (24/24 receipt ·
diagnostic Top-K · trước cutoff · zero official write · idempotent · scorer đọc được). Nhưng
**18/19 quyết định hợp lệ là `ABSTAIN`** — nên nhãn trung thực là **B**, và B **không được tô
thành predictive lift**.

---

## 5 · ĐÃ LÀM GÌ

| § | việc | kết quả |
|---|---|---|
| U1 | hạ trạng thái V11177 | append-only vào `REPORT_V11177.md` + `CONVERSATION_CONTEXT` · `RL-035` |
| U2–U3 | payload V1.1 | **486 live facts** · **6–17 candidate/miền** · đài đích thật · fingerprint ổn định |
| U4 | output contract | `decision_output` + `diagnostic_ranked_topk` tách riêng · abstain **vẫn có Top-K** nhãn `NON_ACTIONABLE_LOW_EVIDENCE` |
| U5 | roster | **8 LLM** từ `model_registry` · **24/24 receipt** · 0 im lặng |
| U6 | lịch theo lane | 3 cron: `BASE_D1` **13:30** · `MT delta` **16:38** (timeout 780s) · `MB delta` **17:33** (1100s) · wrapper có **flock + timeout + log + exit code** · chốt `LATE_REJECTED` |
| U7 | storage | bảng phụ `v11178_challenger_runs` (UNIQUE `date,region,stage,model_id,method_version`) + `INSERT OR IGNORE` |
| U8 | thống kê | discovery/holdout tách · transform đóng băng · FDR chỉ ở discovery |
| U9 | ranker tất định | **15 dòng** `deterministic_ranked_topk`, không gọi model |
| U10 | test | **35/35 ĐẠT** gồm metamorphic |
| U13 | nợ | row ID **860/862/864** (`RL-036`) · `evaluate_all_history` xác minh **đúng exit 2** |

### 5.1 · MA TRẬN MODEL × MIỀN (§U14)

```
              ABSTAIN  RANKED  ERROR   tổng
    MN            6       1      1       8
    MT            6       0      2       8
    MB            6       0      2       8
    ─────────────────────────────────────────
    tổng         18       1      5      24     ← 8 model × 3 miền, KHÔNG thiếu ai
```

**Mã lỗi thật, không im lặng:** `gemini-2.5-pro` → `429 RESOURCE_EXHAUSTED` ×3 ·
`gpt-oss-120b` → cooldown backoff ×2.

### 5.2 · IDEMPOTENCY — sửa xong H6

| | lần 1 | lần 2 |
|---|---|---|
| payload fingerprint | `ed97b8825034b1fc` | **`ed97b8825034b1fc`** |
| `v11178_challenger_runs` | 1 | **1** |
| `shadow_candidates` | 10 | **10** |
| exit code | 0 | **0** |

Lỗi ban đầu: `run_label` nhúng payload fingerprint, mà payload chứa `sealed_at` (dấu thời gian)
⇒ fingerprint đổi mỗi lần chạy. Sửa: **loại `sealed_at` khỏi fingerprint** + `run_label` **tất
định** (`METHOD|stage|date|region`).

---

## 6 · CỔNG KIỂM

| cổng | kết quả |
|---|---|
| `_v11178_thu.py` (§U10) | **35/35 ĐẠT** |
| ACTIVE_WRITER_PROOF W1–W4 | **KHÔNG thành lập** ⇒ cửa sổ an toàn |
| ZERO-WRITE official | **ĐẠT** — `final_bundles`/`predictions`/`day_governance`/`ocr` không đổi |
| production DB `mode=ro` | **CHẶN ghi** (`attempt to write a readonly database`) |
| idempotent rerun | **ĐẠT** |
| lane wrapper | `rc=0`, log riêng, flock hoạt động |

⚠️ **Ba phép ĐẠT RỖNG, ghi thẳng:** `B1` (MT same-day) · `B2` (MB same-day) · `C5` (đổi một
fact) — lúc 02:00 MN/MT **chưa xổ** nên "0 fact cùng ngày"; `C5` không có candidate liên quan.
**Chúng chỉ được kiểm thật khi lane delta chạy chiều nay 16:38 / 17:33.**

---

## 7 · VƯỚNG VẤP

| # | vấp | ai bắt |
|---|---|---|
| 1 | 🔴 **Kiểm ô nhiễm TỰ BẮT CHÍNH NÓ** — tên trường `official_picks_included` chứa chữ `official`, phép quét chuỗi thô báo ô nhiễm giả (`RM-09` lần nữa) | chính lần chạy đầu |
| 2 | 🔴 **Idempotency trượt** — `sealed_at` trong fingerprint làm `run_label` đổi mỗi lần | negative test |
| 3 | 🟠 Độ phủ candidate quá thấp (6/25 điều kiện) vì bắt khớp cả `lag`; nới thành khớp **ô nguồn** + ghi rõ `lag_match` | quan sát |
| 4 | 🟡 Ba phép test **đạt rỗng** vì chạy lúc 02:00 | tự phát hiện |

---

## 8 · GỠ VỀ

| việc | cách gỡ |
|---|---|
| cron V1.1 | `crontab /tmp/cron_pre_v11178.bak` (148 dòng) |
| dữ liệu shadow | `DELETE FROM shadow_candidates WHERE method_key='context_only_v11'; DROP TABLE v11178_challenger_runs;` |
| mã | 3 tệp mới (`_v11178_context_only_v11.py`, `_v11178_ranker.py`, `_v11178_thu.py`) + `_v11178_lane.sh` — **xoá là đủ**, không tệp official nào bị sửa |

**Không có gì để gỡ ở runtime:** 0 restart, PID `3870722` không đổi, health 200.

---

## 9 · THEO DÕI TIẾP

### 9.1 · Việc kế tiếp chính xác

> **Hôm nay 11/09:** `BASE_D1` **13:30** (chạy lại, idempotent) · `MT delta` **16:38** ·
> `MB delta` **17:33**. Sau closeout tự nhiên: chấm ba nhánh
> `CURRENT_OFFICIAL` × `DETERMINISTIC_CONTEXT_RANKER` × `PER_MODEL_CONTEXT_ONLY`,
> theo Top1 / Top2 / Top-K và hạng của đuôi trúng. **Không dùng kết quả để sửa ngược cùng ngày.**

### 9.2 · Nợ mở

| mức | nợ |
|---|---|
| 🔴 P1 | **`PREDICTIVE_LIFT = NOT_PROVEN`** · `POOL_VERDICT` = **HOLD** |
| 🔴 P1 | Ba phép test **đạt rỗng** — chờ lane delta chiều nay |
| P1 | Độ phủ candidate thấp (2–17/miền) ⇒ Top-K ngắn; cần mở rộng họ điều kiện |
| P1 | So sánh ba nhánh **chưa đủ** — official chưa sinh bundle 11/09 |
| P2 | `gemini-2.5-pro` 429 · `gpt-oss-120b` cooldown — cần backoff/retry ở lane |
| P2 | Roster 8 LLM < 19 model chạy trong official; shadow-active models chưa gộp |
| P2 | R6 · R7 · R8 vẫn `NOT_PERFORMED` · `PURE_CONTEXT_PARTIAL` |
| P3 | Report debt **39/254** — `LEGACY_ADMIN_DEBT`, không chặn |

### 9.3 · Không có việc nào chặn ở owner

Mọi vấn đề kỹ thuật trong §U đều tự giải được trong IDE. Không có lựa chọn mơ hồ cần owner phân xử.

---

## §62 — NGUỒN BA LỚP

### `OWNER_SAID`
> *«Tiếp tục tổng lực mạnh tay hơn nữa, đừng chần chừ» · «Không tiếp tục sản xuất một challenger
> chỉ ghi abstain vì payload không chứa dữ kiện đủ để suy ra số»* — 11/09/2026 ~01:18 ICT.

### `CODE_DID`
- `/tmp/v11177_payload_MB_2026-09-11.json` — `conditions[0]` **không có** trường quan sát nào.
- `shadow_candidates` V11177 — **1 dòng** (`MB`/`deepseek-chat`/`abstain`).
- V1.1: **486 live facts** · **24/24 run receipt** · **99 + 15 dòng ranked**.
- `v11178_challenger_runs` UNIQUE + `INSERT OR IGNORE` ⇒ rerun `1→1`, `10→10`, exit 0.
- `final_bundles=585` · `predictions=14686` · `day_governance=584` · `ocr NOT NULL=0` — **không đổi**.
- SQL row ID: **860 / 862 / 864**.
- `daily_evaluation.py --backfill` → **exit 2**, 0 traceback.

### `DOC_SAID`
- `REPORT_V11177.md` — *«CONTEXT_ONLY_SHADOW_READY_FOR_NEXT_LIVE»* ⇒ **đã hạ** (`RL-035`).
- `REPORT_V11176.md` — *«860 / 861 / 862»* ⇒ **chép sai**, đúng là **860 / 862 / 864** (`RL-036`).

**LỆCH BA LỚP:**
1. `DOC_SAID` ≠ `CODE_DID`: V11177 tuyên bố "ready"; payload không có live fact ⇒ **hạ trạng thái**.
2. `DOC_SAID` ≠ `CODE_DID`: báo cáo V11176 ghi ID sai; **evidence JSON đúng** ⇒ lỗi ở văn bản.
3. `OWNER_SAID` = `CODE_DID`: *«không tiếp tục abstain rỗng»* — abstain nay **kèm Top-K chấm được**.

---

TanPhatAI cần làm: ghi **`V11178`** — `governance_seq 493`, công khai bản này cùng `CONVERSATION_CONTEXT_V11178_20260911.md`. Ghi **TERMINAL: `ACTION_ABSTAIN_WITH_DIAGNOSTIC_RANKING` (B)**. Ghi **BẢY NGHI VẤN: H1·H2·H3·H5·H7 CONFIRMED · H4 REFUTED · H6 PARTIAL**. Ghi **V11177 ĐÃ BỊ HẠ TRẠNG THÁI** xuống `CONTEXT_ONLY_STRUCTURAL_PROTOTYPE · LIVE_PREDICTIVE_OUTPUT_NOT_PROVEN`, đính chính **append-only**, `RL-035` — lý do: payload V11177 **KHÔNG có một giá trị quan sát nào**, nên `abstain` là **hệ quả của payload thiếu cấu trúc**, KHÔNG phải lựa chọn dựa trên bằng chứng; cách diễn giải cũ **có lợi cho chính agent**. Ghi **V1.1 có 486 LIVE FACTS** với `observed_raw_value`/`observed_tail`/`available_at`/`source_row_id`, và **candidate derivation ánh xạ sang 00–99** — hai thứ V11177 thiếu hẳn. Ghi **roster 8 LLM đọc từ `model_registry`** (V11177 hardcode 4), **24/24 receipt, 0 im lặng bỏ sót**; ma trận **MN 6A/1R/1E · MT 6A/0R/2E · MB 6A/0R/2E**; mã lỗi thật `429 RESOURCE_EXHAUSTED` ×3 và cooldown ×2. Ghi **có diagnostic Top-K THẬT: 99 dòng + 15 dòng deterministic** — abstain nay **chấm được**, khác hẳn V11177. Ghi **idempotent ĐẠT** (fingerprint giống hệt, `1→1`, `10→10`, exit 0) sau khi loại `sealed_at` khỏi fingerprint và làm `run_label` tất định. Ghi **discovery `2026-01-14→07-12` / holdout `07-13→09-10` KHÔNG chồng lấn**, transform **đóng băng** lúc `01:45`, **FDR chỉ ở discovery**. Ghi **3 lane cron có flock + timeout + log + exit code**, chốt `LATE_REJECTED`. Ghi **35/35 test ĐẠT gồm metamorphic**, nhưng **3 phép ĐẠT RỖNG** (B1/B2/C5) vì MN/MT chưa xổ lúc 02:00 — chỉ kiểm thật được ở lane delta chiều nay. Ghi **ZERO-WRITE official xác minh**: `final_bundles=585` · `predictions=14686` · `day_governance=584` · `ocr=0`, **0 restart**. Ghi **§U13: row ID thật 860/862/864 — evidence JSON ĐÚNG, báo cáo V11176 chép sai (`RL-036`)**; **`evaluate_all_history` xác minh ĐÚNG claim** (RuntimeError + exit 2 + 0 traceback). Ghi **`SC12 = CLOSED · DO_NOT_REOPEN`**, **`PREDICTIVE_LIFT = NOT_PROVEN`**, **`POOL_VERDICT = HOLD`**. **Không mở Prompt 44. Không mở FU mới. Không mở Plan mới. Không trộn ERP. CHƯA sync Notion.**
