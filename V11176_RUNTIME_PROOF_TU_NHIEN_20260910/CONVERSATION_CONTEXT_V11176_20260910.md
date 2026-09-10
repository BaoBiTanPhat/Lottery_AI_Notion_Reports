# CONVERSATION CONTEXT — V11176 · 10/09/2026

> Nguyên văn lời owner · agent làm gì · vấp ở đâu (§57.2). Giờ **Việt Nam (UTC+07:00)**.
> `CURRENT_ACTOR = CLAUDE_CODE` · **Prompt 43 R1 giữ `PARTIAL` — không mở Prompt 44.**
> **`PRODUCTION_MUTATIONS = 0` · `DB MUTATIONS (bởi phiên) = 0` · `DEPLOY/RESTART = 0`**
> **SC-12 LIVE PATH: `DEPLOYED_PENDING_CONSUMER_UI_PROOF`**

---

## 1 · Owner nói gì — NGUYÊN VĂN

| giờ ICT | NGUYÊN VĂN | loại | agent đã làm gì | trạng thái |
|---|---|---|---|---|
| **~13:45** | *«[CONTINUATION · PROMPT TỔNG LỰC LẦN 43 R1 · §S] [V11175 GOVERNANCE CLOSEOUT + PRE-SCHEDULED RUNTIME PROOF + NATURAL CONSUMER EVIDENCE]»* | `YÊU_CẦU` | §S0→§S2 ngay · §S1 xong trước 16:20 · **freeze 16:16:01** · quan sát lượt tự nhiên 16:37–18:34 · §S4–§S8 | `ĐÃ_LÀM` |

---

## 2 · Điều đáng nói nhất — một dòng bảng nói hết

```
2026-09-05 MT   completed=13  →  DEGRADED_LIVE_DAY / EXCLUDE_PRIMARY
2026-09-06 MT   completed=13  →  DEGRADED_LIVE_DAY / EXCLUDE_PRIMARY
2026-09-07 MT   completed=13  →  DEGRADED_LIVE_DAY / EXCLUDE_PRIMARY
2026-09-08 MT   completed=13  →  DEGRADED_LIVE_DAY / EXCLUDE_PRIMARY
2026-09-10 MT   completed=13  →  VALID_LIVE_DAY    / INCLUDE
```

**Cùng một con số đầu vào. Phán quyết đổi.** Đó là toàn bộ điều SC-12 muốn sửa, và hôm nay nó
xảy ra trong production, do `auto_verify` **tự chạy**, không có một lệnh tay nào.

Và quan trọng hơn: em đã **niêm phong kỳ vọng lúc 16:41:00**, khi `day_governance` cho MT còn
`null`. Output ghi lúc **17:30:01**. **Cách nhau 49 phút.** Không thể viết ngược.

---

## 3 · Điều đáng nói thứ hai — input KHÔNG đứng yên, và em suýt niêm phong nhầm

Bộ lấy mẫu v2 của em niêm phong **lần đầu** thấy bundle. Với MN, bundle có từ 05:26:43 với
`mc=14`. Em niêm phong lúc 14:07:45 → kỳ vọng `EXCLUDE_PRIMARY`.

Đến snapshot B lúc 16:12 thì `mc = 15` — kỳ vọng thành `INCLUDE`. Truy lại mẫu:

```
15:40:06   MN mc: 14 → 15     (created_at VẪN 05:26:43)
```

Đúng mốc **`t10_chot` MN 15:40**. Bundle được **cập nhật tại chỗ**, `created_at` không đổi —
**bằng chứng độc lập cho `RL-018`**: `created_at` **không phải** dấu chốt.

Nếu em không kiểm lại, «preregistration» của em đã niêm phong trên **input chưa hoàn chỉnh**, và
kết quả `INCLUDE` sẽ trông như *sai kỳ vọng* trong khi thực ra là **em đo sai đối tượng**.
Đã nâng lên v3 (niêm phong lại mỗi khi `INPUT_HASH` đổi) **trước** mốc freeze, và **giữ cả hai
seal** chứ không lặng lẽ thay.

