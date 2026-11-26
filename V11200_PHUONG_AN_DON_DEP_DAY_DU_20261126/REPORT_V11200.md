# V11200 — Phát hành phương án dọn dẹp đầy đủ (`docs/KE_HOACH_DON_DEP_20261126.md`)

> **Phiên bản:** V11200 · **Ngày:** 26/11/2026 ~13:40 → 14:00 ICT · **Repo riêng:** `Lottery_AI_Test` commit `33aedc9`
> (nhánh `fu438/admin-only-p0a` + `master`) · **governance_seq:** 515 · **Căn cứ:** owner 26/11 ~10:10 + QD-082 ·
> **Tầng (RM-12):** `REPORT_PROVEN` (tài liệu) · **Runtime đổi:** không.

## 1. Tóm tắt

- Phương án dọn dẹp đầy đủ đã phát hành: bức tranh cồng kềnh có số đo, bốn đợt từ an toàn tới phức tạp, mỗi câu owner cần chốt
  có mã + khuyến nghị (1B–1J · 2A–2F · 3A–3G), danh sách những thứ phải giữ, đề xuất đã bác, mâu thuẫn giữa các mặt.
- **Nói thẳng:** dọn dẹp không làm tăng tỉ lệ trúng (30 ngày mọi cách chơi trong vùng may rủi). Phần nhắm vào chất lượng dự đoán là
  Đợt 2 — đơn giản hoá đường chọn số chỉ qua shadow, ngưỡng khai trước, mỗi miền chỉ tiến không lùi.
- Bản công khai (`evidence/KE_HOACH_DON_DEP_20261126_ban_cong_khai.md`) **ẩn mục bảo mật máy chủ** — chi tiết chỉ ở kho riêng.

## 2. Owner yêu cầu gì (nguyên văn) — §62 lớp `OWNER_SAID`

| giờ (ICT) | nguyên văn |
|---|---|
| 26/11 ~10:10 | *«Lên phương án kế hoạch dọn dẹp hệ thống đi cồng kềnh quá mà chả hiệu quả gì cả em?»* |
| 26/11 ~11:47 | *«kiểm xong chưa tiến hành dọn dẹp được chưa ? chờ  anh chốt vấn đề gì?»* |
| 26/11 ~12:0x | *«tiến hành các đề xuất an toàn trước, tuần tự , cuốn chiếu từ dễ đến khó từ đơn giản rõ ràng đến phức tạp tra soát, soi xét kỹ lưỡng  v..v...»* |

## 3. Đào bới / phát hiện — liệt kê ĐỦ

- **Luồng kiểm kê** 21 tác tử chỉ đọc (8 kiểm kê · 8 phản biện · soát thiếu · 3 việc bù · tổng hợp), 2.246 lần gọi công cụ, 0 lỗi.
- **Số đo chính** (mục 2 của tài liệu): crontab sáng 26/11 có 90 dòng (nay 81) · 47 job APScheduler, 424 lượt chạy/ngày ·
  `scheduler_logs` 7 ngày ~44% nhiễu · DB 1.099,6 MB tăng ~3,7 MB/ngày · 180/593 tệp `.py` sống · ≥ 10 bộ canh nhưng không phép nào
  canh «model official trả rỗng» · 36/39 panel đo chỉ được gọi trong 1 ngày (cửa sổ nginx rơi vào quãng hệ đứng — chưa chứng minh
  «không cần») · dữ liệu 76 ngày không có bản sao ngoài VPS (đã xử V11198).
- **Phản biện đã bác/hạ mức** nhiều đề xuất nếu làm theo sẽ hỏng `/choi`, prompt hoặc phép kiểm sổ quyết định — ví dụ cắt bảng
  preview MB (đầu vào `/choi` MB), tắt `_v10869` (A/B cắt model §59), cắt 8 lượt `_v10879` (đã cứu 18 lần early_block trượt).
- **Đính chính của agent điều phối** (mục A): 1A chưa dừng — `compute_view()` chỉ đọc cho thấy so sánh hứa hẹn chưa đo đúng; lỗi in
  nhật ký đã vá ở V11199; dữ liệu tổng hợp bị cắt nên phần chưa phản biện để ở Phụ lục B.

