# NOTION_SYNC_DELTA_PACKET — V11185 · §AA · 13/09/2026

> **Agent IDE KHÔNG ghi Notion** (§57.1) và **không tuyên bố Notion đã sync**. Gói này là đầu vào
> cho TanPhatAI, cập nhật **sau khi** private/public/code/runtime đã khớp.

> 🔴 **GÓI NÀY CÓ BỐN MỤC ĐÃ RÚT LẠI** (`RL-044`–`RL-047`, ngày 14/09/2026 theo §AB-B).
> TanPhatAI **KHÔNG** được sync các terminal đã gạch. Đọc `V11186` §2 trước.

---

## A. MƯỜI BẢY TERMINAL §AA-W

| terminal | giá trị |
|---|---|
| `TOKEN_CALL_ROSTER_SSOT` | **DEPLOYED** |
| `UNBOUNDED_SHADOW_PROVIDER_CALLS` | 🔴 **RÚT LẠI RL-045** → **DEPLOYED_PENDING_NATURAL_RECEIPT** |
| `INITIAL_LLM_ROSTER_COMPRESSION` | **APPLIED_ROLLBACK_READY** |
| `DIRECT_OFFICIAL_GENERATOR_MODELS` | **MAX_4_PER_REGION** |
| `MODEL_OUTSIDE_ROSTER_HTTP_CALLS` | 🔴 **RÚT LẠI RL-044** → **STATIC_SCHEDULER_PROOF_ONLY · SYSTEM_WIDE_LIVE_PROOF_PENDING** |
| `DETERMINISTIC_PROVIDER_RETRIES` | **ZERO** |
| `COST_OBSERVABILITY` | **EXACT_BLOCKER** (hạn 20/09) |
| `TRACE_COVERAGE` | **ACTIVE_LANE_RETIRED** |
| `COMBO_SUPER_EXTRA_CALLS` | **COUNTED_SEPARATELY** |
| `OVERRIDE_LINEAGE` | **EXACT_BLOCKER** (hạn 20/09) |
| `FAMILY_LINEAGE` | **EXACT_BLOCKER** (hạn 20/09) |
| `RETRAIN_SAFETY` | **EXACT_BLOCKER** (hạn trước CN 20/09 02:00) |
| `PURE_CONTEXT` | 🔴 **RÚT LẠI RL-046** → **DEFERRED_PENDING_ROSTER_LIVE_PROOF · ZERO_TOKEN_SPENT** |
| `TOTAL_FORMULA` | **UNCHANGED** |
| `CURRENT_WEIGHTS` | **UNCHANGED** |
| `PREDICTIVE_LIFT` | **NOT_PROVEN** |
| `POOL_VERDICT` · `SC12` | **HOLD** · **CLOSED_DO_NOT_REOPEN** |

---

## B. ROSTER VERSION — ghi vào trang trạng thái

**`token_call_roster/2026.09.14-1`**
· `owner_approval_ref` = `QD-080 · §Z khoá 2-6 (13/09/2026 20:44 ICT) · §AA mục D`
· `effective_from` = `2026-09-14T00:00:00+07:00`
· **activate thật lúc 22:36 ngày 13/09** (restart PID `85063 → 97754`)
· `previous_version` = `null` (đây là bản đầu tiên của cơ chế)
· rollback = một lệnh `LOTTERY_ROSTER_KHAN_CAP=1` + restart

| miền | CORE | CHALLENGER |
|---|---|---|
| MN | claude-opus-4-6 · gemini-2.5-flash · gpt-oss-120b | claude-sonnet-4-6 |
| MT | claude-opus-4-6 · gemini-2.5-flash · glm-5.1 | gpt-oss-120b |
| MB | claude-opus-4-6 · gemini-2.5-flash · gpt-oss-120b | glm-5.1 |

**`QD-080` chuyển từ "chưa lật" sang ĐÃ THI HÀNH.**

---

## C. TRẠNG THÁI MODEL — ghi đúng nhãn

