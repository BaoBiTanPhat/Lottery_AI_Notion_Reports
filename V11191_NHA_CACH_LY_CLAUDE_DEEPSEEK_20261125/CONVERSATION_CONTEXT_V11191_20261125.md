# CONVERSATION CONTEXT — V11191 · Nhả cách ly Claude + DeepSeek, 25/11/2026 13:12 → 13:4x ICT

## 1. Owner nói gì — nguyên văn

| giờ (ICT) | nguyên văn | loại |
|---|---|---|
| 25/11 ~13:12 | *"deepseek và claude athopic anh đã nạp tiền rồi ah em"* | XÁC_NHẬN |

Đây là câu trả lời cho danh sách chốt agent gửi lúc ~11:58 (việc 1: nạp Anthropic hay chuyển qua OpenRouter — agent
khuyên nạp). Owner không nói thêm gì giữa phiên.

## 2. Thứ tự thật của phiên

1. Ghi lời owner vào sổ trước. Lệnh lấy giờ trả **06:13** — mâu thuẫn với dòng sổ 11:58 ⇒ kiểm lại: Git Bash bỏ qua
   `TZ=Asia/Ho_Chi_Minh` và trả UTC; giờ thật **13:13**. Khung cấm deploy còn xa (15:30).
2. Đọc `data/provider_quarantine.json` trên VPS: 6 model bị cách ly. Chỉ 4 model thuộc hai hãng owner đã nạp.
3. Đọc `_v11184_cach_ly_provider.py`: nhả cần bằng chứng; chú thích nói «nhả về CHALLENGER (§Z E5)». Kiểm `grep
   tra_ve_hang` — không ai đọc; tìm nguyên văn owner — không có. Roster `QD-080` mới là thứ quyết định hàng.
4. Tra số dư DeepSeek (miễn phí): 19,94 USD.
5. Tìm đường khoá thật: production lấy khoá từ **DB trước `.env`** qua `scheduler._get_api_key_for_model` ⇒ bài gọi
   thử phải dùng đúng hàm này. Kiểm import `scheduler` không tự khởi động lịch.
6. Viết `_v11191_thu_suc_khoe_provider.py`; sao lưu tệp cách ly; chạy một lần `--nha` lúc 13:17 — 4/4 đạt, nhả 4.
7. Tra giờ gọi Claude ngày thường ⇒ lượt thật đầu tiên là MT ~16:38 chiều nay.
8. Tra lịch sử DeepSeek + chạy thẳng cổng `uy_quyen_goi` ⇒ DeepSeek `DENY_OUTSIDE_ROSTER` mọi lớp.
9. Ghi tài liệu (`_v11191_ghi_tai_lieu.py`, seq 506), cổng §63 đạt, sổ quyết định 0 TRÔI, commit `7ff3b31`, push.

## 3. Điều quan trọng nhất cho người đọc sau

- **Nạp tiền ≠ model được gọi.** Claude chạy lại vì nó vốn có trong roster. DeepSeek không có trong roster từ 14/09
  nên nạp xong vẫn bị cổng uỷ quyền từ chối ở mọi đường.
- **Gọi thử phải đi đúng đường khoá production** — khoá trong DB được ưu tiên hơn `.env`.
- Chú thích «nhả về CHALLENGER» trong mô-đun cách ly **không được thi hành** và không có lời owner đứng sau.

## 4. Vấp ở đâu

Xem REPORT §7 — ba chỗ: giờ UTC trong Git Bash, nháy đơn SQL trong ssh, suýt tin chú thích mô-đun.

## 5. Điều phiên CỐ Ý không làm

- Không gọi lại model nào lần thứ hai (lệnh owner 13/09: không retry).
- Không đụng `gpt-5.4`/`gpt-5-mini` — OpenAI chưa nạp.
- Không đưa DeepSeek vào roster — phải thay một model, là quyết định của owner.
- Không sửa chú thích §Z E5 trong mô-đun đang nạp trong service.
- Không chạy dự đoán bù cho hôm nay — lượt MT/MB chiều nay sẽ tự có Opus.

## 6. Câu phải nhớ khi đọc lại

> Hỏi «tiền nạp rồi thì model đã được gọi chưa?» bằng cổng uỷ quyền cuối, không bằng số dư.
