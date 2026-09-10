# CONVERSATION CONTEXT — V11178 · 11/09/2026

> Nguyên văn lời owner · agent làm gì · vấp ở đâu (§57.2). Giờ **Việt Nam (UTC+07:00)**.
> `CURRENT_ACTOR = CLAUDE_CODE` · **Prompt 43 R1 tiếp tục — không mở Prompt 44.**
> **TERMINAL: `ACTION_ABSTAIN_WITH_DIAGNOSTIC_RANKING`**

---

## 1 · Owner nói gì — NGUYÊN VĂN

| giờ ICT | NGUYÊN VĂN | loại | agent đã làm gì | trạng thái |
|---|---|---|---|---|
| **~01:18** | *«[CONTINUATION · §U] [REPAIR REAL CONTEXT-ONLY CHALLENGER · LIVE RANKED OUTPUT · STOP EMPTY-ABSTAIN LOOP]»* · *«Tiếp tục tổng lực mạnh tay hơn nữa, đừng chần chừ»* | `YÊU_CẦU` | §U0→§U14 đủ | `ĐÃ_LÀM` |

---

## 2 · Điều đáng nói nhất — em đã tự khen một khiếm khuyết thiết kế

V11177 em viết: *«model correctly abstains vì không đủ bằng chứng»* và coi đó là **kết quả
trung thực**.

Owner nghi ngờ. Em đi kiểm bằng lệnh trên **chính tệp payload** mình đã sinh:

```
conditions[0] có: condition_id, source_region, source_station, source_prize,
                  source_position, lag, support, stability, z_vs_nen, du_manh...
conditions[0] KHÔNG có: source_date · observed_raw_value · observed_tail · available_at
```

Model được cho biết *«ô `MT.Đà Nẵng.Giải sáu[1]` lag=1 có stability 0,45 trên 40 mẫu»* nhưng
**không bao giờ được cho biết SỐ NÀO đã ra ở ô đó**.

⇒ Model **không thể** gọi tên bất kỳ đuôi nào. **`abstain` là output DUY NHẤT CÓ THỂ**, bất kể
bằng chứng mạnh hay yếu. Ngay cả `z=10` cũng không cứu được.

**Nghĩa là:** em đã biến một **khiếm khuyết cấu trúc** thành một **«kết luận trung thực»** — và
cách diễn giải đó **có lợi cho chính em**. Đây là dạng sai nguy hiểm hơn một con số sai, vì nó
nghe **giống như sự cẩn trọng**.

Đã hạ trạng thái V11177, đính chính **append-only** (không xoá dấu vết), `RL-035`.

---

## 3 · Điều đáng nói thứ hai — sửa cấu trúc thì abstain có nghĩa khác hẳn

V1.1 thêm **LỚP B — LIVE FACTS**, thứ V11177 thiếu hẳn:

```
486 live facts, mỗi cái có:
   observed_raw_value  ·  observed_tail  ·  available_at  ·  source_row_id
và LỚP C biến chúng thành số:  T2_reverse("45") = "54"
```

Kết quả chạy thật, **24/24 model×miền đều có receipt**:

```
              ABSTAIN  RANKED  ERROR
    MN            6       1      1
    MT            6       0      2
    MB            6       0      2
```

Vẫn phần lớn `ABSTAIN` — **nhưng lần này abstain là một QUYẾT ĐỊNH**, và đi kèm **99 dòng
diagnostic Top-K chấm được**. Đó là khác biệt giữa *«không có gì để nói»* và *«tôi đã cân nhắc,
bằng chứng yếu, nhưng đây là thứ tự tôi xếp»*.

---

## 4 · Vấp ở đâu

| # | vấp | ai bắt |
|---|---|---|
| 1 | 🔴 **Hàm kiểm ô nhiễm TỰ BẮT CHÍNH NÓ** — tên trường `official_picks_included` chứa chữ `official` (`RM-09` lần nữa) | lần chạy đầu |
| 2 | 🔴 **Idempotency trượt** — `sealed_at` nằm trong fingerprint nên `run_label` đổi mỗi lần ⇒ rows 20→40 | negative test |
| 3 | 🟠 Độ phủ candidate quá thấp vì bắt khớp cả `lag` — nới thành khớp **ô nguồn**, ghi rõ `lag_match` | quan sát |
| 4 | 🟡 **Ba phép test ĐẠT RỖNG** (B1/B2/C5) vì 02:00 MN/MT chưa xổ — ghi thẳng, không tính là đã kiểm | tự phát hiện |

---

## 5 · Cho TanPhatAI đọc tiếp

**Terminal: `ACTION_ABSTAIN_WITH_DIAGNOSTIC_RANKING` (B).** Mọi tiền đề kỹ thuật của A đều đạt,
nhưng 18/19 quyết định hợp lệ là `ABSTAIN` ⇒ nhãn trung thực là B.

**Đừng đọc «có diagnostic Top-K» thành predictive lift.** `PREDICTIVE_LIFT = NOT_PROVEN`,
`POOL_VERDICT = HOLD`.

**Đừng đọc V11177 mà bỏ qua đính chính.** Trạng thái `CONTEXT_ONLY_SHADOW_READY_FOR_NEXT_LIVE`
**đã bị hạ**.

**Row ID của V11176 là `860 / 862 / 864`**, không phải `860/861/862` — evidence JSON đúng từ đầu.

**`SC12 = CLOSED · DO_NOT_REOPEN`.**

---

TanPhatAI cần làm: ghi **`V11178`** — công khai bản này cùng `REPORT_V11178.md`. Ghi **TERMINAL `ACTION_ABSTAIN_WITH_DIAGNOSTIC_RANKING`**. Ghi **H1·H2·H3·H5·H7 CONFIRMED · H4 REFUTED · H6 PARTIAL**. Ghi **V11177 ĐÃ HẠ TRẠNG THÁI** (`RL-035`) — payload không có một giá trị quan sát nào nên `abstain` là **hệ quả cấu trúc**, không phải lựa chọn; **cách diễn giải cũ có lợi cho agent**. Ghi **V1.1 có 486 live facts + candidate derivation ánh xạ 00–99**. Ghi **roster 8 LLM từ registry, 24/24 receipt, 0 im lặng**; **99 + 15 dòng ranked**; **idempotent ĐẠT**; **discovery/holdout không chồng lấn**; **35/35 test** nhưng **3 phép đạt rỗng**. Ghi **ZERO-WRITE official xác minh, 0 restart**. Ghi **row ID V11176 đúng là 860/862/864 (`RL-036`)** và **`evaluate_all_history` xác minh đúng exit 2**. Ghi **`SC12 = CLOSED · DO_NOT_REOPEN` · `PREDICTIVE_LIFT = NOT_PROVEN` · `POOL_VERDICT = HOLD`**. **Không mở Prompt 44/FU/Plan. Không trộn ERP. Chưa sync Notion.**
