# CONVERSATION CONTEXT — V11193 · Đánh giá dự đoán 25/11 + OpenRouter chặn, 25/11 21:35 → 22:0x ICT

## 1. Owner nói gì — nguyên văn

| giờ (ICT) | nguyên văn | loại |
|---|---|---|
| 25/11 ~21:35 | *"phần của anh nhiều vài rút gọn quá chỉ có khuyên của em ko chưa đủ em cần trình bày rõ hơn đi , kiểm tra đánh giá việc dự đoán hôm nay sao rồi em"* | YÊU_CẦU |

Câu này đến sau khi agent báo kết quả nghiệm thu 18:45 (V11192) kèm danh sách A/B/C rút gọn.

## 2. Thứ tự thật của phiên

1. Ghi lời owner vào sổ tương tác.
2. Viết phép đo một ngày (`_v11193_danh_gia_ngay.py`) theo thước tiền của `/choi`, nền đúng ngày.
3. Chạy trên VPS và thấy `gpt-oss-120b`, `glm-5.1` có `0/0` ở cả ba miền. Phép đo đánh giá ngày đã làm lộ sự cố này.
4. Tra 30 ngày: hôm qua còn đủ, hôm nay rỗng hết. Journal ghi HTTP 400 `Request path cannot be relayed`.
5. Nghi lần khởi động lại 24/11 23:17 là thủ phạm. Kiểm tệp đổi và mã gọi thì không có gì trên đường gọi model.
6. Gọi thử một lượt ngoài service: tra khoá 200, gọi model 400. Tìm web thấy người khác gặp cùng ngày.
7. Một báo cáo gợi ý soi header `cf-ray` để loại khả năng proxy cục bộ. Kiểm thì có `cf-ray …-HKG`, nghĩa là OpenRouter
   trả thật.
8. Đọc `QD-080`. Mục 6 cho phép cách ly khi circuit-open, nhưng đọc mã chấm combo-super thì dòng rỗng không bị tính.
   Vì vậy quyết **không cách ly**, giữ khả năng tự hồi phục.
9. Đo ứng viên thế chỗ trên một thước so được giữa các cửa sổ (chênh so với nền đúng ngày).
10. Lấy bối cảnh 30 ngày.
11. Đọc lại nguyên văn sổ cho từng việc của owner để viết lại cho rõ. Phát hiện câu sai ở việc 6a, đính chính.
12. Ghi tài liệu, commit `ac30090`, viết báo cáo này.

## 3. Điều quan trọng nhất cho người đọc sau

- **Lỗi OpenRouter không phải lỗi của hệ.** Khoá hợp lệ, mã không đổi, phản hồi do chính OpenRouter trả.
  Muốn biết đã thông chưa thì chạy `_v11193_thu_openrouter.py`: `POST` trả 200 là thông.
- **Hai lần trong 14 ngày, model chính chết mà không ai được báo**: Claude 11/11 và OpenRouter 25/11.
  Việc dựng cảnh báo (B, `FU-328`) phải bao cả trường hợp nhà cung cấp chặn, không chỉ hết tiền.
- **Một ngày lời +3,95tr không đổi kết luận.** 30 ngày vẫn trong vùng may rủi.

## 4. Cổng báo cáo

Chạy sau khi đẩy báo cáo này: `_v10921_report_gate.py` ① toàn dải, rồi ② `V11193`.
Lệnh ① vẫn báo 39 bản cũ thiếu. Con số này có từ trước phiên, phiên này không thêm bản thiếu.

## 5. Vấp ở đâu

- Viết danh sách việc owner theo trí nhớ ở lượt 13:4x, nên ghi sai số ở 6a. Lần này đọc lại sổ trước khi viết.
- Bước 5: ban đầu nghi chính lần khởi động lại V11189 gây lỗi. Phải kiểm tệp và mã mới loại được giả thuyết đó.
  Đây là bằng chứng phải chứng minh nguồn trước khi kết luận (RM-13).

## 6. Điều phiên CỐ Ý không làm

- Không cách ly hai model OpenRouter (lý do ở REPORT §4).
- Không đổi roster hay đưa DeepSeek vào. Chờ owner (`FU-460`).
- Không gọi OpenRouter quá hai lượt thử (một lượt chẩn đoán, một lượt kiểm header). Không retry.
- Không đọc dòng `/choi` «theo khuyến nghị» làm thành tích.

## 7. Câu phải nhớ khi đọc lại

> Khoá trả 200 chưa có nghĩa là gọi được model. Thử bằng chính lệnh gọi model, một lượt, rồi đọc header để biết ai trả lời.
