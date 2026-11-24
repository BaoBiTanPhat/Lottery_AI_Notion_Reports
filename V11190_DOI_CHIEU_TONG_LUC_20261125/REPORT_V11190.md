# V11190 — Đối chiếu tổng lực: 57 phép đo treo đã chấm; Bảng chơi chưa vượt may rủi; khuyến nghị /choi ghi sau giờ xổ; mốc final /choi đã sửa

**Ngày:** 25/11/2026 · **Commit riêng:** `ff92c3e` (`Lottery_AI_Test`, nhánh `fu438/admin-only-p0a` = `master`) ·
**Trạng thái:** `choi.html` `DEPLOYED` (tệp tĩnh, không restart) · 10 việc **CHỜ OWNER** · nối tiếp `V11189`

---

## 1. Tóm tắt

Owner hỏi bốn việc sau báo cáo V11189. Trả lời ngắn:

1. **Đã đối chiếu hết báo cáo cũ chưa?** — V11189 **chưa**. V11190 kiểm kê đủ (thư mục gốc, Cursor, GitHub) và cho
   3 agent CHỈ ĐỌC chấm **57 phép đo đang treo** theo đúng ngưỡng đã đăng ký, đo trên DB VPS: **ĐẠT 19 · TRƯỢT 12 ·
   HẾT_TIỀN_ĐỀ 11 · CHƯA_ĐỦ_MẪU 2 · KHÔNG_ĐO_ĐƯỢC 4 · CẦN_OWNER_NHÌN 9**.
2. **Bảng chơi / Dự đoán các ngày trước?** — cùng thước tiền của `/choi`, 142 ngày: **Bảng chơi đánh đủ +5,9M** ·
   **Dự đoán lô 2 số −90,4M** · **bạch thủ −64,8M**; **không cách nào vượt may rủi có ý nghĩa** (|z| < 1). Đang chơi
   ở `/choi` theo tài liệu; «Ví P&L» không có lượt chơi thật nào sau 20/05. 🔴 Khuyến nghị CHƠI/NGHỈ lưu trong lịch
   sử bị ghi **sau giờ xổ** ⇒ không dùng được để đánh giá.
3. **Thiếu model nào, gọi qua đâu?** — Claude (Anthropic) · GPT (OpenAI) · DeepSeek gọi **thẳng API hãng**, cả ba hết
   tiền; `glm-5.1`, `gpt-oss-120b` gọi qua **OpenRouter còn 6,29 USD** (~1,5–4 tháng).
4. **Việc 2, 3 là gì?** — giải thích lại bằng lời thường ở §3.4.

Đã sửa: mốc final `/choi` MT/MB **16:53/17:53 → 16:58/17:58** (deploy) · cổng stdout V11189 nay chạy cả khi commit
từ Claude Code (trước chỉ chạy ở Cursor) · `NEXT_ACTION.md` công khai thôi báo «0 mục quá hạn» khi có 165.
Hai bản rút lại: `RL-048` (pool 7 → 9), `RL-049` (FU-284 MT đọc sớm).

## 2. Owner yêu cầu gì (nguyên văn) — §62 lớp `OWNER_SAID`

Mục **OWNER YÊU CẦU** đủ của phiên (`PRJ-INTERACTION-LEDGER-001`):

| giờ (ICT) | `OWNER_SAID` — nguyên văn | loại |
|---|---|---|
| 24/11 ~22:50 | *"rất lâu rồi chưa kiểm tra hệ vận hành , hiện anh để khá lâu rồi em tiến hành đo kiểm tổng lực dùm anh , phát hiện gì , xử lý ra sao em?"* (→ V11189) | YÊU_CẦU |
| 24/11 ~23:44 | *"trước đó nhiều đo lương , báo cáo  có trong root, trong thư mục tạm của cursor và cả github report em đã xem hết chưa kiểm tra so sánh đối chiếu tổng lực toàn diện chưa? - theo hình menu bảng chơi nay ổn nhỉ, các ngày trước thì sao , còn menu " dự đoán thì sao? chúng ta đang chơi ở menu nào em? các việc cần anh chưa rõ, 1/ em xác dịnh dang thiếu model nào API hãng hay dùng qua openrouter, 2 , 3 thực sự chưa hiểu đang nói gì ngắn gọn quá"* — kèm 2 ảnh chụp `/choi` và `/du-doan` (MT) | HỎI + YÊU_CẦU |

