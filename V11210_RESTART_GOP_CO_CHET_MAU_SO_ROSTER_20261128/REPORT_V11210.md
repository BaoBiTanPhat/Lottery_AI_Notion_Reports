# V11210 — Restart gộp 28/11: bỏ cờ 3 model chết + mẫu số theo roster · chốt khuyến nghị `/choi` trước giờ xổ · gỡ 5 job tắt · sửa 3 báo động giả · cảnh báo thiếu output

> **Phiên bản:** V11210 · **Ngày:** 28/11/2026 06:33 → ~07:10 ICT (mã soạn và thử 27/11 tối) · **Repo riêng:** `2474d78` · **governance_seq:** 524
> · **Quyết định:** QD-084 khoản 7 · QD-083 (C) Đợt 1 mục 1J · **Tầng (RM-12):** `DEPLOYED` — service khởi động lại, PID đổi, kiểm trên mã đã
> triển khai đạt. **Chưa** `RUNTIME_PROVEN`: các điểm phải đọc trong ngày (chốt `/choi` 15:43 / 16:56 / 17:56, verify ba miền, MB_WATCHDOG
> 17:55) chưa tới giờ.

## 1. Tóm tắt

- **Mỗi miền nay bỏ phiếu và tính mẫu số đúng 11 model.** Ba model chết (deepseek-reasoner · gemini-2.5-pro · gpt-5.4, dòng chính thức cuối
  11–13/09) bỏ **cờ output**, vẫn ở trong registry (bỏ cờ, **không** dừng hẳn — §59). Danh sách toàn cục 15 → 12. Phiếu **không đổi**:
  76 ngày × 3 miền, dòng đi qua bộ lọc cũ và mới y hệt. Pool AI combo-super 9 → 5, ML giữ 4.
- **Khuyến nghị CHƠI/NGHỈ của `/choi` chốt trước giờ xổ** (FU-455). Trước đây khuyến nghị bị ghi đè sau khi có kết quả: 100% dòng từ 28/06.
- **Gỡ 5 job đã tắt từ 31/05 · sửa 3 báo động giả** (khoảng 114 lần/ngày · MB mỗi ngày · cổng tự kiểm đỏ 16 tuần) · **cảnh báo model chính
  thức thiếu output** nay ghi vào `system_alerts`, bảng này im từ 11/05.
- Restart 06:35:40, ngay sau lượt chạy 06:35 · PID 1277779 → 1516954 · health 200 · admin 401 · băm 4 bảng khoá trước = sau.
- **Vấp sau deploy:** sổ quyết định báo 1 TRÔI (QD-020). Nguyên nhân: một phép **phát lại ngày 03/08**, không phải lỗi chạy. Đã xử, 0 TRÔI.

## 2. Owner yêu cầu gì (nguyên văn)

| giờ (ICT) | nguyên văn |
|---|---|
| 27/11 ~14:50 | *«C đồng ý theo khuyến nghị nha em. ==> tất cả kiểm tra đối chiếu , đối soát , xử lý bài bản chuẩn chỉnh dùm anh nha em. Tinh gọn chính xác ổn định»* (trích phần C của tin nhắn) |
| 27/11 ~17:35 | *«OK ĐỒNG Ý VỚI ĐỀ XUẤT NHƯNG CÒN 1 ĐIỂM NỮA LÀ CÁC MODEL HIỆN TẠI CÒN BAO NHIÊU MODEL CÓ CẦN CẮT GIẢM BỔ SUNG MODEL NÀO KHÔNG EM?»* |
| 27/11 ~17:50 | *«OK ANH DUYỆT THEO KHUYẾN NGHỊ EM. EM TIẾN HÀNH XỬ LÝ HOÀN TẤT DỨT ĐIỂM SẠCH SẺ DÙM ANH»* |

Phạm vi đã duyệt, ghi trong sổ quyết định (`QD-084` khoản 7, **không phải lời owner**): dọn 3 cờ official chết (bỏ cờ, không dừng hẳn) + 4 tên
chết khỏi pool AI combo-super + mẫu số theo roster từng miền, chạy khô trước. Sau 17:50 ngày 27/11 owner **không nói thêm** tới khi viết báo
cáo này.

