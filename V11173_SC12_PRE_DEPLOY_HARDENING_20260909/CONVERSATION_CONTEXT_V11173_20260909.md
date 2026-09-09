# CONVERSATION CONTEXT — V11173 · 09/09/2026

> Nguyên văn lời owner · agent làm gì · vấp ở đâu (§57.2). Giờ **Việt Nam (UTC+07:00)**.
> `CURRENT_ACTOR = CLAUDE_CODE` · **Prompt 43 R1 giữ `PARTIAL` — không mở Prompt 44.**
> **Trạng thái kết thúc: `BLOCKED_WITH_EXACT_REASONS`**

---

## 1 · Owner nói gì — NGUYÊN VĂN

| giờ ICT | NGUYÊN VĂN | loại | agent đã làm gì | trạng thái |
|---|---|---|---|---|
| ~13:00 | *«Đọc và thi hành đúng phần "MỆNH LỆNH HIỆN HÀNH · SC-12 MEASUREMENT INTEGRITY REPAIR" từ mục J đến P trong Prompt Tổng Lực Lần 43 R1»* | `YÊU_CẦU` | Tìm J–P — **không có trong kho**; hỏi owner. Owner chọn **thi hành theo phạm vi trong tin nhắn** + **viết/test giờ, deploy tối nay** | `ĐÃ_LÀM` |
| **20:05** | *«[CONTINUATION · PROMPT TỔNG LỰC 43 R1 · PHẦN Q] … DO_NOT_EXECUTE_THE_PASTED_RUNBOOK_UNCHANGED … 20:30 là earliest consideration, không phải automatic green gate»* | `YÊU_CẦU` | Q0 làm cứng runbook · Q1 receipt tươi · Q2 chứng minh cohort · Q3 cổng idle → **BLOCKED** | `ĐÃ_LÀM` |

---

## 2 · Điều đáng nói nhất — lớp phản biện chặn một báo cáo SAI

Runbook em viết ở lượt trước có bước:

```
"$PY" "$A/v11165_h12_patch.py" --cai-dat
```

**Bước đó là NO-OP.** `DICH` trỏ **chính đường dẫn của tệp**, `--cai-dat` chỉ
`io.open(DICH,"w").write(src)` — tự chép lên chính mình. **Không một dòng nào** mở `main.py` hay
`database.py`. Chính tệp đó tự khai `"trang_thai": "CANDIDATE_KHONG_DEPLOY"`.

**Nếu em chạy runbook như đã viết:** nó in `DA CHEP CANDIDATE PATCH ->` rồi **thoát 0**, em
restart dịch vụ, health 200, và **báo cáo "đã deploy VA-h12" trong khi mã production không đổi một
byte**. Kèm theo đó là một chuỗi số liệu «sau vá» hoàn toàn bịa.

**Hai góc phản biện độc lập (góc 3 và góc 4) cùng bắt được** — em thì không.

**Bài học:** *«đã có vá, 30/30 test, chờ owner ký»* trong sổ **không có nghĩa là vá cài được**.
`30/30` đó kiểm **ba hàm thuần tái dựng lại**, không kiểm bản vá thật — vì bản vá thật **không tồn
tại**. Phải mở tệp ra đọc `--cai-dat` làm gì, không tin nhãn.

---

## 3 · Điều đáng nói thứ hai — "sau 20:30" không phải cửa xanh

Em đã tính deploy sau 20:30. Prompt phần Q bắt chứng minh idle. Đo ra:

`du_doan_test_auto` có **178 mốc riêng biệt hôm nay**, **cách nhau đúng 5 phút**, từ **05:30 tới
20:15**. Quét cả ngày: **KHÔNG có khoảng trống ≥30 phút nào**. Nó **không nằm trong crontab** —
đăng ký ở `scheduler.py:7196`, tức **chạy bên trong tiến trình `lottery`** và **ghi bảng**.
`systemctl restart lottery` sẽ **giết nó giữa chừng**.

⇒ Cửa sổ khả thi duy nhất: **00:35–04:45**.

---

## 4 · Điều đáng nói thứ ba — con số đẹp sẽ KHÔNG tự xuất hiện

Bảng «gộp cả hai = 161 dòng / 86 ngày / MT 61» là **mô phỏng offline** áp logic mới cho **toàn bộ
156 ngày lịch sử**.

Production **không bao giờ làm thế**: `classify_day_status` chỉ được gọi với **`today`**
(`scheduler.py:1670/1739/1811`). Muốn số đó thành thật phải chạy
**`backfill_day_governance.py`** — tệp **có tồn tại** (1.713 byte) nhưng **runbook của em thiếu
hẳn bước này**.

