# V11205 — Câu B owner giao agent tra soát: FU-345 đóng ĐẠT · FU-459 áp nhãn 36/44 mục theo từng nhãn

> **Phiên bản:** V11205 · **Ngày:** 27/11/2026 ~15:30 → 15:50 ICT · **Repo riêng:** `297c1bd` · **governance_seq:** 519 · **Quyết định:** QD-083 (B)
> · **Tầng (RM-12):** `REPORT_PROVEN` (sổ theo dõi) trên số đo `RUNTIME_PROVEN` (trace + DB VPS) · **Runtime đổi:** không.

## 1. Tóm tắt

- **FU-345 → CLOSED_PASS.** Dấu vết lỗi gốc (prompt chỉ 64 ký tự) **0 lần** ở cả 3 miền trên 3.140 lượt từ 09/08. Ngưỡng 10.000 ký tự
  bỏ ở cả 3 miền — nó là thước gián tiếp; 26 lượt MN dưới mức đó dồn vào 3 ngày tháng 8, không lặp lại từ 18/08.
- **FU-459:** trong 57 mục V11190, 11 đã xử trước, 2 cố ý chờ (QD-081); **36 mục áp nhãn**, mỗi mục một khối + một dòng bằng chứng.
  Còn 8 mục giao diện (agent tự kiểm tối nay) và FU-451(b) tính bù (22:10).

## 2. Owner yêu cầu gì (nguyên văn)

**27/11 ~14:50:** *«B. Ba câu cũ đang treo ==> cái này em cần kiểm tra tra soát đối chiếu chứ em»*

## 3. Đào bới / phát hiện — liệt kê ĐỦ

| việc | phát hiện |
|---|---|
| FU-345 đo lại | MN 1.075 · MT 1.019 · MB 1.046 lượt; = 64 ký tự: 0 · < 1.000: 0 cả ba; MN < 10.000: 26 (nhỏ nhất 9.809) |
| FU-345 đối chiếu 26 lượt MN | dồn vào 09 · 14 · 17/08 (8–9 lượt/ngày trên ~21), trải 7 model ⇒ dao động theo ngày, không phải model mất khối dữ liệu |
| FU-459 nhãn hiện tại | đọc khối trên cùng bằng `_v10958_fu_reader`: 46 mục còn nhãn chờ cũ; FU-195/FU-183 cố ý chờ (QD-081) ⇒ 44 |
| tiền đề có thể đổi sau 25/11 | cách ly nhà cung cấp còn `gpt-5-mini`, `gpt-5.4`; lane Nghiệm Thu 25–26/11 đủ 3 miền; `_v10900` 23–26/11 lệch 0, C23/C24 OK |
| vấp | truy vấn đầu tìm `check_id='C23'` ra 0 vì tên thật là `C23_vung_ban_dung_bien` — đọc tên thật rồi mới kết luận (RM-10) |
| FU-451(b) | bảng scorecard 0 dòng 14/09→24/11 (216 miền-ngày có kết quả); hàm gốc đọc lại trace 39 MB ~3.200 lần ⇒ dựng bộ bọc chỉ mục một lần, thử tương đương **42/42** mẫu khớp |

## 4. Hướng xử lý và vì sao chọn

Owner ký 09/08 *«CẤM đóng hàng loạt. Rà THEO NHÃN»* ⇒ không đóng theo danh sách: mỗi mục một khối riêng, gom theo nhãn, mục có tiền đề
có thể đổi thì đo lại trước. Mục TRƯỢT/KHÔNG ĐO ĐƯỢC mà còn việc thật thì **giữ mở với nhãn đúng và hạn thật**, không đóng cho sạch sổ.

## 5. Đã làm gì

| nhãn | số | mục |
|---|---|---|
| `CLOSED_PASS` | 16 | FU-252 276 325 427 268 256 258 245 330 331 370 373 357 355 341 336 |
| `CLOSED_REPORT` | 7 | FU-186 196 359 344 321 291 237 — chưa được phép kết luận (RM-04) |
| `CANCELLED` | 6 | FU-203 202 200 197 204 198 — hết tiền đề |
| `CLOSED` | 3 | FU-356 (→ FU-450) · FU-358 (→ FU-264) · FU-360 (giữ mã chặn) |
| giữ MỞ, nhãn đúng | 4 | FU-328 (hạn 28/11, làm cùng việc nối cảnh báo) · FU-292 · FU-318 · FU-285 (hạn 15/12) |

FU-345 `CLOSED_PASS`. Đọc lại bằng bộ đọc sổ: 36/36 khớp nhãn định áp, 0 mục mồ côi.

## 6. Cổng kiểm

| cổng | kết quả |
|---|---|
| `_v11062_nang_version.py --kiem` | ĐẠT |
| bộ đọc `_v10958_fu_reader` đọc lại 36 mục | 36/36 khớp · `trang_thai_mo_coi()` rỗng |
| `_v11205_tinh_bu_scorecard.py --thu` | 42/42 mẫu tương đương hàm gốc (chưa ghi) |
| `_v10921_report_gate.py` ② `V11205` | xem `CONVERSATION_CONTEXT` §4 |

## 7. Vướng vấp

- Tên mục cũ trong sổ có chỗ ghi «ĐÃ LÀM» cho việc vẫn còn mở (FU-328) — khối mới dùng tên ngắn theo cột «việc» của V11190.
- Ghi nhận: số `32,69%` của FU-204 chưa tái lập — ghi rõ không dùng làm căn cứ (RM-17); chưa có quyết định nào dựa vào nó.

## 8. Gỡ về

`git revert 297c1bd` (sổ theo dõi; khối cũ còn nguyên phía dưới).

## 9. Theo dõi tiếp — liệt kê ĐỦ

| mã | việc | ai | hạn |
|---|---|---|---|
| FU-459 | 8 mục giao diện: kiểm route + API có đăng nhập + dữ liệu | agent | 27/11 tối |
| FU-451(b) | tính bù scorecard 14/09→24/11, gắn nhãn `TINH_BU_V11205` | agent | 27/11 22:10 |
| FU-328 | cổng model ra thiếu số — cùng việc nối cảnh báo | agent | 28/11 |
| FU-292 · FU-318 · FU-285 | sửa định nghĩa cổng / quyết đưa lên hay bỏ / dựng bộ chấm | agent → owner (Đợt 2) | 15/12 |

## 10. Ba lớp nguồn (§62)

| lớp | nội dung | bằng chứng |
|---|---|---|
| `OWNER_SAID` | giao agent tra soát đối chiếu câu B | kho riêng `docs/SO_TUONG_TAC_OWNER.md` 27/11 ~14:50 |
| `CODE_DID` | trace: lỗi gốc 0 lần; DB: tiền đề 44 mục đối chiếu | `_v11195_do_fu345.py` · truy vấn DB `mode=ro` |
| `DOC_SAID` | V11190 đề xuất nhãn cho 57 mục; FU-345 «MN trượt theo chữ» | `docs/DOI_CHIEU_58_MUC_V11190.md` |

**Lệch:** `DOC_SAID` gọi MN «trượt» theo ngưỡng 10.000; `CODE_DID` cho thấy lỗi gốc không tái phát lần nào — chữ «trượt» đến từ thước gián
tiếp, không phải từ lỗi. Đã đổi nghiệm thu sang dấu vết lỗi gốc.

**TanPhatAI cần làm:** cập nhật FU-345 (đóng), 36 mục FU-459 theo bảng mục 5, FU-459 còn 8 mục giao diện. Code đi trước tài liệu: không.
