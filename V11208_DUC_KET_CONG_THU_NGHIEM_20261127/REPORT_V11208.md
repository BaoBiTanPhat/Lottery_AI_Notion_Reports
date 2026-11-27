# V11208 — Bản đúc kết · cổng thử nghiệm mới · luật PRJ-EXPERIMENT-GATE-001 sáu mặt

> **Phiên bản:** V11208 · **Ngày:** 27/11/2026 ~18:15 → 18:45 ICT · **Repo riêng:** `ce87d37` · **governance_seq:** 522 · **Quyết định:** QD-084
> · **Tầng (RM-12):** `CODE_PUSHED` (cổng chạy ở máy dev, thử thật đạt) · **Runtime VPS:** không đổi.

## 1. Tóm tắt

- **Bản đúc kết một trang:** `evidence/DUC_KET_HE_DU_DOAN_20261127.md` — kết luận, đã thử gì, vì sao bốn tháng không ra gì khác ngẫu nhiên,
  lỗi phương pháp, từ nay làm gì.
- **Cổng máy mới** chặn commit khi dựng thử nghiệm / thêm model mà chưa đăng ký trước, hoặc cần > 120 ngày mà không có owner duyệt.
- **Luật mới** `PRJ-EXPERIMENT-GATE-001` vào đủ sáu mặt quy tắc; câu «official đúng 15/15» sửa thành «đủ roster từng miền (hiện 11/11)».

## 2. Owner yêu cầu gì (nguyên văn)

27/11 ~17:50: *«OK ANH DUYỆT THEO KHUYẾN NGHỊ EM. EM TIẾN HÀNH XỬ LÝ HOÀN TẤT DỨT ĐIỂM SẠCH SẺ DÙM ANH»* (duyệt khuyến nghị 17:25: đúc kết ·
cổng máy cho thử nghiệm mới · đóng băng đường dự đoán).

## 3. Đào bới / phát hiện

- Cổng commit của Claude Code và Cursor có **hai danh sách riêng** (FU-457) ⇒ cổng mới phải nối cả hai, nếu không sẽ thành cổng không ai gọi.
- Câu «An toàn cứng: official đúng 15/15» ở 4 mặt quy tắc đã lệch thật từ 14/09 (mỗi miền bỏ phiếu 11).
- Ví dụ cỡ mẫu trong sổ đăng ký lúc đầu ghi sai («≈ 453 ngày»); công thức của chính cổng ra 718 lượt ≈ 240 ngày gộp 3 miền.

## 4. Hướng xử lý và vì sao chọn

Luật §61: một lỗi tái phạm nhiều lần thì nhắc suông không đủ, phải thành cổng máy. Cổng soi đúng thứ đã gây hại: **tệp mới mang dáng thử
nghiệm** và **model mới** — chỉ cho qua khi đã khai giả thuyết · nền · MDE · ngưỡng · ngày đọc trước; cổng tự tính n cần.

## 5. Đã làm gì

| việc | TRƯỚC | SAU | KIỂM |
|---|---|---|---|
| bản đúc kết | rải rác V10945 · V11190 · V11206 | một trang, mọi số trỏ script đã commit | — |
| cổng `_v11208_cong_thu_nghiem.py` + sổ `docs/DANG_KY_THU_NGHIEM.json` | không gì chặn | K1 tệp mới dáng thử nghiệm phải đăng ký · K2 đủ trường, n cần tự tính, > 120 ngày cần owner duyệt · K3 thêm model cần duyệt | `--thu-chan` 8/8 · thử trên git thật: chặn (thoát 1) / cho qua (thoát 0) |
| nối cổng | — | cả hai cổng commit | lần commit này: 11/11 cổng con qua |
| luật sáu mặt | — | `PRJ-EXPERIMENT-GATE-001` ở 4 mặt sửa tay + sinh lại 2 mặt | `_v10925_rule_sync_check.py` «SÁU MẶT ĐỒNG BỘ» · `_v11027` không mục nào mất |

## 6. Cổng kiểm

| cổng | kết quả |
|---|---|
| `_v11208_cong_thu_nghiem.py --thu-chan` (RM-15) | 8/8 |
| cổng commit (gồm cổng mới) | 11/11 qua |
| `_v11062_nang_version.py --kiem` | ĐẠT |
| `_v10921_report_gate.py` ② `V11208` | xem `CONVERSATION_CONTEXT` §4 |

## 7. Vướng vấp

- Lần thử chặn đầu tiên 6/7: cổng **để lọt** model mới thêm vào registry (biểu thức chỉ khớp khi `id` đứng đầu dòng) — sửa, 8/8.
- Chính tệp cổng tên có `thu_nghiem` suýt tự chặn mình — thêm ngoại lệ cho tệp cổng (`_cong_`) và một ca thử.
- Cổng ghi an toàn `_v11019` chặn commit đầu (ghi tệp không đóng tay) — sửa sang ghi tạm + fsync + thay thế.

## 8. Gỡ về

`git revert ce87d37`; bỏ dòng cổng mới ở hai tệp hook.

## 9. Theo dõi tiếp

| mã | việc | ai | hạn |
|---|---|---|---|
| FU-465 (a) | dọn cờ chết + mẫu số theo roster — áp mã, restart gộp, so PID | agent | 28/11 06:35 |
| FU-464 | nhãn «chưa có lợi thế đo được» — demo cho owner | agent → owner | 28/11 |
| FU-451 (b) | tính bù bảng scorecard 14/09→24/11 | agent | 27/11 22:10 |

## 10. Ba lớp nguồn (§62)

| lớp | nội dung | bằng chứng |
|---|---|---|
| `OWNER_SAID` | duyệt đúc kết + cổng máy + đóng băng | kho riêng `docs/SO_TUONG_TAC_OWNER.md` 27/11 ~17:50 |
| `CODE_DID` | cổng chặn thật trên git; sáu mặt đồng bộ | `_v11208_cong_thu_nghiem.py` · `_v10925_rule_sync_check.py` |
| `DOC_SAID` | «official đúng 15/15» | 4 mặt quy tắc (đã sửa) |

**Lệch:** `DOC_SAID` («15/15») ≠ `CODE_DID` (11/miền từ 14/09) — đã sửa trong bản này.

**TanPhatAI cần làm:** ghi luật `PRJ-EXPERIMENT-GATE-001` (thử nghiệm / model mới phải đăng ký trước, > 120 ngày cần owner duyệt) và câu «đủ
roster từng miền (11/11)». Đọc `evidence/DUC_KET_HE_DU_DOAN_20261127.md`. Code đi trước tài liệu: không.
