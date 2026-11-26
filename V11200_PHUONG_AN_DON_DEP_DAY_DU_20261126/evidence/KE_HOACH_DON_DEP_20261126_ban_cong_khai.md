<!-- V11200 · phương án dọn dẹp 26/11/2026 · owner yêu cầu 10:10 («Lên phương án kế hoạch dọn dẹp hệ thống …») và 12:0x (QD-082:
     «tiến hành các đề xuất an toàn trước, tuần tự, cuốn chiếu từ dễ đến khó…»). Nguồn: luồng kiểm kê 21 tác tử (chỉ đọc) + agent
     điều phối. Bản tổng hợp gốc của luồng nằm nguyên văn từ mục «Phương án dọn dẹp hệ thống…» bên dưới. -->

# PHƯƠNG ÁN DỌN DẸP — 26/11/2026 (V11200)

## A. Agent điều phối đọc trước — đính chính và bổ sung cho bản tổng hợp

**A1. Đã làm hôm nay (theo QD-082, sổ FU-462):**

| bản | việc | kiểm |
|---|---|---|
| V11196 | dừng 4 lịch không ai đọc (cron 17 · 56 · 82 · 141) | crontab 90 → 86, 162 dòng khác y hệt |
| V11197 | ghi phán quyết rồi dừng 5 phép đo: FU-264 KHÔNG ĐẠT · FU-287 ĐẠT · FU-317 KHÔNG CÓ LỢI THẾ · FU-367 KHÔNG CÓ · FU-398 KHÔNG ĐẠT | crontab 86 → 81 |
| V11198 | sao lưu production ra ngoài VPS lần đầu sau 76 ngày · khoá quyền bản DB để hở trong `/tmp` · QD-082 thay MỘT PHẦN QD-058 | băm khớp; sổ quyết định 0 TRÔI |
| V11199 | vá gốc «print của service chết sau 19:20» (v94/v95 thay `sys.stdout` lúc import; cổng V11189 mù `importlib`) · rút lại RL-052 | tái hiện + thử chặn; kiểm lượt thật 26/11 21:05 |

**A2. Sửa khuyến nghị 1A của bản tổng hợp (6 phép đo tháng 7):** KHÔNG dừng ngay. Agent đã chạy `compute_view()` của cả 6 (kết
nối chỉ đọc): có so sánh trông hơn official chưa được đo đúng — TOTAL-v2 MT đo tiến `m1` bạch thủ 38,6% vs official 29,8%
(n 114); bộ chọn K10/K13 MB cộng phiếu thô 31% vs official 24%. Cùng chiều với FU-400 (luật thô hơn trọng số, z −1,80) và V10917
(lớp ghi đè lỗ). ⇒ Chuyển 1A sang Đợt 2: **đo lại cho đúng** (nền ngày, tách cửa sổ, McNemar ghép cặp, ngưỡng khai trước) rồi
mới quyết dừng hay trình owner đưa vào. Chúng không gọi API model nên chạy tiếp không tốn tiền.

**A3. Mục «lỗi gấp» (in nhật ký) đã xử ở V11199** — bản tổng hợp xếp vào lần restart 27/11; thực tế vá được ngay không cần restart.

**A4. Giới hạn của bản tổng hợp:** tác tử tổng hợp nhận dữ liệu bị cắt (bản kiểm kê vượt trần độ dài). Agent điều phối đã đọc đủ
kết quả gốc của mặt lịch chạy, lane và phản biện các mặt; các mục ở Phụ lục B vẫn **chưa qua phản biện** — không xếp vào đợt.

**A5. Bảo mật máy chủ — cần owner quyết.**
> 🔒 Mục bảo mật máy chủ: chi tiết chỉ ghi ở kho riêng (không công bố công khai) — đang chờ owner quyết.
**A6. Câu owner cần chốt — gom một chỗ:** 1B–1J · 2A–2F · 3A–3G (bên dưới, mỗi câu có khuyến nghị) · A5.1–A5.4 · FU-345 (6f
MN) · FU-459 · FU-453 · FU-451b · FU-270 (= 2A). Trả lời kiểu «1B theo khuyến nghị» là đủ.

---

# Phương án dọn dẹp hệ thống Lottery_AI_Test — bản tổng hợp ngày 26/11/2026

Đây mới là phương án. Phiên kiểm kê không cắt, không sửa, không tắt gì. Việc cắt thật chỉ làm sau khi anh duyệt từng nhóm. Mỗi câu hỏi cần anh quyết đều có mã (ví dụ **1A**), anh trả lời kiểu «1A theo khuyến nghị» là đủ.

**Giới hạn của bản này, em nói trước:** dữ liệu em nhận để tổng hợp bị cắt mất một phần.
- Mặt mã chỉ có phản biện cho 3/24 mục.
- Năm mặt lane, model, giao diện, tài liệu và đường chọn số chỉ được nhắc lại qua phần soát thiếu, em không có kết quả gốc của chúng.
- Việc bù thứ hai bị cắt dở, việc bù thứ ba không có.

Vì vậy chỉ những mục đã qua phản biện mới được xếp vào đợt. Các mục còn lại em để ở Phụ lục B, chờ phản biện bổ sung.

---

## 0. Việc anh hỏi thêm: kiểm tra dự đoán hôm qua và hôm nay

Không mặt kiểm kê nào nhận việc này. Phần soát thiếu đọc nhanh trên DB VPS được mấy số sau:
- **Số model trong bundle chính thức:**
  - Ngày 25/11: MB 7, MN 8, MT 8.
  - Ngày 26/11: MN 11, cao nhất trong 7 ngày.
