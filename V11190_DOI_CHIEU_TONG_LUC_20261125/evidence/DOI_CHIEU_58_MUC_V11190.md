# ĐỐI CHIẾU 58 MỤC «CHỜ DỮ LIỆU SỐNG» SAU 71 NGÀY HỆ ĐỨNG — V11190 (25/11/2026)

**Phạm vi:** mọi mục còn treo trong `docs/FOLLOW_UP_TRACKER.md` mang nhãn `DEPLOYED_PENDING_LIVE_VERIFY` (30) ·
`WAIT_LIVE` (18) · `DEPLOYED_PENDING_OWNER_VERIFY` (7) · `DO_TIEN_DANG_CHAY` (3). Trừ `FU-451` (mở trong V11189,
nghiệm thu 25/11) còn **57 mục**, chấm theo **đúng ngưỡng đã đăng ký** trong sổ, đo lại **trên DB VPS** (`mode=ro`).

**Cách làm:** 3 agent kiểm toán CHỈ ĐỌC chạy song song (24/11 23:49 → 25/11 ~00:10 ICT), mỗi mục trích cam kết
nguyên văn kèm `tệp:dòng`, lệnh đo, con số thật. Nháp đo nằm ở scratchpad phiên (không commit). Hai phát hiện nặng
nhất được agent điều phối **tự kiểm lại** trước khi dùng: (1) `du_doan_test_results` toàn `PENDING` từ 03/08 —
**xác nhận**; (2) cơ chế rò nhãn `DO_TIEN` (`weekly_rule_miner.py:202` + `_v11025_khoa_luat_ben.py:241`) —
**xác nhận ở tầng mã**; (3) số `FU-284` — **tái lập được** (`RL-049`).

**KHÔNG ÁP NHÃN tự động.** Owner ký 09/08 (Q4c): *«CẤM đóng hàng loạt. Rà THEO NHÃN»*. Cột «đề xuất» chờ owner
duyệt (`FU-459`).

## Tổng

| phán quyết | số | ghi chú |
|---|---|---|
| ĐẠT | 19 | cơ chế đã vá vẫn đứng vững / ngưỡng đã đạt |
| TRƯỢT | 12 | đủ mẫu mà không đạt ngưỡng, hoặc cổng chưa từng được nối |
| HẾT_TIỀN_ĐỀ | 11 | model/làn đã rời cuộc (roster §AA 13/09, shadow tắt 14/09, cách ly do hết tiền) |
| CHƯA_ĐỦ_MẪU | 2 | cửa sổ đã chốt, owner cấm kéo dài |
| KHÔNG_ĐO_ĐƯỢC | 4 | thiết kế bất khả / công cụ chưa lên VPS / không có bộ chấm |
| CẦN_OWNER_NHÌN | 9 | tab giao diện admin — agent chỉ kiểm được tầng tệp/route |

## Nhóm model · combo · chọn model (16)

