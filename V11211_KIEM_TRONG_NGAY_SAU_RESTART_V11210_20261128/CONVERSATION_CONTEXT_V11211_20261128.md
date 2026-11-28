# CONVERSATION CONTEXT — V11211 · Kiểm trong ngày sau restart V11210 · 28/11 16:48 → ~20:45 ICT

## 1. Owner nói gì — nguyên văn

| giờ (ICT) | nguyên văn | loại |
|---|---|---|
| 27/11 ~17:50 | *«OK ANH DUYỆT THEO KHUYẾN NGHỊ EM. EM TIẾN HÀNH XỬ LÝ HOÀN TẤT DỨT ĐIỂM SẠCH SẺ DÙM ANH»* | XÁC_NHẬN + YÊU_CẦU |

Ngày 28/11 owner không gửi tin nhắn nào. Phiên này thi hành bước 8 runbook V11210 (*«RM-16 trong ngày»*) — phần đã duyệt, không phải yêu cầu
mới. Sổ tương tác owner không có dòng mới cho ngày 28/11.

## 2. Thứ tự thật

1. Sáng 28/11 (V11210) — đặt hai tác vụ chờ: 16:48 và 20:30, cùng chạy `_v11210_kiem_trong_ngay.py` trên VPS (chỉ đọc).
2. 16:48:01 — MN: C1 · C3 · C4 · C7 đạt, 12 điểm chưa tới giờ, 0 trượt. Tác vụ chờ báo exit 1 vì `grep -c` đếm 0 Traceback.
3. Đặt thêm lượt 17:00:30 để đọc bundle MT sớm (lượt mã mới đầu tiên; nếu hỏng cần biết trước MB 17:58).
4. 17:00:32 — MT: chốt `/choi` 16:56 · bundle 16:43 BT 75 · 11 phiếu. 6 đạt, 0 trượt.
5. 17:01 — so tập model MT/MN với mã cũ; phát hiện đọc nhầm `source_predictions_json` (dict chẩn đoán) thành danh sách model. Đổi sang
   khoá `model_wr`: trùng 26–27/11. Rà báo cáo V11210: không câu nào dựa vào trường đó. Sửa tên trường trong script phát lại.
6. 20:30:01 — đủ 18/18 đạt; PID 1516954; 0 Traceback; `system_alerts` hôm nay 0 dòng.
7. 20:31 — chứng minh hàm cảnh báo có chạy (dòng `auto_verify` + 0 `V11210_ALERT_ERR`); đọc MB 9/11 = 2 model trượt cổng BT.
8. 20:32 — viết + chạy `_v11211_dem_fu453.py` (MN 60 · MT 56 · MB 34 / 75); chạy lại bộ kiểm: vẫn 18/18.
9. V11211 trống (`_v11044`) ⇒ sao lưu năm tệp quản trị ⇒ ghi bốn mặt (seq 525) + 7 khối FU ⇒ cổng nâng version ĐẠT ⇒ đồng bộ dữ liệu sống
   20:33:59 ⇒ sổ quyết định 0 TRÔI ⇒ commit `be747cc` ⇒ đẩy nhánh + `master` ⇒ báo cáo này.

## 3. Điều quan trọng nhất cho người đọc sau

- V11210 **đã chạy sống trọn một ngày** và mọi điểm kiểm đều đạt. Không còn việc gì của V11210 chờ trong ngày; chỉ còn `_v10800` thứ Hai.
- MB `INCOMPLETE 8–9/11` là **bình thường**: đếm phiếu sau cổng chất lượng. Đừng đọc thành thiếu model — cảnh báo thiếu output đếm riêng.
- Số FU-453 là **cận dưới** và **chỉ đếm** — chưa đổi nhãn ngày nào.

## 4. Cổng báo cáo

`_v11088_cong_cua_so_chon.py --tep` · `_v11085_cong_rut_lai.py --tep` · `_v11083_sinh_dieu_huong.py` · `_v10921_report_gate.py` ① toàn dải và
② `V11211` — chạy sau khi viết hai tệp này (kết quả trong phản hồi cuối phiên của agent).

## 5. Vấp ở đâu

- Đọc nhầm dict chẩn đoán thành danh sách model (mục 2 bước 5) — kết luận V11210 không đổi, script đã sửa.
- Exit 1 giả của tác vụ chờ 16:48 (`grep -c`).

## 6. Điều CỐ Ý không làm

- Không phân loại lại 75 ngày 14/09 → 27/11 (FU-453) — owner chọn.
- Không đào vì sao `combo-no-token` có WR mà không bỏ phiếu — có từ trước V11210, đường dự đoán đóng băng.
- Không đụng giao diện sống — demo chờ owner.
- Không deploy, không restart: V11211 chỉ đọc.

## 7. Câu phải nhớ

«0 cảnh báo» chỉ là bằng chứng khi chứng minh được bộ cảnh báo **có chạy**. Một hàm im khi không có gì để báo thì phải tìm dấu vết
của lời gọi, không phải dấu vết của kết quả.
