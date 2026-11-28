# V11211 — Kiểm trong ngày 28/11 sau restart V11210: 18/18 đạt · đóng FU-465 · FU-455 · FU-328 · đếm FU-453

> **Phiên bản:** V11211 · **Ngày:** 28/11/2026 16:48 → ~20:45 ICT · **Repo riêng:** `be747cc` · **governance_seq:** 525 · **Quyết định:** QD-084
> (thi hành, không quyết định mới) · **Tầng (RM-12):** V11211 tự nó `REPORT_PROVEN` — **không đổi runtime**. Mã V11210 ở các điểm C1–C8:
> `RUNTIME_PROVEN` **cho ngày 28/11** (đọc dữ liệu thật sau lượt chạy thật). **Chưa** chứng minh: nhánh báo thật của cảnh báo thiếu output
> (chưa miền nào thiếu) · `_v10800` (chạy thứ Hai 30/11).

## 1. Tóm tắt

- **Mã V11210 chạy sống trọn ngày 28/11, 8 điểm kiểm (18 phép theo miền) đều đạt.** Đọc thẳng DB VPS ở 16:48 · 17:00:30 · 20:30:01,
  chạy lại 20:32 cùng kết quả. PID 1516954 cả ngày, 0 Traceback.
- **Bundle MT 16:43 là lượt thật đầu tiên trên mã mới:** 11 phiếu, bạch thủ 75, tập model được chấm **y hệt** MT 26–27/11 (mã cũ).
- **`/choi` chốt khuyến nghị trước giờ xổ ở cả ba miền**, và sau xổ `money_board_log` ghi đúng bản chốt. FU-455 đóng.
- **MN · MT `COMPLETE 11/11`** — lần đầu từ 14/09 có ngày COMPLETE. MB `INCOMPLETE 9/11`: random-forest · xgboost trượt cổng bạch thủ
  (10% < 12%), cả 11 model đều có output đúng hạn. FU-465 đóng.
- **combo-super được chấm lại** ở MN · MT (`daily_eval_log` có dòng — lần đầu từ 11/09).
- **Hết báo động giả:** MB_WATCHDOG «already complete»; `WATCHDOG_MISS shadow_after_chain` 0 (27/11: 113); `system_alerts` 0 dòng vì
  không miền nào thiếu output — và đã chứng minh hàm cảnh báo **có chạy**. FU-328 đóng.
- **Đếm cho FU-453:** trong 75 ngày 14/09 → 27/11, số ngày đủ mẫu số mới (≥ 11 phiếu) **ít nhất** MN 60 · MT 56 · MB 34 — những ngày đó đã
  bị loại khỏi chấm combo-super. **Không đổi nhãn** — chờ owner.

## 2. Owner yêu cầu gì (nguyên văn)

| giờ (ICT) | nguyên văn |
|---|---|
| 27/11 ~17:50 | *«OK ANH DUYỆT THEO KHUYẾN NGHỊ EM. EM TIẾN HÀNH XỬ LÝ HOÀN TẤT DỨT ĐIỂM SẠCH SẺ DÙM ANH»* |

Ngày 28/11 owner **không gửi tin nhắn nào** (từ 06:33 tới lúc viết báo cáo). Phiên này là bước 8 của runbook V11210 (*«RM-16 trong ngày»*),
thuộc phần đã duyệt 27/11 ~17:50 — **không phải** yêu cầu mới. Không có yêu cầu trực tiếp nào khác trong phiên.

## 3. Đào bới / phát hiện

