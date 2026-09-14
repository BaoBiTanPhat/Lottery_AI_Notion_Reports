# NOTION_SYNC_DELTA_PACKET — V11187 · deploy gói §AB · 14/09/2026

> **Agent IDE KHÔNG ghi Notion** (§57.1) và **không tuyên bố Notion đã sync**. TanPhatAI chỉ sync
> **sau khi** code / private / public / runtime đã khớp.

---

## A. HAI CÂU PHẢI GHI ĐÚNG, ĐỪNG GỘP

| | |
|---|---|
| **Ngày 14/09 (chạy dưới V11185)** | **`ROSTER_SYSTEM_WIDE_LIVE_PROOF_FAIL`** — MN `OK` · MT `OK` · **MB `FAIL`** |
| **Gói §AB (deploy 20:05)** | **`DEPLOYED_PENDING_NATURAL_PROOF`** — PID `97754` → `169960` |

Hai câu này **khác nhau**. Deploy **không** biến ngày 14/09 thành pass, và **không** tự nó là
chứng minh runtime cho V11186.

---

## B. PHẢN CHỨNG SỐNG — cấm ghi `ZERO` cho ngày 14/09

`gemini-2.5-pro`, model **ngoài roster MB**, chạm HTTP **200** lúc **17:33:43** ngày 14/09, dưới
chính V11185.

| miền | terminal | ngoài roster | model chạm HTTP | cost |
|---|---|---|---|---|
| MN | `OK` 10/10 | 0 | 4 | **0/5 dòng** |
| MT | `OK` 10/10 | 0 | 4 | **0/4 dòng** |
| **MB** | **`FAIL` 8/10** | **`gemini-2.5-pro` ×1** | **5 (> trần 4)** | **0/5 dòng** |

⇒ Terminal đúng cho 14/09: **`MODEL_OUTSIDE_ROSTER_HTTP_CALLS = MB_NONZERO_LIVE_PROVEN`**.
Bản rút lại `RL-044` (hạ `ZERO` → `STATIC_SCHEDULER_PROOF_ONLY`) nay **được bằng chứng xác nhận
là đúng**.

---

## C. NGUỒN ĐÃ QUY ĐƯỢC: COMBO SUPER — và ghi đúng mức bằng chứng

Combo Super là bước **cuối cùng** của `_run_ai_models_predict` (`scheduler.py:5114`).
`scheduler_logs` ghi mốc đầu/cuối của nó (naive = **UTC**, §55, phải cộng 7 giờ):

| miền | cửa sổ Combo | lượt nằm trọn trong cửa sổ | ngoài roster? |
|---|---|---|---|
| MN | 05:16:35 → 05:17:32 (57 s) | `claude-opus-4-6` | không — **may, không nhờ cổng** |
| MT | 16:43:58 → 16:44:02 (**4 s**) | không có | — |
| MB | 17:33:05 → 17:33:43 (38 s) | **`gemini-2.5-pro`** | **CÓ** |

**Mức bằng chứng: `QUY_DUOC_BANG_LONG_THOI_GIAN`.** KHÔNG được ghi thành
`QUY_DUOC_BANG_TRUONG_CALLER` — trace của V11185 không có trường `caller`. Dứt điểm chỉ có từ
15/09.

---

## D. DEPLOY — số liệu đối chiếu được

| | |
|---|---|
| PID | **97754 → 169960** · NRestarts 0 · ActiveState `active` |
| health · `/monitoring` | **200** · **401** |
| journal 3 phút sau restart | **0** dòng traceback/CRITICAL/ImportError |
| 4 bảng khoá | `14965 / 597 / 15483 / 14829` — **khớp từng con số** với ảnh chụp preflight |
| crontab | `81efcf8de5c90c62`, **90 job** — không đổi |
| epoch | 14/09 trọn ngày V11185 · 15/09 trọn ngày V11186 — **không miền nào bị chẻ** |
| bộ thử trên VPS trước restart | §AB **102/102** · §AB-L **45/45** · thử ngược sự cố **17/17** · §AA **45/45** · §Z **65/65** |
| sau restart | `gemini-2.5-pro` @MB và @MN lớp `combo_super` ⇒ **`DENY_OUTSIDE_ROSTER`** |

---

## E. ĐƯỜNG GỠ VỀ NAY CÓ THẬT

- **CẤP 1**: 5 tệp `.pre_v11186` trên VPS, sha256 khớp bản **trước** deploy cả 5.
  Trước V11186b, runbook trỏ vào một thư mục **không tồn tại** — thủ tục không thực thi được.
- **CẤP 2**: `LOTTERY_ROSTER_KHAN_CAP=1`, **hạn 24 h** đo từ **lần bật đầu tiên** (restart không
  reset), hết hạn **tự về trần 4** (không fail-closed), **ALERT stderr**, biến viết sai ⇒
  **từ chối mở cửa**.
- **Lưu ý khi cân nhắc CẤP 1**: V11185 là bản **đã được đo là còn rò** ở Combo.

---

## F. ĐIỀU TANPHATAI KHÔNG ĐƯỢC LÀM

- **Không** ghi `MODEL_OUTSIDE_ROSTER_HTTP_CALLS = ZERO` cho ngày 14/09 dưới bất kỳ dạng nào.
- **Không** nâng `DEPLOYED_PENDING_NATURAL_PROOF` thành `ROSTER_SYSTEM_WIDE_LIVE_PROOF_OK` —
  chờ ba receipt tự nhiên ngày 15/09.
- **Không** ghi nguồn lượt vi phạm là "đã chứng minh bằng `caller`" — mức đúng là lồng thời gian.
- **Không** đọc "MN sạch 14/09" thành "MN đã được bảo vệ" — đó là may.
- **Không** ghi `TOKEN_REDUCTION` bằng bất kỳ con số nào — vẫn `NOT_YET_MEASURED`; cost trắng
  **3/3 miền**.
- **Không** ghi `COST_OBSERVABILITY` là xong — mã vừa deploy, số đo đầu tiên từ 15/09.
- **Không** ghi `OVERRIDE_LINEAGE` · `FAMILY_LINEAGE` · `RETRAIN_SAFETY` là xong — cả ba vẫn
  `EXACT_BLOCKER` (20/09 · 20/09 · **19/09 23:00**).
- **Không** ghi `PURE_CONTEXT` là `RETIRED` — nó là `DEFERRED`, zero token spent.
- **Không** nâng `PREDICTIVE_LIFT` khỏi `NOT_PROVEN`; giữ `POOL_VERDICT=HOLD` · `SC12=CLOSED`.