- **Hệ đã ghi «Nghiêm trọng: chỉ 7/15 model (47%)»** cho MB các ngày 20, 21, 22, 24 và 25/11 (bảng `day_governance`, mức EXCLUDE_ALL), nhưng không trang nào hiện cảnh báo này ra.
- **Ngày 25/11** đã được đánh giá ở bản V11193 (commit `ac30090`), chỉ cần đối chiếu lại.
- **Ngày 26/11:** kết quả xổ về sau 16:35, 17:30 và 18:30, nên phải kiểm riêng sau giờ đó. Số phải đọc từ DB, vì phần in nhật ký của service sẽ tắt lúc 19:20 (xem Đợt 0).

---

## 1. Nói thẳng trước

**Dọn dẹp KHÔNG làm tăng tỉ lệ trúng.** Theo đề bài, trong 30 ngày (27/10 → 25/11, thước tiền /choi, gộp 3 miền):

| cách chơi | lãi/lỗ | độ lệch so với may rủi (z) |
|---|---|---|
| bạch thủ | −23,3 triệu | −0,65 |
| lô 2 số | −27,0 triệu | −0,46 |
| /choi đánh đủ | −37,4 triệu | −0,92 |

Cả ba cách đều nằm trong vùng may rủi. Ba con số này lấy từ đề bài, chưa mặt nào đo lại và chưa có lệnh tái lập. Muốn công bố thì phải tái lập trước (RM-11).

**Cái dọn dẹp mang lại được:**
- Ít chỗ hỏng âm thầm hơn. Ví dụ: hai lần trong 14 ngày model chính chết mà không cổng nào báo (11/11 Claude hết tiền, 25/11 OpenRouter từ chối).
- Báo động đúng chỗ. Hiện có hai bộ canh ngày nào cũng báo giả, làm chìm báo thật.
- Sửa nhanh hơn, vì tìm trong mã bớt 70–78% kết quả nhiễu.
- Máy nhẹ hơn: ít tiến trình chen nhau trong khung ra số MT/MB, ít tranh khoá DB.
- Bớt việc chạy mà không ai dùng kết quả.

**Phần «chả hiệu quả» là chất lượng dự đoán.** Chỉ Đợt 2 nhắm vào phần này. Cách làm: sửa thước đo trước, rồi thử từng cách đơn giản hoá đường chọn số bằng shadow chạy song song. Ngưỡng đăng ký trước, mỗi miền chỉ được tiến, không được lùi. Bản chính thức không bị đụng cho tới khi đủ bằng chứng.

Có một sự thật anh nên biết trước (kết quả việc bù 1, chưa qua phản biện). Tính trên 315 ngày-miền từ 03/08, số bạch thủ /choi thật sự chơi trùng số bạch thủ chính thức ở:
- MN: 99/99 ngày;
- MT: 14/106 ngày;
- MB: 60/110 ngày.

Nghĩa là /choi MN thực chất đang chơi đúng số chính thức. Còn MT thì đi đường riêng phức tạp, và hiện không ai chấm được đường đó thắng hay thua: bộ chấm lane đứng từ 03/08 (FU-270).

---

## 2. Bức tranh cồng kềnh

| mặt | số đo chính |
|---|---|
| Lịch chạy cron | Sáng 26/11 có 90 dòng đang bật, gọi 56 đích, khoảng 349 lượt khởi chạy mỗi ngày. Riêng `_v10979_early_block` chạy mỗi phút, chiếm 240 lượt. Sau V11196 và V11197 còn **81 dòng**. |
| Lịch APScheduler | 45 lời gọi add_job, ra 47 job. Ngày 25/11 có 424 **lượt** chạy của 42 job. Sổ 21/08 ghi «424 job khác nhau» là sai, phải rút lại. |
| Nhật ký `scheduler_logs` | 376.965 dòng, mỗi ngày thêm khoảng 1.190 dòng, 63% không có tên job. Trong 7 ngày gần nhất khoảng 44% là nhiễu: trigger 5 phút chiếm 34%, báo giả WATCHDOG_MISS chiếm 10%. |
| DB production | 1.099,6 MB: 257 bảng, 56 view, 350 chỉ mục. Tăng 358,4 MB trong 97 ngày (khoảng 3,7 MB/ngày, chừng 1,35 GB/năm). 8 bảng gánh 68% mức tăng. |
| Phân loại bảng | 4 bảng khoá (215,0 MB) · 165 bảng sống (711,7 MB) · 48 bảng ngừng ghi nhưng còn người đọc (164,2 MB) · 29 bảng không ai đọc (8,5 MB) · 11 bảng rỗng. Không view nào hỏng. |
| Mã trên VPS | 593 tệp .py trong `web/`, chỉ 180 tệp sống. `web/backend` có 537 tệp. 15 tệp không sống có câu ghi vào 4 bảng khoá; 6 tệp trong đó gắn cứng đường DB kèm lệnh `DELETE`/`UPDATE predictions`. |
| Mã ở máy local | `web/backend` có 1.880 tệp .py. Khoảng 72–78% kết quả tìm `final_bundles` hay `model_daily_eval` rơi vào script chạy một lần. |
| Cảnh báo | Ít nhất 10 bộ canh. `system_health` báo «ALL OK» 3.934 lần trên khoảng 4.300 lượt, nhưng không có phép nào canh «model trả rỗng». Bảng `system_alerts` 199 ngày không có cảnh báo nào. |
| Lượt xem (nginx 12–26/11) | `/api/admin/money-board` 138 lượt · `/du-doan` và `/choi` 50 lượt tải trang · 36/39 panel đo chỉ có lượt gọi trong đúng 1 ngày. Lưu ý: cửa sổ này rơi vào quãng dự án đứng 71 ngày, nên chỉ chứng minh được «không ai xem trong 3 ngày có hoạt động», không chứng minh «không cần». |
| Sao lưu | Trước 12:32 hôm nay, dữ liệu từ 11/09 (76 ngày) không có bản sao nào ngoài VPS. V11198 đã sao lưu một lần. Chưa có lịch sao lưu định kỳ. |
| Đĩa VPS | `data/` 1,8 GB · `web/backend/logs` 163 MB, không xoay vòng (`optimizer_once.log` 129.764.159 byte, tăng khoảng 10 MB/tuần) · `/tmp` 1.022 MB · venv 1,9 GB · `.git` 264 MB |
| Đĩa máy local | `artifacts/live_sync` 300,9 GB tệp DB và 8,2 GB jsonl · `backups/` khoảng 11,2 GB |

