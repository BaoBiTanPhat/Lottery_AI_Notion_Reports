# V11207 — QD-084 owner duyệt · RL-053 (thiệt cài sẵn của lô là 2%, không phải 10%/14%) · 8 mục giao diện · chạy khô dọn cờ chết

> **Phiên bản:** V11207 · **Ngày:** 27/11/2026 ~17:35 → 18:20 ICT · **Repo riêng:** `07a2def` · **governance_seq:** 521 · **Quyết định:** QD-084
> · **Rút lại:** RL-053 · **Tầng (RM-12):** `REPORT_PROVEN` trên số đo `RUNTIME_PROVEN` (DB VPS chỉ đọc) · **Runtime đổi:** không (áp mã 28/11).

## 1. Tóm tắt

- Owner duyệt (QD-084): không chuyển Hermes để mong dự đoán tốt hơn · viết bản đúc kết · cổng máy cho thử nghiệm mới · **đóng băng** đường
  dự đoán · FU-464 hướng 1 · **không thêm, không cắt model theo chất lượng** · dọn cờ chết.
- Chạy khô dọn cờ chết: mỗi miền 15 → **11**, **0 dòng** dự đoán của model bị bỏ ⇒ phiếu công bố **y hệt**. Áp mã 28/11 06:35.
- **RL-053:** con số «thiệt cài sẵn khoảng 10% ở MN/MT và 14% ở MB» (V10945, 01/08) **sai** — lô trả theo nháy ⇒ thiệt thật **2,0%**.
- 8 mục giao diện FU-459: 5 ĐẠT · 3 giữ mở có lý do. FU-459 đóng.

## 2. Owner yêu cầu gì (nguyên văn)

27/11 ~17:35: *«OK ĐỒNG Ý VỚI ĐỀ XUẤT NHƯNG CÒN 1 ĐIỂM NỮA LÀ CÁC MODEL HIỆN TẠI CÒN BAO NHIÊU MODEL CÓ CẦN CẮT GIẢM BỔ SUNG MODEL NÀO
KHÔNG EM?»* · ~17:50: *«OK ANH DUYỆT THEO KHUYẾN NGHỊ EM. EM TIẾN HÀNH XỬ LÝ HOÀN TẤT DỨT ĐIỂM SẠCH SẺ DÙM ANH»*

## 3. Đào bới / phát hiện — liệt kê ĐỦ

| phép | kết quả |
|---|---|
| đếm model từ mã + DB VPS (§59) | registry 49 · cờ output 15 (3 cờ chết: `deepseek-reasoner`, `gemini-2.5-pro`, `gpt-5.4`) · bỏ phiếu thật **11/miền** · pool AI combo-super 9 tên, 4 còn chạy/miền |
| từng model gộp 3 miền 14/09→26/11 | Opus z +2,33 · lstm +2,22 · combo-no-token +2,08 … xgboost −1,67; 13 phép so ⇒ cần |z| ≈ 2,9 — không model nào được phép kết luận |
| mẫu số «15 model» | mọi ngày bị gắn INCOMPLETE ⇒ loại khỏi đánh giá chính (gốc FU-453); một nguồn khác trong mã đã tính theo miền — hai định nghĩa song song |
| chạy khô dọn cờ chết | xem mục 5 |
| ngưỡng hoà vốn trong tài liệu cũ | so «xác suất ≥1 nháy» với 18/98 — sai phép vì lô trả theo nháy (RL-053) |
| luật «official đúng 15/15» | còn ở 4 mặt quy tắc sửa tay — lệch mã từ 14/09 |
| 8 mục giao diện | builder chạy thật trên VPS · route 401 · dấu HTML: ĐẠT FU-149 · 152 · 153 · 156 · 118; FU-154 · 155 tab trống trên VPS (thư mục dữ liệu chỉ ở máy dev); FU-131 khối đọc bảng chấm đứng từ 03/08 |
| vấp | khối đóng V11205 ghi «hạn 27/11» (ngày đóng) cho FU-186/FU-203 ⇒ cổng lịch QD-021 đỏ; sửa về hạn đã xếp 08/08, cổng ĐẠT 8/8 |

## 4. Hướng xử lý và vì sao chọn

Không cắt/thêm model theo những chênh chưa đủ mức — đó chính là kiểu thử nghiệm không phương pháp owner vừa phê. Dọn cờ chết chỉ được làm khi
**chứng minh trước** phiếu không đổi. Rút lại số sai tại **đúng chỗ đã công bố** (PRJ-RETRACTION-001), kể cả báo cáo công khai cũ.

