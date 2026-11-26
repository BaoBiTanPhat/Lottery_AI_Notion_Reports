# CONVERSATION CONTEXT — V11196 · Dọn dẹp cuốn chiếu Đợt 1, 26/11 ~11:47 → 12:12 ICT

## 1. Owner nói gì — nguyên văn

| giờ (ICT) | nguyên văn | loại |
|---|---|---|
| 26/11 ~11:47 | *«kiểm xong chưa tiến hành dọn dẹp được chưa ? chờ  anh chốt vấn đề gì?»* | HỎI |
| 26/11 ~12:0x | *«tiến hành các đề xuất an toàn trước, tuần tự , cuốn chiếu từ dễ đến khó từ đơn giản rõ ràng đến phức tạp tra soát, soi xét kỹ lưỡng  v..v...»* | YÊU_CẦU |

## 2. Thứ tự thật của phiên

1. 11:47 — trả lời tiến độ thật của luồng kiểm kê (8/8 kiểm kê, 4/8 phản biện) và danh sách câu chờ owner.
2. 12:0x — ghi lời owner; kiểm luồng: 16/17 tác tử xong, còn «soát thiếu».
3. Đọc phản biện mặt lịch chạy (giữ 25 · hạ mức 10 · bác 1), chọn 5 dòng rõ ràng nhất.
4. Soát sổ quyết định + cổng + route: rút `_v10869` (panel phụ thuộc theo ngày). Còn 4 dòng.
5. Tự grep người đọc trên VPS — chỉ chính tệp.
6. `_v11067 --doc` lấy tổng kết FU-402.
7. Script dừng: thử (diff 4 dòng) → cài → kiểm (86 dòng, 162 dòng khác y hệt) → chạy lại thì script từ chối.
8. Ghi bốn mặt (seq 511), FU-462, FU-402, QD-082. Commit `589487f`.

## 3. Điều quan trọng nhất cho người đọc sau

- Dọn dẹp đi theo **đợt nhỏ**; đợt sau chỉ mở khi đợt trước đã kiểm xong (FU-462).
- **Dừng lịch ≠ xoá**: bảng, tệp, log của 4 job còn nguyên; bật lại bằng cách bỏ tiền tố `# V11196 DỪNG … |`.
- Phản biện đã bác/hạ mức nhiều đề xuất «an toàn» bề ngoài — đọc `REPORT_V11196.md` §3 trước khi đề xuất dừng thêm.

## 4. Cổng báo cáo

Chạy sau khi đẩy báo cáo này: `_v10921_report_gate.py` ① toàn dải rồi ② `V11196`. Lệnh ① vẫn báo các bản cũ thiếu báo
cáo từ trước; phiên này không thêm bản thiếu.

## 5. Vấp ở đâu

- Suýt đưa `_v10869` vào Đợt 1 dù panel của nó đọc bảng theo ngày.

## 6. Điều phiên CỐ Ý không làm

- Không dừng các phép đo đã quá hạn khi chưa ghi phán quyết cuối (để Đợt 2).
- Không đụng các đề xuất người phản biện bác/hạ mức.
- Không xoá bảng, tệp, log; không restart.

## 7. Câu phải nhớ khi đọc lại

> Một dòng cron chỉ được dừng khi đầu ra của nó không ai đọc — kiểm bằng grep toàn bộ mã sống trên máy chủ, không bằng tên.
