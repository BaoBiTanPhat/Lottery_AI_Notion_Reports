# V11197 — Dọn dẹp cuốn chiếu · Đợt 2a: đóng 5 phép đo đã có phán quyết rồi mới dừng lịch (QD-082)

> **Phiên bản:** V11197 · **Ngày:** 26/11/2026 12:12 → 12:25 ICT · **Repo riêng:** `Lottery_AI_Test` commit `d81e7b6`
> (nhánh `fu438/admin-only-p0a` + `master`) · **governance_seq:** 512 · **Căn cứ:** `QD-082` · **Tầng (RM-12):**
> `DEPLOYED` (crontab VPS cài, `crontab -l` khớp) — lượt «không chạy» kiểm 27/11 · **Runtime đổi:** crontab (không restart).

## 1. Tóm tắt

- Đợt 2a đóng 5 phép đo **đã quá ngày đọc và đã có phán quyết trong chính log của chúng**: ghi phán quyết vào sổ TRƯỚC, rồi
  mới dừng lịch. Crontab **86 → 81** dòng đang bật (từ đầu ngày: 90 → 81).
- Kết quả theo đúng ngưỡng đăng ký trước: ghép `/nghiem-thu` × official **KHÔNG ĐẠT** · chống bầy đàn **ĐẠT** · ML × luật ×
  lọc **KHÔNG CÓ LỢI THẾ** · lane G2-MB **KHÔNG CÓ** · prompt 3 tầng **KHÔNG ĐẠT**.
- **Hoãn có chủ ý:** 5 phép đo tháng 7 (log không in phán quyết) và cụm nghiên cứu `/choi` (log cho thấy cách khác «hơn
  official» ở MT nhưng chưa đo đúng — không được dừng hay đưa vào khi chưa đo lại).

## 2. Owner yêu cầu gì (nguyên văn) — §62 lớp `OWNER_SAID`

**26/11/2026 ~12:0x ICT:** *«tiến hành các đề xuất an toàn trước, tuần tự , cuốn chiếu từ dễ đến khó từ đơn giản rõ ràng đến
phức tạp tra soát, soi xét kỹ lưỡng  v..v...»* — QD-082. Đợt 2a là bước thứ hai của chuỗi đó (Đợt 1: V11196).

## 3. Đào bới / phát hiện — liệt kê ĐỦ

### 3.1 Năm phép đo — phán quyết (`evidence/dot2_log_cuoi.txt`)

| phép đo | mã | ngưỡng đăng ký trước | kết quả cuối | phán quyết |
|---|---|---|---|---|
| ghép `/nghiem-thu` × official (`_v10984`) | FU-264 · QD-024 (B) | ≥ 60 ô · ≥ 150 lượt · hơn official ≥ 3 điểm · z ≥ 2 | 5/5 cách «không đạt ngưỡng»; cần thêm ~578 ngày mới thấy chênh 3 điểm | **KHÔNG ĐẠT** |
| độ phân tán số giữa model (`_v11017`) | FU-287 | ≥ 0,50 và hơn nền ≥ 0,05 | 0,474 (n 64) → **0,608** (n 330) | **ĐẠT** |
| ML × luật × lọc (`_v11018`) | FU-317 | z ≥ +1,96 | 3 nguồn 43,2% vs 1 nguồn 43,1%, z +0,04 | **KHÔNG CÓ LỢI THẾ** |
| đuôi G2 MB về MN/MT (`_v11037`) | FU-367 | 60 ngày đo tiến; `CO_THAT` z ≥ 2,539 | đo tiến 109 ngày: 9/9 mức không đạt, đa số z âm | **KHÔNG CÓ** |
| prompt 3 tầng T-B (`_v11089`) | FU-398 · QD-059 | ≥ 96 cặp lệch · ≥ 14 ngày · \|z\| ≥ 1,96 | 331 ✓ · 34 ✓ · \|z\| 0,76 ✗ | **KHÔNG ĐẠT** |

### 3.2 Soi người đọc (`evidence/dot2_ai_doc.txt`, script `evidence/doc_ghi_dot2.py`)

Ba bảng chỉ chính tệp đọc (cộng route panel). `ghep_nt_official_daily` thêm hai script không cron. Bảng của lane T-B: cổng
`_v11055_kiem_p4.py` chỉ nhắc tên. Bộ quét báo `_v11089` «ghi `lottery_results`» — **dương giả**: đó là bảng TẠM trong bộ
nhớ của `thu_chan()` (dòng 296–302).

### 3.3 Cụm nghiên cứu `/choi` — vì sao chưa đụng
Các `_build_*` của cụm chỉ được endpoint panel gọi (không vào `/choi`). Nhưng log lượt 25/11 cho thấy, ví dụ, MT
`CONS_FREESHADOW` bạch thủ 41,9% vs official 35,2% (n 270) và `output_final_lab` MT/MB có cách đánh lời +45tr trên 271
ngày. Những con số này **không có nền đúng ngày, không tách trong/ngoài cửa sổ, không kiểm ý nghĩa** — có thể là lợi
thế thật, có thể là ảo. Đo lại cho đúng trước (PRJ-SELECTION-WINDOW-001), rồi mới quyết dừng hay trình owner đưa vào.

### 3.4 Năm phép đo tháng 7
`_v10789` (4 dòng), `_v10801`, `_v10803`, `_v10821`, `_v10829`, `_v10844`: log chỉ in số dòng đã ghi, không in phán quyết ⇒
cần chạy chế độ xem để lấy phán quyết trước khi dừng (Đợt 2b).

## 4. Hướng xử lý và vì sao chọn

