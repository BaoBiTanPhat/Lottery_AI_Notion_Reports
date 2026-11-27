# V11204 — Đợt 1 dọn dẹp: dừng 9 lịch hết việc · khai tử vòng AI-limit 01/06 · phán quyết D-30 · thu hẹp `_v10979`

> **Phiên bản:** V11204 · **Ngày:** 27/11/2026, cài lúc 15:24 ICT (trước khung cấm 15:30) · **Repo riêng:** `e922ba9` · **governance_seq:** 518
> · **Quyết định:** QD-083 (owner duyệt C) · QD-072 → `DONG_PHAN_QUYET` · **Tầng (RM-12):** `RUNTIME_PROVEN` cho crontab/mã cron
> (đọc lại trên VPS); kiểm sau triển khai còn chờ lượt MT/MB hôm nay · **Service `lottery`:** không restart.
> *Số `V11203` để trống — đổi thứ tự làm việc trong phiên.*

## 1. Tóm tắt

- Crontab VPS **81 → 73** dòng đang bật. Không xoá dòng nào — dòng dừng mang tiền tố `# V11204 DỪNG …`.
- Vòng AI-limit 01/06 chưa từng được áp (cờ `enabled=0` 178 ngày) nhưng vẫn dán **5 nhãn REDUCED giả** lên model owner đang giữ ⇒ khai tử,
  nhãn giả hết (0 REDUCED).
- D-30 đã phán quyết đúng tiền đăng ký: DIRECT_BASE_ONLY **INCONCLUSIVE_EXTEND** (không kéo dài) · CAP5 **INVALID_EXPERIMENT**.
- `_v10979` từ 240 xuống **146** lượt/ngày, mọi giờ chốt 115 ngày qua vẫn nằm trong khung.

## 2. Owner yêu cầu gì (nguyên văn)

**27/11 ~14:50:** *«C đồng ý theo khuyến nghị nha em.»* · *«==> tất cả kiểm tra đối chiếu , đối soát , xử lý bài bản chuẩn chỉnh dùm anh
nha em. Tinh gọn chính xác ổn định»* (C = Đợt 1 của phương án dọn dẹp 26/11, mục 1B–1J).

## 3. Đào bới / phát hiện — liệt kê ĐỦ

| việc | phát hiện |
|---|---|
| **1B** `_v10708` (05:40 · 20:35) | ghi `mined_rules_m[nt]_daily`; người đọc chỉ còn 2 lane đã nghỉ (cron tắt), probe chạy tay, một khối /du-doan-test. Prompt official chỉ nạp khối luật MN/MT khi có cờ môi trường của lane đã nghỉ (`gpt_analyzer.py:5521`) — service không có cờ đó ⇒ **không chạm prompt** (kiểm ba tầng: bảng · mã · cấu hình) |
| **1C** AI-limit (`_v10645` · `_v10662` · `_v10664` · `_v10665`) | `slice_policy.enabled=0` cả 3 miền; `_v10642_model_progress` đọc danh sách chặn **bỏ qua cờ** ⇒ REDUCED giả cho MN gpt-oss-120b · MT gemini-2.5-flash, claude-opus-4-6 · MB glm-5.1, gpt-oss-120b. **§60:** `_v10647_system_health` canh «weakest_watch cập nhật hôm nay» ⇒ dừng writer mà không sửa thì mỗi giờ báo cũ GIẢ |
| **1E** `_v10869` CP-L6 | ba nhánh A/B gần trùng từ 14/09 (lệch nhiều nhất 19/218 miền-ngày); chỉ panel đọc; tệp phải giữ (cổng `_v10900` dùng) |
| **1F** gan hội tụ (FU-394) | −0,94 điểm, CI95 [−5,5; +3,6]; chỉ API admin đọc |
| **1G** D-30 | 89 tệp ngày (30/08 → 26/11), 6 dòng/ngày; **CAP5 264/264 không có số** (top-5 chưa từng lưu); prereg hash khớp |
| **1H** `_v10979` | 115 ngày: MN 05:15 → 05:33 · MT 16:37 → 16:57:32 · MB 17:31 → 17:46 |
| crontab | kiểm thử khô trước: đúng 12 dòng đổi, 154 dòng y hệt |

## 4. Hướng xử lý và vì sao chọn

Dừng lịch, **giữ bảng và tệp** (QD-082: không xoá khi chỉ cần dừng). 1C sửa tận gốc nhãn giả (đọc đúng cờ `enabled`) thay vì xoá dữ liệu
`slice_policy`. 1G đọc **đúng cửa sổ tiền đăng ký 31/08 → 30/09**; dữ liệu sau đó chỉ in tham khảo (RM-03 · PRJ-SELECTION-WINDOW-001).
Không kéo dài D-30 dù ra EXTEND: cần 897 cặp ≈ 10 tháng, phần ngoài cửa sổ đã bị nhìn (nghiêng về official, p 0,15), lane không gọi
API nên dừng không mất gì đo bù được.

## 5. Đã làm gì

