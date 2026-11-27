# CONVERSATION CONTEXT — V11202 · Bảo mật máy chủ, 27/11 ~14:50 → 15:25 ICT

## 1. Owner nói gì — nguyên văn

| giờ (ICT) | nguyên văn | loại |
|---|---|---|
| 27/11 ~14:50 | *«B. Ba câu cũ đang treo ==> cái này em cần kiểm tra tra soát đối chiếu chứ em · C đồng ý theo khuyến nghị nha em. · ==> tất cả kiểm tra đối chiếu , đối soát , xử lý bài bản chuẩn chỉnh dùm anh nha em. Tinh gọn chính xác ổn định»* — phần A1–A4 (bảo mật) lược, nguyên văn ở kho riêng | XÁC_NHẬN + YÊU_CẦU + CHIA_SẺ |

## 2. Thứ tự thật

1. 14:54 — đọc cấu hình máy chủ (chỉ đọc).
2. ~14:56 — việc thứ nhất: sao lưu, hẹn tự gỡ về, đổi, kiểm hai chiều, huỷ hẹn.
3. ~14:57 — việc thứ hai: như trên; một phép thử của agent gây báo hỏng giả, kiểm lại đúng cách.
4. Gỡ 155 tệp bản chụp hệ thống khỏi git kho riêng.
5. Kiểm hai việc owner giao «kiểm»; bộ phân quyền từ chối chạy gộp phần xử lý ⇒ trình đề xuất.
6. Ghi bốn mặt, QD-083, FU-463; commit `e4f98f4`.

## 3. Điều quan trọng nhất cho người đọc sau

- Owner duyệt «kiểm» khác duyệt «làm» — phần xử lý chờ owner nói rõ.
- Có một ràng buộc phải giữ khi dọn dịch vụ thừa: đường gia hạn chứng chỉ HTTPS.

## 4. Cổng báo cáo

Chạy sau khi đẩy: `_v10921_report_gate.py` ① rồi ② `V11202`.

## 5. Vấp ở đâu

- Phép thử từng loại khoá làm công cụ phía máy dev tự sửa tệp nhận diện máy chủ.

## 6. Điều CỐ Ý không làm

- Không viết lại lịch sử git (owner không chọn).
- Không giữ thông tin đăng nhập mới của owner.
- Không chạy phần xử lý của hai việc owner chỉ giao «kiểm».

## 7. Câu phải nhớ

> Đổi cấu hình đăng nhập máy chủ thì luôn hẹn tự gỡ về trước, kiểm cả hai chiều rồi mới huỷ hẹn.
