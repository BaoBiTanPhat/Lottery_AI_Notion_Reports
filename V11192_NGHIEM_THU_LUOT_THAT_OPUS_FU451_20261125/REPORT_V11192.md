# V11192 — Nghiệm thu lượt thật 25/11: Opus chạy lại ở MT/MB, vá stdout FU-451a đạt, sửa nhãn mồ côi FU-452

> **Phiên bản:** V11192 · **Ngày:** 25/11/2026 13:37 → 18:5x ICT · **Repo riêng:** `Lottery_AI_Test` commit `15fe1c7`
> (nhánh `fu438/admin-only-p0a` + `master`) · **governance_seq:** 507 · **Tầng (RM-12):** FU-451a `RUNTIME_PROVEN` ·
> FU-452 `RUNTIME_PROVEN` cho MT/MB, MN chờ 26/11 · **Runtime đổi:** không — phiên chỉ đọc trên VPS.
>
> ⚠ **RÚT LẠI — RL-052 (26/11/2026, V11199):** «FU-451a `RUNTIME_PROVEN`» là **SAI**. Print của service vẫn chết sau 19:20 mỗi ngày (`_materialize_v94_safe_batch` / `_materialize_v95_data_integrity_audit` thay `sys.stdout` lúc import, nạp bằng `importlib` lúc 19:18/19:20; cổng V11189 mù `importlib`). Phép kiểm ở bản này chỉ soi tới 18:45. Đo 25/11 19:21–21:00: print 0 dòng. Vá ở V11199.

## 1. Tóm tắt

- Bài kiểm hẹn sẵn ở V11191 chạy **18:45** trên VPS, **thoát 0**, cả hai phần **ĐẠT**.
- **FU-452:** `claude-opus-4-6` ra số thật, không lỗi, ở **MT 16:36** và **MB 17:31** (`ai_chain`). MT và MB mỗi miền
  có đủ **4 model AI** đúng roster `QD-080`. MN hôm nay còn 2 model AI vì lượt MN 05:15 chạy **trước** lúc nhả cách
  ly (13:17). MN chờ lượt 05:15 ngày **26/11**.
- **FU-451a:** sổ điểm xét thăng hạng (`SHADOW-PROMOTION-SCORECARD`) ghi đủ 3 miền, `inserted=27` mỗi miền;
  `closed file` = 0; journal có lại dòng `print()`; PID `1122833` không đổi.
- **Tự sửa lỗi V11191:** khối FU-452 mang nhãn `DEPLOYED`, nhãn này ngoài từ vựng của bộ đọc sổ theo dõi ⇒ FU-452
  thành «mồ côi», rơi khỏi mọi bộ đếm. Nay đổi sang `DEPLOYED_PENDING_LIVE_VERIFY`.
- Owner hỏi lúc 13:37 vì sao nạp tiền DeepSeek lại «phí». Câu trả lời thẳng: **tiền DeepSeek chưa cần** cho vận hành
  hiện tại. Danh sách sáng 25/11 có ghi điều này nhưng để ở chú thích, không đủ nổi. 19,94 USD còn nguyên.

## 2. Owner yêu cầu gì (nguyên văn) — §62 lớp `OWNER_SAID`

| giờ (ICT) | nguyên văn | loại |
|---|---|---|
| 25/11 ~13:37 | *"là sao anh nạp tiền phí phạm vậy em? Chốt lại em cần list ra việc cần anh làm , chốt. việc em xử lý ngay và việc em làm sau khi anh chốt và làm là gì liệt kê cụ thể tiếp dùm a"* | HỎI + YÊU_CẦU |

Dòng này đã vào `docs/SO_TUONG_TAC_OWNER.md` lúc 13:3x (commit `3cd9943`). Owner không nói thêm gì trong phiên.
Việc kiểm lượt thật 18:45 **không phải yêu cầu mới** — đó là bước nghiệm thu V11191 đã hẹn (`FU-452`, `FU-451`).

