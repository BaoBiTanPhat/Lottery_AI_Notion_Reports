# CONVERSATION CONTEXT — V11190 · Đối chiếu tổng lực, 24/11/2026 23:44 → 25/11 00:2x ICT

## 1. Owner nói gì — nguyên văn

| giờ (ICT) | nguyên văn | loại |
|---|---|---|
| 24/11 ~23:44 | *"trước đó nhiều đo lương , báo cáo  có trong root, trong thư mục tạm của cursor và cả github report em đã xem hết chưa kiểm tra so sánh đối chiếu tổng lực toàn diện chưa? - theo hình menu bảng chơi nay ổn nhỉ, các ngày trước thì sao , còn menu " dự đoán thì sao? chúng ta đang chơi ở menu nào em? các việc cần anh chưa rõ, 1/ em xác dịnh dang thiếu model nào API hãng hay dùng qua openrouter, 2 , 3 thực sự chưa hiểu đang nói gì ngắn gọn quá"* — kèm ảnh `/choi` (24/11 tối) và `/du-doan` MT | HỎI + YÊU_CẦU |

Owner không trả lời giữa phiên. Mọi việc cần quyết được **trình**, không tự làm.

## 2. Thứ tự thật của phiên

1. Trả lời thẳng: V11189 **chưa** đối chiếu báo cáo cũ.
2. Kiểm kê `reports/`, `~/.cursor/{plans,projects}`, log tạm Cursor (chỉ IDE mở kho), GitHub 467 thư mục.
3. Lọc sổ theo dõi bằng máy: 202 treo, 58 chờ dữ liệu sống. Phát hiện `NEXT_ACTION.md` báo «0 quá hạn».
4. Kiểm `PRAGMA journal_mode` = WAL (đọc song song an toàn — bài học FU-403), rồi giao 3 agent CHỈ ĐỌC.
5. Trong lúc chờ: tra `/choi` là bảng chơi (SSOT V10776); viết phép đo P&L cùng thước; **phát hiện khuyến nghị ghi
   sau giờ xổ** từ kết quả quá đẹp (z +2,18) ⇒ kiểm giờ ghi ⇒ 100% sau 18:30 ⇒ 23/23 ngày NGHỈ đều trượt.
6. Đường gọi model + số dư (OpenRouter 6,29 USD — đo tốc độ tiêu trước khi báo động).
7. Phát hiện pool combo 9 không phải 7 ⇒ `RL-048`.
8. Nhận kết quả 3 agent; tự kiểm lại phát hiện nặng (lane test PENDING, rò DO_TIEN, FU-318, hook 9 vs 10).
9. Tái lập FU-284 ⇒ `RL-049`.
10. Sửa `/choi` mốc final, nối cổng stdout vào hook Claude Code, sửa điều hướng công khai.
11. Ghi tài liệu trước (hook deploy đòi) ⇒ deploy `choi.html` (không restart) ⇒ commit `ff92c3e` (hook 10/10).

## 3. Điều quan trọng nhất cho người đọc sau

- **Không cách chơi nào vượt may rủi có ý nghĩa** trên 142 ngày. Tháng tốt/tháng xấu ±70M là dao động.
- **Đừng dùng cột khuyến nghị CHƠI/NGHỈ trong lịch sử `money_board_log`** để đánh giá — nó được ghi sau giờ xổ.
- Hàng loạt phép đo «có lợi thế không» đã đủ mẫu và **không vượt ngưỡng** — 57 mục có bảng đủ trong evidence.
- Hai bộ cổng commit (Claude Code và Cursor) **khác nhau** — câu «cổng commit N cổng» phải nói rõ hook nào.

## 4. Vấp ở đâu

Xem REPORT §7 — tám chỗ, đều do agent, đều sửa trước khi dùng hoặc rút lại tại chỗ.

## 5. Điều phiên CỐ Ý không làm

- Không áp nhãn cho 57 mục (owner cấm đóng hàng loạt).
- Không vá khuyến nghị `/choi` đêm nay (cần restart mô-đun service; 3 agent đang đo).
- Không nối `_v11050` (~97 s) vào hook Claude Code — cần cân thời gian commit (`FU-457`).
- Không rút lại «32,69%» của FU-204 — chưa tự tái lập.
- Không sửa câu «nhịp hệ thống» `/monitoring` — phải dựng lại từ nguồn mốc thật (`FU-458`).

## 6. Câu phải nhớ khi đọc lại

> Một con số z +2,18 xuất hiện đúng lúc mình mong nó xuất hiện là lý do để kiểm giờ ghi, không phải để công bố.