## 3. Đào bới / phát hiện

1. **PRE 06:33:** sha 11 tệp trên VPS = sha bản sao lưu ở máy dev (11/11) ⇒ không ai sửa tay trên máy chủ từ lúc thử.
2. **Chọn giờ restart:** lượt `du_doan_test_auto` 06:35 ghi log lúc 06:35:02, bỏ qua nhanh, không có tiến trình con ⇒ restart 06:35:40.
3. **Kiểm trên mã đã triển khai** (`_v11210_kiem_fu465a.py --db`, DB sống): **10/10**. K7 cho thấy 76 ngày, dòng qua lọc cũ = lọc mới:
   MN 809 · MT 818 · MB 816.
4. **QD-020 TRÔI lúc 06:39:** phép *«bộ dò chạy thật trên 03/08 MB: ĐÃ XONG, sớm 786 giây»* ✓ → ✗. Đo: bộ dò đếm kho model theo danh sách
   output **toàn cục**. Ngày 03/08 ba model chết còn bỏ phiếu ⇒ phát lại ra `CHUA_DU_KHO` (kho 12 < 14). Ngày hiện tại vẫn đúng: MB 26/11
   sớm 1384 s · MT 27/11 861 s · MB 27/11 1281 s. **Bộ dò không hỏng; tiền đề của phép phát lại không còn đúng.**
5. **Quét ngược toàn kho (§60.3) — đây là phần §60.2 sót trước deploy:** 69 tệp đọc danh sách output, 15 tệp chạy sống (cron / scheduler /
   main). Bộ bị bỏ theo miền là 3 model chết + glm-5.1 ở MN / sonnet ở MT · MB, và **cả năm không có dòng `predictions` nào từ 14/09**,
   shadow lẫn official (Q2 = 0 · 0 · 0).

   | loại chỗ đọc | ở đâu | sau V11210 |
   |---|---|---|
   | bỏ phiếu | `main.py:9709` · `main.py:481` | dòng y hệt 76 ngày × 3 miền |
   | một ngày / cửa sổ từ 14/09 | money board · `_v10789` · `_v10861` · `_v10872`/`_v10979` (hôm nay) · wave1 · scorecard · cảnh báo mới | **cùng các dòng** (Q2 = 0) |
   | cửa sổ dài / phát lại ngày cũ | `_v10871` (từ 01/04) · `_v10869` `roster_kind` · trang admin số liệu từng model (≤ 90 ngày) · phép QD-020 | ngày ≤ 13/09: 3 model chết **không còn tính là official** — chỉ đổi **nhãn** kiểm toán, không đổi phiếu, không đổi số |

6. **QD-046 «5 model rớt sàn»** (bản trước báo 1): chạy lại trên VPS ra `NO_ANSWER_V11036=DAT`, 0 rớt sàn. Con số 5 do **DB local cũ**
   (RM-01), không do V11210.
7. **Sáu lane thử nghiệm MN (FU-467):** tối 27/11 agent nói «dừng từ 02/11». **Sai:** lane mờ dần từ tháng 8. Số ngày có dòng theo tháng 07→11
   là MN 31 · 12 · 5 · 1 · 1, so với MT 31 · 26 · 25 · 30 · 24 và MB 31 · 29 · 29 · 29 · 27. Nguyên nhân **chưa đào**.
8. **`system_alerts`:** dòng mới nhất 11/05 — xác nhận bảng im 6 tháng trước khi nối cảnh báo.
9. **K7 chỉ chép lại bộ lọc — chưa phép nào chạy trọn đường ra bundle bằng mã mới.** MN 28/11 chạy 05:15 bằng mã **cũ**, nên lượt thật đầu tiên
   trên mã mới là MT ~16:42. Phát lại `generate_final_bundle` trên **bản sao** kho (07:00), mã cũ và mã mới cùng một DB chép
   (`_v11210_phat_lai_bundle.py`, nạp từ thư mục sao, từ chối chạy nếu trỏ vào kho thật): **MN 28/11 · MT 27/11 · MB 27/11 cũ = mới, y hệt
   từng byte**, và trùng bundle thật — MN `79` · lô `79 56` · MT `98` · lô `98 42` · MB `28` · lô `28 68`.
