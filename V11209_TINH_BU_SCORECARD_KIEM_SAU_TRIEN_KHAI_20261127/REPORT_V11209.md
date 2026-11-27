# V11209 — Tính bù bảng xét thăng hạng 14/09→24/11 · kiểm sau triển khai Đợt 1 · lane rc≠0 nay giữ lỗi

> **Phiên bản:** V11209 · **Ngày:** 27/11/2026 ~18:50 → 22:20 ICT · **Repo riêng:** `40515ea` · **governance_seq:** 523 · **Quyết định:** QD-083 B
> · **Tầng (RM-12):** `DEPLOYED` (tệp `_v10979_early_block.py` đã lên VPS, chạy bằng cron) · tính bù DB đã ghi và đọc lại · bản vá rc≠0
> **chưa** `RUNTIME_PROVEN` — chỉ chứng minh được khi lane trả rc≠0 lần sau.

## 1. Tóm tắt

- **FU-451 (b) xong:** bảng xét thăng hạng shadow (`shadow_model_promotion_scorecard_daily`) trống 14/09 → 24/11 nay đủ — **216 miền-ngày,
  5.832 dòng**, mỗi dòng mang nhãn `TINH_BU_V11205`. 14/09 → 27/11 đủ **75/75 ngày** mỗi miền. Băm 4 bảng khoá trước = sau.
- **Kiểm sau triển khai Đợt 1 dọn dẹp (V11204) ĐẠT:** không cảnh báo mới; «ĐÃ XONG» đúng giờ cả ba miền trong khung chạy đã thu hẹp; lane
  Nghiệm Thu có số cả ba miền.
- **Lỗi cũ rc=1 của lane Nghiệm Thu** (21 lần từ 08/08) chưa từng để lại nguyên nhân vì lỗi bị bỏ. Nay `_v10979` giữ ba dòng cuối của lỗi.

## 2. Owner yêu cầu gì (nguyên văn)

| giờ (ICT) | nguyên văn |
|---|---|
| 27/11 ~14:50 | *«B. Ba câu cũ đang treo ==> cái này em cần kiểm tra tra soát đối chiếu chứ em»* (QD-083 B: FU-345 · FU-459 · FU-451 b) |
| 27/11 ~17:50 | *«OK ANH DUYỆT THEO KHUYẾN NGHỊ EM. EM TIẾN HÀNH XỬ LÝ HOÀN TẤT DỨT ĐIỂM SẠCH SẺ DÙM ANH»* |

Không có lời owner mới trong khoảng 18:50 → 22:20.

## 3. Đào bới / phát hiện

1. **Bảng tính bù trước khi ghi:** 0 dòng trong 14/09 → 24/11 (kiểm lúc 22:08) ⇒ không có gì để đè.
2. **Đọc lại sau khi ghi (RM-16):** mỗi miền 75 ngày, 2.025 dòng trong 14/09 → 27/11; 0 miền-ngày có kết quả xổ mà thiếu dòng; ngày biên 13/09
   (trước vùng) và 25/11 (cron tự nhiên) cùng 27 dòng/ngày như vùng tính bù.
3. **Ai đọc bảng này (RM-20):** cron `_v10644_shadow_scoreboard.py` 09:10 hằng ngày. Bảng chỉ để đo, không đổi quyền bỏ phiếu của model nào.
4. **Kiểm 18:50 cho Đợt 1:** MN 05:16:50 · MT 16:43:39 · MB 17:36:39 — «ĐÃ XONG» trùng giờ bản chốt cuối; `_v10647` 0 mục không OK;
   crontab 73 dòng. Lane Nghiệm Thu 27/11: MN `17` · MT `98` · MB `55`.
5. **MT hôm nay ghi `rc=1`** ⇒ tra lịch sử: 21 dòng `rc=1` — MN 8 (10/08 → 13/09) · MT 8 (08/08 → 27/11) · MB 5 (18/08 → 30/10). 19 dòng tới
   30/10 khớp con số «trượt 19 lần» trong kế hoạch dọn dẹp 26/11; thêm MT 26/11 và 27/11. **Cả 21 ngày đều có số Nghiệm Thu** — các lượt
   cron sau đã bù. Đây là lỗi **cũ**, không do Đợt 1 gây ra.
6. **Vì sao 21 lần không ai biết nguyên nhân:** lane chết **trước dòng in đầu tiên** (đầu ra trống), còn dòng lỗi thì hàm gọi lane bỏ đi.
   Giả thuyết «cơ sở dữ liệu đang bị khoá đúng lúc chuỗi chính thức vừa ghi» (kết nối chờ mặc định 5 giây) **chưa được chứng minh**.
7. **Không kết luận được lượt nào đã bù:** giờ trong bảng Nghiệm Thu là giờ **chấm**, không phải giờ chốt số.

## 4. Hướng xử lý và vì sao chọn

- **Tính bù:** chạy đúng script V11205 đã thử tương đương 42/42 mẫu với hàm gốc, chặn tự động nếu vùng đã có dòng, gắn nhãn để gỡ được.
- **rc=1:** **không** đoán rồi vá (RM-10). Kế hoạch dọn dẹp ghi phải điều tra rc=1 **trước** khi cắt 8 lượt predraw ⇒ bước đúng là cho lỗi
  tự để lại dấu: giữ ba dòng cuối của lỗi, giữ nguyên tiền tố `rc=N` để các truy vấn cũ vẫn khớp. Không đụng lane, không đụng chuỗi chính thức.
- **Không restart:** hàm sửa chỉ chạy từ cron; service chỉ dùng `compute_view` (không đổi) của tệp này.