| mã | việc | phán quyết | con số chính | đề xuất nhãn |
|---|---|---|---|---|
| FU-186 | 7 ngày sau tắt lớp ghi đè | ĐẠT (tiêu chí 1, 3) | MT/MB phiếu = công bố **116/116** ngày; tỉ lệ 7/21 = 33,3% vs nền 34,2% (chưa được phép kết luận) | `CLOSED_REPORT` |
| FU-203 | gemini-3.5-flash chấm tuần | HẾT_TIỀN_ĐỀ | 02–08/08: 7/21; ngưỡng 30% còn **dưới nền** 34% | `CANCELLED` |
| FU-202 | gemini lọt top-2 combo | HẾT_TIỀN_ĐỀ | được chọn 5/128 lượt; rời cuộc 14/09 | `CANCELLED` |
| FU-200 | đổi total trước combo | HẾT_TIỀN_ĐỀ | thay model chưa từng diễn ra (V10934 không deploy) | `CANCELLED` |
| FU-196 | đo hoán đổi model | HẾT_TIỀN_ĐỀ | lệch so với nền +4,5 → +1,8 điểm, n=14/miền | `CLOSED_REPORT` |
| FU-195 | ngưỡng gỡ glm-5.1 | **TRƯỢT theo chữ** | 11–24/11: 2/28 = 7,1% > 6% — **ngưỡng nổ vì nhiễu** (P≈0,42 với nền 5,1%); MT lỡ hạn 0 ngày | chờ owner — gỡ glm-5.1 làm MT còn 2 AI |
| FU-197 | gemini sau 503 | HẾT_TIỀN_ĐỀ | lỗi nhà cung cấp 0/40 | `CANCELLED` |
| FU-204 | gpt-5.4 gọi về | HẾT_TIỀN_ĐỀ | BT 14/40 = 35% ≈ nền; **«32,69%» không tái lập được** (chưa xác minh độc lập) | `CANCELLED` + rút lại sau khi tái lập |
| FU-198 | gemini-3.5 vs 3.6 | HẾT_TIỀN_ĐỀ | 33,6% vs 29,4%, McNemar z +0,90 | `CANCELLED` |
| FU-356 | glm-5.2 rỗng ở MB | HẾT_TIỀN_ĐỀ | ngưỡng đã nổ 27/08 (6 lần/14 ngày) → xử ở FU-450 | `CLOSED` (thay bởi FU-450) |
| FU-359 | model tiến triển sau đổi prompt | CHƯA_ĐỦ_MẪU | cửa sổ chốt, owner cấm kéo dài (20/08) | `CLOSED_REPORT` |
| FU-344 | ngưỡng FU-284 | CHƯA_ĐỦ_MẪU | tái lập: MT +10,5 z +1,30 (công bố +14,2 z +1,72) → `RL-049` | `CLOSED_REPORT` |
| FU-340 | PHẦN 4 luật ngoài cửa sổ | **TRƯỢT** (tập không rò) | bản nguyên văn z +4,9…+8,2 nhưng **rò**; tập không rò MN +1,41 · MT +1,91 · MB −0,47 | chờ owner (bộ lọc dựng sau khi thấy số) |
| FU-338 | M4 nhóm DO_TIEN | **TRƯỢT** (tập không rò) | nguyên văn z +2,95; không rò z +0,96 (ngang luật giả) | chờ owner |
| FU-183 | lớp V10640 MN | ĐẠT theo mã / TRƯỢT theo chữ sổ | 01–31/08 chênh vs phiếu **+14,7M**, lãi tuyệt đối −24,5M; **từ 15/09: 1 cứu · 3 phá** | chờ owner chọn cách đọc |
| FU-285 | đóng băng vs học lại ML | KHÔNG_ĐO_ĐƯỢC | không có bộ chấm; 3 mốc 07/09·07/10·07/11 trôi qua; thư mục đóng băng thiếu lstm/meta | `BLOCKED_NO_SCORER` |

## Nhóm lane đo · đo tiến · thử nghiệm (14)