Chỉ dừng phép đo khi **phán quyết cuối đã có và đã ghi sổ** — dừng trước khi ghi là mất công đo. Phép đo nào kết quả còn
mập mờ (cụm `/choi`) thì không coi là «dễ», dù đầu ra chỉ vào panel. Mọi việc khác giữ khuôn Đợt 1: kiểm đúng tên script từng
dòng, thử rồi cài, sao lưu, không xoá.

## 5. Đã làm gì

1. Lấy dòng cron + đường log của 15 script ứng viên; soi bảng ghi và người đọc trên VPS.
2. Xác minh các `_build_*` của cụm `/choi` chỉ do route panel gọi.
3. Đọc khối cuối log của 15 script; tách 5 phép đo có phán quyết rõ.
4. Kiểm cổng `_v11055` và sổ quyết định (QD-024, QD-059 có nhắc các phép đo này).
5. `dung_cron_v11197.py` thử → cài; sao lưu `crontab.pre_v11197.txt`; kiểm diff đúng 5 dòng.
6. Ghi bốn mặt (seq 512), 6 khối FU, kết quả vào QD-024 và QD-059. Commit `d81e7b6`.

## 6. Cổng kiểm

| cổng | kết quả |
|---|---|
| script dừng | 5/5 dòng đúng tên script · `crontab -l` khớp bản mới · 81 dòng đang bật |
| diff crontab | đúng 5 dòng đổi (`evidence/crontab_diff_5_dong.txt`) |
| `_v10920_decision_ledger.py` | 0 TRÔI · QD-024 🟢 5/5 · QD-059 🟢 5/5 sau khi dừng |
| `_v11062_nang_version.py --kiem` | `ĐẠT` (seq 512) |
| `_v11027_so_muc_quan_tri.py` | không mục nào biến mất |
| `trang_thai_mo_coi()` | trống |
| `_v10921_report_gate.py` ① + ② `V11197` | xem `CONVERSATION_CONTEXT` §4 |

## 7. Vướng vấp

- Bộ quét bảng báo `_v11089` ghi `lottery_results` (bảng khoá) — phải đọc mã mới thấy là bảng tạm trong bài thử.
- Ban đầu xếp cụm `/choi` vào «dễ» vì đầu ra chỉ vào panel; đọc log mới thấy số hứa hẹn chưa được đo đúng ⇒ rút ra.
- **Đính chính giờ:** bản đầu V11196/V11197 ghi giờ ƯỚC LƯỢNG («~12:20», «~12:55», «~13:05», «~13:10») — sai so với giờ thật. Đã sửa tại chỗ theo giờ tệp sao lưu crontab trên VPS (12:05:11 · 12:15:27) và giờ commit (12:10:20 · 12:23:25).

## 8. Gỡ về

`crontab /root/Lottery_AI_Test/backups/crontab.pre_v11197.txt` (bản sao local `backups/crontab.pre_v11197.txt`), hoặc bỏ tiền
tố `# V11197 DỪNG … |`. Tài liệu: `git revert d81e7b6`.

## 9. Theo dõi tiếp — liệt kê ĐỦ

| mã | việc | ai chặn | khi nào |
|---|---|---|---|
| `FU-462` | 9 log (Đợt 1 + 2a) không có dòng mới sau giờ chạy cũ; `_v10900` không thêm LỆCH | lượt tự nhiên | 27/11 |
| Đợt 2b | 5 phép đo tháng 7: chế độ xem → phán quyết → sổ → dừng | agent | tiếp theo |
| cụm `/choi` | đo lại đúng (nền ngày, tách cửa sổ, kiểm ý nghĩa) trước khi quyết | agent → owner | sau Đợt 2b |
| FU-394 · anti-trap · D-30 | dừng cần owner hoặc QD mới (RM-19) | owner | khi trình |
| Đợt 3 | báo động giả + cảnh báo model official trả rỗng (FU-328) | agent | sau Đợt 2b |

## 10. Ba lớp nguồn (§62)

| lớp | nội dung | bằng chứng |
|---|---|---|
| `OWNER_SAID` | QD-082 — an toàn trước, tuần tự, soi kỹ | `docs/SO_TUONG_TAC_OWNER.md` dòng 26/11 ~12:0x |
| `CODE_DID` | crontab 86 → 81; 5 phép đo dừng sau khi ghi phán quyết | `evidence/cai_cron_dot2a.txt` · `evidence/crontab_diff_5_dong.txt` |
| `DOC_SAID` | FU-264/287/317/367/398 trước phiên còn `DEPLOYED_PENDING_LIVE_VERIFY` / `WAIT_LIVE` / `DO_TIEN_DANG_CHAY` dù ngày đọc đã qua 3–4 tháng | `docs/FOLLOW_UP_TRACKER.md` khối cũ |

**Lệch:** sổ để 5 phép đo «đang chờ» nhiều tháng sau ngày đọc, trong khi log đã có kết quả mỗi tối — nay đã đóng đúng phán quyết.

**TanPhatAI cần làm:** cập nhật hiểu biết — FU-264 · FU-317 · FU-367 · FU-398 đóng KHÔNG ĐẠT, FU-287 đóng ĐẠT; QD-024 vế (B) và
QD-059 đã có kết quả cuối ghi trong sổ quyết định; crontab còn 81 dòng đang bật. Theo dõi FU-462 (27/11). **Code đi trước tài
liệu:** crontab cài 12:15:27 (giờ tệp sao lưu trên VPS), commit tài liệu 12:23:25 — cùng phiên; căn cứ `docs/SO_TUONG_TAC_OWNER.md` dòng «26/11 ~12:0x».