## 5. Đã làm gì

| việc | TRƯỚC | SAU | PHIÊN BẢN | KIỂM |
|---|---|---|---|---|
| tính bù bảng xét thăng hạng | 14/09 → 24/11 trống | 216 miền-ngày · 5.832 dòng · nhãn `TINH_BU_V11205` | V11205 script, chạy 27/11 22:08 (46 giây) | `TINH_BU_V11205=DAT` · đọc lại 75/75 ngày/miền · băm 4 bảng khoá trước = sau |
| `_v10979_early_block._kich_hoat_lane` | rc≠0 ⇒ chỉ ghi `rc=1` | rc≠0 ⇒ `rc=N … · ERR: <ba dòng cuối lỗi>` (≤ 300 ký tự) | V11209, 27/11 ~22:12, lên VPS, sha hai bên khớp | `_v11209_thu_bat_loi_kich_hoat.py` 3/3 ở máy dev và trên VPS |
| bốn mặt + theo dõi | — | CHANGELOG · SSOT · STATE (seq 523) · HISTORY; FU-451 `CLOSED_PASS`; FU-462 cập nhật | V11209 | `_v11062_nang_version.py --kiem` ĐẠT |

Bằng chứng: `evidence/KIEM_V11209.txt`.

## 6. Cổng kiểm

| cổng | kết quả |
|---|---|
| `_v11205_tinh_bu_scorecard.py --ap-dung` | `TINH_BU_V11205=DAT` |
| `_v11033_bam_4_bang.py` trước / sau | `predictions` · `final_bundles` · `lottery_results` · `model_daily_eval` y hệt (RM-02: chỉ chứng minh không ghi bậy) |
| `_v11209_thu_bat_loi_kich_hoat.py` | 3/3 máy dev · 3/3 VPS |
| `_v11062_nang_version.py --kiem` | ĐẠT |
| cổng commit (gồm cổng thử nghiệm mới V11208) | qua — `40515ea` |
| `_v10921_report_gate.py` ① toàn dải · ② `V11209` | xem `CONVERSATION_CONTEXT` §4 |

## 7. Vướng vấp

- Đoán tên cột `model_id` trong bảng xét thăng hạng — sai (RM-10); tên thật là `ai_model`. Tra `PRAGMA table_info` rồi chạy lại.
- Ca thử thứ hai ở máy dev hỏng lần đầu vì **lane giả** in tiếng Việt ra console cp1252 — lỗi của bài thử, không phải của bản vá (lane thật
  tự đặt utf-8). Chính lần hỏng đó cho thấy bản vá bắt đúng lỗi.
- Tệp băm 4 bảng chưa có trên VPS — đẩy lên rồi mới băm.
- Ghi giờ ước «~22:20 / ~22:25» vào hai khối tài liệu, đồng hồ thật là 22:14 — sửa trước commit.

## 8. Gỡ về

- Tính bù: `DELETE FROM shadow_model_promotion_scorecard_daily WHERE notes LIKE '%TINH_BU_V11205%'`.
- Bản vá: chép lại `backups/_v10979_early_block.py.pre_v11209` (có ở máy dev và VPS).
- Tài liệu: `git revert 40515ea`.

## 9. Theo dõi tiếp

| mã | việc | ai | hạn |
|---|---|---|---|
| FU-462 | lần rc=1 sau: đọc `lane_ket_qua` ⇒ có nguyên nhân thật mới xét cắt 8 lượt predraw | agent | khi xảy ra |
| FU-465 (a) | dọn cờ chết + mẫu số theo roster — restart gộp, so PID | agent | 28/11 06:35 |
| FU-455 | khoá khuyến nghị `/choi` lúc chốt — cùng lần restart | agent | 28/11 |
| FU-462 1J | nối cảnh báo vào `system_alerts` — cùng lần restart; giao diện demo trước | agent → owner | 28/11 |
| FU-464 | nhãn «chưa có lợi thế đo được» — demo cho owner | agent → owner | 28/11 |
| FU-185 / 1D | `.sh` lane MB | agent | 30/11 |
| FU-463 | owner tự đặt mật khẩu root mới | owner | 29/11 |
| FU-462 | Đợt 2 (2A–2G) · Đợt 3 (3A–3G) | owner chốt | — |

## 10. Ba lớp nguồn (§62)

| lớp | nội dung | bằng chứng |
|---|---|---|
| `OWNER_SAID` | giao agent tra soát rồi xử FU-451 b; duyệt xử lý dứt điểm | kho riêng `docs/SO_TUONG_TAC_OWNER.md` 27/11 ~14:50 · ~17:50 |
| `CODE_DID` | 5.832 dòng tính bù; `_kich_hoat_lane` giữ lỗi khi rc≠0 | `evidence/KIEM_V11209.txt` · `web/backend/_v10979_early_block.py` |
| `DOC_SAID` | kế hoạch dọn dẹp: «trượt 19 lần … phải điều tra lỗi rc=1 trước» | kho riêng `docs/KE_HOACH_DON_DEP_20261126.md:194` |

**Lệch:** không có — 19 lần trong kế hoạch khớp số đếm tới 30/10; 21 là số mới tính cả 26/11 và 27/11.

**TanPhatAI cần làm:** ghi FU-451 đã đóng (bảng xét thăng hạng shadow đủ 14/09 → 27/11, 216 miền-ngày mang nhãn `TINH_BU_V11205`); theo dõi
lần rc=1 kế tiếp của lane Nghiệm Thu — `lane_ket_qua` nay có ` · ERR:` — để có nguyên nhân trước khi xét cắt 8 lượt predraw. Code đi trước
tài liệu: không.