10. **MB 27/11 phát lại ra 9 phiếu, bundle thật 8** — cũ và mới **cùng** 9 ⇒ không do V11210. Lúc chốt, glm-5.1 trượt cổng BT (10% < 12%);
    chính 27/11 glm-5.1 trúng bạch thủ (`34`) ⇒ phát lại **sau** giờ xổ thì cửa sổ 30 ngày đã gồm kết quả hôm đó, glm-5.1 qua cổng. Số công
    bố không đổi. Phát lại sau xổ ≠ lượt sống (PRJ-SELECTION-WINDOW-001).

## 4. Hướng xử lý và vì sao chọn

- **Một lần restart cho mọi thay đổi trong service:** mỗi lần restart là một lần rủi ro cho đường chính thức. Gộp bốn việc đã thử xong vào khung
  an toàn 06:30–15:30, sau lượt chạy 5 phút.
- **Lọc theo roster bên trong `get_output_eligible_ids(region)`**, không sửa từng nơi gọi: mọi nơi đã gọi hàm này nhận cùng một câu trả lời. Lỗi
  hoặc roster hỏng ⇒ **không lọc** (giữ hành vi cũ), không bao giờ trả rỗng.
- **Cảnh báo thiếu đếm OUTPUT, không đếm nhãn:** nhãn `day_governance` MB là 8/11 mỗi ngày vì cổng chất lượng loại 3 phiếu. Báo theo nhãn
  sẽ thành báo giả hằng ngày, đúng thứ đang dọn.
- **QD-020:** giữ ý của phép («bộ dò chạy thật kết luận ĐÃ XONG với số giây chính xác»), đổi neo sang một ngày sau khi roster đổi. **Không** làm bộ
  dò nhớ roster theo ngày: không đường sống nào phát lại ngày trước 14/09, và đổi bộ chọn của lane Nghiệm Thu là thêm rủi ro trong lúc đóng băng.

## 5. Đã làm gì

| việc | TRƯỚC | SAU | PHIÊN BẢN | KIỂM |
|---|---|---|---|---|
| cờ output + mẫu số (FU-465a) | 15 toàn cục, mẫu số 15 mọi miền ⇒ ngày đủ 11/11 bị dán INCOMPLETE | 12 toàn cục · 11 mỗi miền · `expected_model_count(region)` ở 4 chỗ | V11210, lên 06:35:40 | `_v11210_kiem_fu465a.py --db` 10/10 |
| pool AI combo-super | 9 (4 tên chết) | 5 · ML 4 | V11210 | K8 |
| `/choi` (FU-455) | verdict/stake ghi đè sau xổ | bảng `money_board_verdict_lock`, chốt trước CUTOFF MN 16:00 · MT 17:00 · MB 18:00 | V11210 | `_v11210_thu_fu455.py` 5/5 · mã cũ 2/5 |
| 5 job tắt | 5 khối đăng ký + 1 dòng lịch tĩnh | gỡ, để chú thích | V11210 | 35 dòng đăng ký lúc khởi động, không còn V81/V101/V104/V105 |
| báo động giả ×3 (FU-454) | MISS shadow ~114/ngày · MB_WATCHDOG mỗi ngày · `_v10800` đỏ 16 tuần | đi theo roster / dữ liệu sống | V11210 | `_v11210_thu_canh_bao.py` 8/8 |
| cảnh báo thiếu output (1J · FU-328) | `system_alerts` im từ 11/05 | `OFFICIAL_MODEL_MISSING` sau 3 điểm verify | V11210 | `_v11210_thu_bao_thieu.py` 4/4 |
| sổ quyết định | 11 phép `== 15` · neo QD-074/075 = 15 · QD-020 neo 03/08 | `== 12` · neo 12/11 (thay một phần bởi QD-084 k7) · QD-020 neo 27/11 MB; giữ `bieu_thuc_cu` | V11210 | `_v10920_decision_ledger.py` 06:48 «KHÔNG CÓ QUYẾT ĐỊNH NÀO BỊ TRÔI» |
| quét ngược | — | `_v11210_quet_nguoc.py` (Q1–Q5) | V11210 | `QUET_NGUOC_V11210=DAT` |
| phát lại trọn đường bundle | chưa có | `_v11210_phat_lai_bundle.py` — mã cũ vs mã mới trên bản sao kho | V11210, 28/11 07:01 | 3/3 miền-ngày cũ = mới = bundle thật; bản sao 2,2 GB đã xoá |
| bốn mặt + theo dõi | — | seq 524; FU-465 · 455 · 454 · 328 · 255 `DEPLOYED_PENDING_LIVE_VERIFY`; FU-453 · 462 cập nhật; mở FU-466 · FU-467 | V11210 | `_v11062_nang_version.py --kiem` ĐẠT · bộ đọc FU 0 mồ côi |

