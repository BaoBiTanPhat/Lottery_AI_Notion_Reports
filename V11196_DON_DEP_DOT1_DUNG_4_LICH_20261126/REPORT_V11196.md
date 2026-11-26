# V11196 — Dọn dẹp cuốn chiếu · Đợt 1: dừng 4 lịch chạy hết việc, không ai đọc (QD-082)

> **Phiên bản:** V11196 · **Ngày:** 26/11/2026 ~12:02 → 12:12 ICT · **Repo riêng:** `Lottery_AI_Test` commit `589487f`
> (nhánh `fu438/admin-only-p0a` + `master`) · **governance_seq:** 511 · **Quyết định:** `QD-082` · **Tầng (RM-12):**
> `DEPLOYED` (crontab VPS đã cài, `crontab -l` khớp) — lượt «không chạy» kiểm 27/11 · **Runtime đổi:** crontab (không restart).

## 1. Tóm tắt

- Owner cho tiến hành dọn dẹp theo đợt, an toàn trước, từ dễ tới khó (QD-082).
- **Đợt 1:** dừng 4 dòng cron mà đầu ra không ai đọc: `_v10661_live_edge_monitor` · `_perpos_matrix_report` ·
  `_v10784_verify_0607` (chỉ viết cho ngày 06/07, skip mỗi ngày từ đó) · `_v11067_lay_mau_khoa_db` (bộ lấy mẫu FU-402 —
  đã đủ 112.007 mẫu, và chính nó giữ khoá ghi DB mỗi 5 giây trong khung MT/MB).
- Crontab **90 → 86** dòng đang bật; **162 dòng khác y hệt**. Không xoá bảng, tệp, log. Gỡ về bằng một lệnh.

## 2. Owner yêu cầu gì (nguyên văn) — §62 lớp `OWNER_SAID`

| giờ (ICT) | nguyên văn |
|---|---|
| 26/11 ~11:47 | *«kiểm xong chưa tiến hành dọn dẹp được chưa ? chờ  anh chốt vấn đề gì?»* |
| 26/11 ~12:0x | *«tiến hành các đề xuất an toàn trước, tuần tự , cuốn chiếu từ dễ đến khó từ đơn giản rõ ràng đến phức tạp tra soát, soi xét kỹ lưỡng  v..v...»* |

Bối cảnh: tin nhắn 10:10 *«Lên phương án kế hoạch dọn dẹp hệ thống đi cồng kềnh quá mà chả hiệu quả gì cả em?»*. Cả ba
dòng có trong `docs/SO_TUONG_TAC_OWNER.md`.

## 3. Đào bới / phát hiện — liệt kê ĐỦ

- **Kiểm kê 8 mặt + phản biện** (luồng nền, chỉ đọc): 212 đề xuất. Người phản biện mặt lịch chạy: giữ 25 · hạ mức 10 ·
  bác 1. Bốn dòng Đợt 1 đều «giữ đề xuất», độ tin cao.
- **Tự kiểm lại (RM-20), không chỉ tin phản biện:** grep toàn `web/` trên VPS (py · html · js · sh · json) cho tên bảng/tệp
  đầu ra của 4 job ⇒ **chỉ chính tệp đó** nhắc tới. Sổ quyết định và các cổng `_v10900`, `_v10861`, `_v10800`,
  `_v10647`, `_v10891`, `_v10648` không đòi các dòng này. `_v10900` C4/C5/C6 so crontab ở việc khác (khoá `/choi`, giờ
  lane Nghiệm Thu).
- **FU-402** (`evidence/v11067_doc_fu402_dau.txt`): 112.007 mẫu, 1.426 lần DB bị khoá (1%) trong khung 16:35–18:05.
- **Rút `_v10869` khỏi Đợt 1:** route `/api/admin/cp-l6-lean` gọi `compute_view()` đọc bảng theo ngày ⇒ dừng lịch là
  panel trống mà không ai biết vì sao.
- **Bốn đề xuất người phản biện bác/hạ mức** (không làm theo bản gốc): `_v10879` 8 lượt predraw (đã cứu 18 lần lane
  early_block trượt) · `_v10703` MN/MT (bảng sàng lọc trên `/du-doan-test` còn đọc) · 3 bộ AI-limit (panel model-progress
  sẽ gắn nhãn REDUCED giả) · `auto_daily_eval` (hỏng im lặng từ 11/09, không phải hết việc).
- Con số «424 job khác nhau» trong `docs/KIEM_KE_DON_DEP_20260821.md:55` thật ra là **424 lượt chạy mỗi ngày của 42 job**
  (đếm journal 25/11) — ghi để rút lại khi phát hành phương án đầy đủ.

## 4. Hướng xử lý và vì sao chọn

Đợt 1 chỉ gồm việc **rõ ràng nhất**: dòng cron mà đầu ra không ai đọc, không ghi bảng nào có người đọc, không đụng đường
`/du-doan` · `/choi` · prompt · roster. Chỉ **comment** dòng (giữ nguyên nội dung sau tiền tố `# V11196 DỪNG … |`) để bật
lại bằng cách bỏ tiền tố. Không restart. Làm trước 15:30 để không đổi lịch giữa khung ra số.

## 5. Đã làm gì