Ghi vào `docs/SO_TUONG_TAC_OWNER.md` trong cùng phiên. Không có xác nhận/bác bỏ nào khác của owner.

## 3. Đào bới / phát hiện — liệt kê ĐỦ, kể cả phép đo ra kết quả âm

### 3.1 Kiểm kê nơi chứa báo cáo

| nơi | nội dung | mới tới |
|---|---|---|
| `reports/` (gốc) | 61 báo cáo đối soát | 11/04 |
| `~/.cursor/plans` | 20 kế hoạch | trước 01/08 |
| `~/.cursor/projects/…/agent-transcripts` | 223 phiên agent Cursor | **05/08** |
| `~/.cursor/projects/…/canvases` | bảng trực quan P&L / official vs lane | 28/07 (261 tệp «tháng 11» là `node_modules`) |
| `Temp/cursor-agent-logs-Admin` | 4 log hôm nay 22:42–22:56 | chỉ là IDE mở kho — **không ghi/commit/SSH** |
| GitHub `Lottery_AI_Notion_Reports` | 467 thư mục | V11189 |
| `docs/FOLLOW_UP_TRACKER.md` | 202 mục treo · **58 chờ dữ liệu sống** | — |

`NEXT_ACTION.md` công khai in **«0 mục quá hạn»** trong khi có **165** — cửa sổ −14 ngày (`QD-066`) giấu nợ cũ.

### 3.2 Đối chiếu 57 phép đo treo (chi tiết: `evidence/DOI_CHIEU_58_MUC_V11190.md`)

| nhóm | ĐẠT | TRƯỢT | HẾT_TIỀN_ĐỀ | CHƯA_ĐỦ | KHÔNG_ĐO | CẦN_OWNER |
|---|---|---|---|---|---|---|
| model · combo · chọn model (16) | 2 | 3 | 8 | 2 | 1 | — |
| lane đo · đo tiến (14) | 5 | 6 | 1 | — | 2 | — |
| cổng · hook · giờ · giao diện (27) | 12 | 3 | 2 | — | 1 | 9 |

**Những phép đo «có lợi thế không» đã đủ mẫu đều KHÔNG vượt ngưỡng:**
- trọng số vs luật thô `FU-400`: n=749, −2,80pp, z −1,72;
- anti-trap `FU-397`: n=117, z_MH −0,56; **phần đo tiến +2,9pp đổi dấu so với hồi tố −12,8pp**;
- ghép Nghiệm Thu × official `FU-264`: z 0,99;
- lane G2-MB `FU-367`: 108 ngày, cả 6 mức `KHONG_CO`;
- prompt 3 tầng `FU-398`: 331 cặp bất đồng, z −0,76;
- M-A ML × luật `FU-317`: z −0,11;
- PHẦN 4 / M4 của luật `FU-340/338`: bản nguyên văn z +2,9…+8,2 nhưng **rò**; trên tập không rò MN +1,41 · MT +1,91 · MB −0,47.

**Phát hiện mới, đã tự kiểm lại trước khi dùng:**
- **Bộ chấm lane test đứng từ 03/08** — `du_doan_test_results` WIN/LOSE cuối cùng 03/08; sau đó `PENDING`: 08 1.163 ·
  09 979 · 10 995 · 11 698 dòng ⇒ nhãn trên `/du-doan-test` dựa trên số đóng băng ~4 tháng (`FU-270`).
- **Nhãn `DO_TIEN` của luật rò** — `weekly_rule_miner.py:202` bù 112 ngày mỗi tuần; `_v11025_khoa_luat_ben.py:241-242`
  gắn `DO_TIEN` theo ngày luật xuất hiện LẦN ĐẦU (`FU-456`).