---

## 3. Đã làm sáng nay (theo QD-082, sổ FU-462)

| bản | việc | trạng thái |
|---|---|---|
| V11196 | Dừng 4 dòng cron hết việc, không ai đọc: 17 (`_v10661`), 56 (`_perpos_matrix_report`), 82 (`_v10784_verify_0607`), 141 (`_v11067` lấy mẫu khoá DB). | Đã làm. Kiểm lại ngày 27/11. |
| V11197 | Ghi phán quyết rồi mới dừng 5 phép đo: FU-264 KHÔNG ĐẠT, FU-287 ĐẠT, FU-317 KHÔNG CÓ LỢI THẾ, FU-367 KHÔNG CÓ, FU-398 KHÔNG ĐẠT (dòng 131–134, 142). | Đã làm. Crontab 86 → 81 dòng. |
| V11198 | Sao lưu DB (1.099.997.184 byte, sha256 `c45e2f66…`) cùng `prediction_trace.jsonl` ra ngoài VPS. Khoá quyền bản DB để hở `/tmp/lottery_ai.db.pre_w`. Nối QD-082 ↔ QD-058: vế «đừng đi lùi» giữ nguyên. | Đã làm |

Phần đánh số đợt bên dưới thay cho cách đánh số trong FU-462 (0b, 1, 2a, 2b).

---

## 4. Kế hoạch theo đợt

Luật chung cho mọi đợt:
- Làm xong đợt này mới sang đợt sau.
- Mỗi nhóm việc xong là một bản đóng trọn: bốn mặt CHANGELOG/SSOT/STATE/HISTORY, commit, báo cáo công khai.
- Soi người đọc trước khi dừng (RM-20).
- Sao lưu trước khi sửa.
- Mọi việc sửa `scheduler.py` hay `main.py` gom vào **một lần restart có kế hoạch**, có so PID trước và sau. FU-462 đã khai lần này vào sáng 27/11.
- Không restart hay sửa cron quanh 30/11 00:30 (FU-456 đang chờ lần đào luật thật).

### Đợt 0 — việc không cần anh quyết

**Anh không cần làm gì ở đợt này.** Không xoá gì.

**0a. Ghi sổ, gắn nhãn, rút lại số sai (chỉ sửa tài liệu)**

| việc | bằng chứng | được | mất / rủi ro | gỡ về | kiểm sau khi làm |
|---|---|---|---|---|---|
| Ghi nhãn RETIRED trong SSOT, mỗi nhãn kèm ngày ngừng: `gan_signal_shadow_v100`; 7 bảng V105/V104/V99; `prompt_3tang_ab_shadow_v11059`; 11 bảng mà giao diện vẫn đọc; 6 bảng mà pipeline vẫn đọc; 4 bảng rỗng (`rule_effectiveness`, `training_records`, `bundle_replay_compare_daily`, `mb_t3_prereg_daily`); 14 tệp lane đã nghỉ (ghi trong sổ, không sửa tệp) | Phản biện mặt bảng và mặt mã: giữ hoặc hạ mức | Người đọc sau không lấy số tháng 5–7 làm số đang sống | Không có | Gỡ nhãn | Grep SSOT ra đủ nhãn |
| Ghi đúng trạng thái cho bảng không phải RETIRED: `daily_eval_log` «tạm dừng theo FU-453»; hai bảng `v10883_*` «chờ sự kiện»; `pp1_live_watch_daily` vẫn sống (0 sự kiện); `v10810_station_repair_backup` là **vật chứng, cấm xoá** | Phản biện mặt bảng | Tránh gắn nhầm nhãn, lỗi đã gặp ngày 08/09 | Không có | Sửa dòng sổ | — |
| Rút lại tại chỗ gốc theo PRJ-RETRACTION-001: (1) «424 job khác nhau» (`docs/KIEM_KE_DON_DEP_20260821.md:55`), đúng là 424 lượt của 42 job; (2) «16 bảng ngừng ghi còn người đọc», đúng là 27 bảng (131,1 MB), có 13 bảng bị sót; (3) «6,5 MB», đúng là 8,17 MB khi tính cả chỉ mục; (4) FU-451(a) «RUNTIME_PROVEN» (xem mục lỗi gấp bên dưới) | Kiểm kê, soát thiếu, việc bù 0 | Sổ khớp sự thật | Không có quyết định nào đã dựa trên số (1)–(3), vì QD-070 chưa cắt gì | — | Đủ bốn phần rút lại |
| Lập danh sách «cấm dời» dùng chung: 27 tệp .py mà kiem_code hoặc go_ve của quyết định ACTIVE trỏ tới; 3 tệp `migration_*.py` (tab Migrations trên /monitoring đọc); thư mục `scripts/` ở gốc VPS (`scheduler.py:754-763` và `:1878-1890` import từ đây); tệp lane cần cho `_v10919_retire_lanes.py --rollback`; `CHANGELOG.md` và `docs/` trên VPS | Soát thiếu; phản biện mặt mã | Đợt 3 không làm gãy cổng | Không có | — | Danh sách được commit |
| Commit các script đo và chụp dữ liệu thô vào `evidence/`. Chốt một định nghĩa cho các số đang lệch giữa các mặt | Soát thiếu: mọi lệnh tái lập đang trỏ vào scratchpad tạm; journal chỉ giữ khoảng 6 ngày | Số công bố tái lập được | Không có | — | Chạy lại ra đúng số |

