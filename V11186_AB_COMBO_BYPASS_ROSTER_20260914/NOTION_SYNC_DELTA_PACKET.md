# NOTION_SYNC_DELTA_PACKET — V11186 · §AB · 14/09/2026

> **Agent IDE KHÔNG ghi Notion** (§57.1) và **không tuyên bố Notion đã sync**. TanPhatAI chỉ sync
> **sau khi** code/private/public/runtime đã khớp.

> ⚠️ **ĐỌC TRƯỚC:** gói V11185 có **bốn mục đã rút lại**. Xem §A dưới đây trước khi sync bất cứ gì.

---

## A. BỐN MỤC RÚT LẠI CỦA V11185 (RL-044 – RL-047)

| mã | terminal cũ (SAI) | terminal đúng |
|---|---|---|
| `RL-044` | `MODEL_OUTSIDE_ROSTER_HTTP_CALLS = ZERO` | **`STATIC_SCHEDULER_PROOF_ONLY · SYSTEM_WIDE_LIVE_PROOF_PENDING`** |
| `RL-045` | `UNBOUNDED_SHADOW_PROVIDER_CALLS = ZERO` | **`DEPLOYED_PENDING_NATURAL_RECEIPT`** |
| `RL-046` | `PURE_CONTEXT = RETIRED_BEFORE_TOKEN_SPEND` | **`DEFERRED_PENDING_ROSTER_LIVE_PROOF · ZERO_TOKEN_SPENT`** |
| `RL-047` | `−74,7% token` như số giảm | **`ESTIMATE_ONLY`** |

Đã sửa tại **chính chỗ đã công bố** trong `V11185_AA_TOKEN_CALL_ROSTER_20260913/` kèm banner.
**TanPhatAI không được sync các terminal đã gạch.**

---

## B. TRẠNG THÁI THẬT HÔM NAY

| | |
|---|---|
| VPS đang chạy | **V11185** (PID 97754, NRestarts 0, health 200) |
| Mã §AB | **`STAGED_NOT_DEPLOYED`** — hoàn tất trong repo, **chưa** lên VPS |
| Vì sao chưa deploy | §AB-J cấm "MN một version, MT/MB version khác". MN đã chạy 05:00 sáng nay ⇒ giữ **một epoch V11185** trọn ngày 14/09 |
| Deploy khi nào | **sau EOD 14/09, effective trước 04:00 ngày 15/09** |

---

## C. RECEIPT SỐNG — chỉ MỘT miền, KHÔNG được suy thành ba

**`MN_ROSTER_LIVE_PROOF_OK`** (10/10) — lượt MN tự nhiên 05:00–05:17 ngày 14/09:

| | |
|---|---|
| model chạm HTTP | `claude-opus-4-6`×2 · `claude-sonnet-4-6` · `gemini-2.5-flash` · `gpt-oss-120b` |
| **ngoài roster / bị cách ly** | **0 / 0** |
| model duy nhất | 4 (≤ trần 4) |
| bundle | `bach_thu=24` |
| token | 151.015 · **cost: 0/5 dòng có** |
| điểm mở | `claude-opus-4-6` 2 lượt — **`LUOT_THEM_CHUA_QUY_DUOC_NGUON`**, trace không ghi caller/fingerprint nên **KHÔNG đoán** |

**MT và MB CHƯA CHẠY.** Bộ thu nền đang đợi trên VPS. **Không được ghi
`ROSTER_SYSTEM_WIDE_LIVE_PROOF_OK` khi chưa đủ ba miền.**

---

## D. BYPASS LÀ THẬT — số đo 30 ngày

Model **ngoài roster** từng có mặt trong bundle (90 ngày-miền):

| miền | model | số ngày |
|---|---|---|
| MN | `gemini-2.5-pro` | **29/30** |
| MT | `gemini-2.5-pro` | 28 |
| MB | `gemini-2.5-pro` · `deepseek-reasoner` | 27 · 27 |
| MT | `deepseek-reasoner` | 26 |
| MN | `deepseek-reasoner` · `glm-5.1` | 24 · 24 |
| MT / MB | `claude-sonnet-4-6` | 23 / 17 |

**Đọc đúng:** phần lớn là lượt gọi của **scheduler TRƯỚC §AA**, không phải riêng Combo. Bằng chứng:
bundle 13/09 MN có `gemini-2.5-pro`, bundle **14/09 MN có 0 model ngoài roster** — cổng scheduler
của §AA đã đóng đường chính trên thực tế.

Cái còn hở là **cấu trúc**: pool riêng của Combo vẫn chứa 4 model không được phép. Hôm nay không
dùng tới, **nhưng "hôm nay không dùng" ≠ "không thể dùng"**.

---

## E. MÃ §AB ĐÃ HOÀN TẤT (staged)

- **Combo gate**: giao pool với roster **trước khi chấm điểm**; đóng fallback `else AI_MODELS`;
  nhãn `COMBO_AI_PHASE_SKIPPED_NO_AUTHORIZED_MODEL`. Thuật toán chọn top-N **giữ nguyên**.
- **Uỷ quyền tại dispatcher cuối**: 7 kết quả; fail-closed khi thiếu `target_region`/
  `execution_class`; caller **không được tự bịa** lớp; cửa bảo trì TẮT mặc định + có hạn.
- **Ngữ cảnh truyền từ entry point canonical**: cả **7 call-site sống**, xác minh bằng AST.
- **Request fingerprint** 11 trường; chỉ reuse khi **giống hệt**; đổi một trường ⇒ không reuse.
- **Cost**: đọc cả `cost_est` và `cost_estimate`; phân biệt `ACTUAL_PROVIDER`/`UNKNOWN`;
  **không bao giờ biến UNKNOWN thành 0**.
- **Bộ thử**: `_v11186_thu_ab.py` **102/102** trên mã đã vá.

---

## F. ĐIỀU TANPHATAI KHÔNG ĐƯỢC LÀM

- **Không** sync bốn terminal đã rút lại của V11185.
- **Không** ghi mã §AB là đã deploy — nó là `STAGED_NOT_DEPLOYED`.
- **Không** suy `MN_ROSTER_LIVE_PROOF_OK` thành ba miền pass.
- **Không** ghi `TOKEN_REDUCTION` bằng bất kỳ con số nào — hiện là **`NOT_YET_MEASURED`**.
- **Không** ghi `COST_OBSERVABILITY`, `OVERRIDE_LINEAGE`, `FAMILY_LINEAGE`, `RETRAIN_SAFETY` là
  đã xong — cả bốn vẫn `EXACT_BLOCKER`.
- **Không** ghi `PURE_CONTEXT` là `RETIRED` — nó là `DEFERRED`, zero token spent.
- **Không** nâng `PREDICTIVE_LIFT` khỏi `NOT_PROVEN`.