| mã | việc | phán quyết | con số chính | đề xuất nhãn |
|---|---|---|---|---|
| FU-252 | lane Nghiệm Thu đủ 3 miền | ĐẠT | 15/09–24/11 **213/213** ô đúng hạn; chuỗi đủ dài nhất **103 ngày** | `CLOSED_PASS` |
| FU-264 | ghép /nghiem-thu × official | **TRƯỢT** | 768 lượt/đài; NT 19,01% vs official 18,10%, z 0,99; McNemar p 0,49 | `CLOSED_FAIL` (tín hiệu hậu kiểm MT/MB ngược chiều — cấm dùng) |
| FU-358 | /nghiem-thu mức 20pp | KHÔNG_ĐO_ĐƯỢC | thiết kế bất khả (cửa sổ trước đóng băng); phép thay McNemar p 0,40 | `CLOSED` → câu hỏi sang FU-264 |
| FU-367 | lane G2-MB 60 ngày | **TRƯỢT** | 108 ngày, M1–M6 đều `KHONG_CO`, z cao nhất −0,52 | `CLOSED_FAIL` |
| FU-400 | trọng số vs luật thô | **TRƯỢT** | n=749 miền-ngày, **−2,80pp**, CI95 [−5,85; +0,24], z −1,72 | `CLOSED_FAIL` (nghiêng về luật thô) — chờ owner vì chạm đường chọn số |
| FU-398 | prompt 3 tầng T-B vs official | **TRƯỢT** | 331 cặp bất đồng, 34 ngày, z −0,76; lane tắt 13/09 | `CLOSED_FAIL` |
| FU-397 | anti-trap đo tiến | **TRƯỢT** | n=117, z_MH −0,56; **phần đo tiến +2,9pp đổi dấu so với hồi tố −12,8pp** | `CLOSED_FAIL` — chờ owner về câu dạy anti-trap trong prompt |
| FU-317 | M-A ML × luật × bộ lọc | **TRƯỢT** | 28.735 dòng; 3 nguồn vs 1 nguồn z −0,11 (còn rò cửa sổ chọn, nghiêng có lợi mà vẫn không thấy) | `CLOSED_FAIL` |
| FU-318 | M-C canh trôi PSI | KHÔNG_ĐO_ĐƯỢC | **công cụ chưa từng lên VPS** — nhãn «đã deploy» là sai | `READY_NOT_DEPLOYED` |
| FU-276 | cổng bằng chứng V10991 | ĐẠT (tái dựng) | lối cũ không trúng cao hơn: z +0,44, p 0,66 | `CLOSED_PASS` (tái dựng) |
| FU-325 | lượt đo bầy đàn sạch | ĐẠT | 9 lượt TB 0,552; mở rộng 111 lượt 0,583, z ≈ +7,5 (đo **độ phân tán**, không đo trúng) | `CLOSED_PASS` |
| FU-427 | bộ chấm T-B in đủ 3 điều kiện | ĐẠT | log 24/11: 331 [≥96] ✓ · 34 [≥14] ✓ · z 0,76 [≥1,96] ✗ | `CLOSED_PASS` |
| FU-360 | chặn ghi đè chéo lane | HẾT_TIỀN_ĐỀ | từ 13/09 không còn lane TEST ghi vào `predictions` | `CLOSED` (giữ mã chặn) |
| FU-287 | phép đo cơ chế bầy đàn | ĐẠT | cron sống (24/11 19:05); 328 lượt TB 0,609; ⚠ từ 14/09 n_model 10–12 nên tỉ lệ tự cao (RM-21) | `CLOSED_PASS` |

## Nhóm cổng · hook · giờ chốt · giao diện (27)

