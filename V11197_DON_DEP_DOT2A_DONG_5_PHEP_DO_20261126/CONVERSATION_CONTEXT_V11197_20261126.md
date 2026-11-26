# CONVERSATION CONTEXT — V11197 · Dọn dẹp Đợt 2a, 26/11 ~12:35 → ~13:10 ICT

## 1. Owner nói gì — nguyên văn

Không có lời mới trong đợt này. Đợt 2a thi hành tiếp lời owner 26/11 ~12:0x: *«tiến hành các đề xuất an toàn trước, tuần tự ,
cuốn chiếu từ dễ đến khó từ đơn giản rõ ràng đến phức tạp tra soát, soi xét kỹ lưỡng  v..v...»* (QD-082).

## 2. Thứ tự thật

1. Lấy dòng cron + đường log của 15 script «phép đo quá ngày đọc» mà người phản biện để «giữ đề xuất».
2. Soi bảng ghi và người đọc (script `doc_ghi_dot2.py`); xác minh panel builder của cụm `/choi` chỉ do route panel gọi.
3. Đọc khối cuối log 15 script: 5 phép đo có phán quyết rõ; 5 phép đo tháng 7 không in phán quyết; cụm `/choi` có số hứa
   hẹn chưa đo đúng.
4. Kiểm sổ quyết định: QD-024 có kiem_code nhắc FU-264 — vẫn đạt sau khi dừng.
5. Dừng 5 dòng (thử → cài), ghi sổ, commit `d81e7b6`.

## 3. Điều quan trọng nhất cho người đọc sau

- Năm phép đo này đã «chờ» trong sổ 3–4 tháng sau ngày đọc dù log có kết quả mỗi tối — sổ treo vì không ai đọc log.
- Cụm nghiên cứu `/choi` **không phải rác**: có cách «hơn official» trên giấy ở MT/MB. Phải đo đúng trước khi quyết.

## 4. Cổng báo cáo

Chạy sau khi đẩy báo cáo này: `_v10921_report_gate.py` ① rồi ② `V11197`. Lệnh ① vẫn báo các bản cũ thiếu từ trước phiên.

## 5. Vấp ở đâu

- Dương giả «ghi `lottery_results`» của bộ quét — bảng tạm trong bài thử của chính script.
- Suýt xếp cụm `/choi` vào việc dễ.

## 6. Điều CỐ Ý không làm

- Không dừng phép đo nào chưa có phán quyết ghi sổ.
- Không dừng FU-394, anti-trap, D-30 (cần owner hoặc QD mới).
- Không sửa giao diện panel (thay đổi UI cần owner duyệt bản demo trước).

## 7. Câu phải nhớ

> Đóng một phép đo = ghi phán quyết theo đúng ngưỡng đã đăng ký, rồi mới dừng lịch. Không có phán quyết thì chưa được dừng.