- **Cổng Claude Code ≠ cổng Cursor** — nhật ký hook: commit V11189 lúc 23:53 chạy **9** cổng con (thiếu cổng stdout);
  sau sửa: **10/10**. Vẫn thiếu `_v11044`, `_v11048`, `_v11050`; cổng giờ deploy + hook đầu phiên chỉ ở Cursor (`FU-457`).
- `FU-318`: công cụ canh trôi PSI **chưa từng lên VPS**, sổ ghi «đã deploy».
- `FU-292`: cổng tên đài lạ **không thể nổ** (cửa sổ 400 ngày chứa 30 ngày).
- `FU-328`: cổng model ra thiếu số chưa nối — từ 15/09 có 11 ngày model trả rỗng không ai được báo.

### 3.3 Bảng chơi vs Dự đoán — cùng thước tiền (`_v11190_so_bang_choi_du_doan.py`, chạy trên VPS)

Thước của chính `/choi` (`_v10759_money_board.py:17-18, 353-359`): 50 điểm/số/đài · MN/MT 18.000đ, MB 27.000đ ·
trả 98.000đ/nháy. Nền ngẫu nhiên và phương sai tính **đúng từng ngày** từ phân bố đuôi thật (RM-18).

| gộp 3 miền | 71 ngày đứng (15/09→24/11) | 142 ngày (06/07→24/11) | z (142 ngày) |
|---|---|---|---|
| Bảng chơi — đánh đủ mọi ngày | +24,6M | **+5,9M** (nền −23,6M) | +0,39 |
| Dự đoán — lô 2 số | +47,9M | **−90,4M** (nền −36,1M) | −0,59 |
| Dự đoán — bạch thủ | +14,2M | **−64,8M** (nền −18,1M) | −0,71 |

| tháng | Bảng chơi đánh đủ | Dự đoán lô 2 | Dự đoán bạch thủ |
|---|---|---|---|
| 07 (từ 06/07) | +11,5 | −72,8 | −36,4 |
| 08 | −61,5 | −93,1 | −31,9 |
| 09 | +21,0 | +26,9 | −18,4 |
| 10 | +68,8 | +63,7 | +36,8 |
| 11 (đến 24/11) | −33,8 | −15,1 | −14,9 |

Theo miền (142 ngày): MT Bảng chơi **+47,3M** (z +1,17) trong khi MT Dự đoán lô 2 **−66,9M** · bạch thủ **−65,3M**;
MB Dự đoán bạch thủ **+21,4M** (z +0,85) trong khi MB Bảng chơi **−35,4M**. MN Bảng chơi = bạch thủ official (khớp
từng ngày, kiểm chéo). **Chưa được phép kết luận** miền nào có lợi thế (RM-04).

🔴 **Khuyến nghị CHƠI/NGHỈ ghi SAU giờ xổ.** `money_board_log` ghi 18:30–18:34 (100% dòng từ 28/06; có dòng 22:27);
`snapshot()` ghi đè `verdict` (`_v10759_money_board.py:820-824`) và «form 7 lần gần» (`:133-134`) khi đó đã gồm kết
quả hôm nay. 71 ngày qua **23/23** ngày ghi NGHỈ (trừ T7) đều trượt. Con số tính theo khuyến nghị (MN +31,4M · cả ba
+79,4M, z +2,18) là **ẢO — không công bố làm thành tích**. Cặp số SẠCH: khoá 15:43/16:56/17:56, khớp 200/200 dòng.
«Ví P&L» (`pnl_daily_bets`) chỉ có lượt chơi thật **07/05→20/05**.

### 3.4 Việc 2 và 3 — nói lại bằng lời thường