**0b. Sửa báo động (có sửa mã, đi cùng lần restart gộp, không cắt chức năng nào)**

| việc | được | rủi ro / lưu ý | kiểm |
|---|---|---|---|
| V10785 watchdog: chỉ chạy phép `shadow_after_chain` khi roster shadow có model (đọc lúc chạy). Chỉ sửa phép kiểm ở `_v10785_late_fill.py:231-260`, **không đụng điểm kích** trong chuỗi AI chính thức (`scheduler.py:5700-5770`). | Bớt khoảng 113–116 báo giả mỗi ngày | Biến nhớ trong RAM bị xoá mỗi lần restart | Thử hai chiều bằng `run_watchdog_checks(dry_run=True)` (RM-15) |
| MB_WATCHDOG 17:55: lấy ngưỡng từ roster lúc chạy (đúng hướng FU-454) | Hết báo giả mỗi ngày | Giữ nguyên job | RM-15 |
| `_v10800` (báo đỏ 16 tuần liền): sửa ngưỡng theo roster và lane đang sống; bỏ `mn/mt_rule_context` khỏi phép 4 | Cổng báo đúng trở lại | Đổi định nghĩa cổng | RM-15 |
| **Thêm** cảnh báo «mỗi model chính thức có output hợp lệ ở mỗi miền-ngày». Cách rẻ nhất: hiện ra cảnh báo «chỉ 7/15 model» mà `day_governance` đã ghi sẵn. Thêm trước, bớt bộ canh cũ sau. | Bắt đúng loại sự cố đã lọt 2 lần | Không bỏ bộ canh nào trong đợt này | Phát lại ngày 11/11 và 25/11 phải đỏ, ngày sạch phải xanh |

**Lỗi gấp nằm ngoài dọn dẹp** (việc bù 0, có bằng chứng journal nhưng chưa qua phản biện):
- **Nguyên nhân:** `_materialize_v94_safe_batch.py:52` và `_materialize_v95_data_integrity_audit.py:32` thay `sys.stdout` ngay lúc được nạp. Hai job nạp chúng chạy 19:18 và 19:20. Sau lần nạp thứ hai, phần in của service chết im lặng tới lần restart sau.
  - Ngày 25/11: trước 19:20 có 886/901 dòng tới journal, sau 19:20 thì 0/559.
- **Dự đoán và kết quả vẫn chạy đúng.** Thứ mất là khả năng quan sát.
- **Vì sao phải rút lại FU-451(a):** cổng `_v11189_cong_stdout.py` dò bằng biểu thức chuỗi nên không thấy `importlib.import_module`, và báo DAT oan.
- **Cách sửa:** vá 2 dòng, cộng sửa cổng cho nhận ra `importlib`.
  - Hai mô-đun này chỉ được nạp từ 19:18. Nên đặt bản vá lên đĩa trước 19:18 là có hiệu lực ngay, không cần restart.
  - FU-462 đã xếp việc này vào lần restart 27/11.
- **Còn một chỗ mâu thuẫn:** việc bù 0 nói `_v101_shadow_pilot.py:38` được nạp lúc 19:23. Mặt job và mặt bảng thì cho thấy hai chỗ nạp đó nằm dưới lệnh `return` của job đã tắt, tức không bao giờ chạy. Vẫn nên vá luôn vì rẻ, nhưng không phải lý do gấp.

**Nếu anh chưa chốt:** đợt này không cần anh chốt.
**Ước lượng (của em, không phải số đo):** 0a mất 1 phiên. 0b mất 1 phiên cộng lần restart gộp, rồi theo dõi 7 ngày.

### Đợt 1 — dừng job, lane, lệnh chạy đã hết việc; giữ bảng làm bằng chứng

