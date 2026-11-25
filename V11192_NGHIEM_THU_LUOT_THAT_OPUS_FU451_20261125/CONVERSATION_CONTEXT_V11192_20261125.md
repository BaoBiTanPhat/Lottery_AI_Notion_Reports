# CONVERSATION CONTEXT — V11192 · Nghiệm thu lượt thật 25/11, 13:37 → 18:5x ICT

## 1. Owner nói gì — nguyên văn

| giờ (ICT) | nguyên văn | loại |
|---|---|---|
| 25/11 ~13:37 | *"là sao anh nạp tiền phí phạm vậy em? Chốt lại em cần list ra việc cần anh làm , chốt. việc em xử lý ngay và việc em làm sau khi anh chốt và làm là gì liệt kê cụ thể tiếp dùm a"* | HỎI + YÊU_CẦU |

Câu này đến sau khi agent báo ở V11191 rằng DeepSeek đã có tiền nhưng vẫn không được gọi (ngoài roster).

## 2. Thứ tự thật của phiên

1. Ghi lời owner vào `docs/SO_TUONG_TAC_OWNER.md` trước (commit `3cd9943`).
2. Đo lại số dư lúc 13:38: DeepSeek 19,94 USD (nguyên vẹn), OpenRouter 6,29 USD.
3. Trả lời owner:
   - Tiền Anthropic **cần và đang dùng**: Opus là model chính ở cả 3 miền.
   - Tiền DeepSeek **chưa cần**. Danh sách sáng có ghi điều này, nhưng để ở chú thích; agent nhận lỗi trình bày.
   - Khuyến nghị giữ DeepSeek làm dự phòng, thay vào OpenRouter khi cạn.
   - Kèm danh sách A (owner) / B (agent làm ngay) / C (agent làm sau khi owner chốt), mỗi mục có khuyến nghị.
4. 18:45 — bài kiểm nền hẹn từ V11191 chạy trên VPS: FU-452 ĐẠT (MT/MB), FU-451a ĐẠT, thoát 0.
5. Đọc thêm journal để đủ điều kiện (a) của FU-451: có lại dòng `print()`.
6. Trước khi ghi sổ, tra từ vựng của `_v10958_fu_reader` ⇒ phát hiện FU-452 mồ côi do nhãn `DEPLOYED` của V11191.
7. Sao lưu, ghi bốn mặt (seq 507) + hai khối sổ theo dõi; cổng §63, sổ quyết định, số mục quản trị đều đạt.
8. Commit `15fe1c7`, đẩy lên nhánh và `master`. Viết báo cáo này.

## 3. Điều quan trọng nhất cho người đọc sau

- **Opus đã thật sự chạy lại.** Đây là bằng chứng từ dòng `predictions`, không phải từ số dư hay cổng uỷ quyền.
- **MN 25/11 chỉ 2 model AI là đúng.** Lượt MN chạy 05:15, cách ly được nhả lúc 13:17. Đừng đọc thành lỗi.
- **Nhãn trạng thái trong sổ theo dõi phải lấy từ danh sách đã khai** trong `_v10958_fu_reader.py`. Tên tầng RM-12
  (`DEPLOYED`, `RUNTIME_PROVEN`) **không** tự động là nhãn hợp lệ; chỉ `CODE_PUSHED` đã được khai.

## 4. Cổng báo cáo

Chạy sau khi đẩy báo cáo này: `_v10921_report_gate.py` ① toàn dải, rồi ② `V11192`. Kết quả ① có từ trước phiên:
39/268 bản cũ thiếu hoặc thiếu phần (mới nhất V11157). Phiên này không thêm bản thiếu nào.

## 5. Vấp ở đâu

- Trình bày danh sách sáng 25/11: việc **không** cần làm bị để ở chú thích ⇒ owner nạp tiền DeepSeek không cần thiết.
- Nhãn `DEPLOYED` ở V11191 ⇒ FU-452 mồ côi gần 6 giờ; cổng commit chỉ cảnh báo.

## 6. Điều phiên CỐ Ý không làm

- Không chạy dự đoán bù cho MN 25/11.
- Không đổi roster để đưa DeepSeek vào — chờ owner.
- Không sửa khối FU-452 cũ của V11191 — thêm khối mới phía trên.
- Không biến cảnh báo mồ côi ở cổng commit thành chặn — đó là thay đổi cổng, cần thử RM-15 riêng. Đề xuất làm cùng
  việc B `FU-457` (cổng Claude Code chạy giống Cursor); chưa ghi vào sổ theo dõi.

## 7. Câu phải nhớ khi đọc lại

> Bảng việc gửi owner phải nói thẳng cả việc KHÔNG cần làm — chú thích dưới bảng là chỗ owner không đọc tới.