| mã | việc | phán quyết | con số chính | đề xuất nhãn |
|---|---|---|---|---|
| FU-268 | /du-doan-test sửa 4 nhãn | ĐẠT (mã + DB) | 0 chuỗi sai; `lane_health` ra STOPPED; URL cam kết là 404 (route thật `/{region}`) | `CLOSED_PASS` |
| FU-256 | biên giờ chốt MT/MB | ĐẠT | C19/C20 có mặt 113/113 ngày; từ 16/09 MT biên thấp nhất 6,7′, MB 11,2′ | `CLOSED_PASS` |
| FU-258 | cổng mồ côi | ĐẠT | K8 0/2; thử chặn đạt | `CLOSED_PASS` (chưa nối hook/cron) |
| FU-245 | hook đầu phiên im | ĐẠT (phạm vi Cursor) | 18 dòng `VAO_HOOK`; Claude Code không có hook đầu phiên → FU-349 / FU-457 | `CLOSED_PASS` |
| FU-330 | thôi xoá bộ đếm đo tiến | ĐẠT | `DO_TIEN` tăng 45 → 2.025 qua 16 lượt (⚠ nhãn này rò — FU-456) | `CLOSED_PASS` |
| FU-331 | lần đào không xoá bằng chứng | ĐẠT | MRE 3.662 → 9.336, không giảm | `CLOSED_PASS` |
| FU-321 | số thành lời kể | HẾT_TIỀN_ĐỀ | FU-284 đóng không kết luận | `CLOSED_REPORT` |
| FU-291 | prompt thôi ép chọn | HẾT_TIỀN_ĐỀ | như trên | `CLOSED_REPORT` |
| FU-345 | chuỗi lỗi bơm vào prompt | **TRƯỢT theo chữ** | 0 lượt = 64 ký tự từ 08/08 (lỗi gốc không tái phát); nhưng **177 lượt < 10.000** (MT p10 9.851 — ngưỡng không hợp MT) | chờ owner rút ngưỡng MT |
| FU-328 | cổng model ra thiếu số | **TRƯỢT** | cổng chưa nối cron/panel; từ 15/09 **11 ngày** có model trả rỗng không ai được báo | `MEASURED_BUT_NOT_FIXED` |
| FU-370 | hạn biến mất im lặng | ĐẠT | 4/4; cổng chỉ chạy tay | `CLOSED_PASS` |
| FU-292 | canh tên đài lạ | **TRƯỢT** | chưa nối cron; **cổng không thể nổ** (cửa sổ 400 ngày chứa 30 ngày ⇒ `TEN_LA` luôn 0) | `MEASURED_BUT_NOT_FIXED` |
| FU-373 | C23/C24 trong cron | ĐẠT | có mặt 108/108 ngày | `CLOSED_PASS` |
| FU-357 | `decide()` nói dối | ĐẠT | 7/7; dữ liệu thật p 0,567 ⇒ đúng «chưa được phép kết luận» | `CLOSED_PASS` |
| FU-237 | giờ cấm deploy | KHÔNG_ĐO_ĐƯỢC | journal chỉ còn từ 19/11; **hook giờ cấm chỉ có ở Cursor** | `CLOSED_REPORT` + FU-457 |
| FU-355 | lượt rỗng chấm LOSE | ĐẠT | 60 dòng `NO_ANSWER`, 0 dòng `LOSE` | `CLOSED_PASS` |
| FU-341 | context pack shadow vỡ | ĐẠT | 0 lượt = 64 ký tự (343 lượt shadow tới 13/09) | `CLOSED_PASS` |
| FU-336 | cửa sổ đóng băng không bị phá | ĐẠT (thực chất) | 0 commit 08/08 14:25 → 21/08 09:42; lệnh cam kết dùng ngày trần + `--until` lệch 1 ngày | `CLOSED_PASS` |
| FU-392 | biên `anchor_date` | CẦN_OWNER_NHÌN | 2 chỗ đã vá; `_v104_shadow_prompt_injection.py:297` còn `<= ?`; dữ liệu chết | giữ — hỏi owner chỗ còn lại |
| FU-156 · 155 · 154 · 153 | tab V87–V90 /monitoring | CẦN_OWNER_NHÌN | 29 tab có mặt; API 401 khi chưa đăng nhập | owner nhìn một lần |
| FU-152 | section V82 | CẦN_OWNER_NHÌN | section có; route 401 | owner nhìn |
| FU-149 | trang /v82-monitor | CẦN_OWNER_NHÌN | 8/9 bảng nguồn sống | owner nhìn (FU-224 còn treo) |
| FU-131 | khối «Trải nghiệm hôm nay» | CẦN_OWNER_NHÌN | khối + hàm có; nguồn sống | owner nhìn |
| FU-118 | `source_proof` /du-doan-test | CẦN_OWNER_NHÌN | các trường có trong `main.py` | owner nhìn |

## Phát hiện mới ngoài 57 mục (agent kiểm toán nêu, đã xếp mục)

| phát hiện | xác minh | mục |
|---|---|---|
| Bộ chấm lane test `du_doan_test_results` **toàn `PENDING` từ 03/08** (3.835 dòng) — trang lane test dán nhãn bằng thống kê cũ ~4 tháng | ✅ agent điều phối tự đếm theo tháng | `FU-270` (cập nhật) |
| Nhãn `DO_TIEN` của luật **rò**: bù 112 ngày mỗi tuần + nhãn theo ngày luật xuất hiện lần đầu | ✅ đọc mã | `FU-456` |
| Cổng commit của **Claude Code** thiếu 4 cổng so với Cursor (`_v11044` · `_v11048` · `_v11050` · `_v11189`); cổng giờ deploy và hook đầu phiên chỉ có ở Cursor | ✅ đọc hook; `_v11189` đã nối trong V11190 | `FU-457` |
| `/choi` ghi cứng mốc final MT/MB 16:53/17:53 (thật 16:58/17:58) | ✅ | **đã sửa V11190** |
| Bảng phán quyết V11033b (`FOLLOW_UP_TRACKER.md:5476-5487`) đã đóng FU-268/245 nhưng bộ đọc không thấy | ✅ (bộ đọc chỉ đọc khối `### FU-`) | `FU-459` |
| `/monitoring:7402` câu «nhịp hệ thống» còn giờ cũ V10798 | ✅ | `FU-458` |