---

## 4 · Điều đáng nói thứ ba — «45» đúng từ đầu, em mới là người đếm sai

V11174 báo *«49 = 46 + 3, lệch +1, `INDETERMINATE`, xung đột `RL-014`»*. V11175 giữ nguyên.

§S7 đối chiếu **từng dòng**:

```
dry-run 49 · thật sự đổi 48 · hiệu = {('2026-07-25','MT')}
chiều ngược = RỖNG
```

Dòng thừa `25/07 MT` — **chính tệp dry-run** ghi `cu_status = moi_status = DEGRADED_LIVE_DAY`,
tức **không đổi gì**. Số đúng **48 = 45 + 3**.

⇒ **«45» trong sổ ĐÚNG TỪ ĐẦU. `RL-014` ĐÚNG. «46» của em mới sai.**
Và **bản rút lại mà em viết ở V11175** (nói rằng «45» sai) **chính là một bản rút lại SAI** —
nay rút lại chính nó (`RL-034`).

Tiền đề *«không có script gốc để tái lập»* là **sai**: không cần script gốc, chỉ cần đối chiếu
từng dòng. `INDETERMINATE` phải kèm **đã thử phép đo nào**, nếu không nó thành chỗ trú.

---

## 5 · Điều đáng nói thứ tư — lỗi UI không còn là suy đoán

MT hôm nay là **đúng ca kích hoạt**:

```
DB thô  wr_gate_filtered = ['claude-opus-4-6', 'claude-sonnet-4-6']
API     trả về            = []                                        ← VA-2′ sạch
UI      du-doan.html:1438  if (!qualityFilteredModels.length && sourcePreds.wr_gate_filtered)
                              → điều kiện THÀNH ĐÚNG → lấy lại danh sách nhiễm
```

Nghĩa là **hôm nay, trên dữ liệu sống, giao diện hiện đúng hai model bị TRẦN CỐ Ý như thể chúng
«trượt quality»** — trong khi backend và API đều đã sạch. Đó là `CONSUMER_UI_PARTIAL`, và vì thế
**chưa được ghi `SC12_LIVE_PATH_RUNTIME_PROVEN`**.

Em **không vá** — `du-doan.html` là mặt official, ngoài phạm vi, và vá trong epoch này sẽ **trộn
bằng chứng**. Đã có đặc tả + 8/8 test, chờ một cửa sổ an toàn khác.

---

## 6 · Vấp ở đâu

| # | vấp | ai bắt |
|---|---|---|
| 1 | 🔴 **`QD-074` của em sai schema và LÀM CHẾT cổng sổ quyết định** — 75/76 mục dùng `list[dict]`, riêng của em là chuỗi ⇒ probe ném `AttributeError` ⇒ cổng báo «KHÔNG ĐO ĐƯỢC» | cổng, khi chạy lại |
| 2 | 🔴 **Niêm phong trên input chưa hoàn chỉnh** (mục 3) | snapshot B |
| 3 | 🔴 **`dau_hieu` của `RL-034` viết KHÔNG DẤU** ⇒ cổng mù với chữ có dấu; sửa xong nó bắt ngay một chỗ thật | chính cổng |
| 4 | 🟠 **Hai báo động giả do đếm chuỗi thô** (`RM-09` lần hai): `\|\| echo n/a` phá phép so preimage; `-i ERROR` khớp chữ «errors:» trong dòng WARNING | tự kiểm khi thấy vô lý |
| 5 | 🟠 **Em ước lượng giờ thay vì đo** — báo «15:50» khi thực tế **14:37** | tự phát hiện |
| 6 | 🟡 SSH rớt 255 nhiều lần vì `pkill -f 's2_mon'` **khớp chính shell của lệnh ssh** | truy nguyên |
| 7 | 🟡 Heredoc mangling `\n` — đúng lỗi đã ghi trong bộ nhớ, vẫn tái phạm | assert của script |