1. **C1–C8 (`_v11210_kiem_trong_ngay.py`) — 18/18 đạt**, nguyên văn ở `evidence/KIEM_V11211.txt`:

   | điểm | 28/11 (mã mới) | 27/11 (mã cũ) |
   |---|---|---|
   | C1 chốt `/choi` | MN `NGHỈ` 15:43 · MT `CHƠI` Full 16:56 · MB `CÂN NHẮC` Nửa 17:56 — trước CUTOFF 16:00 / 17:00 / 18:00 | bảng chốt chưa có |
   | C2 log sau xổ | = bản chốt cả ba miền | log ghi khuyến nghị **sau** giờ xổ |
   | C3 bundle | MN 05:16 BT 79 · 11 (mã **cũ**) · MT 16:43 BT 75 · 11 · MB 17:34 BT 43 · 9 | — |
   | C4 mẫu số | MN · MT `COMPLETE 11/11` · MB `INCOMPLETE 9/11` | MN · MT `INCOMPLETE 11/15` |
   | C5 MB_WATCHDOG | «prediction already complete (ai_chain=5, bundle=1)» | báo thiếu |
   | C6 watchdog shadow | 0 | 113 |
   | C7 cảnh báo thiếu | 0 dòng · 0 model thiếu thật | bảng im từ 11/05 |
   | C8 chấm combo-super | `daily_eval_log` MN 1 · MT 1 | 0 dòng từ 14/09 |

2. **Kiểm C7 có thể đạt «vờ»** — hàm cảnh báo im khi không thiếu, nên «0 cảnh báo» cũng ra như thế nếu hàm không chạy. Đã chứng minh hàm
   **được gọi**: nó nằm trên **cùng dòng** với `classify_day_status(source='auto_verify')` (`scheduler.py:1691/1760/1832`); `day_governance`
   hôm nay có `auto_verify` 16:39:42 · 17:31:33 · 18:31:03; `scheduler_logs` có 0 dòng `V11210_ALERT_ERR`. Nhánh **báo thật** chưa gặp trên
   sống; đã thử trên phát lại (V11210, 4/4).
3. **MT trên mã mới chấm đúng tập model cũ.** Khoá `model_wr` của bundle MT 28/11 trùng MT 26/11 và 27/11. Tập cũ ∩ model có dòng hôm nay =
   tập mới ∩ model có dòng hôm nay ở cả MN lẫn MT; 4 model bị bỏ mỗi miền có **0** dòng hôm nay.
4. **Lệch 12 ↔ 11 trong chẩn đoán** — `model_wr` có 12 khoá vì `combo-no-token` được tính WR nhưng không bỏ phiếu (`total_models` 11). Đã
   như vậy ở mọi bundle 26–27/11 (mã cũ) ⇒ không do V11210. Không đào thêm: đường dự đoán đóng băng (QD-084).
5. **MB 9/11 đúng thiết kế hai trục:** `model_count` đếm phiếu **sau** cổng WR/BT. Hôm nay random-forest · xgboost bt 10,0% (3/30) < 12%.
   V11210 viết «MB `INCOMPLETE 8/11` mỗi ngày» — chính xác hơn: **8–9/11 tuỳ ngày**, theo số model trượt cổng.
6. **FU-453 — đếm, không đổi nhãn** (`_v11211_dem_fu453.py`, VPS 20:32): [14/09, 28/11) mỗi miền 75 ngày, 0 `COMPLETE`, 0 ngày có
   `daily_eval_log` (dòng cuối 11/09). Ngày `completed_model_count ≥ 11`: MN **60** · MT **56** · MB **34**. Đây là **cận dưới** số ngày
   sẽ COMPLETE nếu phân loại lại — `classify_day_status` cộng thêm model bị trần (V11174), nên chỉ có thể nhiều hơn.
7. **Tên trường sai trong script phát lại V11210** — xem mục 7.

## 4. Hướng xử lý và vì sao chọn

- **Đọc DB thật, không tin chuỗi tự kiểm** (RM-16): mỗi điểm đọc bảng mà luồng sống ghi, ở giờ sau mốc của nó; điểm nào chưa tới giờ in
  `CHUA_TOI_GIO` chứ không đoán trước.
- **Ba lượt theo mốc** (16:48 MN · 17:00:30 MT · 20:30 đủ) thay vì một lượt cuối ngày — bundle MT là lượt mã mới đầu tiên, nếu hỏng cần biết
  trước MB 17:58. Hỏng thì gỡ về (không vá giữa 15:30–18:15).
