# CONVERSATION CONTEXT — V11177 · 10/09/2026

> Nguyên văn lời owner · agent làm gì · vấp ở đâu (§57.2). Giờ **Việt Nam (UTC+07:00)**.
> `CURRENT_ACTOR = CLAUDE_CODE` · **Prompt 43 R1 tiếp tục — không mở Prompt 44.**
> **`DEPLOY/RESTART` = 0 restart · số MN/MT/MB KHÔNG ĐỔI**

---

## 1 · Owner nói gì — NGUYÊN VĂN

| giờ ICT | NGUYÊN VĂN | loại | agent đã làm gì | trạng thái |
|---|---|---|---|---|
| **~19:45** | *«[CONTINUATION · §T] [STOP MEASUREMENT-ONLY LOOP · CLOSE SC-12 · START PREDICTIVE CHALLENGER]»* · *«Xử lý dứt điểm, không tiếp tục lề mề thăm dò đo lường mỗi ngày»* | `YÊU_CẦU` | T0 EOD · T1 vá UI · T2 backfill 48 dòng · T3 cho nghỉ · T4 fast-forward · T5 challenger chạy thật · T7 đóng | `ĐÃ_LÀM` |

---

## 2 · Điều đáng nói nhất — em SAI BA LẦN LIÊN TIẾP về cùng một ngày

Owner hỏi *«vì sao live tệ»*. Em trả lời sai **ba lần**, và cả ba đều do **dùng sai thước đo**:

**Lần 1 — `GENERATOR_MISS` cả ba miền.** Em kết luận «không đuôi trúng nào nằm trong candidate».
Sai hoàn toàn: `main_numbers` là **JSON array text**, em tách bằng dấu phẩy nên sinh token rác
`["76"`. Bằng chứng tự phản bác nằm ngay trong bảng của em: MN lô2 có trạng thái **`PARTIAL`**,
mà `82` **có** trong đuôi trúng.

**Lần 2 — `SELECTOR_MISS` cả ba miền.** Em xếp hạng bằng **đếm phiếu thô** rồi kết luận
«số trúng đứng hạng 1 mà selector chọn số khác». Nhưng hệ dùng **`weighted_voting_wr`**, và bảng
xếp đúng **nằm sẵn** trong `source_predictions_json.ranked_numbers` có score. Dùng đúng thước thì
hệ **chọn đúng #1 của chính nó** ở cả ba miền ⇒ **đổ oan cho selector**.

**Lần 3 — «20/20 điều kiện mạnh, z≈3,8».** Em vừa **tự viết cảnh báo** về bẫy n-nhỏ ở đúng đoạn
trên, rồi vẫn in ra bảng 20 điều kiện `du_manh=True`. Em đào **8.676 cell**, sắp theo z giảm dần
rồi lấy top 20 — z cao nhất trong 8.676 phép thử là **định nghĩa** của bẫy so sánh bội, không phải
bằng chứng. Sau Bonferroni (`z ≥ 4,53`): **0 điều kiện sống sót**.

**Cả ba lần đều được cứu bởi cùng một thứ: nhìn kết quả thấy vô lý thì đo lại.** Không cổng máy
nào bắt được — vì chưa có cổng nào cho «bạn đang dùng sai thước».

---

## 3 · Điều đáng nói thứ hai — câu trả lời thật cho «vì sao live tệ»

Root cause đúng: **`RANKING_MISS` cả ba** — số trúng **có** trong `ranked_numbers`, ở hạng
**2 / 4 / 3** trên 10.

Nhưng đọc `RANKING_MISS` thành *«có lỗi kỹ thuật cần vá»* là **sai**:

```
MN  ranked 10 số → 4 trúng = 40,0%   nền 40%   +0,0
MT  ranked 10 số → 4 trúng = 40,0%   nền 47%   −7,0
MB  ranked 10 số → 3 trúng = 30,0%   nền 24%   +6,0
────────────────────────────────────────────────────
    30 số        → 11 trúng = 36,7%  nền 37,0%  −0,3 điểm
```

**Bảng xếp hạng đạt đúng bằng ngẫu nhiên.** Không khiếm khuyết nào được nhận diện ngoài
*«xếp hạng không có lợi thế»*. Với **n=3** bạch thủ, ngày này **không chứng minh được gì mới**.

---

## 4 · Điều đáng nói thứ ba — challenger trả lời «không có bằng chứng», và đó là kết quả

Owner yêu cầu **dừng vòng đo lường**, dựng challenger thật. Em dựng xong và cho chạy:

```
8.676 phép thử  ·  ngưỡng Bonferroni z ≥ 4,53  ·  0 điều kiện sống sót  ·  cả BA miền
```

Model được gọi thật, trả JSON **đúng contract**, và chọn **`abstain`** với `uncertainty: high`.

**Đó là output đúng, không phải thất bại.** Với 0 điều kiện vượt nền, mọi ranked list đều sẽ là
bịa. Em cho ghi **chính cái abstain** thành bản ghi shadow, để mỗi ngày vẫn có dữ liệu đối chiếu
`CURRENT_OFFICIAL` vs `CONTEXT_ONLY_CHALLENGER`.

