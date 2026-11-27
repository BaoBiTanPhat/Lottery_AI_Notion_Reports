# CONVERSATION CONTEXT — V11209 · Tính bù scorecard · kiểm sau triển khai · lane rc≠0, 27/11 ~18:50 → 22:20 ICT

## 1. Owner nói gì — nguyên văn

| giờ (ICT) | nguyên văn | loại |
|---|---|---|
| 27/11 ~14:50 | *«B. Ba câu cũ đang treo ==> cái này em cần kiểm tra tra soát đối chiếu chứ em»* | YÊU_CẦU |
| 27/11 ~17:50 | *«OK ANH DUYỆT THEO KHUYẾN NGHỊ EM. EM TIẾN HÀNH XỬ LÝ HOÀN TẤT DỨT ĐIỂM SẠCH SẺ DÙM ANH»* | XÁC_NHẬN + YÊU_CẦU |

Trong khoảng 18:50 → 22:20 owner không nói thêm; agent làm tiếp phần đã duyệt.

## 2. Thứ tự thật

1. 18:50 — đọc kết quả kiểm sau triển khai V11204: ba miền «ĐÃ XONG» đúng giờ, MT ghi `rc=1`.
2. Tra lịch sử rc=1 ⇒ lỗi cũ (21 lần từ 08/08), cả 21 ngày vẫn có số Nghiệm Thu.
3. 22:08 — kiểm vùng tính bù trống, không job nặng đang chạy, script trên VPS trùng sha máy dev ⇒ băm 4 bảng ⇒ chạy tính bù ⇒ băm lại ⇒ đọc lại.
4. Đọc mã lane: chết trước dòng in đầu, lỗi bị hàm gọi bỏ ⇒ sửa hàm gọi giữ lỗi; thử 3 ca hai nơi; đẩy VPS.
5. Ghi bốn mặt (seq 523) ⇒ commit `40515ea` ⇒ đẩy nhánh + `master`.

## 3. Điều quan trọng nhất cho người đọc sau

- Bảng xét thăng hạng shadow nay đủ ngày. Mọi dòng tính bù mang nhãn — đếm hay gỡ đều theo nhãn.
- **Chưa biết nguyên nhân rc=1.** Bản vá chỉ để lần sau lỗi tự khai ra. Đừng cắt 8 lượt predraw trước khi đọc được `· ERR:`.

## 4. Cổng báo cáo

Chạy sau khi đẩy: `_v10921_report_gate.py` ① toàn dải rồi ② `V11209`.

## 5. Vấp ở đâu

- Đoán tên cột (`model_id`) — sai, tên thật `ai_model` (RM-10).
- Bài thử máy dev hỏng một ca vì lane giả in tiếng Việt ra console cp1252 — lỗi bài thử, sửa bài thử.
- Ghi giờ ước vào tài liệu trước khi xem đồng hồ — sửa trước commit.

## 6. Điều CỐ Ý không làm

- Không gọi lại lane Nghiệm Thu thật để «tái hiện» rc=1: lượt gọi tối nay sẽ chốt sớm số ngày mai và làm lệch phép đo của lane.
- Không tăng thời gian chờ khoá DB theo giả thuyết chưa chứng minh.
- Không restart service — không cần.

## 7. Câu phải nhớ

> Hai mươi mốt lần lỗi mà không lần nào để lại nguyên nhân — lỗi bị nuốt thì không đếm được thành bài học.
