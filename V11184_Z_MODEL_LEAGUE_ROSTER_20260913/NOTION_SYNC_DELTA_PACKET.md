# NOTION_SYNC_DELTA_PACKET — V11184 · §Z · 13/09/2026

> **Agent IDE KHÔNG ghi Notion** (§57.1) và **không tuyên bố Notion đã sync**. Gói này là đầu vào cho
> TanPhatAI. Mọi dòng là delta so với trạng thái sau V11183.

---

## A. CHÍN TERMINAL BẮT BUỘC CỦA §Z

| terminal | giá trị |
|---|---|
| `V11183_PRIVATE_PUBLIC_LINEAGE` | **RECONCILED** |
| `CURRENT_REGIME_MODEL_LEADERBOARD` | **PUBLISHED** (kèm cảnh báo ở §D) |
| `INITIAL_LLM_ROSTER_COMPRESSION` | **NO_SAFE_CHANGE_WITH_REASON** |
| `DIRECT_TOKEN_CALL_CAP` | **EXACT_BLOCKER** (đã giảm 8→6, chưa đạt MAX_4) |
| `PROVIDER_WASTE` | **QUARANTINED_NO_RETRY** |
| `QD079_OPTIMIZER_GATE` | **DEPLOYED_TESTED** |
| `RETRAIN_SAFETY` | **CANDIDATE_PROMOTION_AND_ROLLBACK_READY** |
| `PURE_CONTEXT_GENERATOR` | **OFFLINE_PASS_TO_BOUNDED_SHADOW** |
| `PREDICTIVE_LIFT` | **NOT_PROVEN** — giữ nguyên |

---

## B. QUYẾT ĐỊNH → `docs/OWNER_DECISION_LEDGER.json`

- **`QD-079`** → `OWNER_APPROVED_C1_C2_C3_20260913_2044_ICT`, **ĐÃ TRIỂN KHAI**.
  `weight_optimizer.py` sha (LF) `35bd1fff…` → `4bfcf5fb…`. Restart PID `3870722→62494`.
- **`QD-080`** (MỚI) → `OWNER_APPROVED_20260913_2044_ICT` · `XH1309` ·
  `WEEKLY_MODEL_LEAGUE + INITIAL_LLM_ROSTER_COMPRESSION`. Giới hạn cứng: 3 CORE + 1 CHALLENGER mỗi
  miền · cap 4 direct-token call/miền/lượt · 1 swap/miền/tuần · tinh gọn đầu tiên **đúng một lần**.
  **Trạng thái thi hành: CHƯA LẬT ROSTER** — xem §E.

---

## C. FOLLOW-UP → `docs/FOLLOW_UP_TRACKER.md`

- `FU-430` = **CLOSED** · `RETRAIN_ACTIVATED_METRIC_NOT_COMPARABLE`
- `FU-351` = **SUPERSEDED_BY_V11183_GENERATOR_MISS**

**Sáu việc treo MỚI, mỗi việc có hạn và terminal bắt buộc:**

| # | việc | hạn | terminal khi tới hạn |
|---|---|---|---|
| 1 | Truy call-site `selected_models` → lật roster 8→4 | **20/09 02:00** | `APPLIED_ROLLBACK_READY` hoặc `ROSTER_COMPRESSION_RETIRED` — **không gia hạn lần hai** |
| 2 | Vá lệch khoá `cost_est`→`cost_estimate` | 20/09 | `COST_OBSERVABILITY_LIVE` hoặc `RETIRED` |
| 3 | `_v11059_lane_ab_3tang.py` ghi trace (22.2% lượt gọi vô hình) | 20/09 | `TRACE_COMPLETE` hoặc `LANE_AB_RETIRED` |
| 4 | Shadow hữu hạn generator thuần ngữ cảnh (≤20% ngân sách) | 27/09 (Day 14) | `PROVISIONAL_CHALLENGER` / `REGION_ONLY` / `RETIRE` |
| 5 | `main_selection_reason` ghi đúng khi override nổ | 20/09 | `FIXED` hoặc `ACCEPTED_AS_KNOWN_DEFECT` |
| 6 | Bảy nợ P0 (backup ngoài máy · SSH · swap/OOM) | chờ Owner | ưu tiên rủi ro cao nhất |

---

## D. LEADERBOARD — ĐỌC ĐÚNG, ĐỪNG ĐỌC SAI

**0/156 ô có ý nghĩa thống kê** (0/45 ở 30 ngày · 0/51 ở 90 ngày · 0/60 ở 180 ngày). Một ô 30 ngày
trung bình có **1.7 sự kiện** rescue+break; test dấu cần ≥6 sự kiện lệch hẳn một phía.

⇒ Bảng này chứng minh **Gate 2 (predictive/marginal) không dùng được để xếp hạng**, **không** chứng
minh model nào hơn model nào. **Cấm trích một dòng của nó làm bằng chứng ưu thế.**

Cổng tái lập: **99.38%** (480/483) sau khi tìm ra công thức đầy đủ. Chỉ tính trên **402 ngày
không-override**.

---

## E. PHÁT HIỆN LỚN NHẤT — ghi vào trang kiến trúc

**Bạch thủ official KHÔNG phải top-1 của phiếu model trong 16.8% số ngày (81/483).**