## 3. Đào bới / phát hiện — liệt kê ĐỦ

### 3.1 Số dư và lý do «phí» (trả lời câu 13:37)

- DeepSeek đo lại lúc 13:38 qua cổng tra số dư (không gọi model): **19,94 USD**. Hai lượt gọi thử lúc 13:17 tốn dưới
  0,01 USD.
- OpenRouter (chạy `gpt-oss-120b`, `glm-5.1`): **6,29 USD**, khoảng 0,05 USD/ngày.
- DeepSeek **ngoài roster `QD-080` từ 14/09** ⇒ cổng `uy_quyen_goi` trả `DENY_OUTSIDE_ROSTER` ở mọi lớp (đo V11191).
  Có tiền mà không được gọi.
- Gốc: danh sách chốt gửi owner lúc ~11:58 ghi «OpenAI và DeepSeek không cần nạp» ở chú thích dưới bảng. Owner đọc
  bảng và nạp cả hai. **Lỗi trình bày của agent**, không phải của owner.
- Không kết luận gì về hoàn tiền: agent không có bằng chứng về chính sách của DeepSeek.

### 3.2 Lượt thật FU-452 (`_v11191_kiem_luot_that.py 2026-11-25`, VPS 18:45)

| giờ tạo (VN) | miền | model | đường | số ra | lỗi |
|---|---|---|---|---|---|
| 16:36 | MT | `claude-opus-4-6` | `ai_chain` | `["98", "24"]` | không |
| 17:31 | MB | `claude-opus-4-6` | `ai_chain` | `["49"]` | không |

| miền | model AI có dòng `predictions` 25/11 |
|---|---|
| MN | 2 — `gemini-2.5-flash` · `gpt-oss-120b` (lượt 05:15 chạy trước khi nhả) |
| MT | 4 — `claude-opus-4-6` · `gemini-2.5-flash` · `glm-5.1` · `gpt-oss-120b` |
| MB | 4 — `claude-opus-4-6` · `gemini-2.5-flash` · `glm-5.1` · `gpt-oss-120b` |

Cách ly lúc 18:45 còn đúng `gpt-5-mini`, `gpt-5.4`. Không Claude nào bị cách ly lại.

Kết quả xổ (`PARTIAL` MT, `LOSE` MB) **không thuộc phép nghiệm thu**. Một ngày một model là **chưa được phép kết
luận** về chất lượng (`RM-04`).

### 3.3 FU-451a — vá stdout (V11189)

| nguồn | MN | MT | MB |
|---|---|---|---|
| `scheduler_logs` (UTC naive → +7, §55 quy ước thứ tư) | 16:34 `inserted=27` | 17:30 `inserted=27` | 18:32 `inserted=27` |
| journal `lottery` | 16:34:57 | 17:30:23 | 18:32:55 |

`closed file` từ 04:30 VN: 0 trong `scheduler_logs`, 0 trong journal. Journal: 6.689 dòng từ 04:30. MainPID `1122833`
trước và sau như nhau.

### 3.4 FU-452 rơi thành «mồ côi» từ V11191

`web/backend/_v10958_fu_reader.py` lấy token đầu ô `**status**`. V11191 ghi `DEPLOYED` — không có trong
`TREO_STATUSES` lẫn `DONG_STATUSES` ⇒ `trang_thai_mo_coi()` trả FU-452. Cổng commit (`_v10980_mk_commit`) chỉ cảnh
báo, nên commit V11191 vẫn qua. Cùng họ với V10980 (14 mục tàng hình) và FU-430 (nhãn in đậm, 72 ngày mồ côi).

Kiểm sau sửa (`evidence/q_mo_coi_fu_sau.txt`): FU-452 = `DEPLOYED_PENDING_LIVE_VERIFY`, FU-451 =
`OWNER_DECISION_NEEDED`, danh sách mồ côi **trống**.