- **FU-453 chỉ đếm:** phân loại lại 75 ngày là đổi nhãn lịch sử — owner chọn. Số đếm có script commit kèm để tái lập (RM-11).
- **Đóng FU theo từng nhãn**, không đóng hàng loạt: FU-465 · FU-455 · FU-328 đủ điều kiện ghi trong chính mục đó; FU-454 còn `_v10800`
  thứ Hai; FU-255 phần giao diện chờ owner.

## 5. Đã làm gì

| việc | TRƯỚC | SAU | PHIÊN BẢN | KIỂM |
|---|---|---|---|---|
| kiểm trong ngày | C1–C8 `CHUA_TOI_GIO` (sáng 28/11) | 18/18 `DAT` | V11211, 28/11 20:30 | `_v11210_kiem_trong_ngay.py` ⇒ `KIEM_TRONG_NGAY_V11210=DAT` |
| FU-465 · FU-455 · FU-328 | `DEPLOYED_PENDING_LIVE_VERIFY` | `CLOSED_PASS` | V11211 | kho riêng `docs/FOLLOW_UP_TRACKER.md` |
| FU-454 | chờ MB_WATCHDOG + watchdog + `_v10800` | chỉ còn `_v10800` 30/11 | V11211 | C5 · C6 |
| FU-255 | `DEPLOYED_PENDING_LIVE_VERIFY` | `AWAITING_OWNER_OK` (giao diện) | V11211 | — |
| FU-453 | «chờ owner» không số | kèm số MN 60 · MT 56 · MB 34 / 75 | V11211 | `_v11211_dem_fu453.py` ⇒ `DEM_FU453_V11211=XONG` |
| script phát lại | trường `model_bo_phieu` = khoá chẩn đoán | `khoa_chan_doan` · `model_cham_wr` · `total_models` | V11211 | `py_compile` |
| bốn mặt | seq 524 · last V11210 | seq 525 · last V11211 | V11211 | `_v11062_nang_version.py --kiem` ĐẠT |

## 6. Cổng kiểm

| cổng | kết quả |
|---|---|
| `_v11210_kiem_trong_ngay.py` (VPS 20:30:01 · 20:32) | `KIEM_TRONG_NGAY_V11210=DAT (18 đạt · 0 trượt · 0 chưa tới giờ)` |
| `_v11211_dem_fu453.py` (VPS 20:32:10) | `DEM_FU453_V11211=XONG` |
| `_v11062_nang_version.py --kiem` | `NANG_VERSION_V11062=ĐẠT` · seq 525 · last V11211 |
| `_v10920_decision_ledger.py` (sau đồng bộ dữ liệu sống 20:33:59) | «KHÔNG CÓ QUYẾT ĐỊNH NÀO BỊ TRÔI» |
| `_v11044_cong_so_hieu.py` | V11211 trống trước khi cấp · `SO_HIEU_V11044=KHOP` |
| `_v10921_report_gate.py` ① toàn dải · ② `V11211` | xem `CONVERSATION_CONTEXT` mục 4 |

## 7. Vướng vấp

- **Tên trường sai trong `_v11210_phat_lai_bundle.py`.** Script ghi khoá của `source_predictions_json` dưới tên `model_bo_phieu`; dict đó là
  **chẩn đoán** (38 khoá: `bt_gate_threshold`, `model_wr`, …), không phải danh sách model. Phát hiện 17:01 khi dùng lại cách đọc đó cho
  bundle MT. **Kết luận V11210 «cũ = mới» vẫn đúng**: phép so là cả dòng `KQ_BUNDLE` (gồm số, `model_count`), và không câu nào trong báo cáo
  V11210 dựa vào trường đó. Đã sửa tên trường, thêm danh sách model thật (`model_cham_wr`).
- **Tác vụ chờ 16:48 báo «failed» (exit 1)** — do `grep -c` thoát 1 khi đếm ra 0 Traceback, không phải bộ kiểm trượt (nó in `DO_DO`, 0
  trượt). Lượt 17:00 thêm `; true` cuối lệnh.