| mã | việc | bằng chứng | được | mất / rủi ro | gỡ về |
|---|---|---|---|---|---|
| 1A | 6 phép đo tháng 7: `_v10789` (dòng 84–87), `_v10801` (89), `_v10803` (90), `_v10821` (92), `_v10829` (96), `_v10844` (103). Chạy chế độ xem lấy phán quyết, ghi vào SSOT, rồi mới dừng. | Ngưỡng đã tới từ tháng 7; không có FU nào theo dõi; lane TOTAL V2/V3 không cần các cron này | Bớt 9 tiến trình mỗi ngày | Giữ tệp vì `_v10822`/`_v10832` còn import | Bỏ dấu # |
| 1B | `_v10708` MN/MT (dòng 63, 64), kèm gắn nhãn «đã đông» cho khối luật MN/MT trên /du-doan-test (`main.py:14889`) | Chỉ nuôi lane V10707, lane này nghỉ từ 01/08 | Bớt 2 tiến trình mỗi ngày | Không đụng rerank MB | Bỏ dấu # |
| 1C | Ba bộ AI-limit (dòng 18, 25, 29), `_v10645` (dòng 7), `slice_policy` và phần gắn nhãn «reduced» trong `model_progress`: khai tử cùng một lượt | Kế hoạch chưa từng được áp suốt 178 ngày; panel đang gắn nhãn REDUCED cho cả glm-5.1, model anh vừa giữ | Bớt 4 tiến trình mỗi ngày, hết nhãn giả | Phải có QD mới ghi rõ «QD-080 thay vòng LIMIT 01/06» (RM-19) | Khôi phục từ bản sao lưu |
| 1D | `_mb_advanced_lane_daily.sh`: bỏ 2 lane đã nghỉ `_v10679`/`_v10680`, gộp dòng 52 với 66, giữ lượt 17:43 (đóng FU-185, quá hạn 109 ngày) | Owner đã cho nghỉ hai lane này ngày 01/08 | Bớt khoảng 6 tiến trình trong khung MB | Số phụ MB trên /du-doan-test còn 1 ứng viên; pool /choi MB đổi từ thứ Hai sau | Lấy lại .sh từ bản sao lưu |
| 1E | `_v10869` CP-L6 (dòng 105): đóng CP-L6 bằng một quyết định ghi rõ, gắn nhãn panel, giữ `v10869_m2_roster_ab_daily` | Từ 14/09 ba nhánh A/B gần trùng nhau: lệch nhiều nhất 19/218 miền-ngày | Bớt 1 tiến trình mỗi ngày; 27 MB ngừng tăng | Giao thức CP-L6 ghi «bắt buộc trước MỌI xử lý», nên phải có quyết định của anh | Bỏ dấu # |
| 1F | Gan hội tụ (FU-394, dòng 135): đóng | −0,94 điểm, CI95 [−5,5; +3,6]; muốn thấy +5 điểm phải đo 4–6 năm | Bớt 1 tiến trình mỗi ngày | Anh chưa chốt FU-394 | Bỏ dấu # |
| 1G | D-30 (dòng 143): chạy đúng thủ tục phán quyết của QD-072, rồi dừng | Quá ngày đọc 57 ngày; mọi bản ghi đều sinh sau mốc khoá | Chốt được một phép đo đã treo | Nhiều khả năng ra INVALID_EXPERIMENT | Bỏ dấu # |
| 1H | `_v10979`: thu hẹp khung chạy còn MN 05:10–06:30, MT 16:30–16:59, MB 17:25–17:59 | 114 ngày qua, giờ chốt muộn nhất là MN 05:33, MT 16:57, MB 17:46 | Bớt khoảng 97 tiến trình mỗi ngày | Đây là việc anh yêu cầu ngày 04/08; không làm cùng đợt với `_v10879` | Khôi phục 3 dòng cron |
| 1I | Gộp V93/V94/V95 (mục D4 của FU-160) | FU-160 tự đề xuất gộp | Gọn lịch chạy | **Phải vá lỗi in nhật ký trước**; gộp không chữa được lỗi đó | git revert |
| 1J | `system_alerts` (FU-255): nối lỗi nhà cung cấp và việc cách ly model vào bảng này rồi hiện lên trang, hay khai tử | 199 ngày không có cảnh báo dù đã có 2 sự cố thật | Có một chỗ chứa cảnh báo có cấu trúc | — | — |

**Không cần anh quyết** (đã duyệt từ trước hoặc chỉ dọn phần đuôi, làm trong lần restart gộp):
- Gỡ 5 job APScheduler đã tắt (V81, V101, V104 materializer, V104 Phase B, V105) cùng mã chết nằm dưới `return`. Anh đã duyệt tắt ngày 31/05. Sửa kèm `_v87_master_board.py:349`.
- Trigger 5 phút: chỉ đổi cách ghi nhật ký (ghi khi trạng thái miền đổi). Giữ nhịp và cổng sẵn sàng. So `du_doan_test_bundles` 7 ngày trước và sau.
- `_v10660`: dựng phép tương đương trong `_v10900`, chạy song song ít nhất 7 ngày rồi mới tắt dòng 15. **Giữ tệp**, vì kiem_code của QD-031/032 chạy chính tệp này.
- `_v10879`: **không cắt** 8 lượt predraw. Lượt early_block gọi lane đã trượt 19 lần, và 18 lần trong đó do chính các lượt này cứu lại. Phải điều tra lỗi rc=1 trước.

**Owner cần quyết:**
- **1A** dừng sau khi đã ghi phán quyết? Khuyến nghị: **đồng ý**. Ngưỡng đã quá hạn từ tháng 7, và phán quyết được ghi trước khi dừng.
- **1B** đồng ý? Khuyến nghị: **đồng ý**, lane nguồn đã nghỉ từ 01/08.
- **1C** ghi QD «QD-080 thay vòng LIMIT 01/06» rồi khai tử cả cụm? Khuyến nghị: **đồng ý**. Kế hoạch chưa từng được áp, và đang gắn nhãn sai cho model anh vừa chốt giữ.
- **1D** đồng ý? Khuyến nghị: **đồng ý, làm vào thứ Hai**. Đây là việc anh đã quyết ngày 01/08.
- **1E** đóng CP-L6? Khuyến nghị: **đóng**. A/B đã mất sức đo từ khi có roster QD-080.
- **1F** đóng FU-394? Khuyến nghị: **đóng**, vì không có lợi thế và không thể đo đủ trong thời gian hợp lý.
- **1G** chạy thủ tục phán quyết D-30? Khuyến nghị: **đồng ý**.
- **1H** thu hẹp khung chạy? Khuyến nghị: **đồng ý**, vì vẫn bắt được ca chốt trễ kiểu 13/08.
- **1I** gộp? Khuyến nghị: **chưa gộp**. Vá lỗi in nhật ký trước, rồi mới quyết.
- **1J** nối hay khai tử? Khuyến nghị: **nối**, vì cảnh báo chính là chỗ đang hổng.

**Nếu anh chưa chốt:** mục nào chưa chốt thì giữ nguyên, vẫn chạy như hiện nay. Không mục nào gây hại khi để nguyên.
**Ước lượng (của em):** 1–2 phiên, cộng 7 ngày kiểm rằng log của các job đã dừng không có dòng mới và `_v10900` không thêm LỆCH.