> **PHẠM VI — đọc trước khi trích:** 16.8% là tỉ lệ trên **TOÀN BỘ 483 bundle có dữ liệu**, KHÔNG phải số đo của một cửa sổ. Đây là **đặc tính kiến trúc**, không phải tuyên bố hiệu quả, nên không có bản 14 ngày / 30 ngày / 90 ngày / 180 ngày cho riêng nó. Mọi tuyên bố về **hiệu quả** trong gói này đều đã nêu đủ bộ **14 ngày · 30 ngày · 90 ngày · 180 ngày** ở §D và ở `REPORT_V11184.md` §4.2.

Bốn tầng ghi đè được Owner duyệt, tất cả flag-gated và đảo ngược được:

| tầng | phạm vi | vị trí |
|---|---|---|
| `V10640` per-slice BT override | MN | `main.py:10255` |
| `V10767` MB prev-day ML-plurality | MB | `main.py:10276` |
| `V10789 K11a` MB lane promote (`MB_OUTPUT_V1`) | MB | `main.py:10296` |
| `V10790 K15` MT lane promote (`MT_OUTPUT_V1`) | MT | `main.py:10316` |

**Kèm một khuyết tật quan sát:** `main_selection_reason` được gán **cứng** ở `main.py:10397` là
`"max_ranked_score_after_gate_and_lane_weight"` **sau** cả bốn nhánh ⇒ bản ghi **nói sai** điều đã
xảy ra ở đúng 16.8% số ngày đó.

---

## E2. SỤP PHỔ HỆ — ghi vào trang kiến trúc

`voter_count` của bundle **phóng đại tính độc lập**. Ngày 13/09 MN, BT=89 có 4 voter nhưng
**60.96% điểm truy về cùng cặp xgboost+random-forest** (`smart-ensemble` + `smart-ml` + phần
`combo-super`); chỉ `gemini-2.5-pro` (39.05%) là phổ hệ khác thật.

**Không model ML trực tiếp nào bỏ phiếu 89 trong top-2 của mình** — 89 vào bundle chỉ qua bộ dẫn
xuất đọc top-5 ⇒ BT official ngày đó **do tầng tổng hợp sinh ra**, củng cố `GENERATOR_MISS`.

Tần suất: **21/93 cặp ngày-miền trong 30 ngày (22.6%)**, output trùng **21/21**.

**Lỗi nhãn:** `smart-ensemble.analysis_text` ghi `meta_numbers`/`lstm_numbers` nhưng nội dung là
`xgboost`/`random-forest`. **Đừng đọc trường đó để suy phổ hệ.**

⇒ Mọi phép đếm "số nguồn độc lập" trên toàn bộ voter đang **phóng đại**. Gate 3 phải đếm **phổ hệ
GỐC**.

---

## F. ROSTER ĐÃ TÍNH XONG (chưa lật) — để TanPhatAI biết trước

| miền | CORE | CHALLENGER | bỏ |
|---|---|---|---|
| MN | claude-opus-4-6 · gemini-2.5-flash · gpt-oss-120b | claude-sonnet-4-6 | gemini-2.5-pro |
| MT | claude-opus-4-6 · gemini-2.5-flash · glm-5.1 | gpt-oss-120b | claude-sonnet-4-6, gemini-2.5-pro |
| MB | claude-opus-4-6 · gemini-2.5-flash · gpt-oss-120b | glm-5.1 | claude-sonnet-4-6, gemini-2.5-pro |

**Replay:** MN −0.79pp · MT +0.72pp · MB −0.74pp, **p = 1.0000 cả ba** ⇒ cắt một nửa LLM không mất
gì đo được.

**CORE ≠ "đã chứng minh lift"** (khoá Owner số 9). CORE = lựa chọn tốt nhất hiện có theo reliability
+ independence + cost.

---

## G. TOKEN — số nền cho mọi so sánh về sau

| | 30 ngày |
|---|---|
| Lượt gọi provider | 2.262 (75.4/ngày) |
| Token | 66.051.826 (2.2M/ngày) |
| **Vào model KHÔNG được ra output** | **39.805.853 = 60.3%** |
| Chi phí USD | **KHÔNG CÓ DỮ LIỆU** (0/1.760 dòng) |
| Lượt gọi không có bản ghi token | 502 = 22.2% |

**Đã cách ly, không retry:** `deepseek-reasoner` (402) · `gpt-5.4` (429 hết tiền) · `gpt-5-mini` ·
`deepseek-v4-pro-real`. Trạng thái **bền qua restart** tại `data/provider_quarantine.json`. Mở lại
**bắt buộc có bằng chứng sức khoẻ**, và trả về hàng **CHALLENGER**, KHÔNG tự về CORE.

---

## H. ĐIỀU TANPHATAI KHÔNG ĐƯỢC LÀM

- Không nâng `PREDICTIVE_LIFT` khỏi `NOT_PROVEN`.
- Không ghi `INITIAL_LLM_ROSTER_COMPRESSION` là đã áp dụng — **chưa lật**.
- Không mở lại `RANKER_V2_LINEAGE_DEDUP_CALIBRATED`.
- Không trích một dòng leaderboard làm bằng chứng model nào tốt hơn.
- Không đọc `main_selection_reason` như sự thật khi bundle có override.
- Không gia hạn mục §C.1 quá 20/09 — terminal bắt buộc đã đăng ký.
