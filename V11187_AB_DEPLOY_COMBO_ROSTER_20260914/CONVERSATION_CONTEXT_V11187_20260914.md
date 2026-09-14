# CONVERSATION CONTEXT — V11187 · deploy gói §AB, 14/09/2026 chiều–tối

## 1. Owner nói gì — nguyên văn

**Không có yêu cầu mới trong đoạn phiên này.** Toàn bộ việc làm theo hai câu Owner đã khoá ở §AB:

> *"Nếu không hoàn tất trước 03:30: giữ một epoch V11185 cho trọn ngày 14/09; next action duy
> nhất là thu actual Combo call receipt; deploy bản hoàn chỉnh sau EOD; không mở nhánh công việc
> khác."* (§AB-V)

> *"Cấm: deploy giữa cascade; MN một version, MT/MB version khác; restart khi provider job đang
> chạy; backdate config; ép xanh để kịp giờ."* (§AB-J)

---

## 2. Chuyện gì đã xảy ra, theo thứ tự thật

| giờ (VN) | việc |
|---|---|
| ~13:00 | Đóng nốt cổng báo cáo V11186 (thiếu mục *"owner yêu cầu (nguyên văn)"*) |
| ~13:20 | Phát hiện **đường gỡ về §15 tôi tự công bố KHÔNG chạy được** — `backups/` không tồn tại trên VPS |
| ~13:30 | Vá CẤP 2: hạn 24 h + ALERT (`_v11186_thu_khan_cap.py` 45/45); lập 5 tệp backup CẤP 1, sha khớp |
| ~13:46 | Preflight lần 1 ⇒ **NO_GO** (C1 đồng hồ · C2 epoch chưa khép · C4 thiếu receipt) |
| 16:47 | Receipt **MT `OK` 10/10** |
| 17:36 | Receipt **MB `FAIL` 8/10** — `gemini-2.5-pro` ngoài roster chạm HTTP |
| 17:40–18:20 | Truy nguồn: loại rerun, loại diversity pass, quy về **Combo Super** bằng lồng thời gian |
| ~18:30 | Thử ngược **chính sự cố thật** trên mã đã vá ⇒ **17/17** |
| 20:05 | Preflight lần 2 ⇒ **GO** cả 7 phép |
| 20:06 | Chép 8 tệp, sha khớp cả 8, `CR=0` |
| 20:06 | Bộ thử **trên VPS trước restart**: 102/102 · 45/45 · 17/17 · 45/45 · 65/65 |
| 20:07 | **Restart: PID 97754 → 169960**, health 200 |
| 20:07 | Xác minh sau restart: 0 traceback · 4 bảng khoá y nguyên · crontab không đổi |
| 20:08 | Đặt bộ thu receipt ba miền cho 15/09 (PID 170282) |

---

## 3. Điều quan trọng nhất cho người đọc sau

**Ngày 14/09 đã cho một phản chứng sống, và nó tới TRƯỚC khi bản vá kịp deploy.**

Buổi trưa tôi viết trong V11186: *"bundle 14/09 MN có 0 model ngoài roster ⇒ cổng scheduler §AA
đã đóng đường chính trên thực tế. Cái còn hở là **cấu trúc**: pool riêng của Combo vẫn chứa 4
model không được phép. Hôm nay không dùng tới, **nhưng 'hôm nay không dùng' ≠ 'không thể dùng'**."*

Đến 17:33 chiều cùng ngày, nó **dùng tới**. Đúng model đó, đúng đường đó.

Điều này nói hai chuyện trái nhau mà cả hai đều đúng:
- Câu cảnh báo buổi trưa **đúng**, và đúng nhanh hơn tôi tưởng.
- Câu *"MN sạch"* buổi trưa là **may**, không phải nhờ cổng — Combo ở MN cũng gọi ngoài kiểm
  soát, chỉ tình cờ bốc trúng một model nằm trong roster MN. Nếu hôm đó nó bốc `gemini-2.5-pro`
  thì MN đã FAIL từ 05:17 và bức tranh cả ngày đã khác.

---

## 4. Vấp ở đâu

### 4.1 Tôi suýt ép một giả thuyết đúng bằng bằng chứng sai

Nghi Combo từ sớm, đi tìm dòng in `🎛️ [UNIFIED]` / `🏆 Selected` của chính nó. **Không có dòng
nào** — journal lẫn mọi `*.log`. Nếu coi "không tìm thấy" là "đã loại", tôi đã bỏ qua thủ phạm
đúng và đi tìm một đường không tồn tại.