**Năm trong bảy vấp là PHÉP ĐO CỦA EM SAI, không phải hệ thống sai.** Ba lần suýt báo cáo một
điều không có thật. Cách duy nhất bắt được: **thấy kết quả vô lý thì đo lại có phân loại**.

---

## 7 · Cho TanPhatAI đọc tiếp

**Bốn dòng trạng thái, cấm gộp:**
`SC12_LIVE_PATH = DEPLOYED_PENDING_CONSUMER_UI_PROOF` ·
`SC12_HISTORICAL = SC12_HISTORICAL_REPAIR_PENDING` ·
`PURE_CONTEXT = PURE_CONTEXT_PARTIAL` · `PREDICTIVE_LIFT = NOT_PROVEN`.

**Đừng đọc «MT ra INCLUDE» thành «hệ dự đoán tốt hơn».** Đây là **sửa phép đo**. Kết luận V11170
*«hệ không hơn ngẫu nhiên»* **vẫn đứng nguyên**.

**Đừng đọc «classifier proven» thành «consumer proven».** UI vẫn nhiễm.

**Đừng dùng journal để đếm số miền đã phân loại** — chỉ đường MN in `[DAY-GOV]`; MT/MB không.
Tín hiệu đáng tin là `day_governance.classification_source`.

**Một việc chặn ở owner:** `DEFAULT_BRANCH_STATE_CONFLICT` — `master` ở **V11123**, sau `fu438`
**54 commit**. Em không tự merge.

---

TanPhatAI cần làm: ghi **`V11176`** — công khai bản này cùng `REPORT_V11176.md`. Ghi **bốn dòng trạng thái RIÊNG**: `DEPLOYED_PENDING_CONSUMER_UI_PROOF` · `SC12_HISTORICAL_REPAIR_PENDING` · `PURE_CONTEXT_PARTIAL` · `PREDICTIVE_LIFT = NOT_PROVEN`. Ghi **`auto_verify` chạy TỰ NHIÊN cả ba miền, `classification_source = auto_verify`, 0 lệnh tay, agent freeze từ 16:16:01**. Ghi **bằng chứng quyết định: cùng `completed=13`, MT 05–08/09 đều `EXCLUDE_PRIMARY`, 10/09 ra `INCLUDE`**. Ghi **kỳ vọng niêm phong TRƯỚC output: MT seal 16:41:00, output 17:30:01, cách 49 phút**. Ghi **input MN đổi 14→15 lúc 15:40:06 trong khi `created_at` vẫn 05:26:43 — bằng chứng độc lập cho `RL-018`**, và **agent suýt niêm phong nhầm trên input chưa hoàn chỉnh**. Ghi **backend consumer proven: `daily_eval_log` 432 → 435**. Ghi **`CONSUMER_UI_PARTIAL` — MT hôm nay là ca kích hoạt thật: API trả `[]` nhưng UI rơi ngược về `wr_gate_filtered` 2 phần tử**; **KHÔNG vá** vì sẽ trộn evidence epoch. Ghi **no-drift: digest phạm vi khoá `0c5f84f8…` KHỚP trên 582 dòng, 0 bề mặt cấm đổi, PID 3870722 NRestarts 0, 0 lỗi journal**. Ghi **`MT EXCLUDE_PRIMARY` vẫn 98 — backfill CHƯA chạy**. Ghi **§S7 gỡ `INDETERMINATE`: đúng 48 = 45 + 3, «45» ĐÚNG TỪ ĐẦU, `RL-014` ĐÚNG, và bản rút lại của agent ở V11175 là bản rút lại SAI (`RL-034`)**. Ghi **`FU-451` không được tạo — append `FU_451_INVALID_REFERENCE`**. Ghi **CHẶN Ở OWNER: `DEFAULT_BRANCH_STATE_CONFLICT`, `master` ở V11123 sau `fu438` 54 commit**. **Không mở Prompt 44. Không mở Plan mới. Không mở FU mới. Không trộn ERP. Notion KHÔNG cập nhật lượt này.**