## 8. Gỡ về

Không áp dụng vì V11211 **không đổi runtime**: hai script mới chỉ đọc (`mode=ro`), script phát lại chỉ chạy trong bản sao thư mục. Gỡ về
V11210 vẫn như báo cáo V11210 mục 8.

## 9. Theo dõi tiếp

| việc | ai chặn | ở đâu |
|---|---|---|
| FU-454 — `_v10800` thứ Hai 30/11 08:10 chỉ đỏ ở chỗ hỏng thật | lịch chạy | kho riêng `docs/FOLLOW_UP_TRACKER.md` |
| FU-453 — có phân loại lại 75 ngày 14/09 → 27/11 không (MN 60 · MT 56 · MB 34 ngày đủ mẫu số) | **owner** | như trên |
| FU-255 / FU-462 — demo giao diện 4 mục, hai câu hỏi trong trang | **owner** | `web/frontend/_v11210_demo_nhan_preview.html` (kho riêng) |
| FU-466 — rút lại các số «P&L theo khuyến nghị `/choi`» từ 28/06 (hạn 05/12) | agent | kho riêng `docs/FOLLOW_UP_TRACKER.md` |
| FU-467 — 6 lane thử nghiệm MN mờ dần từ tháng 8: sửa hay để nghỉ | **owner** | như trên |
| 1D thứ Hai 30/11 (FU-185) | lịch | như trên |
| FU-463 — mật khẩu root mới (hạn 29/11) | **owner** | kho riêng |
| Đợt 2 (2A–2G) · Đợt 3 (3A–3G) | **owner** | kho riêng `docs/FOLLOW_UP_TRACKER.md` FU-462 |
| nhánh báo thật của `OFFICIAL_MODEL_MISSING` — đọc khi lần đầu có model thiếu output | sự kiện | `system_alerts` |

## 10. Ba lớp nguồn (§62)

| lớp | nội dung | bằng chứng |
|---|---|---|
| `OWNER_SAID` | 27/11 ~17:50 duyệt xử lý dứt điểm theo khuyến nghị; 28/11 không nói gì | kho riêng `docs/SO_TUONG_TAC_OWNER.md` 27/11 |
| `CODE_DID` | 28/11: chốt `/choi` 3 miền trước CUTOFF · MN · MT COMPLETE 11/11 · MB 9/11 (cổng BT) · 0 báo động giả · combo-super chấm lại MN · MT | `evidence/KIEM_V11211.txt` |
| `DOC_SAID` | báo cáo V11210 mục 1: «MB vẫn `INCOMPLETE 8/11` mỗi ngày»; FU-465 · FU-455 · FU-328 «còn kiểm trong ngày» | báo cáo `V11210_…/REPORT_V11210.md` · kho riêng `docs/FOLLOW_UP_TRACKER.md` |

**Lệch:** `DOC_SAID` «8/11 mỗi ngày» ≠ `CODE_DID` 9/11 hôm nay — con số đổi theo số model trượt cổng; nay ghi «8–9/11 tuỳ ngày» (không phải số
sai được dùng làm căn cứ quyết định). `DOC_SAID` FU «chờ kiểm» ⇒ đã cập nhật `CLOSED_PASS` theo `CODE_DID` trong cùng phiên.

**TanPhatAI cần làm:** cập nhật FU-465 · FU-455 · FU-328 → `CLOSED_PASS`, FU-255 → `AWAITING_OWNER_OK`; ghi mã V11210 đã chạy sống trọn ngày 28/11
(MN · MT COMPLETE 11/11, MB 8–9/11 do cổng BT là bình thường); ghi số FU-453 (MN 60 · MT 56 · MB 34 / 75 ngày) để owner chọn; theo dõi
`_v10800` thứ Hai 30/11 08:10 (FU-454) và hạn FU-466 05/12. Code đi trước tài liệu: không — hai script và bốn mặt cùng commit `be747cc`.