### Đợt 2 — đơn giản hoá đường chọn số, chỉ qua shadow

Luật của đợt:
- Đăng ký ngưỡng trước ngày chốt (RM-03).
- Nền đúng cho từng bên (RM-18). Hằng số như VIF phải đo lại trên chính thước đang dùng (RM-21).
- Tách trong và ngoài cửa sổ chọn (PRJ-SELECTION-WINDOW-001).
- Chỉ đo tiến. Một miền lùi có ý nghĩa là DỪNG, dù tổng thể vẫn dương.
- Không đụng `/du-doan` chính thức.
- Việc nào làm đổi đầu vào của method /choi đang khoá thì chỉ áp vào thứ Hai và ghi số trước/sau. Theo việc bù 1, các việc đó gồm: nhịp/điều kiện trigger 5 phút, phần MB của `_v10703`, tensor, nhánh «tomorrow» của V67/V71, writer của chân đang khoá.

**2.1 Sửa thước đo trước.** Không đo được thì không đơn giản hoá được.

| mã | việc | bằng chứng | được | rủi ro |
|---|---|---|---|---|
| 2A | Bộ chấm lane (FU-270): sửa, hay ghi rõ lane không còn được chấm | Việc bù 1 (chưa qua phản biện): `_du_doan_test_closeout_evaluator.py:127` gọi `int(run_id)` trong khi run_id dạng chữ; lần chấm cuối 03/08 | Biết lane thắng hay thua | **Không bao giờ cắt `du_doan_test_runs`**. Sửa bộ chấm không đổi số /choi. |
| 2B | Mẫu số «15 model» (`database.py:5021-5025`) trong khi bundle chỉ có 7–11 model | Mọi ngày từ 12/09 đều bị loại, nên sổ điểm combo-super đứng từ 11/09 | Chấm lại được combo-super | Mẫu số này quyết cổng phát hành `/api/final-bundle` (`main.py:10962-11024`): tính song song trước, không đổi cổng. Giữ `auto_daily_eval` tới khi xong (FU-453). |
| 2C | Nhánh «today» của V70/V71 và V77 lúc 19:00 ghi đè bản HYBRID sau giờ xổ | Việc bù 1: tuần này số /choi đã chơi khác bản đang lưu ở cả 3/3 ngày | Bản ghi khớp số đã chơi | Giữ nhánh «tomorrow», vì nó nuôi chân MT_HYBRID_V1. Chụp lại 14 ngày trước khi đổi. Vẽ sơ đồ phụ thuộc của 7 job tối trước. |

**2.2 Các cách đơn giản hoá đem thử bằng shadow:**
- **2D Tensor độ mạnh model đứng từ 05/05.** Chọn dựng lại writer, hay bỏ số hạng tensor. Chạy cả hai thành biến thể shadow của bộ chọn budget, so với bản hiện hành, rồi xử cả 4 chỗ đọc.
- **Lọc 5 voter đã chết** (deepseek-reasoner, gemini-2.5-pro, gpt-5-mini, gpt-5.4, qwen3-max-thinking): họ đang chiếm 28% chỗ voter. Chạy khô trước để chứng minh số không đổi.
- **2E `_v10703`.** Chọn (a) dời lượt MN/MT lên trước mốc chốt, hoặc (b) chỉ chạy MB và gắn nhãn RETIRED cho bảng sàng lọc MN/MT. Không đổi phần MB.
- **Cụm nghiên cứu /choi.** V11197 ghi rằng ở MT có cách «hơn official» (bạch thủ 41,9% so với 35,2%), nhưng chưa có nền, chưa tách cửa sổ, chưa kiểm ý nghĩa. Phải đo lại cho đúng rồi mới dừng hay đưa vào.
- **Các phép đo shadow.** Quyết theo từng phương pháp (FU-418), không theo từng bảng. Riêng chuỗi lag1 → adaptive_exploit phải trả lời được nó còn phục vụ gì (QD-075).
- **`_mb_perpos_daily.sh`.** Ba ý kiến ngược nhau (xem Phụ lục C). Phải dump prompt MB từ hàm đang serve (RM-14) trước khi bỏ dòng nào.
- **2F Bảng cộng dồn so cặp model** (QD-071): nối cron và panel, hay ghi RETIRED.

**Owner cần quyết:**
- **2A** Khuyến nghị: **sửa bộ chấm**. Lỗi gốc chỉ có một dòng, và không có bộ chấm thì /choi đang chọn trong mù.
- **2B** Khuyến nghị: **tính song song theo roster**.
- **2C** Khuyến nghị: **đồng ý, làm vào thứ Hai**.
- **2D** Khuyến nghị: **chạy cả hai biến thể shadow**, chưa đổi bản thật.
- **2E** Khuyến nghị: **(b)**, đơn giản hơn. MN/MT có 0/61 ngày ra trước giờ chốt, nên chưa từng là đo tiến.
- **2F** Khuyến nghị: **nối**, vì đó là phần anh đã ký dựng.

**Nếu anh chưa chốt:** đường chọn số giữ nguyên. Chỉ có 2.1 là sửa thước đo.
**Ước lượng (của em):** 2.1 mất 2–3 phiên. Mỗi biến thể shadow cần ít nhất 14 ngày rồi mới đọc, và chỉ đọc khi đủ n theo bản đăng ký trước.

### Đợt 3 — dữ liệu cũ và lưu trữ