## 4. Hướng xử lý và vì sao chọn

Đi theo đợt: Đợt 0 (sổ sách, nhãn, sửa báo động — không cần owner) → Đợt 1 (dừng việc hết hạn, giữ bảng) → Đợt 2 (đơn giản hoá qua
shadow) → Đợt 3 (dữ liệu cũ, lưu trữ — sau khi có lịch sao lưu). Mỗi việc có bằng chứng · được · mất · gỡ về · kiểm sau. Việc chạm
đường chọn số hoặc định nghĩa owner đã khoá luôn trình owner.

## 5. Đã làm gì

1. Đọc bản tổng hợp + kết quả gốc các mặt; đối chiếu với các việc đã làm hôm nay (V11196–V11199).
2. Viết mục A (đính chính + bổ sung) lên đầu tài liệu; giữ nguyên văn bản tổng hợp bên dưới.
3. Tạo bản công khai ẩn mục bảo mật máy chủ; gỡ chi tiết bảo mật khỏi `REPORT_V11198.md` đã công bố sáng nay.
4. Ghi bốn mặt (seq 515), FU-462. Commit `33aedc9`.

## 6. Cổng kiểm

| cổng | kết quả |
|---|---|
| `_v11062_nang_version.py --kiem` | `ĐẠT` (seq 515) |
| `_v11027_so_muc_quan_tri.py` | không mục nào biến mất |
| quét từ khoá bảo mật trên mọi báo cáo công khai V11193–V11200 | 0 chỗ còn |
| `_v10921_report_gate.py` ① + ② `V11200` | xem `CONVERSATION_CONTEXT` §4 |

## 7. Vướng vấp

- Bản tổng hợp của luồng nhận dữ liệu bị cắt (kết quả kiểm kê vượt trần độ dài) ⇒ phần chưa phản biện phải để riêng.
- Báo cáo công khai V11198 (sáng nay) có ghi chi tiết bảo mật máy chủ — đã gỡ ở bản này; lịch sử git của kho công khai vẫn còn bản cũ.

## 8. Gỡ về

`git revert 33aedc9` (tài liệu). Không có thay đổi runtime.

## 9. Theo dõi tiếp — liệt kê ĐỦ

| mã | việc | ai chặn | khi nào |
|---|---|---|---|
| `FU-462` | 9 lịch đã dừng không chạy; `_v10900` không thêm LỆCH | lượt tự nhiên | 27/11 |
| Đợt 0a | rút lại 3 số của `KIEM_KE_DON_DEP_20260821.md` sau khi tự tái lập | agent | 27/11 |
| restart gộp | FU-455 + 5 job tắt còn đăng ký + báo động giả (soi kỹ điểm kích) | agent | sáng 27/11 |
| 1B–1J · 2A–2F · 3A–3G | các câu owner trong tài liệu | owner | — |
| bảo mật máy chủ | các việc cấu hình (chi tiết ở kho riêng) | owner | — |
| `FU-451` (a) | kiểm print sau 19:20 | lượt tự nhiên | 26/11 21:05 |

## 10. Ba lớp nguồn (§62)

| lớp | nội dung | bằng chứng |
|---|---|---|
| `OWNER_SAID` | ba lời 26/11 (§2) | `docs/SO_TUONG_TAC_OWNER.md` |
| `CODE_DID` | số đo của luồng kiểm kê trên VPS (chỉ đọc) | lệnh tái lập ở Phụ lục E của tài liệu |
| `DOC_SAID` | `docs/KIEM_KE_DON_DEP_20260821.md`: «424 job khác nhau», «16 bảng», «6,5 MB» | đo lại: 424 lượt/42 job, 27 bảng, 8,17 MB (chờ tự tái lập rồi rút lại) |

**Lệch:** ba số của tài liệu 21/08 lệch số đo mới — rút lại ở Đợt 0a sau khi agent tự tái lập (RM-11).

**TanPhatAI cần làm:** dùng `docs/KE_HOACH_DON_DEP_20261126.md` làm phương án dọn dẹp hiện hành; theo dõi FU-462 và các câu owner
1B–3G. Không có code đi trước tài liệu trong bản này.