Bằng chứng: `evidence/KIEM_V11210.txt` (chạy lại trên VPS sau deploy + nhật ký triển khai nguyên văn).

## 6. Cổng kiểm

| cổng | kết quả |
|---|---|
| sha 11 tệp VPS = bản sao lưu dev (trước) · = commit (sau) | 11/11 · 11/11 |
| `py_compile` trên VPS | 17/17 |
| PID trước / sau · health · admin | 1277779 → 1516954 · 200 · 401 ×3 |
| `_v11033_bam_4_bang.py` TRUOC / SAU | y hệt (RM-02: chỉ chứng minh không ghi bậy, không chứng minh dữ liệu đúng) |
| `_v11210_kiem_fu465a.py --db` | 10/10 trên mã đã triển khai |
| `_v11210_phat_lai_bundle.py` (cũ vs mới) | MN 28/11 · MT 27/11 · MB 27/11 y hệt từng byte |
| `_v11210_thu_fu455.py --db` trên VPS, ngày 28/11 (bản sao tạm) | 5/5 |
| `_v10920_decision_ledger.py` | 0 TRÔI · 0 không kết luận (sau đồng bộ dữ liệu sống) |
| `_v11062_nang_version.py --kiem` | ĐẠT |
| cổng commit (gồm cổng thử nghiệm V11208) | qua — `2474d78` |
| `_v10921_report_gate.py` ① toàn dải · ② `V11210` | xem `CONVERSATION_CONTEXT` §4 |

## 7. Vướng vấp

- **§60.2 sót một hạng chỗ đọc:** trước deploy đã quét `kiem_code` của sổ quyết định (tìm ra 13 phép), nhưng **chưa** quét hết người đọc danh
  sách output ⇒ QD-020 TRÔI sau deploy. Quét đủ sau đó cho thấy không chỗ đọc sống nào đổi dòng (Q2 = 0). Bài học ghi ở FU-465: đổi danh sách
  dùng chung ⇒ quét **mọi** người đọc **trước** khi đẩy, không chỉ sổ.
- Bộ thử trước deploy chép lại bộ lọc phiếu mà không chạy trọn hàm sinh bundle — bù bằng phát lại cũ/mới trên bản sao sau deploy (mục 3.9),
  trước lượt MT thật đầu tiên.
- Đoán đường kiểm admin `/api/admin/pnl/summary` ⇒ 404 (RM-10). Tra route thật trong `main.py` rồi kiểm lại ⇒ 401 ×3.
- Nạp bản sao lưu `.pre_v11210` bằng `spec_from_file_location` ⇒ `None` (đuôi tệp lạ); đổi sang `SourceFileLoader`.
- `git add` đường `artifacts/…` (bị `.gitignore`) làm lần commit đầu không chạy; bỏ tệp đó, commit lại.
- Câu nói tối 27/11 «6 lane MN dừng từ 02/11» sai — đo lại ra mờ dần từ tháng 8 (mục 3.7). Chỉ nói trong chat, chưa vào tài liệu công bố nào.

## 8. Gỡ về

- Mã: chép 11 tệp `backups/<tệp>.pre_v11210` (có trên VPS và máy dev) → `systemctl restart lottery` → so PID.
- Sổ quyết định: `backups/OWNER_DECISION_LEDGER.json.pre_v11210` (trước cả hai lần ghi) hoặc `git revert 2474d78`.
- Bảng `money_board_verdict_lock`: để nguyên — mã cũ không đọc.