## 4. Hướng xử lý và vì sao chọn

- **Chỉ đọc, không chạy bù.** Lượt MN 25/11 thiếu Opus là đúng thời điểm; chạy dự đoán bù sau giờ xổ là rò dữ liệu
  tương lai. Chờ lượt tự nhiên 26/11.
- **Sửa nhãn bằng khối mới trên cùng**, không sửa khối V11191. Sổ theo dõi chỉ thêm khối; bộ đọc lấy khối đầu.
- **Chọn `DEPLOYED_PENDING_LIVE_VERIFY` cho FU-452**, không chọn nhãn ĐÓNG: MN còn chờ. Theo nguyên tắc ghi trong bộ
  đọc, chiều an toàn là TREO.
- **FU-451 sang `OWNER_DECISION_NEEDED`:** phần (a) xong, phần còn lại (b) là quyết định tính bù của owner.
- **DeepSeek: khuyến nghị giữ làm dự phòng.** Đổi roster lúc Opus vừa quay lại là hai biến cùng lúc (`QD-018`).
  Khi OpenRouter gần cạn, thay DeepSeek vào `gpt-oss-120b`/`glm-5.1` thì không phải nạp thêm OpenRouter.

## 5. Đã làm gì

1. 13:38 — đo lại số dư DeepSeek (19,94 USD) và OpenRouter (6,29 USD); trả lời owner kèm danh sách A/B/C cập nhật.
2. 18:45 — bài kiểm nền (hẹn từ V11191) chạy `_v11191_kiem_luot_that.py` trên VPS + đếm `closed file` trong journal +
   đọc MainPID. Thoát 0.
3. 18:4x — đọc thêm journal: dòng `SHADOW-PROMOTION-SCORECARD` cả 3 miền, số dòng từ 04:30.
4. Phát hiện FU-452 mồ côi, đọc từ vựng `_v10958_fu_reader.py` (dòng 92–171).
5. Sao lưu `CHANGELOG.md`, `CURRENT_TRUTH_SSOT.md`, `AUTOMATION_STATE.json`, `FOLLOW_UP_TRACKER.md` →
   `backups/*.pre_v11192`.
6. Chạy `web/backend/_v11192_ghi_tai_lieu.py`: bốn mặt §63 (seq 507) + khối FU-452, FU-451.
7. Commit `15fe1c7`, đẩy lên nhánh và `master`.

**TRƯỚC / SAU (§60.4):**

| | TRƯỚC | SAU | PHIÊN BẢN | KIỂM |
|---|---|---|---|---|
| FU-452 status | `DEPLOYED` (mồ côi) | `DEPLOYED_PENDING_LIVE_VERIFY` | V11191 → V11192 | `trang_thai_mo_coi()` = `[]` |
| FU-451 status | `DEPLOYED_PENDING_LIVE_VERIFY` | `OWNER_DECISION_NEEDED` (a đạt) | V11189 → V11192 | `load_fu_latest()` |

## 6. Cổng kiểm

| cổng | kết quả |
|---|---|
| `_v11191_kiem_luot_that.py 2026-11-25` (VPS) | FU-452 ĐẠT · FU-451a ĐẠT · thoát 0 |
| `_v11044_cong_so_hieu.py V11192` | số trống, khớp |
| `_v11062_nang_version.py --kiem` | `NANG_VERSION_V11062=ĐẠT` (seq 507, last_version V11192) |
| `_v10920_decision_ledger.py` | 0 TRÔI · 1 «không kết luận được» vì DB local cũ (RM-01), không đọc thành TRÔI |
| `_v11027_so_muc_quan_tri.py` | không mục nào biến mất |
| `_v10921_report_gate.py` ① toàn dải + ② `V11192` | xem `CONVERSATION_CONTEXT` §4 |

## 7. Vướng vấp

