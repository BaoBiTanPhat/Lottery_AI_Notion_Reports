# CONVERSATION CONTEXT — V11174 · 10/09/2026

> Nguyên văn lời owner · agent làm gì · vấp ở đâu (§57.2). Giờ **Việt Nam (UTC+07:00)**.
> `CURRENT_ACTOR = CLAUDE_CODE` · **Prompt 43 R1 giữ `PARTIAL` — không mở Prompt 44.**
> **Trạng thái kết thúc: SC-12 `DEPLOYED_PENDING_SCHEDULED_PROOF` · Pure Context `PURE_CONTEXT_PARTIAL`**

---

## 1 · Owner nói gì — NGUYÊN VĂN

| giờ ICT | NGUYÊN VĂN | loại | agent đã làm gì | trạng thái |
|---|---|---|---|---|
| 09/09 ~21:00 | *«Làm gì tiếp theo em đã đề xuất và tổng hợp báo cáo đầy đủ lên github chưa em»* | `HỎI` | Kiểm bằng lệnh, không bằng trí nhớ: xác nhận V11173 đã push cả hai kho; trình bảng việc kế tiếp | `ĐÃ_LÀM` |
| **10/09 ~01:45** | *«[CONTINUATION · PROMPT TỔNG LỰC LẦN 43 R1 · §R] [SC-12 CLOSURE + FULL-SYSTEM AMBIGUITY/DEBT AUDIT + PURE-CONTEXT COMPLETION PLAN]»* — kèm khoá mới **`FINAL_BUNDLES_ZERO_WRITE`** và *«Không hỏi Owner câu mơ hồ như "có cho ghi final_bundles không?"»* | `YÊU_CẦU` | R0 chụp trạng thái → R1 viết installer THẬT → R2/R3 test → R4 dry-run backfill → R5 **13/13 cổng** → **DEPLOY 02:00:19** → R5.7 receipt. **R6/R7/R8 KHÔNG làm** — báo thẳng | `ĐÃ_LÀM (một phần, khai báo rõ phần không làm)` |

---

## 2 · Điều đáng nói nhất — khoá `FINAL_BUNDLES_ZERO_WRITE` không chặn việc, nó **mở** việc

Hôm 09/09 em treo một câu hỏi phạm vi: *«VA-1/VA-2 ghi 6–7 khoá mới vào `final_bundles` —
có nằm trong phạm vi SC-12 không?»* và dừng lại chờ owner.

§R trả lời bằng **một khoá cấm**, đồng thời **cấm em hỏi lại câu đó**. Nghe như bế tắc.
Nhưng khi đi đọc dữ liệu thật thay vì đọc thiết kế cũ, em thấy:

**Cái metadata mà VA-2 muốn GHI — nó ĐÃ CÓ SẴN TRONG DB.**

```
MT 2026-09-08 → model_exclusion_reasons có reason='max_voters_cap'
              → ['claude-opus-4-6', 'claude-sonnet-4-6']
MT 2026-09-06 → ['meta-learning', 'smart-ensemble']      ← đổi theo ngày, không phải hằng số
MN 2026-09-08 → []                                        ← miền không bị trần thì rỗng
```

⇒ **Không cần ghi gì cả. Chỉ cần ĐỌC cái đã có.** VA-1 và VA-2 — hai mảnh duy nhất chạm
`final_bundles` — **bị bỏ hẳn**, thay bằng **VA-2′ sửa phía ĐỌC** ở `main.py:489`.

**Bài học:** một khoá cấm phạm vi buộc em đi đọc **dữ liệu thật** thay vì đi theo **thiết kế đã
viết sẵn** — và thiết kế đó hoá ra thừa. Nếu owner cho phép ghi, em đã ghi trùng cái đang có.

---

## 3 · Điều đáng nói thứ hai — hai tiêu chí idle của chính em đã SAI