1. Ghi hai dòng lời owner vào sổ tương tác.
2. Đọc kết quả kiểm kê + phản biện; chọn 4 dòng «giữ đề xuất» không phụ thuộc.
3. Tự grep người đọc trên VPS; soát sổ quyết định và các cổng.
4. Chạy `_v11067 --doc` lấy tổng kết FU-402 trước khi dừng.
5. `dung_cron_v11196.py`: đòi mỗi dòng chứa đúng tên script, thử (diff) rồi cài; sao lưu crontab cũ ra `backups/`.
6. Kiểm: `crontab -l` khớp bản mới · 90 → 86 · 162 dòng khác y hệt · chạy lại script ⇒ từ chối (dòng đã dừng).
7. Ghi bốn mặt (seq 511), FU-462, FU-402, QD-082. Commit `589487f`.

## 6. Cổng kiểm

| cổng | kết quả |
|---|---|
| script dừng — kiểm tên script từng dòng | khớp 4/4; chạy lại ⇒ «DỪNG: dòng 17 không phải dòng đang bật» |
| `crontab -l` sau cài | khớp bản mới · 86 dòng đang bật · 4 dòng mang tiền tố V11196 |
| 162 dòng còn lại | y hệt bản sao lưu (`evidence/crontab_diff_4_dong.txt` chỉ có 4 dòng đổi) |
| `_v11062_nang_version.py --kiem` | `ĐẠT` (seq 511) |
| `_v11027_so_muc_quan_tri.py` | không mục nào biến mất |
| `trang_thai_mo_coi()` | trống; FU-462 `DEPLOYED_PENDING_LIVE_VERIFY` hạn 27/11 |
| `_v10921_report_gate.py` ① + ② `V11196` | xem `CONVERSATION_CONTEXT` §4 |

## 7. Vướng vấp

- Danh sách «an toàn» ban đầu có `_v10869`; soi route mới thấy panel phụ thuộc theo ngày — rút ra.
- Bản kiểm kê ghi số dòng cron theo thứ tự `crontab -l` (gồm cả dòng chú thích) — script dừng kiểm tên script ở chính dòng
  đó để không comment nhầm dòng nếu crontab đổi giữa chừng.

## 8. Gỡ về

`crontab /root/Lottery_AI_Test/backups/crontab.pre_v11196.txt` (bản sao ở local `backups/crontab.pre_v11196.txt`), hoặc bỏ
tiền tố `# V11196 DỪNG … |` ở từng dòng. Tài liệu: `git revert 589487f`.

## 9. Theo dõi tiếp — liệt kê ĐỦ

| mã | việc | ai chặn | khi nào |
|---|---|---|---|
| `FU-462` | kiểm 4 log không có dòng mới sau giờ chạy cũ; `_v10900` 18:05 không thêm LỆCH | lượt tự nhiên | 27/11 |
| `FU-462` Đợt 2 | đóng phép đo đã quá ngày đọc: `--view` lấy phán quyết cuối, ghi sổ, rồi dừng lịch | agent | sau Đợt 1 |
| `FU-462` Đợt 3 | báo động giả (watchdog V10785, MB_WATCHDOG FU-454, `_v10800`) + cảnh báo model official trả rỗng (FU-328) | agent | sau Đợt 2 |
| `FU-462` Đợt 4–5 | `.sh` lane MB (FU-185), nhãn panel đông, xoay vòng log nén | agent | sau Đợt 3 |
| phương án đầy đủ | `docs/KE_HOACH_DON_DEP_20261126.md` — các việc cần owner (CHỐT GẤP qua shadow, lưu trữ, giữ dữ liệu bao lâu) | agent → owner | bản sau |
| `FU-402` | vá gốc khoá DB khung MT/MB; bật lại bộ lấy mẫu khi thử bản vá | agent | sau các đợt lịch chạy |

## 10. Ba lớp nguồn (§62)

| lớp | nội dung | bằng chứng |
|---|---|---|
| `OWNER_SAID` | 26/11 ~12:0x — an toàn trước, tuần tự, từ dễ tới khó (nguyên văn §2) | `docs/SO_TUONG_TAC_OWNER.md` · QD-082 |
| `CODE_DID` | crontab VPS 90 → 86 dòng đang bật; 4 dòng comment có tiền tố; 162 dòng khác y hệt | `evidence/cai_cron.txt` · `evidence/crontab_diff_4_dong.txt` |
| `DOC_SAID` | `KIEM_KE_DON_DEP_20260821.md:55` «424 job khác nhau» | đo lại: 424 LƯỢT/ngày của 42 job |

**Lệch:** `DOC_SAID` ≠ `CODE_DID` ở con số 424 (lượt, không phải job) — rút lại khi phát hành phương án đầy đủ.

**TanPhatAI cần làm:** cập nhật hiểu biết — từ 26/11 crontab còn 86 dòng đang bật; 4 job `_v10661` · `_perpos_matrix_report`
· `_v10784_verify_0607` · `_v11067` đã dừng có chủ ý (QD-082), đừng đọc bảng/log của chúng thành «job chết». Theo dõi
FU-462 (kiểm 27/11). **Code đi trước tài liệu:** crontab cài 12:05:11 (giờ tệp sao lưu trên VPS) rồi mới ghi tài liệu, commit 12:10:20 — cùng phiên; mục sổ
tương ứng: `docs/SO_TUONG_TAC_OWNER.md` dòng «26/11 ~12:0x».