| mã | TRƯỚC | SAU | PHIÊN BẢN | KIỂM |
|---|---|---|---|---|
| 1B | 2 lịch chạy | dừng | V11204 | K1 |
| 1C | 4 lịch + nhãn REDUCED giả | 4 lịch dừng · `_v10642` chỉ tính `enabled=1` · `_v10647` bỏ phép weakest_watch | V11204 | K1 · K3 · K4 = 0 REDUCED |
| 1E | lịch 21:20 | dừng · CP-L6 ĐÓNG (lộ trình ghi rõ) | V11204 | K1 |
| 1F | lịch 21:40 | dừng · FU-394 `CLOSED_REPORT` | V11204 | K1 |
| 1G | lane 19:15, quá ngày đọc 58 ngày | phán quyết + dừng · QD-072 `DONG_PHAN_QUYET` | V11204 | `evidence/d30_phan_quyet.txt` |
| 1H | mỗi phút 05–06h · 16h · 17h | MN 05:10–06:30 · MT 16:30–16:59 · MB 17:25–17:59 | V11204 | K2 |
| 1I | — | chưa gộp (theo khuyến nghị) | — | — |
| 1D · 1J | — | thứ Hai 30/11 · lần restart gộp 28/11 | — | FU-185 · FU-255 |

**Phán quyết D-30** (`web/backend/_v11204_d30_phan_quyet.py`, chỉ đọc):

| lane | cửa sổ | n | lane | official | nền | b / c | p | n cần | phán quyết |
|---|---|---|---|---|---|---|---|---|---|
| DIRECT_BASE_ONLY | 31/08→30/09 | 93 | 35,5% | 31,2% | 33,6% | 13 / 9 | 0,523 | 897 | **INCONCLUSIVE_EXTEND** — chưa được phép kết luận |
| DIRECT_BASE_ONLY | 01/10→26/11 *(ngoài cửa sổ, không dùng)* | 171 | 35,1% | 40,9% | 34,3% | 15 / 25 | 0,154 | 887 | — |
| CAP5_CANDIDATE_PRESERVING | 31/08→30/09 | 0 | — | — | — | — | — | — | **INVALID_EXPERIMENT** |

## 6. Cổng kiểm

| cổng | kết quả |
|---|---|
| `_v11204_kiem_dot1.py` (K1–K4, đọc VPS) | `DOT1_V11204=DAT` |
| `_v11204_kiem_dot1.py --thu-chan` (RM-15) | 7/7: sạch ⇒ ĐẠT; 6 vi phạm giả ⇒ TRƯỢT |
| `_v11204_sua_crontab.py` | thử khô 12 dòng đổi; cài xong đọc lại khớp; 73 dòng bật |
| `_v11062_nang_version.py --kiem` | ĐẠT |
| `_v10920_decision_ledger.py` | QD-072 🟢 6/6 · QD-083 🟢 2/2 · 0 TRÔI |
| `_v10921_report_gate.py` ② `V11204` | xem `CONVERSATION_CONTEXT` §4 |

## 7. Vướng vấp

- Câu khuyến nghị 26/11 «1G nhiều khả năng ra INVALID» chỉ đúng cho CAP5 — đã ghi sửa.
- Bản nháp cổng K4 giả định cột `computed_at` không có thật (RM-10) — đọc schema rồi sửa (`model_progress` giữ trạng thái hiện tại).
- Chạy cổng ở máy Windows: `subprocess` giải mã cp1252 vỡ chữ Việt — thêm `encoding="utf-8"`.

## 8. Gỡ về

`crontab /root/Lottery_AI_Test/backups/crontab.pre_v11204.txt` · khôi phục `backups/_v10642_model_progress.py.pre_v11204`,
`backups/_v10647_system_health.py.pre_v11204` · tài liệu: `git revert e922ba9`.

## 9. Theo dõi tiếp — liệt kê ĐỦ

| mã | việc | ai | hạn |
|---|---|---|---|
| FU-462 | kiểm sau triển khai: `_v10647` không thêm cảnh báo; `_v10979` ghi «ĐÃ XONG» MT/MB hôm nay trong khung hẹp | agent | 27/11 tối |
| FU-185 | 1D `.sh` lane MB | agent | 30/11 |
| FU-255 | 1J nối `system_alerts` + nhãn «đã đóng» cho panel 1B/1E/1F — restart gộp, demo giao diện trước | agent → owner xem demo | 28/11 |
| FU-462 | Đợt 2 (2A–2G) · Đợt 3 (3A–3G) | owner | 03/12 |

## 10. Ba lớp nguồn (§62)

| lớp | nội dung | bằng chứng |
|---|---|---|
| `OWNER_SAID` | «C đồng ý theo khuyến nghị» — 27/11 ~14:50 | kho riêng `docs/SO_TUONG_TAC_OWNER.md` |
| `CODE_DID` | 9 lịch dừng · 1H khung hẹp · 0 REDUCED · D-30 phán quyết | `_v11204_kiem_dot1.py` = DAT · `evidence/d30_phan_quyet.txt` |
| `DOC_SAID` | phương án 26/11: «1G nhiều khả năng INVALID_EXPERIMENT»; «1C khai tử cả cụm» (không nhắc `_v10647`) | `docs/KE_HOACH_DON_DEP_20261126.md` mục 1C · 1G |

**Lệch:** `DOC_SAID` ≠ `CODE_DID` ở hai chỗ — 1G lane 1 ra EXTEND chứ không INVALID; 1C cần sửa thêm `_v10647` mới không đẻ báo động giả.
Đã ghi đúng ở CHANGELOG V11204.

**TanPhatAI cần làm:** cập nhật FU-462/FU-394/FU-185/FU-255 và QD-072 (`DONG_PHAN_QUYET`, thay bởi QD-083); ghi CP-L6 đã đóng. Code đi
trước tài liệu: không — crontab đổi và tài liệu cùng bản V11204.