Đêm qua em báo *«WAL/SHM tồn đọng ⇒ có writer»* và tính retrain là job **hằng đêm 02:00**.
Đo lại đêm nay:

| em từng nói | sự thật đo được |
|---|---|
| `-shm` 32 KB ⇒ có writer | `-shm` **luôn tồn tại** khi có kết nối mở. Tiêu chí đúng là **WAL size > 0** — và WAL đang **0 byte** |
| Auto Retrain 02:00 hằng đêm | journal ghi rõ **`🧠 Auto Retrain (sun 02:00)`** — **`day_of_week=sun`**. Hôm nay **Thứ Năm** ⇒ không chạy |

Nếu giữ hai tiêu chí sai đó, em đã **tự chặn mình khỏi cửa sổ 02:00 hợp lệ** và lại báo BLOCKED
lần thứ hai — một `BLOCKED` **sai**, cũng tai hại như một `PASS` sai.

---

## 4 · Điều đáng nói thứ ba — vá KHÔNG tẩy trắng, và em đi tìm bằng chứng cho điều đó

Một vá kiểu «cộng thêm số model bị trần» rất dễ trở thành **máy tẩy trắng**: mọi ngày thiếu đều
thành đủ. Nên em không tự nhận, em đi **tìm ca ngược lại** trong dry-run:

```
2026-07-25 MT   model_count=11 + cap=2 = 13   <  15   → VẪN EXCLUDE_PRIMARY
```

Đây là ngày thiếu hụt **thật**, ngoài phần bị trần — và vá **giữ nguyên** phán quyết loại trừ.
48 ngày đổi sang `INCLUDE` đều là `13+2=15`, **đúng đủ**, không dư một ca nào.

---

## 5 · Điều đáng nói thứ tư — lệch +1 mà em KHÔNG ép cho khớp

Dry-run ra **49 ngày đổi**. Sổ ghi mốc **45**. Phân rã:

```
46  (tính đến 04/09, cùng mốc với phép đo cũ)
+3  (05/09, 06/09, 08/09 — ngày mới, giải thích được)
──
49
```

**+3 giải thích được. +1 thì không.** Cùng một mốc 04/09 mà em ra 46, sổ ghi 45. Nặng hơn:
**`RL-014` chính là mục đã rút lại đúng con số này** (46 → 45). Em **không có script gốc** để tái
lập nên **không biết bên nào đúng**.

Em ghi **`INDETERMINATE`** và **không sửa số cho khớp**. Đây đúng chỗ `RM-11`/`RM-17` cảnh báo:
số không tái lập được thì **cấm dùng làm căn cứ**, và cũng **cấm làm nó biến mất**.

---

## 6 · Vấp ở đâu

| # | vấp | ai bắt |
|---|---|---|
| 1 | 🔴 Em đoán **số marker kỳ vọng bằng tay — SAI BA LẦN** (5 vs 3; rồi 6/3 vs 3/1). Sửa tận gốc: **tính số marker từ chính khối vá** (`_so_marker_du_kien()`), không hardcode | bộ test của chính em |
| 2 | 🟠 `_chay.py` chép script sang `artifacts/_run_<tên>.py` ⇒ installer **không nằm ở đường dẫn chuẩn**, bước 1 deploy im lặng báo "No such file" | bước deploy |
| 3 | 🟠 `health: 000` ngay sau restart — app **chưa kịp bind cổng 8000** sau 6 giây. Poll tiếp: **200 lúc 02:00:42**; journal xác nhận `Uvicorn running` lúc 02:00:25 | smoke test |
| 4 | 🟡 Chú thích của em chứa `NOT EXISTS (` làm phép đếm tự dính (đếm 2 thay vì 1) | bộ test |
| 5 | 🟡 Thông điệp commit có dấu nháy làm vỡ shell (`pathspec '0.2310,'`) ⇒ chuyển sang `git commit -F` | shell |

---

