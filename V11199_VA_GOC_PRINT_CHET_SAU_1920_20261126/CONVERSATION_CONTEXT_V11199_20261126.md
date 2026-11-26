# CONVERSATION CONTEXT — V11199 · Vá gốc print chết sau 19:20, 26/11 ~12:50 → 13:40 ICT

## 1. Owner nói gì — nguyên văn

Không có lời mới. Thi hành QD-082 (26/11 ~12:0x): *«tiến hành các đề xuất an toàn trước, tuần tự , cuốn chiếu từ dễ đến khó từ
đơn giản rõ ràng đến phức tạp tra soát, soi xét kỹ lưỡng  v..v...»*.

## 2. Thứ tự thật

1. Luồng kiểm kê (bước bù 0) chỉ ra nghi vấn: v94/v95 thay `sys.stdout` lúc import; cổng V11189 mù `importlib`.
2. Agent tự kiểm: đọc mã + điểm nạp trong `scheduler.py`; đo journal 25/11 (print 0 sau 19:20); tái hiện local.
3. Quét AST cả họ: 3/11 tệp service nạp gán lúc import.
4. Vá 3 tệp + cổng; thử chặn hai chiều; bản cũ + cổng mới ⇒ bị bắt.
5. Lên VPS 13:30, không restart; hẹn kiểm 21:05. Ghi tài liệu, RL-052, commit `977273b`.

## 3. Điều quan trọng nhất cho người đọc sau

- Một cổng «ĐẠT» chỉ có giá trị bằng phạm vi nó thật sự soi. Cổng V11189 soi đúng mẫu lỗi nhưng sai TẬP tệp.
- Phép kiểm lượt thật phải phủ đúng khung giờ lỗi xảy ra (sau 19:20), không phải giờ thuận tiện (18:45).

## 4. Cổng báo cáo

Chạy sau khi đẩy: `_v10921_report_gate.py` ① rồi ② `V11199`. Lệnh ① vẫn báo các bản cũ thiếu từ trước phiên.

## 5. Vấp ở đâu

- Đếm thô 30 tệp có mẫu — phân loại AST mới ra 3 tệp thật sự nguy hiểm.

## 6. Điều CỐ Ý không làm

- Không restart (không cần, tệp chưa nạp).
- Không sửa 8 tệp gán stdout trong `__main__`/hàm (an toàn).

## 7. Câu phải nhớ

> Cấm thay `sys.stdout` lúc import ở bất kỳ tệp nào service có thể nạp — kể cả nạp bằng `importlib`.
