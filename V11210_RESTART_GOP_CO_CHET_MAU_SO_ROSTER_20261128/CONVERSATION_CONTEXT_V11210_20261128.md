# CONVERSATION CONTEXT — V11210 · Restart gộp 28/11 · 06:33 → ~07:10 ICT

## 1. Owner nói gì — nguyên văn

| giờ (ICT) | nguyên văn | loại |
|---|---|---|
| 27/11 ~17:35 | *«OK ĐỒNG Ý VỚI ĐỀ XUẤT NHƯNG CÒN 1 ĐIỂM NỮA LÀ CÁC MODEL HIỆN TẠI CÒN BAO NHIÊU MODEL CÓ CẦN CẮT GIẢM BỔ SUNG MODEL NÀO KHÔNG EM?»* | XÁC_NHẬN + HỎI |
| 27/11 ~17:50 | *«OK ANH DUYỆT THEO KHUYẾN NGHỊ EM. EM TIẾN HÀNH XỬ LÝ HOÀN TẤT DỨT ĐIỂM SẠCH SẺ DÙM ANH»* | XÁC_NHẬN + YÊU_CẦU |

Sáng 28/11 owner chưa nói gì; agent thi hành phần đã duyệt theo runbook soạn tối 27/11 (`docs/RUNBOOK_V11210_RESTART_20261128.md`).

## 2. Thứ tự thật

1. 06:33 — đồng hồ hẹn thức; PRE: một tiến trình service, sha 11 tệp VPS = bản sao lưu dev; băm 4 bảng `TRUOC_V11210`; sao lưu 11 tệp trên VPS.
2. 06:34 — 17 tệp lên thư mục tạm, so sha byte y hệt, `py_compile` 17/17.
3. 06:35:02 — lượt `du_doan_test_auto` 06:35 ghi log ⇒ 06:35:40 chép tệp vào chỗ, restart. 06:36:06 PID mới, health 200; admin 401 ×3.
4. Journal sạch; scheduler đăng ký 35 job, không còn 5 job tắt. Kiểm FU-465a trên mã đã triển khai 10/10; băm `SAU_V11210` = trước.
5. 06:39 — sổ quyết định: QD-020 TRÔI. Đo trên VPS ⇒ phép phát lại 03/08 dựa vào danh sách output toàn cục. Đổi neo sang MB 27/11.
6. Quét ngược 69 tệp / 15 chạy sống ⇒ không chỗ đọc sống nào đổi dòng. Đồng bộ dữ liệu sống về máy dev; 06:48 sổ 0 TRÔI.
7. Đo lại 6 lane MN ⇒ mờ dần từ tháng 8, không phải «dừng 02/11» như đã nói tối qua.
8. Bốn mặt (seq 524) · 9 khối FU ⇒ commit `2474d78` ⇒ đẩy nhánh + `master` ⇒ báo cáo này.

## 3. Điều quan trọng nhất cho người đọc sau

- Phiếu không đổi. Đổi là **nhãn**: ngày đủ 11/11 hết bị gọi «thiếu», và combo-super được chấm lại từ 28/11.
- MB vẫn `INCOMPLETE 8/11` mỗi ngày: con số đó đếm phiếu **sau** cổng chất lượng, không phải model có output. Đừng đọc thành sự cố.
- Phân loại lại 14/09 → 27/11 **chưa làm** — chờ owner (FU-453).

## 4. Cổng báo cáo

Chạy sau khi đẩy: `_v10921_report_gate.py` ① toàn dải rồi ② `V11210`. Kết quả ghi ở tin nhắn kết phiên.

## 5. Vấp ở đâu

- §60.2 trước deploy mới quét sổ quyết định, chưa quét hết người đọc danh sách output ⇒ QD-020 TRÔI sau deploy.
- Đoán đường admin ⇒ 404; tra route thật ⇒ 401.
- Nạp bản sao lưu đuôi lạ bằng `spec_from_file_location` ⇒ `None`; dùng `SourceFileLoader`.
- `git add` một tệp nằm trong thư mục bị `.gitignore` làm lệnh dừng; bỏ tệp đó.

## 6. Điều CỐ Ý không làm

- Không làm bộ dò ĐÃ XONG nhớ roster theo ngày — không đường sống nào phát lại ngày trước 14/09; đổi bộ chọn của lane Nghiệm Thu lúc đóng băng là thêm rủi ro.
- Không sửa 6 lane MN — đường dự đoán đang đóng băng, sửa hay để nghỉ là việc chọn (FU-467).
- Không phân loại lại nhãn lịch sử 14/09 → 27/11 (FU-453, chờ owner).
- Không đụng trang sống: 4 mục giao diện còn ở demo chờ owner duyệt.

## 7. Câu phải nhớ

> Đổi một danh sách dùng chung thì phải hỏi mọi người đọc nó, không chỉ những phép kiểm ghi tên nó.