- **Danh sách chốt sáng 25/11 để câu «DeepSeek không cần nạp» ở chú thích.** Owner nạp tiền không cần thiết. Lần sau:
  việc không cần làm phải ghi thẳng trong bảng việc của owner, có cột «KHÔNG cần làm».
- **Nhãn `DEPLOYED` ở V11191** — agent dùng tên tầng RM-12 làm nhãn trạng thái mà không tra từ vựng bộ đọc. Cổng commit
  chỉ cảnh báo nên không bắt.

## 8. Gỡ về

Phiên không đổi runtime. Gỡ tài liệu: `git revert 15fe1c7` trong `Lottery_AI_Test`. Bản sao trước khi ghi:
`backups/*.pre_v11192`.

## 9. Theo dõi tiếp — liệt kê ĐỦ

| mã | việc | ai chặn | khi nào |
|---|---|---|---|
| `FU-452` | MN có Opus + Sonnet ra số ⇒ đóng phần chạy lại | lượt tự nhiên | 26/11 sau 05:20 |
| `FU-452` | DeepSeek giữ dự phòng hay thay ngay | owner | — |
| `FU-451b` | tính bù bảng xét thăng hạng 14/09→24/11 | owner | — |
| `FU-453` | sổ điểm combo-super: phương án A/B/C | owner | — |
| `FU-459` | đổi nhãn 57 mục theo nhóm | owner | — |
| `FU-270` | menu Lane test: sửa bộ chấm hay gỡ | owner | — |
| 7 mục chuyên môn | FU-195, FU-340/338/456, FU-397, FU-400, FU-183, FU-345, FU-392 | owner | — |
| 9 mục giao diện | owner xem `/monitoring`, `/v82-monitor`, `/du-doan-test` | owner | — |
| `FU-455` | lưu khuyến nghị `/choi` trước giờ xổ | agent | trước 27/11 |
| — | cảnh báo số dư API + cách ly | agent | trước 27/11 |
| `FU-457` | cổng Claude Code chạy giống Cursor, gồm chặn deploy giờ cấm | agent | trước 28/11 |
| `FU-328` · `FU-292` | cổng model rỗng · cổng tên đài | agent | trước 28/11 |
| `FU-318` · `FU-458` · `FU-204` | nhãn sai · giờ cũ `/monitoring` · tái lập «32,69%» | agent | trước 28/11 |
| cổng báo cáo ① | 39/268 bản cũ thiếu/thiếu phần (mới nhất V11157) — có trước phiên này | agent | rà theo nhãn |

## 10. Ba lớp nguồn (§62)

| lớp | nội dung | bằng chứng |
|---|---|---|
| `OWNER_SAID` | 25/11 ~13:37: *"là sao anh nạp tiền phí phạm vậy em? …"* (nguyên văn §2) | `docs/SO_TUONG_TAC_OWNER.md`, commit `3cd9943` |
| `CODE_DID` | Opus ra số MT 16:36, MB 17:31; scorecard 3 miền `inserted=27`; 0 `closed file` | `evidence/kiem_luot_that_1845.txt`, `evidence/journal_1848.txt` |
| `DOC_SAID` | V11191 ghi FU-452 `DEPLOYED` | `docs/FOLLOW_UP_TRACKER.md` khối FU-452 V11191 |

**Lệch:** `DOC_SAID` (nhãn `DEPLOYED`) ≠ cách bộ đọc hiểu (mồ côi) — đã sửa ở V11192. Không có lệch `OWNER_SAID` ≠
`CODE_DID` mới.

**TanPhatAI cần làm:** cập nhật hiểu biết — `claude-opus-4-6` đã chạy thật ở MT/MB từ 25/11, MN xác nhận sau 05:15
ngày 26/11 (`FU-452`); sổ điểm xét thăng hạng ghi lại từ 25/11 (`FU-451a` đạt, `FU-451b` chờ owner); FU-452 nay đọc
đúng nhãn `DEPLOYED_PENDING_LIVE_VERIFY`. Không có code đi trước tài liệu trong phiên này.