**Việc 2 (`FU-453`) — sổ điểm riêng của combo-super đứng từ 11/09.** Mỗi tối bước `daily_evaluation` chấm combo-super
trúng/trật vào sổ `daily_eval_log`. Luật an toàn cũ: *ngày có ít hơn 15 model thì coi là «thiếu» và không chấm*. Từ
13/09 roster còn 4 AI/miền (owner duyệt) ⇒ không ngày nào đủ 15 ⇒ ngày nào cũng «thiếu» ⇒ sổ điểm combo-super đứng.
Ngay trên ảnh owner chụp: `/du-doan` MT ghi **«✅ Đủ 10/15 model chạy»** (dấu ✅ chỉ xét có model bị lọc chất lượng —
`du-doan.html:1355`) trong khi `day_governance` cùng ngày ghi **INCOMPLETE**. **Không bị ảnh hưởng:** ra số, và xếp
hạng/chọn model (dùng `model_daily_eval`, chạy đủ). *Đính chính phạm vi V11189:* «216 miền-ngày bị loại khỏi đánh
giá» chỉ đúng với sổ điểm combo-super. Số 15 bị khoá trong `QD-074/075` ⇒ owner chọn: **(A)** «đủ» theo roster thật
từng ngày + chấm bù từ 12/09 (khuyến nghị) · **(B)** giữ 15 nhưng ngày thiếu vẫn chấm · **(C)** giữ nguyên, ghi rõ.

**Việc 3 (`FU-451` phần b) — 72 ngày bảng thăng hạng model trống.** `shadow_model_promotion_scorecard_daily` ghi mỗi
ngày từng model đoán trúng/trật, có lật được kết quả official không, chạy nhanh/chậm — căn cứ để quyết **model nào
đáng vào roster, model nào nên cắt**. Lỗi stdout (V11189) làm bảng trống 14/09→24/11. Dữ liệu gốc còn đủ trong DB ⇒
owner chọn: **tính bù** (chỉ ghi bảng đo, không đụng official — khuyến nghị) hay **để trống** kèm ghi chú.

### 3.5 Model thiếu — đường gọi và số dư (`_v11190_so_du_api.py`, chạy trên VPS, không in khoá)

| model | gọi qua | vai trò | trạng thái |
|---|---|---|---|
| `claude-opus-4-6` | **Anthropic trực tiếp** | core cả 3 miền | ❌ hết tiền từ 11/11 |
| `claude-sonnet-4-6` | **Anthropic trực tiếp** | challenger MN | ❌ hết tiền từ 12/11 |
| `deepseek-reasoner` | **DeepSeek trực tiếp** | pool combo | ❌ số dư **−0,05 USD** |
| `gpt-5.4`, `gpt-5-mini` | **OpenAI trực tiếp** | (rời pool 01/08) | ❌ hết tiền từ 13/09 |
| `gemini-2.5-flash` | Google trực tiếp | core cả 3 miền | ✅ |
| `gpt-oss-120b`, `glm-5.1` | **OpenRouter** | core/challenger | ✅ — **còn 6,29 USD** / nạp 510; 0,05–0,14 USD/ngày |

Pool AI combo-super có **9** model (`combo_super.AI_MODELS`); còn sống MN 2 · MT/MB 3.

### 3.6 Phép đo ra kết quả ÂM / không có sự cố
- OpenRouter **chưa khẩn** — em suýt báo động trước khi đo tốc độ tiêu.
- Lượng gọi model sống 18–24/11: gemini 7/7/7 · gpt-oss 7/7/7 · glm-5.1 MT/MB 7/7 — không hụt ngày nào.
- Các trang/API đang sống (`_v10760`, `_v10763`) KHÔNG đọc cột khuyến nghị bị nhiễm.

## 4. Hướng xử lý và vì sao chọn