## 7 · Cho TanPhatAI đọc tiếp — điều QUAN TRỌNG NHẤT

🔴 **Phiên này KHÔNG làm R6, R7, R8.** Không audit tổng lực nợ; không lập condition ledger
pure-context; không lập Improvement Candidate Register.

**Đừng đọc "13/13 cổng PASS" thành "đã kiểm tra toàn bộ hệ thống".** 13 cổng đó chỉ nói về
**một lần deploy**.

**Đừng đọc `DEPLOYED_PENDING_SCHEDULED_PROOF` thành `SC12_RUNTIME_PROVEN`.** Chưa có bằng chứng
runtime nào. `day_governance` vẫn **581 dòng**, `classified_at` mới nhất vẫn là
**09/09 18:32:34** — tức `auto_verify` **chưa chạy lần nào** sau deploy.

**Đừng gộp SC-12 với Pure Context.** Hai trạng thái, hai dòng riêng.

**Đừng coi đây là cải thiện chất lượng dự đoán.** Đây là **sửa phép đo** và **tăng độ tin cậy**.
Kết luận V11170 *«hệ không hơn ngẫu nhiên»* **vẫn đứng nguyên** — phiên này không đo lại nó.

**Con số đứng vững:** V11174 **58/58** · V11173 **43/43** sau tích hợp · dry-run **49 ngày, tất cả
MT** · `final_bundles` **582 dòng, digest `396c7559…` không đổi** · `output_counterfactual_rank`
**0 ghi** · **DB MUTATIONS = 0**.

---

TanPhatAI cần làm: ghi **`V11174`** — công khai bản này cùng `REPORT_V11174.md`. Ghi **SC-12 = `DEPLOYED_PENDING_SCHEDULED_PROOF`** và **Pure Context = `PURE_CONTEXT_PARTIAL`** — **hai dòng riêng, cấm gộp**. Ghi **deploy 02:00:19 ICT 10/09, PID 3370750 → 3870722, NRestarts 0→0, health 200, journal 0 lỗi, DB MUTATIONS = 0, 13/13 cổng PASS**. Ghi **blocker P0 «VA-h12 không có installer thật» ĐÃ ĐÓNG** bằng `v11174_vah12_zerowrite_installer.py` (58/58, test gọi hàm production thật trên DB thật). Ghi **VA-1/VA-2 bị BỎ HẲN** vì chúng ghi `final_bundles` — vi phạm khoá `FINAL_BUNDLES_ZERO_WRITE`; **bằng chứng cho phép bỏ: `model_exclusion_reasons` ĐÃ ghi sẵn `reason='max_voters_cap'`**, chỉ cần ĐỌC. Ghi **vá KHÔNG tẩy trắng**: 25/07 MT `11+2=13` vẫn `EXCLUDE_PRIMARY`. Ghi **dry-run 49 ngày = 46 (đến 04/09) + 3 ngày mới; +1 lệch so với mốc 45 là `INDETERMINATE`, xung đột `RL-014`, KHÔNG ép số**. Ghi **hai tiêu chí idle cũ của agent là SAI đã sửa**: retrain là `day_of_week=sun`; tiêu chí đúng là **WAL size > 0**. Ghi **`evaluate_all_history` CÔ LẬP THẬT** — chỉ trong `__main__` dưới `--backfill`, 0 cron 0 route. Ghi **R6 · R7 · R8 KHÔNG THỰC HIỆN trong phiên này** — agent **không tuyên bố "đã kiểm tra toàn bộ"**. Ghi **backfill lịch sử CHƯA chạy, mới dry-run** — 49 dòng MT vẫn `EXCLUDE_PRIMARY`. Ghi **việc kế tiếp DUY NHẤT: chờ `auto_verify` 16:37–18:34 hôm nay rồi thu bằng chứng runtime**. **Không mở Prompt 44. Không mở Plan mới. Không mở FU mới. Không trộn ERP.**