| nhóm | model | nhãn |
|---|---|---|
| Không còn trong call roster | `gemini-2.5-pro` (mọi miền) · `claude-sonnet-4-6`@MT/MB · `glm-5.1`@MN | **REGION_ONLY / không auto-call** |
| 11 model `SHADOW_AUTO` không phải challenger | — | **`SHADOW_PAUSED`** — **KHÔNG phải RETIRE**; registry và lịch sử **giữ nguyên**, thuận nghịch |
| Cách ly deterministic | `deepseek-reasoner` · `gpt-5.4` · `gpt-5-mini` · `deepseek-v4-pro-real` | **QUARANTINE** — mở lại cần bằng chứng sức khoẻ, về hàng **CHALLENGER** không về CORE |
| Lane A/B | `_v11059_lane_ab_3tang` | **`LANE_AB_RETIRED_ZERO_OFFICIAL_IMPACT`** |

---

## D. GIẢM CHI — ĐỌC ĐÚNG

| | trước | sau (ước lượng) |
|---|---|---|
| lượt gọi provider / 30 ngày | 2.262 | ~489 (**−78.4%**) — 🔴 **RL-047: ESTIMATE_ONLY** |
| token / 30 ngày | 66,051,826 | ~16,741,700 (**−74.7%**) — 🔴 **RL-047: ESTIMATE_ONLY**, chưa tách Combo |

**Phân rã — điều dễ đặt sai ưu tiên:** chặn shadow đóng góp **−54.8%**, tinh gọn roster chỉ
**−19.9%**. 60.3% token của hệ vốn chảy vào model **không được phép ra output**.

⚠️ **Đây là ƯỚC LƯỢNG theo tỷ lệ số model, KHÔNG phải số đo.** Số thật đến từ **natural receipt**
lượt MN sáng 14/09. Đừng trích như số đo.

**Chưa tính:** Combo Super tự gọi thêm provider (`combo_super.py:1134`) — đếm riêng, **không giấu
vào "một voter"**.

---

## E. TÁM VIỆC TREO — mỗi việc có hạn và terminal bắt buộc

| # | việc | hạn | terminal |
|---|---|---|---|
| 1 | Thu và chấm **natural receipt đầu tiên** | 14/09 EOD | `ROSTER_LIVE_PROOF_OK` hoặc auto-rollback |
| 2 | Cost observability (`cost_est`→`cost_estimate` + 4 route + bảng giá versioned) | 20/09 | `COST_OBSERVABILITY_LIVE` hoặc `RETIRED_WITH_REASON` |
| 3 | Override lineage cho bundle MỚI (không backfill 16.8% ngày cũ) | 20/09 | `CORRECT_FOR_NEW_BUNDLES` hoặc `RETIRED_WITH_REASON` |
| 4 | Family lineage + sửa nhãn sai `smart-ensemble` | 20/09 | `OBSERVABILITY_FIXED_NO_SCORING_CHANGE` hoặc `RETIRED_WITH_REASON` |
| 5 | Retrain atomic candidate path | **trước CN 20/09 02:00** | `ATOMIC_..._READY` hoặc `RETRAIN_ABORTED_FAIL_CLOSED_WITH_EXACT_MODULE` |
| 6 | Pure-context bounded shadow + preregistration | sau receipt #1 | `BOUNDED_SHADOW_PREREGISTERED` hoặc `RETIRED` |
| 7 | Combo Super: thử reuse frozen same-run output | 20/09 | `REUSED_OUTPUT_EQUIVALENT` hoặc giữ `COUNTED_SEPARATELY` |
| 8 | Bảy nợ P0 (backup ngoài máy · SSH · swap/OOM) | chờ Owner xếp lịch | — |

---

## F. ĐIỀU TANPHATAI KHÔNG ĐƯỢC LÀM

- Không nâng `PREDICTIVE_LIFT` khỏi `NOT_PROVEN`.
- Không ghi bốn mục `EXACT_BLOCKER` (cost · override lineage · family lineage · retrain) là đã xong.
- Không ghi 11 model shadow là `RETIRE` — chúng là **`SHADOW_PAUSED`**, thuận nghịch.
- Không trích ước lượng −74.7% như số đo.
- Không mở lại `RANKER_V2_LINEAGE_DEDUP_CALIBRATED`.
- Không gia hạn mục §E.1 quá 14/09 EOD, và §E.2–5 quá 20/09.