| việc | chọn | vì sao | loại bỏ |
|---|---|---|---|
| 57 mục treo | 3 agent CHỈ ĐỌC song song, chấm theo ngưỡng đăng ký; agent điều phối **tự kiểm lại** phát hiện nặng | đủ phạm vi trong một đêm; kết quả agent có thể sai mà tự tin | đọc tay 467 thư mục; tin agent không kiểm |
| áp nhãn 57 mục | **không tự áp** — trình owner (`FU-459`) | owner ký 09/08: *«CẤM đóng hàng loạt»* | đóng theo đề xuất agent |
| P&L | thước tiền của chính `/choi` + nền đúng từng ngày + z | so cùng thước, biết đâu là may rủi | so tỉ lệ trúng thô |
| khuyến nghị nhiễm | **không công bố** số theo khuyến nghị; ghi `FU-455` + thiết kế vá | lỗi nhìn trước; vá cần restart mô-đun service | vá vội trong đêm khi 3 agent đang chạy |
| mốc `/choi` | sửa 3 chỗ + deploy tệp tĩnh | thi hành V10931 owner đã duyệt 01/08; trang báo «đã final» sớm 2 phút | chờ owner duyệt lại |
| cổng Claude Code | nối cổng stdout vào hook Claude Code | chính V11189 tuyên bố sai «9 cổng» | nối cả `_v11050` (~97 s) — cần cân thời gian, để `FU-457` |
| số FU-204 «32,69%» | **chưa rút lại** | agent nói không tái lập được nhưng em chưa tự tái lập (RM-11) | rút lại theo lời agent |

## 5. Đã làm gì

| tệp | thay đổi |
|---|---|
| `web/frontend/choi.html:497-498, 788` | mốc final MT/MB `16:53/17:53` → `16:58/17:58` |
| `.claude/hooks/cong_git_commit.py` | thêm `_v11189_cong_stdout.py` vào `SOI` (9 → 10 cổng con) |
| `web/backend/_v11083_sinh_dieu_huong.py` | `NEXT_ACTION.md` bêu số quá hạn ngoài cửa sổ |
| **mới** `_v11190_so_bang_choi_du_doan.py` · `_v11190_so_du_api.py` · `_v11190_rut_lai.py` · `_v11190_deploy.py` · `_v11190_ghi_tai_lieu.py` | đo Bảng chơi/Dự đoán · tra số dư · rút lại · deploy · ghi tài liệu |
| `docs/DOI_CHIEU_58_MUC_V11190.md` | bảng đối chiếu 57 mục |
| `docs/SO_RUT_LAI.json` | `RL-048`, `RL-049` |
| `docs/FOLLOW_UP_TRACKER.md` | đính chính tại chỗ FU-284; FU-455…459 mới; cập nhật FU-270, FU-452, FU-453 |
| bốn mặt §63 + `CHANGELOG_GOVERNANCE_LEDGER` + `DECISION_LOG` + `SO_TUONG_TAC_OWNER` | `governance_seq` 504 → **505** |
| `Lottery_AI_Notion_Reports/V11189_*/REPORT_V11189.md` | rút lại tại chỗ: pool 7 → 9; đính chính «9 cổng» |

**Deploy 00:11 ICT 25/11** (`_v11190_deploy.py`, 8/8 bước): ngoài khung cấm · sao lưu từ xa `/root/backups/v11190_pre/`
· sha khớp local · trên VPS mốc mới 3 chỗ, mốc cũ 0 · **PID 1122833 không đổi** (không restart) · health 200 · `/choi`
401 khi chưa đăng nhập. Bằng chứng: `evidence/deploy_evidence.json`. Backup local: `backups/v11190_pre/`.

## 6. Cổng kiểm

| cổng | kết quả |
|---|---|
| hook commit Claude Code (`_HOOK_DIEM_DANH.log`) | **10/10 cổng con** (V11189 lúc 23:53: 9) |
| `governance_guard` (chạy tay trước deploy) | `allow` |
| `_v10920_decision_ledger` | **0 TRÔI**; 2 không kết luận được (`QD-056` DB local cũ; `QD-027` bảng ngày mới chưa có lúc 00:1x) |
| `_v11038_kiem_han_ke_thua` | `HAN_KE_THUA_V11038=DAT` |
| mồ côi sổ theo dõi | 0 |
| tái lập `FU-284` | MT +10,5 z +1,30 — khớp agent A ⇒ `RL-049` |
| kiểm chéo phát hiện agent | lane test `PENDING` từ 03/08 ✓ · rò `DO_TIEN` ✓ (mã) · `FU-318` không có trên VPS ✓ · hook 9 vs 10 cổng ✓ |
| `_v11083_sinh_dieu_huong.py --thu` | `DIEU_HUONG_KHOP_THU_MUC=DAT`; in «Ngoài cửa sổ còn 165 mục quá hạn» |