**Kiểm chéo ngoài dự kiến:** nền em đo lại hoàn toàn độc lập hôm nay — MN **0,4297** · MT
**0,3497** · MB **0,2365** — **khớp gần tuyệt đối** với V11170 (43,1% / 35,2% / 23,8%).

---

## 5 · Vấp ở đâu

| # | vấp | ai bắt |
|---|---|---|
| 1 | 🔴 `GENERATOR_MISS` sai — parse JSON array bằng dấu phẩy | em, khi thấy Top-K in `('["76"', 5)` |
| 2 | 🔴 `SELECTOR_MISS` sai — dùng đếm phiếu thô thay `ranked_numbers` | em, khi hỏi «hệ xếp hạng thế nào» |
| 3 | 🔴 «20 điều kiện mạnh» sai — chưa hiệu chỉnh 8.676 phép thử | em, ngay sau khi in bảng |
| 4 | 🟠 **Đoán số marker sai LẦN THỨ TƯ** (9 vs 6) — sửa tận gốc: tính từ khối vá | bộ test |
| 5 | 🟠 Preimage `\n` nhưng `du-doan.html` là **CRLF** | assert fail-closed |
| 6 | 🟡 Heredoc mangling `\r\n` — **đúng lỗi đã ghi trong bộ nhớ**, vẫn tái phạm | lỗi cú pháp |
| 7 | 🟡 Ước lượng giờ thay vì đo (tưởng 15:50, thực tế 14:37) — đã sửa thói quen | em |

---

## 6 · Cho TanPhatAI đọc tiếp

**Bốn trạng thái kết thúc, ghi riêng:** `SC12_LIVE_PATH_RUNTIME_PROVEN` ·
`SC12_HISTORICAL_REPAIR_COMPLETE` · `DEFAULT_BRANCH_STATE_CONFLICT_RESOLVED` ·
`CONTEXT_ONLY_SHADOW_READY_FOR_NEXT_LIVE`.

**Đừng đọc «SC-12 đóng» thành «hệ dự đoán tốt hơn».** `PREDICTIVE_LIFT = NOT_PROVEN`.
`POOL_VERDICT` giữ **HOLD**.

**Đừng đọc `RANKING_MISS` thành lỗi cần vá.** Ranked đạt **đúng bằng nền**.

**Đừng đọc `abstain` thành challenger hỏng.** Đó là câu trả lời trung thực khi 0/8.676 điều kiện
sống sót.

**Số dự đoán MN/MT/MB không đổi một ký tự** sau toàn bộ phiên: `95` / `34` / `01`.

---

TanPhatAI cần làm: ghi **`V11177`** — công khai bản này cùng `REPORT_V11177.md`. Ghi **bốn trạng thái kết thúc RIÊNG**: `SC12_LIVE_PATH_RUNTIME_PROVEN` · `SC12_HISTORICAL_REPAIR_COMPLETE` · `DEFAULT_BRANCH_STATE_CONFLICT_RESOLVED` · `CONTEXT_ONLY_SHADOW_READY_FOR_NEXT_LIVE`. Ghi **10/09 THUA cả ba bạch thủ** (`95`/`34`/`01`), **lô2 MN PARTIAL** (`82`); root cause **`RANKING_MISS` cả ba** (số trúng hạng 2/4/3 trên 10, hệ chọn đúng #1 của chính nó). Ghi **ranked 36,7% vs nền 37,0% = −0,3 điểm — ĐÚNG BẰNG NGẪU NHIÊN**, n=3 nên **chưa được phép kết luận**. Ghi **UI sạch**: `76599f6a`→`23f1ca69`, **10/10 assertion JS thật trên bytes đang phục vụ**, **0 restart**. Ghi **backfill đúng 48 dòng**, `MT EXCLUDE_PRIMARY` **98→50**, digest lịch sử **không đổi**; **cohort sạch cho tin xấu**: `wr7` MT **14,3%** vs nền **35,2%**, và **dự báo `→0,0%` trong sổ cũng sai**. Ghi **`evaluate_all_history` = `RETIRED_FAIL_CLOSED`**. Ghi **`master` fast-forward `a4d6636`→`d2a6586`, không force**. Ghi **challenger chạy thật, cron 13:30, 8.676 phép thử, ngưỡng Bonferroni z≥4,53, 0 điều kiện sống sót cả ba miền ⇒ `abstain` là output ĐÚNG**. Ghi **nền đo độc lập khớp V11170**. Ghi **`PREDICTIVE_LIFT = NOT_PROVEN`, `POOL_VERDICT` HOLD**. Ghi **agent sai BA LẦN LIÊN TIẾP về cùng một ngày, cả ba do dùng SAI THƯỚC ĐO**. **Không mở Prompt 44. Không mở Plan mới. Không mở FU mới. Không trộn ERP.**