## 5. Đã làm gì

| việc | TRƯỚC | SAU | KIỂM |
|---|---|---|---|
| chạy khô (`_v11207_chay_kho_co_chet.py`) | danh sách bỏ phiếu 15/miền | 11/miền | 0 dòng của model bị bỏ 14/09→27/11; nhãn ngày MN 75 INCOMPLETE → 60 COMPLETE · MT 56 · MB 34 (phần thiếu là sự cố thật) |
| thiệt cài sẵn (`_v11207_thiet_cai_san.py`) | «10% / 14%» | **2,00%** MN · MT · MB | 781 lượt đài: 18 giải/đài ⇒ 0,18 nháy/số ⇒ 17.640đ/18.000đ; MB 27 ⇒ 26.460đ/27.000đ |
| RL-053 | — | ghi tại 4 chỗ gốc + `docs/SO_RUT_LAI.json` | `_v11085_cong_rut_lai.py` |
| QD-084 | — | sổ quyết định | `_v10920_decision_ledger.py` 0 TRÔI |
| FU | FU-459 mở · FU-464 chờ owner | FU-459 đóng · FU-464 → demo giao diện · FU-465 mở (thi hành 28/11) | bộ đọc sổ 0 mồ côi |

## 6. Cổng kiểm

| cổng | kết quả |
|---|---|
| `_v11207_chay_kho_co_chet.py` | `CHAY_KHO_V11207=DAT` |
| `_v10981_kiem_lich.py` (QD-021) | ĐẠT 8/8 (sau khi sửa hạn FU-186/FU-203) |
| `_v10920_decision_ledger.py` | 0 TRÔI |
| `_v11062_nang_version.py --kiem` | ĐẠT |
| `_v10921_report_gate.py` ② `V11207` | xem `CONVERSATION_CONTEXT` §4 |

## 7. Vướng vấp

- Đoán tên hằng số (`ROSTER`) khi viết chạy khô — sai, đọc tên thật `_CHINH_SACH` rồi chạy lại (RM-10).
- Hàm chèn rút lại kiểm chữ «RL-053» trên cả tệp nên bỏ qua 2 chỗ gốc (vì khối mới đã chứa chữ đó) — sửa kiểm vùng ngay sau mốc.
- Ghi ngày đóng vào chỗ hạn ⇒ cổng lịch đỏ — sửa trong cùng bản.

## 8. Gỡ về

Không đổi runtime. Tài liệu: `git revert 07a2def`; báo cáo công khai V10945 khôi phục từ bản sao `.pre_v11207` ở kho riêng.

## 9. Theo dõi tiếp — liệt kê ĐỦ

| mã | việc | ai | hạn |
|---|---|---|---|
| FU-465 | áp mã dọn cờ chết + mẫu số theo roster (restart gộp, so PID) · sửa luật 15/15 ở 4 mặt + sinh lại 2 mặt · cổng thử nghiệm · bản đúc kết | agent | 28/11 |
| FU-464 | nhãn «chưa có lợi thế đo được» trên `/du-doan`, `/choi` — demo cho owner xem trước | agent → owner | 28/11 |
| FU-154 · 155 · 131 | tab trống / khối chặn bởi bộ chấm | agent / owner (2A) | 15/12 · 03/12 |

## 10. Ba lớp nguồn (§62)

| lớp | nội dung | bằng chứng |
|---|---|---|
| `OWNER_SAID` | duyệt khuyến nghị, giao làm dứt điểm | kho riêng `docs/SO_TUONG_TAC_OWNER.md` 27/11 ~17:35 · ~17:50 |
| `CODE_DID` | mỗi miền bỏ phiếu 11 model; thiệt cài sẵn 2,0% | `evidence/` |
| `DOC_SAID` | «official đúng 15/15» · «thiệt cài sẵn 10%/14%» | `CLAUDE.md:866` · CHANGELOG § V10945 |

**Lệch:** `DOC_SAID` ≠ `CODE_DID` ở cả hai câu — câu thứ hai đã rút lại (RL-053); câu thứ nhất sửa cùng lần áp mã 28/11 (FU-465).

**TanPhatAI cần làm:** ghi RL-053 (thiệt cài sẵn của lô là 2,0%), QD-084, FU-465 (28/11), FU-464 (chờ owner xem demo). Code đi trước tài liệu: không.
