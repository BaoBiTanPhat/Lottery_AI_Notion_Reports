# CONVERSATION CONTEXT — V11198 · Dọn dẹp Đợt 0b, 26/11 12:28 → 12:40 ICT

## 1. Owner nói gì — nguyên văn

Không có lời mới. Đợt 0b thi hành tiếp QD-082: *«tiến hành các đề xuất an toàn trước, tuần tự , cuốn chiếu từ dễ đến khó từ đơn
giản rõ ràng đến phức tạp tra soát, soi xét kỹ lưỡng  v..v...»* (26/11 ~12:0x).

## 2. Thứ tự thật

1. Đọc kết quả bước soát thiếu của luồng kiểm kê: thiếu bản sao 76 ngày · bản DB để hở trong `/tmp` · QD-082 ↔ QD-058.
2. Đọc QD-058: lời owner «đừng đi lùi» — câu «cấm tắt mọi cơ chế» là diễn giải của agent. Ghi thay thế một phần, hai chiều.
3. Đọc mã công cụ đồng bộ rồi chạy (12:32 → 12:34).
4. Soi quyền 4 bản DB; khoá bản trong `/tmp`.
5. Kiểm lại sổ quyết định trên dữ liệu mới: 0 TRÔI, 0 «không kết luận được».
6. Ghi tài liệu, commit `a634502`.

## 3. Điều quan trọng nhất cho người đọc sau

- Từ 12:34 ngày 26/11 có bản sao production ngoài VPS. Trước đó 76 ngày không có.
- Hệ chưa có lịch sao lưu định kỳ ngoài VPS — cần owner chốt tần suất.

## 4. Cổng báo cáo

Chạy sau khi đẩy: `_v10921_report_gate.py` ① rồi ② `V11198`. Lệnh ① vẫn báo các bản cũ thiếu từ trước phiên.

## 5. Vấp ở đâu

- Manifest có địa chỉ máy chủ — công bố bản đã ẩn.

## 6. Điều CỐ Ý không làm

- Không xoá bản sao DB cũ nào (đợt lưu trữ, cần owner).
- Không đổi cấu hình máy chủ (cần owner).

## 7. Câu phải nhớ

> Dọn dẹp bắt đầu bằng sao lưu: chưa có bản sao thì chưa được bỏ bất cứ thứ gì.
