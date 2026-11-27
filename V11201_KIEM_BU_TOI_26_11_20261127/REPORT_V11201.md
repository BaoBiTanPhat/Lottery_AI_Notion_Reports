# V11201 — Kiểm bù tối 26/11: FU-460 + FU-451(a) đóng ĐẠT · 9 lịch đã dừng không chạy lại · đánh giá dự đoán 26/11

> **Phiên bản:** V11201 (+ V11201b sửa hạn) · **Ngày:** 27/11/2026 ~11:15 → 11:45 ICT · **Repo riêng:** commit `e127f9b` + `af83c45`
> · **governance_seq:** 516 · **Tầng (RM-12):** `RUNTIME_PROVEN` cho ba phép kiểm (đọc DB/journal production) · **Runtime đổi:** không.

## 1. Tóm tắt

- Ba lượt kiểm hẹn giờ tối 26/11 **không chạy** (phiên trước kết thúc trước giờ) — chạy bù sáng 27/11, chỉ đọc.
- **FU-451(a) ĐẠT:** sau 19:20 ngày 26/11 có 96 dòng print (25/11: 0) — bản vá V11199 có hiệu lực. **FU-460 ĐẠT:** OpenRouter thông,
  `glm-5.1` và `gpt-oss-120b` ra số ở MT/MB. **9 lịch đã dừng** (V11196–V11197) không chạy lại; `_v10900` 18:05 lệch 0.
- **Dự đoán 26/11:** bạch thủ **+7,95tr** · lô 2 số +1,2tr · `/choi` đánh đủ +8,8tr. 30 ngày vẫn trong vùng may rủi.

## 2. Owner yêu cầu gì (nguyên văn) — §62 lớp `OWNER_SAID`

**27/11 đầu phiên:** *«KIỂM TRA LẠI LẦN NỮA XEM LẠI THẬT KỸ CÔNG VIỆC CỦA ANH LÀ GÌ? CỤ THỂ CHÍNH XÁC ĐỀ XUẤT DỌN DẸP LÀ GÌ  CỤ THỂ
CHÍNH XÁC NHA EM»* — bản này lấy số thật để trả lời (danh sách việc owner trả lời trong IDE, theo `docs/KE_HOACH_DON_DEP_20261126.md`).

## 3. Đào bới / phát hiện — liệt kê ĐỦ (`evidence/kiem_bu_toi_26.txt`)

| phép | kết quả |
|---|---|
| print sau 19:20 | 25/11: logging 71 · print **0** — 26/11: logging 71 · print **96**; `closed file` 0 |
| OpenRouter 26/11 | MT `glm-5.1` `24 16` · `gpt-oss-120b` `23 48`; MB `gpt-oss-120b` `24 32` · `glm-5.1` `32 48` |
| 9 log lịch đã dừng | sửa lần cuối đều trước giờ dừng (25/11 hoặc 26/11 07:30 — trước lúc dừng 12:05) |
| `_v10900` 18:05 | 23 → 26/11: 26 phép, lệch 0 mỗi ngày |

**Dự đoán 26/11** (thước tiền `/choi`, nền đúng ngày MN 38% · MT 44% · MB 26%):

| miền | bạch thủ | lô 2 số | `/choi` đánh đủ |
|---|---|---|---|
| MN | `92` trượt −2,7tr | `92 32` trượt −5,4tr | `92` −2,7tr |
| MT | `80` trúng 2 nháy +7,1tr | `80 16` +4,4tr | `93 80` +9,3tr |
| MB | `48` trúng +3,55tr | `48 80` +2,2tr | `48 60` +2,2tr |

Model trúng bạch thủ: MN 1/12 (kỳ vọng ngẫu nhiên 4,6) · MT 6/12 (5,3) · MB 3/12 (3,1). **30 ngày 28/10 → 26/11:** bạch thủ −14,4tr
(z −0,35) · lô 2 số −23,9tr (z −0,38) · `/choi` đánh đủ −26,2tr (z −0,60). Khuyến nghị `/choi` vẫn ghi sau giờ xổ (FU-455) ⇒ không dùng.

