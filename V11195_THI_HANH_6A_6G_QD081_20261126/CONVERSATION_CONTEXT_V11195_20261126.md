# CONVERSATION CONTEXT — V11195 · Thi hành 6a–6g (QD-081), 26/11 ~10:10 → ~11:20 ICT

## 1. Owner nói gì — nguyên văn

| giờ (ICT) | nguyên văn | loại |
|---|---|---|
| 26/11 ~10:10 | *«6a --> theo khuyến nghị / 6b --> theo khuyến nghị / 6c --> theo khuyến nghị / 6d  --> theo khuyến nghị / 6e --> theo khuyến nghị / 6f --> theo khuyến nghị chú ý ghi nhận lưu lại backup lại nha em / 6g --> theo khuyến nghị --> theo khuyến nghị»* (mỗi dòng một việc, dấu «/» là xuống dòng) | XÁC_NHẬN |
| 26/11 ~10:10 | *«Đồng thời kiểm tra dự đoán hôm qua và hôm nay nha em.»* | YÊU_CẦU — bản riêng |
| 26/11 ~10:10 | *«Lên phương án kế hoạch dọn dẹp hệ thống đi cồng kềnh quá mà chả hiệu quả gì cả em?»* | YÊU_CẦU + HỎI — bản riêng |

Tin nhắn đến sau bản V11194 (05:4x) báo OpenRouter thông lại và FU-452 đạt.

## 2. Thứ tự thật của phiên

1. Ghi ba dòng vào sổ tương tác, kiểm giờ (10:10 — trong khung được deploy tới 15:30).
2. Dựng bao đóng mã sống trên VPS và khởi chạy luồng kiểm kê dọn dẹp ở nền (cho yêu cầu thứ ba).
3. Đọc khối mới nhất của 10 mục FU, đối chiếu V11190, đọc mã thật từng chỗ.
4. 6g: phát hiện job gọi mô-đun đã tắt từ 31/05 ⇒ vá không đổi prompt nào; cổng biên anchor còn in câu đóng băng cũ ⇒ sửa.
5. 6e: đọc chỗ rò; thấy sổ khoá không biết luật nghỉ tuần nào; thấy `mining_log` giữ đủ lịch lần đào ⇒ thiết kế nhãn mới,
   cổng thử chặn hai chiều, script áp nhãn có chế độ thử.
6. Suýt chép cả DB vào RAM ở chế độ thử — sửa trước khi chạy.
7. 6a/6f: viết hai script đo; 6f lộ ra MN cũng dưới 10.000 ⇒ tiền đề khuyến nghị sai (RL-051).
8. 6a: phát hiện số 89,7% có thật trong mã (độ phủ MN) ⇒ câu đính chính tối qua cũng sai (RL-050).
9. Tải lên VPS, băm 4 bảng, thử rồi áp nhãn (983 dòng), băm lại — y hệt.
10. Đo lại luật: MN/MT không tín hiệu, MB kém nền. Kiểm `MINED_RULES_MODE`: vẫn `soft`, CHỐT GẤP +0,40 đang cộng.
11. 6c: tính bảng ghi đè trên DB thật ⇒ bảng đang in «NÊN TẮT». Sửa bảng; journal không có nhật ký truy cập nên đọc nginx ⇒
    mô-đun đã nạp từ 24/11 23:20 ⇒ restart 10:47 (PID 1122833 → 1277779), 47 job giống hệt, 4 bảng không đổi.
12. 6b: chạy lại phép đo trọng số trên DB VPS (bỏ đúng cổng RM-01 dành cho bản local).
13. Ghi tài liệu (seq 510), QD-081, RL-050/051, chú thích rút lại tại chỗ gốc; bộ đọc kế thừa hạn cũ cho FU-345 ⇒ cho hạn
    03/12. Commit `725779b`.

## 3. Điều quan trọng nhất cho người đọc sau

- **Luật soi cầu không mang tín hiệu đo tiến.** Mọi con số «luật hơn nền» trước đây đo trong cửa sổ đã chọn luật. Đo
  đúng: MN +0,1 · MT +1,9 · MB −6,3 (kém nền). CHỐT GẤP +0,40 vẫn đang cộng điểm từ chính các luật đó.
- **Một công cụ canh có thể lật quyết định của owner.** Bảng ghi đè MN in «NÊN TẮT» trên cửa sổ trượt 30 ngày — ai đọc
  bảng mà không đọc sổ sẽ tắt lớp owner vừa chốt giữ.
- **Khuyến nghị sai tiền đề thì thi hành phần đã duyệt, trả phần còn lại** — không tự mở rộng quyết định (FU-345 MN).

## 4. Cổng báo cáo

Chạy sau khi đẩy báo cáo này: `_v10921_report_gate.py` ① toàn dải rồi ② `V11195`. Lệnh ① vẫn báo các bản cũ thiếu báo
cáo từ trước phiên; phiên này không thêm bản thiếu.

## 5. Vấp ở đâu

- Viết khuyến nghị 6f từ dòng tóm tắt, không tách theo miền (RL-051).
- Nói «không nằm trong tài liệu nào» mà chưa grep (RL-050).
- `con.backup(mem)` cho chế độ thử — sẽ chép 1,1 GB vào RAM máy 2 CPU đang chạy production. Bắt được khi đọc lại code.
- Đếm truy cập trong journal ra 0 rồi suýt kết luận «mô-đun chưa nạp, khỏi restart» — journal không ghi truy cập; nginx
  cho thấy đã nạp (RM-13: chứng minh nguồn trước khi kết luận).

## 6. Điều phiên CỐ Ý không làm

- Không đổi `MINED_RULES_MODE` / CHỐT GẤP (đường chọn số — cần owner).
- Không nới ngưỡng 10.000 cho MN (ngoài phần owner duyệt).
- Không đổi hành vi bộ đọc sổ theo dõi (kế thừa hạn là có chủ ý).
- Không đổi prompt, roster, trọng số, `OVERRIDE_CONFIG`.

## 7. Câu phải nhớ khi đọc lại

> «Đo tiến» chỉ có nghĩa khi luật đã được CHỌN trước ngày đó. Chấm bù một ngày luật đang nghỉ là đo trong cửa sổ chọn —
> và mọi luật đều «hơn nền» ở đó.