Điều kiện trước:
- Có lịch sao lưu định kỳ ra ngoài VPS, kèm integrity_check, sha256 và 2 bản.
- Đã gỡ mọi chỗ trong mã còn trỏ tới bảng sắp xoá (A58).
- Xuất `.csv.gz` kèm DDL và sha256 rồi mới DROP.
- VACUUM vào khung yên. Lệnh này khoá ghi toàn DB và cần khoảng 1,1 GB chỗ tạm.
- Anh duyệt theo nhóm (QD-070, FU-390).

| mã | việc | dung lượng | điều kiện riêng |
|---|---|---|---|
| 3A | Lịch sao lưu định kỳ ra ngoài VPS | — | Anh chọn tần suất |
| 3B | Xoá `gan_signal_shadow_v100` và 9 bảng V101–V104 | 67,3 + 57,5 MB | Sau khi gỡ mã chết (Đợt 1), route `v101-shadow-pilot` và khối đọc ở `_v10763:323-330`, `_materialize_adaptive_exploit_v1.py:541` |
| 3C | Xoá 19 bảng replay (đã bỏ `v10810_station_repair_backup` và bảng bị liệt kê trùng) và 4 bảng chết bị sót ngày 21/08 | khoảng 8,2 MB | Anh có thể chọn «không làm», vì quá nhỏ |
| 3D | Xoay vòng log: logrotate (copytruncate, compress) cho job còn sống; nén log của job đã dừng; trích các dòng «DONE … best_lift» ra trước; giữ đọc được lượt 06/09 và 13/09 (bằng chứng QD-079); không đụng `v11067_khoa_db.jsonl` | khoảng 150 MB | Không đụng job tối ưu trọng số (FU-400) |
| 3E | Tệp DB rác: `data/lottery.db`, `_stale_archive`, `v15.bak`, `memory_14d`, `/root/backups/lottery_ai_stale.db`, cùng tệp 0 byte ở gốc. Chép về máy local rồi mới xoá. | khoảng 38,6 MB | — |
| 3F | Ba bản DB cũ (30/05, 11/09 ×2): chuyển về máy local, ghi vào SSOT | khoảng 2,0 GB | Chỉ làm sau 3A |
| 3G | Dời 183 + 66 script chạy một lần trên VPS: một commit `git mv` ở kho riêng trước, rồi mới `mv` trên VPS ra `/root/backups/ma_<ngày>/` kèm INDEX | `web/backend` 537 → khoảng 284 tệp | Giữ 3 tệp `migration_*.py`. Dời cụm `/root/thu_receipt*.sh` đi cùng 2 tệp .py chúng gọi. Trình theo từng nhóm tiền tố. |
| — | Cắt bớt `v10869_model_bucket_scorecard` | 24,4 MB | Chỉ làm sau 1E |
| — | `scheduler_logs`: chỉ tỉa hai mẫu nhiễu | — | Sau khi FU-456 đóng; xuất trước |

Làm nhẹ tài liệu quản trị (CHANGELOG 3,0 MB, SSOT 1,3 MB…): dữ liệu em nhận không có kết quả của mặt tài liệu, nên chưa có đề xuất. Nguyên tắc vẫn giữ: không mất mục nào, cổng `_v11027` chặn.

**Owner cần quyết:**
- **3A** Khuyến nghị: **mỗi ngày**. Hôm nay mới lộ ra 76 ngày không có bản sao nào. Đây là khuyến nghị của em, các mặt không đo tần suất.
- **3B** Khuyến nghị: **đồng ý** sau khi đủ điều kiện.
- **3C** Khuyến nghị: **đồng ý**, gộp chung với 3B.
- **3D** và **3E** Khuyến nghị: **đồng ý**.
- **3F** Khuyến nghị: **đồng ý** sau 3A.
- **3G** Khuyến nghị: **đồng ý**, theo từng nhóm.

**Nếu anh chưa chốt:** DB tăng khoảng 3,7 MB mỗi ngày, ổ còn trống 23 GB, nên không gấp. Riêng 3A thì nên chốt sớm.
**Ước lượng (của em):** 2–3 phiên, cộng một khung VACUUM.

---

## 5. Những thứ PHẢI GIỮ

- **Đường chính thức:**
  - `/du-doan` phải đủ 15/15, luôn hiện số dự đoán.
  - combo_super UNIFIED TOP-3, roster QD-080, sàn pool ML ≥ 4 và AI ≥ 3.
  - `/choi`: money board, cron khoá 100–102, hợp đồng output 104.
  - Lane thử đủ 20/20.
- **Bốn bảng khoá** `predictions`, `final_bundles`, `lottery_results`, `model_daily_eval`: không cắt dòng nào.
- **Cổng an toàn:**
  - `_v10900` (18:05), `_v10891`, `_v10945`, `_v10871`, cổng hạn 120.
  - 10 cổng commit, `session_start`, `report_gate`, `decision_ledger`, `_v11044`, `_doc_prepend`, `_v11062`.
- **Các job nuôi /choi MT:** chuỗi V66→V71 (nhánh «tomorrow») và trigger 5 phút.
- **Khoá của anh:**
  - Ngày 26/11 (QD-081): FU-195, 400, 183, 397, 456/340/338, 345, 392.
  - Ngày 29/07: «đánh giá dùng TOÀN BỘ chiều dài live/shadow», nên không cắt bảng shadow sống theo tuổi.
- **Bảng và tệp phải giữ:**
  - Các bảng `v11178_*` (kiem_code của QD-076).
  - `mt_model_hit_output_drop_shadow` (FU-391) và cặp bảng cohere.
  - `data/models_dong_bang_20260806` (bản đối chứng của FU-285).

---

## Phụ lục A — đã bác và vì sao