**Soát lại đề xuất dọn dẹp trên dữ liệu thật:** `.sh` lane MB còn gọi 2 lane owner cho nghỉ 01/08 và chạy 2 lần/ngày · bảng
`slice_policy` chưa từng áp (`enabled=0`) nhưng vẫn gắn REDUCE cho model đang dùng · biến môi trường nuôi `_v10708` không có trong cấu
hình · bộ chấm lane gãy ở một dòng (`int(run_id)`). Một việc bảo mật máy chủ — chi tiết chỉ ở kho riêng, chờ owner.

## 4. Hướng xử lý và vì sao chọn

Đóng đúng ba mục đã có bằng chứng lượt thật; giữ FU-451(b) và các đợt dọn dẹp sau chờ owner. Cho FU-451/FU-462 hạn thật 03/12 vì bộ
đọc sổ kế thừa hạn cũ khi khối mới ghi «LX».

## 5. Đã làm gì

1. Chạy bù 3 phép kiểm + đánh giá 26/11 + bối cảnh 30 ngày trên VPS (chỉ đọc).
2. Soát lại 5 khẳng định quan trọng của phương án dọn dẹp trên dữ liệu thật.
3. Ghi bốn mặt (seq 516), 3 khối FU. Commit `e127f9b`; sửa hạn `af83c45`.

## 6. Cổng kiểm

| cổng | kết quả |
|---|---|
| `_v11062_nang_version.py --kiem` · `_v11027_so_muc_quan_tri.py` | `ĐẠT` · không mục nào biến mất |
| `trang_thai_mo_coi()` | trống; FU-460 `CLOSED_PASS` · FU-451 `OWNER_DECISION_NEEDED` 03/12 · FU-462 `AWAITING_OWNER_OK` 03/12 |
| `_v10920_decision_ledger.py` | 0 TRÔI · 2 «không kết luận được» do DB local cũ 23 giờ (RM-01) |
| `_v10921_report_gate.py` ① + ② `V11201` | xem `CONVERSATION_CONTEXT` §4 |

## 7. Vướng vấp

- Ba lượt kiểm hẹn giờ chạy bằng tiến trình nền của phiên — phiên kết thúc là mất. Lần sau hẹn giờ bằng cron VPS chỉ đọc, hoặc chạy bù đầu phiên.
- Lần sửa hạn đầu bị cổng tự kiểm của chính script chặn (chuỗi tiêu đề trùng ở khối cũ) — đã sửa đúng khối trên cùng.

## 8. Gỡ về

`git revert af83c45 e127f9b` (tài liệu). Không có thay đổi runtime.

## 9. Theo dõi tiếp — liệt kê ĐỦ

| mã | việc | ai chặn | khi nào |
|---|---|---|---|
| FU-455 | khoá khuyến nghị `/choi` trước giờ xổ (cần restart) | agent | 27/11 khung an toàn |
| FU-451 (b) · FU-345 · FU-459 · FU-453 · FU-270 | câu owner | owner | 03/12 |
| FU-462 | đợt dọn dẹp sau: câu 1B–3G | owner | 03/12 |
| bảo mật máy chủ | chi tiết ở kho riêng | owner | sớm |

## 10. Ba lớp nguồn (§62)

| lớp | nội dung | bằng chứng |
|---|---|---|
| `OWNER_SAID` | 27/11 — kiểm lại kỹ việc của owner và đề xuất dọn dẹp | `docs/SO_TUONG_TAC_OWNER.md` |
| `CODE_DID` | print sống sau 19:20; OpenRouter đủ số; 9 lịch không chạy lại | `evidence/kiem_bu_toi_26.txt` |
| `DOC_SAID` | sổ còn ghi FU-460 `WAIT_LIVE`, FU-451(a) chờ kiểm | `docs/FOLLOW_UP_TRACKER.md` khối cũ |

**Lệch:** sổ chậm hơn thực tế một đêm vì lượt kiểm không chạy — đã cập nhật.

**TanPhatAI cần làm:** cập nhật hiểu biết — FU-460 và FU-451(a) đã đóng ĐẠT; FU-462 chờ owner chốt 1B–3G. Không có code đi trước tài
liệu trong bản này.