Phải đổi sang nguồn khác: `scheduler_logs` ghi mốc đầu/cuối Combo bằng `_add_log` (ghi DB), khác
hẳn `print()` (ra stdout, có thể bị đệm). *Vắng bằng chứng không phải bằng chứng vắng mặt.*

### 4.2 Dấu vân tay tôi tưởng mạnh, hoá ra yếu

Lượt rogue có `runtime_prompt_chars` **22.933** so với **24,7k–25,0k** của bốn model roster. Tôi
đọc ngay thành *"đường dựng prompt khác"*. So bộ khoá trace hai dòng thì **giống hệt** — cùng
`analyze_and_predict` — và chênh lệch giải thích được bằng `selected_source_prizes` (4 prize vs
5). Đã hạ nó xuống đúng vai: **gợi ý**, không phải bằng chứng. Bằng chứng thật là lồng thời gian.

### 4.3 RM-10 chặn hai lần, cả hai đều trước khi viết kết luận

- `scheduler_logs` **không có cột `status`** — nên tín hiệu "job đang bay" của preflight phải lấy
  từ độ im lặng của trace, không từ một cột không tồn tại.
- `predictions` **không có cột `model_name`** (là `ai_model`).
- Và một lần nữa ở tên endpoint: `/api/admin/stats` tôi đoán ⇒ **404**. Phép smoke đúng là
  `/monitoring` = **401**.

### 4.4 §55 suýt phá toàn bộ phép lồng thời gian

`scheduler_logs.log_time` là naive **và là UTC**. Đọc thẳng sẽ lệch 7 giờ, mọi cửa sổ Combo sẽ
trượt khỏi mọi lượt gọi, và tôi sẽ kết luận *"không lượt nào thuộc Combo"* — ngược hẳn sự thật.

### 4.5 Ba lần escape/quoting cắn

- `grep -c` với mẫu CR viết bằng escape shell ⇒ đếm **chữ cái `r`**, báo `CR=2804` cho tệp thật
  có `CR=0`.
- Chính dòng ghi lại điều đó **bị escape CR trong heredoc cắt cụt** trong báo cáo công khai — tôi
  đã có ghi nhớ đúng về bẫy này và vẫn vấp.
- Lệnh kiểm sau deploy vỡ vì `grep -vcE` lồng trong ssh. Làm lại bằng script trên máy đích.

### 4.6 Cổng báo cáo từng báo xanh cho một thứ không tồn tại

Bản đầu V11186 qua cổng §57.3 nhờ **tai nạn**: cổng đọc dòng `#` trong khối code như tiêu đề, và
dòng chú thích bash `# Sau khi deploy (15/09)…` đã khớp hộ phần *"đã làm gì"*. Viết lại §15 làm
dòng đó biến mất ⇒ cổng lập tức báo thiếu. Báo cáo khi ấy **thật sự thiếu**.

---

## 5. Điều phiên CỐ Ý không làm

| việc | không làm vì |
|---|---|
| Gỡ về CẤP 1 hoặc CẤP 2 | Lỗi thuộc **V11185**; gỡ về CẤP 2 đưa ngược về 8 model — mở rộng đúng thứ đang rò |
| Deploy sớm hơn 17:33 | §AB-J cấm chẻ epoch; MN/MT đã chạy dưới V11185 |
| Gọi provider tay để kiểm nhanh | §AB-K cấm. Mọi receipt từ lượt **tự nhiên** |
| Override lineage · family lineage · retrain atomic | §AB-U: P0 chưa đóng thì không mở việc nghiên cứu khác |
| Pure-context | §AB-Q: chỉ sau `ROSTER_SYSTEM_WIDE_LIVE_PROOF_OK` — hôm nay là `FAIL` |
| Sửa cổng `_v10921_report_gate` | Là nhánh công việc khác; đã ghi vào §9 mục 9, **không mở FU mới** theo khoá §AB |
| Bù 39/263 bản thiếu báo cáo | Tồn đọng lịch sử, không sinh từ phiên này; mở ra là nhánh mới |

---

## 6. Câu phải nhớ khi đọc lại

**Deploy không phải chứng minh.** Terminal hôm nay là `DEPLOYED_PENDING_NATURAL_PROOF`. Bản vá đã
được thử ngược trên chính sự cố thật và đạt 17/17 — nhưng đó vẫn là **mã trên đĩa**, không phải
**lượt chạy thật**. Câu trả lời runtime chỉ có sau ba lượt tự nhiên ngày 15/09, và khi ấy trace
sẽ mang `caller` + `execution_class` + `request_fingerprint` để câu hỏi "ai gọi" **tự trả lời**
thay vì phải suy từ lồng thời gian.