## 9. Theo dõi tiếp

| mã | việc | ai | hạn |
|---|---|---|---|
| FU-455 | có dòng chốt verdict cả ba miền trước giờ xổ (15:43 · 16:56 · 17:56); sau xổ `money_board_log.verdict` = bản chốt | agent | 28/11 tối |
| FU-465 | `day_governance` MN · MT `COMPLETE` khi đủ 11/11 sau verify; MB `INCOMPLETE 8/11` là đúng thiết kế | agent | 28/11 tối |
| FU-454 | MB_WATCHDOG 17:55 không báo thiếu khi đủ roster · hết `MISS shadow_after_chain` · `_v10800` thứ Hai 30/11 08:10 | agent | 30/11 |
| FU-328 · FU-255 | `system_alerts` chỉ có dòng khi thật thiếu output; giao diện chờ owner duyệt demo | agent → owner | 28/11 |
| FU-466 | rút lại các phép đo «P&L theo khuyến nghị» từ 28/06 đúng chỗ đã công bố (PRJ-RETRACTION-001) | agent | 05/12 |
| FU-467 | 6 lane MN mờ dần từ tháng 8 — sửa hay để nghỉ (đường dự đoán đang đóng băng) | owner chọn | — |
| FU-453 | phân loại lại 14/09 → 27/11 (phần từ 28/11 đã chạy theo QD-084 k7) | **owner** | — |
| FU-462 | demo 4 mục giao diện (2 câu hỏi trong trang) · 1D thứ Hai 30/11 · Đợt 2 · Đợt 3 | owner duyệt / agent | 30/11 |
| FU-463 | owner tự đặt mật khẩu root mới | owner | 29/11 |

## 10. Ba lớp nguồn (§62)

| lớp | nội dung | bằng chứng |
|---|---|---|
| `OWNER_SAID` | duyệt xử lý dứt điểm theo khuyến nghị; hỏi còn bao nhiêu model, có cần cắt / bổ sung | kho riêng `docs/SO_TUONG_TAC_OWNER.md` 27/11 ~17:35 · ~17:50 |
| `CODE_DID` | 11 model mỗi miền · chốt verdict `/choi` · gỡ 5 job · 3 báo động giả · cảnh báo thiếu output | `evidence/KIEM_V11210.txt` · commit `2474d78` |
| `DOC_SAID` | QD-084 khoản 7 «mẫu số theo roster từng miền»; QD-074 · QD-075 neo `EXPECTED_MODEL_COUNT == 15` | kho riêng `docs/OWNER_DECISION_LEDGER.json` |

**Lệch:** `DOC_SAID` (QD-074/075 neo 15) ≠ `CODE_DID` (11 mỗi miền) — **có chủ ý**, QD-084 khoản 7 thay một phần, ghi `thay_boi_mot_phan` ↔
`thay_the_mot_phan` (RM-19). `DOC_SAID` (phép QD-020 neo 03/08) ≠ `CODE_DID` (phát lại 03/08 ra `CHUA_DU_KHO`) — xử bằng đổi neo, giữ
`bieu_thuc_cu`.

**TanPhatAI cần làm:** cập nhật trạng thái: mỗi miền bỏ phiếu và tính mẫu số 11 (toàn cục 12), ba model chết bỏ cờ chứ **không** dừng hẳn; QD-074 ·
QD-075 bị QD-084 khoản 7 thay **một phần** (neo kế toán). Theo dõi tối 28/11: dòng chốt `/choi` ba miền, `day_governance` MN · MT COMPLETE,
`system_alerts`. Ghi mở FU-466 (rút lại P&L theo khuyến nghị từ 28/06) và FU-467 (6 lane MN). Code đi trước tài liệu: không — mã, sổ quyết định
và bốn mặt cùng commit `2474d78`; script quét ngược `_v11210_quet_nguoc.py` (`245d629`) và phát lại bundle `_v11210_phat_lai_bundle.py` (`2bbfce2`) vào
commit kế, cả hai chỉ đọc kho thật.