## 7. Vướng vấp

| vấp | do ai | hậu quả nếu bỏ qua |
|---|---|---|
| V11189 nối cổng stdout chỉ vào hook Cursor rồi viết «cổng commit 9 cổng» | **agent** | cổng không chạy khi commit từ Claude Code — đúng lỗi «cổng không ai gọi» |
| V11189 ghi pool AI «7 model» | **agent** (đọc nửa danh sách) | số sai lưu hành; đã rút lại `RL-048` |
| V11189 viết «216 miền-ngày bị loại khỏi đánh giá» không nói rõ phạm vi | **agent** | owner hiểu là chọn model bị ảnh hưởng; đã đính chính |
| suýt công bố «Bảng chơi theo khuyến nghị +79,4M (z +2,18)» | **agent** — bắt kịp bằng kiểm giờ ghi | công bố một «lợi thế» hoàn toàn do nhìn trước |
| suýt báo OpenRouter «khẩn» trước khi đo tốc độ tiêu | **agent** | báo động sai |
| script đo bỏ luôn ngày T7 MN của phần Dự đoán; `"null"` trong `songthu`; f-string vỡ do heredoc | **agent** | số MN lệch 10 ngày — đã sửa và chạy lại trước khi dùng |
| chạy `_v11033_verdict_fu284.py` từ `/tmp` ra toàn số 0 | **agent** | suýt kết luận «không có dữ liệu»; chạy lại đúng thư mục |
| ghi giờ «01:xx» trong khi thật là 00:1x | **agent** | mốc sai trong SSOT/RL-049 — đã sửa trước commit |

## 8. Gỡ về

```bash
ssh root@<VPS> 'cp -p /root/backups/v11190_pre/choi.html /root/Lottery_AI_Test/web/frontend/choi.html'   # tức thời, không restart
git revert ff92c3e
```
Gỡ `choi.html` về thì trang lại báo «đã final» lúc 16:53/17:53, sớm hơn T-chốt.

## 9. Theo dõi tiếp — liệt kê ĐỦ

| mã | việc | ngưỡng / điều kiện | ai chặn |
|---|---|---|---|
| `FU-451` (a) · hạn 25/11 | nghiệm thu vá stdout | scorecard 25/11 `inserted>0` cả 3 miền, 0 dòng `closed file` | agent |
| `FU-451` (b) | tính bù 72 ngày bảng thăng hạng | — | **owner** |
| `FU-452` | Claude: nạp Anthropic hay chuyển qua OpenRouter | sau khi có tiền: gọi thử 1 lượt/model ⇒ `giai_phong` ⇒ MN lại 12 dòng `auto_daily` | **owner** |
| `FU-453` | cách tính «đủ model» sổ điểm combo-super (A/B/C) | — | **owner** (`QD-074/075`) |
| `FU-455` · hạn 27/11 | lưu khuyến nghị lúc khoá, `snapshot()` thôi ghi đè; rà báo cáo cũ dùng P&L theo khuyến nghị | khuyến nghị lưu trước giờ xổ 3/3 miền, 7 ngày liền | agent (cần restart) |
| `FU-456` | rò nhãn `DO_TIEN` | owner chấp nhận tập không rò hay đòi nhật ký kích hoạt luật | **owner** |
| `FU-457` | đồng bộ cổng Claude Code ↔ Cursor | 1 danh sách cổng dùng chung; thử chặn từng cổng | agent |
| `FU-458` | câu «nhịp hệ thống» `/monitoring` còn giờ V10798 | dựng lại từ `MOC_FINAL_TOTAL_OUTPUT.md` | agent |
| `FU-459` | áp nhãn cho 57 mục | duyệt cả bảng / theo nhóm / từng mục | **owner** |
| `FU-270` | bộ chấm lane test đứng từ 03/08 | sửa closeout hay ghi rõ lane test không còn chấm | **owner** |
| `FU-195` · `FU-183` · `FU-397` · `FU-400` · `FU-340/338` · `FU-345` · `FU-392` · 9 mục giao diện | xem `evidence/DOI_CHIEU_58_MUC_V11190.md` | theo ngưỡng từng mục | **owner** |
| `FU-204` | «32,69%» không tái lập (theo agent) | agent điều phối tự tái lập rồi mới rút lại | agent |