⇒ Nếu deploy rồi công bố 161/86, đó là **con số sai**.

---

## 5 · Điều đáng nói thứ tư — một câu hỏi phạm vi em không được tự quyết

VA-1/VA-2 ghi **6–7 khoá mới** vào `final_bundles.source_predictions_json` và **đổi giá trị
`incomplete_bundle`**. `final_bundles` là **1 trong 4 bảng khoá**, và **"Combo/FINAL"** nằm trong
danh sách **CẤM** của SC-12.

Số dự đoán công bố **không đổi** (bầu chọn giữ nguyên) — nhưng **bản ghi bundle thì đổi**.
Hai điều này **không thể cùng đúng**. Em **không tự suy diễn là chấp nhận được**; đây là việc
owner phân xử.

---

## 6 · Vấp ở đâu

| # | vấp | ai bắt |
|---|---|---|
| 1 | 🔴 **Runbook của em có bước `--cai-dat` NO-OP** — suýt báo cáo deploy giả | **phản biện góc 3 + góc 4** |
| 2 | 🔴 Em coi "sau 20:30" là cửa khả thi | prompt phần Q + phép đo nhịp job |
| 3 | 🟠 Bản nháp V11173 viết `datetime.timezone(...)` — `daily_evaluation.py:16` chỉ có `from datetime import datetime, timedelta`, `datetime` là **lớp không phải module** ⇒ **sẽ nổ lúc chạy** | test B6 của chính em |
| 4 | 🟠 Docstring V11173 ghi **"không ghi DB"** — sai; `evaluate_day()` **ghi** `daily_eval_log` | phản biện góc 4 |
| 5 | 🟡 Ba hằng số kỳ vọng trong test sai; chú thích chứa `NOT EXISTS (` làm phép đếm tự dính | chính bộ test |

---

## 7 · Cho TanPhatAI đọc tiếp

**Đừng trích bảng «161/86/MT 61» như kết quả sẽ có sau deploy.** Đó là mô phỏng lịch sử; cần bước
backfill riêng.

**Đừng trích «VA-h12 30/30, chờ owner ký» như thể chỉ cần ký là xong.** Gói đó **chưa có installer**.

**Con số đứng vững:** V11173-r2 **43/43** trên exact current target · cohort hiện tại **270 dòng /
157 ngày** trải tới **29/03** cho một nhãn "90 ngày" · MT `wr7` đang dùng **19/06–25/06** ·
`days_back=9999` **376 → 336** (loại 40 dòng backfill) · `days_back=90` loại **0** dòng.

**Cửa sổ deploy duy nhất chứng minh được: 00:35–04:45 ICT.**

---

TanPhatAI cần làm: ghi **`V11173`** — công khai bản này cùng `REPORT_V11173.md`. Ghi **`BLOCKED_WITH_EXACT_REASONS`**, **0 deploy · 0 restart · production không đổi** (PID 3370750 · NRestarts 0 · health 200). Ghi **BLOCKER A: không có khoảng trống ≥30 phút nào trong ngày** — `du_doan_test_auto` 178 mốc cách 5 phút, chạy TRONG tiến trình `lottery` ⇒ cửa sổ duy nhất **00:35–04:45**. Ghi **BLOCKER B (P0): `v11165_h12_patch.py --cai-dat` là NO-OP tự chép chính nó, 0 dòng ghi vào `main.py`/`database.py`, tệp tự khai `CANDIDATE_KHONG_DEPLOY`** ⇒ **VA-h12 KHÔNG CÀI ĐƯỢC**; `30/30` chỉ kiểm ba hàm thuần tái dựng; khối `SAU` của VA-3 **thiếu dòng gán `reason`** ⇒ chép tay sẽ làm `classify_day_status` nổ cho cả ba miền. Ghi **agent TỰ NHẬN đã viết bước hỏng đó vào runbook; phản biện độc lập bắt được**. Ghi **số «161/86/MT 61» KHÔNG tự xuất hiện** — cần `backfill_day_governance.py`, runbook đang thiếu. Ghi **câu hỏi phạm vi CHẶN Ở OWNER: VA-1/VA-2 ghi vào `final_bundles` — bảng khoá, "FINAL" trong danh sách CẤM**. Ghi **đính chính: "không ghi DB" là SAI — `evaluate_day()` ghi `daily_eval_log`, rollback code KHÔNG hoàn tác dữ liệu**. **Không mở Prompt 44. Không mở Plan mới. Không mở FU mới. Không trộn ERP.**