| đề xuất | vì sao bác |
|---|---|
| Điều tra anti-trap (dòng 136) | FU-397 đã đóng CLOSED_FAIL. Phản biện đề nghị chuyển sang tắt nếu có QD thay vế «cấm tắt» của QD-058; V11198 đã gỡ vướng này, nhưng việc tắt chưa qua phản biện riêng nên cần anh duyệt. |
| Xoá 4 bảng `v11178_*` | kiem_code của QD-076 chạy thẳng trên các bảng này |
| Giữ 90 ngày cho `shadow_method_scoreboard` | Khoá của anh ngày 29/07; FU-418 cần lịch sử này; ổ còn 23 GB |
| Giữ 90 ngày cho `shadow_results`/`shadow_candidates` | Cùng khoá trên; còn là bằng chứng cho QD-076/077/078 |
| Giữ 90 ngày cho `experimental_preview_shadow` | FU-270 chưa chốt; trang pnl đọc theo ngày |

## Phụ lục B — chưa qua phản biện, chưa xếp vào đợt

- **Phần soát thiếu:**
  - Journal chỉ giữ 7 ngày.
  - `/tmp` nặng 1 GB.
  - venv 1,9 GB, trong đó có thư viện CUDA trên máy không có GPU.
  - Ba nhánh git cũ.
  - Bộ canh `_v10644` chấm nhầm 6 bảng chết là còn sống.

## Phụ lục C — mâu thuẫn giữa các kết quả

1. **`_mb_perpos_daily.sh`:**
   - Phản biện job: bỏ lệnh `force`, giữ `_v10689`/`_v10693`.
   - Phản biện lane: làm ngược lại.
   - Soát thiếu: `_v10689` không nuôi TIER2, và lệnh `force` lúc 18:10 cũng thừa (13/13 ngày trùng lượt 04:45).
   - Em chọn cách chặt nhất: dump prompt trước.
2. **AI-limit:** phản biện job cho tắt kèm vá, phản biện bảng đòi có QD trước. Em chọn cách chặt hơn (mục 1C).
3. **`auto_daily_eval`:** phản biện job cho gỡ, phản biện bảng và soát thiếu nói đây là lỗi đang mở (mẫu số). Em chọn giữ (mục 2B).
4. **`_v10869` và `_v10660`:** phản biện job cho dừng, các mặt khác chặn. Em chọn cách chặt hơn.
5. **Lỗi in nhật ký:**
   - Soát thiếu dự báo ngày 27/11 bảng điểm lại lỗi 3/3.
   - Việc bù 0 nói bảng điểm vẫn sạch, vì sau V11189 lỗi bị bọc lại; thứ chết là phần in, chết im lặng.
   - Việc bù 0 còn nói V101 được nạp, mặt job và mặt bảng nói không.
6. **Cùng một đại lượng, mỗi mặt một số:**
   - `scheduler_logs` 7 ngày: 8.060 / 8.361 / 8.416 / 8.428.
   - WATCHDOG_MISS: 793 / 810 / 812 / 814.
   - Dòng PENDING: 3.835 / 3.880.

## Phụ lục D — chưa đo được

- CPU, RAM, thời gian chạy của từng job, và tải lúc đỉnh khung MT/MB.
- Giá trị dự đoán của từng lane khi làm ứng viên /choi.
- Thời gian VACUUM và kích thước tệp xuất.
- Cụm cron dày có thật là gốc của FU-402 (hiện mới là giả thuyết).
- Lượt xem cũ hơn 15 ngày.
- Ai đã từng chạy `deploy_all_zip`.
- Kết quả 26/11.

## Phụ lục E — lệnh tái lập các con số chính

Các script nằm trong `C:\Users\Admin\AppData\Local\Temp\claude\a4571337a459c451\c6dde3d1-a5f3-4ecc-8e60-d05f3ac93c04\scratchpad\`. Đây là thư mục tạm, phải commit vào `evidence/` trước khi công bố.

- **Mặt job:** `job_parse_cron.py`, `job_q2.py`–`job_q4.py`, `job_access.py`; phản biện ở `pb_job\q2.py`–`q5.py`.
  - Lệnh đếm lượt chạy APScheduler: `journalctl -u lottery --since '2026-11-25 00:00' --until '2026-11-26 00:00' -o cat | grep -c 'Running job'`
- **Mặt bảng:** `bang_mat\kk_bang.py`, `tong_hop_cum.py`, `dem_giu.py`; phản biện ở `critic_bang\q_db.py`.
- **Mặt mã:** `mat_ma\so_chot.py`, `dem_lop.py`, `rui_ro_ghi.py`, `tai_lap_phu.py`.
- **Lỗi in nhật ký (việc bù 0):** `bu0\b7_chot.py`, `bu0\a3_gate_blind.py`, `bu0\repro\driver.py`.
- **/choi (việc bù 1):** `bu1_do.py`–`bu1_do4.py`.
- **Đã làm sáng nay:** `CHANGELOG.md` dòng 1–101 (V11196–V11198), `docs/FOLLOW_UP_TRACKER.md` dòng 1–14 (FU-462).

TanPhatAI cần làm: cập nhật FU-462 theo bản phương án này. Theo dõi các việc sau:
- Rút lại FU-451(a) và hai số của sổ kiểm kê 21/08 (PRJ-RETRACTION-001).
- Bản vá in nhật ký V94/V95 trong lần restart 27/11.
- Các quyết định 1A–1J, 2A–2F và 3A–3G của owner.
- Chạy phản biện bổ sung cho 21 mục mặt mã và cho các mặt bị cắt khỏi dữ liệu tổng hợp.
- Code đi trước tài liệu ở V11196–V11198: phải đối chiếu với `docs/SO_TUONG_TAC_OWNER.md`, mục ngày 26/11 (QD-082).