## 10. Ba lớp nguồn (§62)

| lớp | nội dung | bằng chứng |
|---|---|---|
| `OWNER_SAID` | 24/11 ~23:44 — *"…em đã xem hết chưa kiểm tra so sánh đối chiếu tổng lực toàn diện chưa?…chúng ta đang chơi ở menu nào em?…1/ em xác dịnh dang thiếu model nào API hãng hay dùng qua openrouter, 2 , 3 thực sự chưa hiểu đang nói gì ngắn gọn quá"*; 31/07 + V10931 01/08 — mốc final MT/MB 16:58/17:58; 09/08 Q4c — *«CẤM đóng hàng loạt. Rà THEO NHÃN»* | `docs/SO_TUONG_TAC_OWNER.md` · `CHANGELOG.md` V10931 |
| `CODE_DID` | `/choi` hiển thị 16:53/17:53 tới 25/11 00:11; `money_board_log` ghi khuyến nghị 18:30+; lane test không chấm từ 03/08; hook Claude Code chạy 9 cổng trước V11190 | `choi.html:497-498,788` (trước sửa) · DB VPS · `_HOOK_DIEM_DANH.log` |
| `DOC_SAID` | SSOT V10776 *«/choi là bảng chơi duy nhất»*; V11189 CHANGELOG *«cổng git commit 8 → 9 cổng»*; sổ ghi `FU-318` «đã deploy» | `docs/CURRENT_TRUTH_SSOT.md` §V10776 · `CHANGELOG.md` §V11189 · `docs/FOLLOW_UP_TRACKER.md` FU-318 |

**Lệch giữa các lớp (finding bắt buộc):**
- `OWNER_SAID` ≠ `CODE_DID`: owner duyệt mốc 16:58/17:58 từ 01/08 — `/choi` vẫn hiện 16:53/17:53 ⇒ **đã sửa**.
- `DOC_SAID` ≠ `CODE_DID`: V11189 ghi «cổng commit 9 cổng» — Claude Code chạy bộ khác, thiếu cổng mới ⇒ **đã nối**.
- `DOC_SAID` ≠ `CODE_DID`: `FU-318` ghi «đã deploy» — tệp không có trên VPS ⇒ `FU-459`.
- `DOC_SAID` ≠ `CODE_DID`: `money_board_log` tự mô tả là «log khuyến nghị kiểm soát forward» — thật ra ghi sau giờ xổ ⇒ `FU-455`.

**TanPhatAI cần làm:** ghi nhận **code đi trước tài liệu ở hai chỗ** — (1) `choi.html` mốc final 16:58/17:58 deploy
00:11 ICT 25/11, (2) hook commit Claude Code thêm cổng stdout — trỏ `docs/SO_TUONG_TAC_OWNER.md` dòng 24/11 ~23:44.
Cập nhật: **bảng chơi là `/choi`**, chưa cách chơi nào vượt may rủi có ý nghĩa; lịch sử khuyến nghị CHƠI/NGHỈ **không
dùng được** (`FU-455`); OpenRouter còn 6,29 USD; lane test không được chấm từ 03/08. Nhắc owner 10 việc chờ trong
`docs/DECISION_LOG.md` mục 24/11 ~23:44 — đặc biệt `FU-452`, `FU-453`, `FU-451b`, `FU-459`.
