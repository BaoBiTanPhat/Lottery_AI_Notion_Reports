# CONVERSATION CONTEXT — V11204 · Đợt 1 dọn dẹp, 27/11 ~15:00 → 15:40 ICT

## 1. Owner nói gì — nguyên văn

| giờ (ICT) | nguyên văn | loại |
|---|---|---|
| 27/11 ~14:50 | *«C đồng ý theo khuyến nghị nha em.»* | XÁC_NHẬN |
| 27/11 ~14:50 | *«==> tất cả kiểm tra đối chiếu , đối soát , xử lý bài bản chuẩn chỉnh dùm anh nha em. Tinh gọn chính xác ổn định»* | YÊU_CẦU |

## 2. Thứ tự thật

1. Soi người đọc từng lịch sắp dừng (RM-20) — 1B kiểm ba tầng vì tên bảng gợi ý có thể vào prompt.
2. Phát hiện §60 ở 1C: `_v10647` sẽ báo giả nếu chỉ dừng writer ⇒ sửa kèm.
3. Viết và chạy phán quyết D-30 đúng cửa sổ tiền đăng ký.
4. Đo giờ chốt 115 ngày cho 1H.
5. Thử khô crontab → cài 15:24 → cổng ĐẠT. Ghi tài liệu, commit `e922ba9`.

## 3. Điều quan trọng nhất cho người đọc sau

- Không xoá gì: dòng cron dừng còn nguyên dạng chú thích; bảng và tệp giữ.
- D-30 lane 1 là «chưa được phép kết luận», không phải «thua» — dừng vì không đo nổi trong thời gian hợp lý.

## 4. Cổng báo cáo

Chạy sau khi đẩy: `_v10921_report_gate.py` ① rồi ② `V11204`.

## 5. Vấp ở đâu

- Dự đoán «1G INVALID» chỉ đúng một nửa.
- Giả định tên cột khi viết cổng (RM-10) — đọc schema rồi sửa.

## 6. Điều CỐ Ý không làm

- Không sửa mã service, không restart (dồn sang lần restart gộp có kế hoạch).
- Không đổi giao diện khi owner chưa xem demo.
- Không kéo dài D-30.

## 7. Câu phải nhớ

> Dừng một writer thì phải hỏi cả «ai đang canh writer này còn chạy không» — không chỉ «ai đọc bảng của nó».
