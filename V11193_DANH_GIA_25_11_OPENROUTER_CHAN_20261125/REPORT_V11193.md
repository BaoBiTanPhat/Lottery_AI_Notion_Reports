# V11193 — Đánh giá dự đoán 25/11; OpenRouter chặn gọi model từ VPS, `gpt-oss-120b` và `glm-5.1` rỗng cả ngày

> **Phiên bản:** V11193 · **Ngày:** 25/11/2026 21:35 → 22:0x ICT · **Repo riêng:** `Lottery_AI_Test` commit `ac30090`
> (nhánh `fu438/admin-only-p0a` + `master`) · **governance_seq:** 508 · **Tầng (RM-12):** `REPORT_PROVEN` (đo, chỉ
> đọc) · **Runtime đổi:** không.

## 1. Tóm tắt

- **25/11 là một ngày lời.** Tính theo thước tiền của `/choi`: `/du-doan` bạch thủ **+3,95tr**, lô 2 số **+3,00tr**.
  MN và MT trúng, MB trượt. Tuy vậy, 30 ngày gần nhất mọi cách chơi đều **trong vùng may rủi** (|z| < 1), và một ngày
  lời là **chưa được phép kết luận** (RM-04).
- **Phát hiện nặng: OpenRouter chặn gọi model từ VPS từ 05:15 sáng 25/11.**
  - `gpt-oss-120b` và `glm-5.1` rỗng ở **cả 5 lượt** trong ngày.
  - Mọi lệnh gọi model nhận HTTP 400 `Request path cannot be relayed`. Khoá vẫn hợp lệ: tra tài khoản trả 200.
  - Phản hồi có `cf-ray …-HKG`, tức chính OpenRouter trả về qua máy biên Hồng Kông. Lỗi không nằm ở mã hay proxy của
    mình.
  - Hậu quả: MT và MB còn **2 model AI sống** (Opus, Gemini), dưới sàn §59.
  - Không ai được báo.
- **Trình owner (`FU-460`):** thay tạm bằng `deepseek-reasoner` hay chờ OpenRouter tự thông.
  - 7 ứng viên đều không khác nền về chất lượng, nên chọn theo độ tin cậy và tính độc lập (QD-080 mục 9).
  - DeepSeek hợp nhất theo hai tiêu chí đó: gọi thẳng, hãng thứ ba, tiền đã nạp.
- **Đính chính** một con số agent nói sai trong phiên chat lúc 13:4x (mục 3.6).

## 2. Owner yêu cầu gì (nguyên văn) — §62 lớp `OWNER_SAID`

| giờ (ICT) | nguyên văn | loại |
|---|---|---|
| 25/11 ~21:35 | *"phần của anh nhiều vài rút gọn quá chỉ có khuyên của em ko chưa đủ em cần trình bày rõ hơn đi , kiểm tra đánh giá việc dự đoán hôm nay sao rồi em"* | YÊU_CẦU |

Hai yêu cầu:
1. Trình bày lại phần việc của owner cho rõ. Không chỉ ghi khuyến nghị, mà phải có bối cảnh, các lựa chọn, được/mất
   của từng lựa chọn.
2. Đánh giá dự đoán hôm nay.

Đã ghi vào `docs/SO_TUONG_TAC_OWNER.md` trước khi làm.

## 3. Đào bới / phát hiện — liệt kê ĐỦ

### 3.1 Kết quả 25/11 (`evidence/danh_gia_25.txt`, chạy trên VPS, `mode=ro`)

Thước tiền: 50 điểm/số/đài · giá 18k MN/MT, 27k MB · trả 98k/điểm. Nền ngẫu nhiên đúng ngày cho 1 số: MN 45% · MT 30% ·
MB 24%.

| miền | /du-doan bạch thủ | /du-doan lô 2 số | /choi (số · khuyến nghị) | model trúng BT / kỳ vọng ngẫu nhiên |
|---|---|---|---|---|
| MN | `12` trúng 1 nháy · **+2,20tr** | `12 85` trúng cả hai · **+4,40tr** | `12` · CÂN NHẮC · đánh đủ +2,20tr | 6/10 · 4,5 |
| MT | `27` trúng · **+3,10tr** | `27 93` trúng một · **+1,30tr** | `14 27` · CÂN NHẮC · đánh đủ +1,30tr | 7/12 (2 rỗng) · 3,6 |
| MB | `12` trượt · **−1,35tr** | `12 49` trượt cả hai · **−2,70tr** | `12` · CHƠI · −1,35tr | 4/12 (2 rỗng) · 2,9 |
| **cộng** | **+3,95tr** | **+3,00tr** | đánh đủ +2,15tr | |

- Bundle `/du-doan` chốt trước giờ xổ: MN 05:17 · MT 16:37 · MB 17:34.
- Khuyến nghị `/choi` ghi lúc **18:32**, sau giờ xổ cả ba miền (`FU-455`), nên không dùng để đánh giá khuyến nghị.
- Opus: MT `98` trúng bạch thủ · MB `49` trượt.

### 3.2 Bối cảnh 30 ngày (`evidence/boi_canh_30_ngay.txt`)

| cách chơi (27/10 → 25/11, gộp 3 miền) | lời/lỗ thật | kỳ vọng nếu chọn ngẫu nhiên | z |
|---|---|---|---|
| /du-doan bạch thủ | −23,3tr | −3,8tr | −0,65 |
| /du-doan lô 2 số | −27,0tr | −7,6tr | −0,46 |
| /choi đánh đủ mọi ngày | −37,4tr | −5,2tr | −0,92 |
| /choi theo khuyến nghị ⚠ ghi SAU giờ xổ | +1,2tr | −3,7tr | +0,18 |

- Ở MN, cả **10 ngày** `/choi` ghi «NGHỈ» thì số đều trượt. Ở 16 ngày CHƠI hoặc CÂN NHẮC, số trúng 10 ngày (62%,
  trong khi nền là 43%).
- Khuyến nghị lại được ghi sau giờ xổ, nên mẫu hình này khớp với giả thuyết **khuyến nghị đã thấy kết quả**.
- Con số +1,2tr của dòng «theo khuyến nghị» **không phải thành tích thật**.

### 3.3 Hai model OpenRouter rỗng (`evidence/q_model_rong.py`)

| ngày | `gpt-oss-120b` có số / dòng | `glm-5.1` có số / dòng |
|---|---|---|
| 27/10 → 24/11 | 3/3 mỗi ngày (17/11: 2/3) | 2/2 mỗi ngày (13/11, 23/11: 1/2) |
| **25/11** | **0/3** | **0/2** |

- Lý do ghi trong dòng: *«đang trong thời gian chờ … Tất cả 4 phương thức đều thất bại»*.
- Journal 05:15:04–05:15:05: cả 4 kiểu gọi nhận HTTP 400 `{"error":{"message":"Request path cannot be relayed","code":400}}`,
  rồi `CIRCUIT_OPEN`.
- MT lúc 16:35 cũng lỗi y như vậy.
- Lượt `200 OK` cuối cùng: 24/11 17:31:30.

### 3.4 Lỗi nằm ở phía nào (RM-13)

| phép kiểm | kết quả | nghĩa |
|---|---|---|
| mã `gpt_analyzer._call_openrouter` | `httpx.post` tới URL cố định; tệp không đổi từ 14/09 | không phải mã mới |
| tệp đổi lúc khởi động lại 24/11 23:17 | chỉ script chạy riêng của bản vá stdout V11189 | không nằm trên đường gọi |
| `GET /api/v1/key` (21:39) | **200** | khoá hợp lệ |
| `POST chat/completions` tối thiểu, 1 lượt | **400** sau 0,25 s, cùng thông điệp | không phụ thuộc prompt hay model |
| header phản hồi | `server: cloudflare` · `cf-ray a60169268f47b1bf-HKG` | OpenRouter trả, qua máy biên Hồng Kông |
| DNS `openrouter.ai` | IP Cloudflare `104.18.2.115`/`104.18.3.115` | không bị trỏ sai |
| biến proxy trong môi trường service · `/etc/hosts` | 0 · 0 | không có gì chặn giữa đường |

**Tài liệu ngoài** (đã đọc 4/5 trang; `linux.do` từ chối truy cập):
- Cùng ngày 25/11, nhiều nhóm báo đúng hiện tượng `/key` 200 nhưng gọi model 400:
  - một dự án ở Malaysia có người dùng Hồng Kông/Trung Quốc, *«Since 08:27 MYT»*;
  - một dự án Việt Nam;
  - hai dự án khác.
- **Chưa có xác nhận chính thức** của OpenRouter về nguyên nhân. Giả thuyết hạn chế theo vùng/IP là **suy đoán**.
- Nguồn:
  [money2time#797](https://github.com/NelsonGan/money2time/pull/797) ·
  [merly-hermes-sales#50](https://github.com/tinnguyenmgol/merly-hermes-sales/pull/50) ·
  [markus#484](https://github.com/markus-global/markus/pull/484) ·
  [ARTEX#528](https://github.com/BaaRai/ARTEX/issues/528).

### 3.5 Ứng viên thế chỗ (`evidence/ung_vien_the_cho.txt`)

Thước `TW-001`: bạch thủ của lượt thật, so với nền đúng từng miền-ngày (RM-18), đo **đủ bộ cửa sổ** 14/30/90/180 ngày
hoạt động gần nhất của từng model (`PRJ-SELECTION-WINDOW-001`). Đơn vị là điểm phần trăm hơn hoặc kém nền, kèm ±2σ.

| model | miền | 14 ngày | 30 ngày | 90 ngày | 180 ngày | gọi qua |
|---|---|---|---|---|---|---|
| claude-opus-4-6 | MN | +32,5 ±27,5 | +11,8 ±18,3 | +8,6 ±10,5 | chưa đủ ngày | Anthropic |
| claude-opus-4-6 | MT | −20,2 ±26,3 | −15,0 ±17,6 | −3,7 ±10,1 | chưa đủ ngày | Anthropic |
| claude-opus-4-6 | MB | −0,5 ±23,5 | +13,9 ±15,9 | **+11,1 ±9,0** | chưa đủ ngày | Anthropic |
| claude-sonnet-4-6 | MN | +5,9 ±26,5 | +16,7 ±18,0 | +5,8 ±10,4 | +0,3 ±7,7 | Anthropic |
| gemini-2.5-flash | MN | +14,0 ±26,4 | −0,1 ±18,1 | −6,5 ±10,4 | −5,3 ±7,4 | Google |
| gemini-2.5-flash | MT | +1,6 ±25,2 | −4,8 ±17,3 | +0,8 ±10,1 | +2,2 ±7,1 | Google |
| gemini-2.5-flash | MB | +4,9 ±22,7 | −0,3 ±15,5 | −1,5 ±9,0 | +1,6 ±6,4 | Google |
| gemini-2.5-pro | MT | +7,6 ±25,3 | +5,9 ±17,6 | +6,2 ±10,1 | +7,1 ±9,3 | Google |
| deepseek-reasoner | MN | +2,6 ±27,4 | −2,0 ±19,0 | −4,3 ±10,6 | −5,4 ±9,9 | DeepSeek (thẳng) |
| deepseek-reasoner | MT | +10,1 ±26,4 | +7,5 ±17,9 | +8,9 ±10,2 | +7,3 ±9,5 | DeepSeek (thẳng) |
| deepseek-reasoner | MB | +14,4 ±23,7 | +3,6 ±15,8 | +6,7 ±9,0 | +5,7 ±8,4 | DeepSeek (thẳng) |
| gpt-oss-120b | MN | −28,8 ±26,4 | −13,4 ±18,1 | −2,1 ±10,5 | chưa đủ ngày | OpenRouter — **đang chặn** |
| gpt-oss-120b | MT | +29,9 ±25,3 | +11,9 ±17,3 | +6,4 ±10,1 | chưa đủ ngày | OpenRouter — **đang chặn** |
| gpt-oss-120b | MB | −0,5 ±23,5 | −3,0 ±15,8 | +0,1 ±9,1 | chưa đủ ngày | OpenRouter — **đang chặn** |
| glm-5.1 | MT | −1,8 ±27,4 | +0,6 ±17,9 | +1,0 ±10,4 | chưa đủ ngày | OpenRouter — **đang chặn** |
| glm-5.1 | MB | −16,6 ±22,7 | −13,7 ±15,5 | −7,6 ±9,1 | chưa đủ ngày | OpenRouter — **đang chặn** |

Bảng đầy đủ, gồm cả Sonnet MT/MB, Gemini Pro MN/MB và glm MN, nằm ở `evidence/ung_vien_the_cho.txt`.

- **Không ứng viên nào khác nền một cách chắc chắn ở mọi cửa sổ.** Riêng Opus MB vượt ±2σ ở cửa sổ 90 ngày, nhưng ở
  cửa sổ 14 ngày lại âm, và trong khoảng 60 phép so thì vài phép vượt ngưỡng là chuyện có thể do ngẫu nhiên.
- Các cửa sổ ngắn **đổi dấu mạnh**, ví dụ `gpt-oss-120b` MN −28,8 nhưng MT +29,9 ở cửa sổ 14 ngày. Đúng lý do luật cấm
  trích một cửa sổ.
- DeepSeek **dương ở cả 4 cửa sổ** ở MT và MB, nhưng vẫn trong vùng nhiễu.
- Dữ liệu của DeepSeek thuộc giai đoạn **trước 13/09** (roster cũ, prompt cũ), không phải số đo của chế độ hiện tại
  (`QD-080` mục 9 «current-regime»). Vì vậy phải gọi thử bằng prompt thật trước khi bật.
- Vì chất lượng không tách được, xét theo `QD-080` mục 9 (độ tin cậy, tính độc lập):
  - DeepSeek là hãng thứ ba, khác Anthropic và Google.
  - Gọi thẳng, không qua OpenRouter.
  - Đã nạp 19,94 USD, gọi thử đạt lúc 13:17.

### 3.6 Đính chính lời agent trong phiên (`PRJ-RETRACTION-001`)

| phần | nội dung |
|---|---|
| chỗ gốc | trả lời owner trong IDE 25/11 ~13:4x, danh sách A, việc 6a |
| nguyên văn câu sai | *«GLM-5.1 (model chính MT): cổng tự động đòi gỡ vì độ phủ 89,7% < 90%»* |
| điều đúng + phép đo | ngưỡng `FU-195` là **tỉ lệ lỗi > 6% trong 14 ngày**; đo 11–24/11: **2/28 = 7,1%** (`docs/DOI_CHIEU_58_MUC_V11190.md:36`, chấm trên DB VPS ở V11190) |
| quyết định đã dựa trên số sai | không có — owner chưa chốt việc 6a |

> ⚠ **BỔ SUNG ĐÍNH CHÍNH — RL-050 (26/11/2026, V11195):** số 89,7% **có thật**, nhưng là **độ phủ Gate 1 của
> glm-5.1 ở MN** (`web/backend/_v11185_roster_goi_token.py:77` — lý do glm-5.1 không làm CORE MN), không phải cổng
> đòi gỡ glm-5.1 khỏi MT. Câu nói thêm trong IDE tối 25/11 «con số sai không nằm trong tài liệu nào» cũng sai. Owner
> chốt 6a ngày 26/11 dựa trên ngưỡng FU-195 đúng (bảng trên), không dựa trên số 89,7%.

## 4. Hướng xử lý và vì sao chọn

- **Không cách ly hai model OpenRouter**, dù `QD-080` mục 6 cho phép.
  - Dòng rỗng không vào điểm chọn combo-super (`combo_super.py:342-349`).
  - Bộ ngắt mạch tự mở lại sau 10 phút, nên OpenRouter thông là hai model tự chạy lại.
  - Cách ly tay thì phải nhả tay, lặp lại rủi ro «13 ngày không ai thấy» của vụ Claude.
- **Không tự đổi roster.** Thêm DeepSeek là chọn model cho hàng chính, mà `QD-080` đã cũ hơn 30 ngày (§56: xin xác nhận).
  Trình owner bằng `FU-460`, hạn 26/11, trước lượt MT 16:38.
- **Thước so ứng viên dùng «chênh so với nền đúng ngày».** Các model dừng ở những thời điểm khác nhau, nên so tỉ lệ thô
  giữa các cửa sổ khác nhau là sai (RM-18).

## 5. Đã làm gì

1. Ghi lời owner vào sổ tương tác.
2. Viết `_v11193_danh_gia_ngay.py`, chạy trên VPS cho ngày 25/11.
3. Chạy lại `_v11190_so_bang_choi_du_doan.py` cho 30 ngày.
4. Tra dòng rỗng và journal, tìm mã lỗi 400.
5. Kiểm tệp đổi lúc khởi động lại 24/11 23:17, cùng mã `_call_openrouter`.
6. Gọi thử OpenRouter: một lượt (`_v11193_thu_openrouter.py`) và một lượt kiểm header (`q_header_cfray.py`).
7. Đọc báo cáo công khai của người khác qua agent phụ, chỉ đọc.
8. Đọc `QD-080` và mã chấm điểm combo-super trước khi quyết không cách ly.
9. Đo ứng viên thế chỗ (`_v11193_ung_vien_the_cho.py`). Bản đầu chỉ một cửa sổ 60 ngày; cổng commit công khai
   chặn (`PRJ_WINDOW_NOT_SPLIT`) nên đo lại đủ 14/30/90/180 ngày.
10. Đọc lại nguyên văn sổ cho từng việc của owner, từ đó phát hiện chỗ sai ở 6a.
11. Ghi bốn mặt (seq 508) và mục `FU-460`. Commit `ac30090`, đẩy lên nhánh và `master`.

## 6. Cổng kiểm

| cổng | kết quả |
|---|---|
| `_v11062_nang_version.py --kiem` | `NANG_VERSION_V11062=ĐẠT` (seq 508) |
| `_v10920_decision_ledger.py` | 0 TRÔI · 1 «không kết luận được» do DB local cũ (RM-01) |
| `_v11027_so_muc_quan_tri.py` | không mục nào biến mất |
| `trang_thai_mo_coi()` | trống; FU-460 đọc ra `OWNER_DECISION_NEEDED` |
| `_v10921_report_gate.py` ① + ② `V11193` | xem `CONVERSATION_CONTEXT` §4 |

## 7. Vướng vấp

- **Hai model chết cả ngày mà không cảnh báo nào nổ.** Đây là cùng họ `FU-328` (cổng model rỗng chưa nối) và vụ Claude
  13 ngày. Agent chỉ phát hiện nhờ owner hỏi đánh giá ngày.
- **Bản đầu của mục 3.5 chỉ trích một cửa sổ 60 ngày.** Cổng `_v11088_cong_cua_so_chon.py` chặn commit; đã đo lại đủ
  bộ cửa sổ, kết luận không đổi. Không bỏ qua cổng.
- **Agent nói sai số ở việc 6a** trong chat lúc 13:4x, do viết theo trí nhớ thay vì đọc sổ (đã đính chính ở 3.6).

## 8. Gỡ về

Phiên không đổi runtime. Gỡ tài liệu: `git revert ac30090`. Bản sao trước khi ghi: `backups/*.pre_v11193`.

## 9. Theo dõi tiếp — liệt kê ĐỦ

| mã | việc | ai chặn | khi nào |
|---|---|---|---|
| `FU-460` | thay tạm DeepSeek (A) hay chờ OpenRouter (B); kiểm OpenRouter mỗi ngày bằng `_v11193_thu_openrouter.py` | owner | trước 26/11 16:38 |
| `FU-452` | MN có Opus + Sonnet ra số (máy tự kiểm 05:25) | lượt tự nhiên | 26/11 |
| `FU-455` | lưu khuyến nghị `/choi` trước giờ xổ; rà dòng «theo khuyến nghị» trong các báo cáo cũ | agent | trước 27/11 |
| `FU-328` + cảnh báo số dư | cổng model rỗng; báo khi model rơi hoặc tài khoản cạn — **nay gồm cả nhà cung cấp chặn** | agent | trước 27/11 |
| `FU-453` · `FU-451b` · `FU-459` · `FU-270` | các việc chờ owner chốt | owner | — |
| `FU-195` · `FU-400` · `FU-183` · `FU-397` · `FU-456` · `FU-340/338` · `FU-345` · `FU-392` | bảy việc chuyên môn chờ owner chốt | owner | — |
| 9 mục giao diện | owner xem `/monitoring`, `/v82-monitor`, `/du-doan-test` | owner | — |
| `FU-457` · `FU-292` · `FU-318` · `FU-458` · `FU-204` | việc agent tự làm | agent | trước 28/11 |

## 10. Ba lớp nguồn (§62)

| lớp | nội dung | bằng chứng |
|---|---|---|
| `OWNER_SAID` | 25/11 ~21:35, nguyên văn ở §2 | `docs/SO_TUONG_TAC_OWNER.md` |
| `CODE_DID` | OpenRouter 400 cho mọi lệnh gọi model; `gpt-oss-120b`/`glm-5.1` 0/5; bundle ra đủ 3 miền | `evidence/thu_openrouter.json`, `evidence/thu_openrouter_header.txt`, `evidence/danh_gia_25.txt` |
| `DOC_SAID` | roster `QD-080`: `gpt-oss-120b` hàng chính MN/MB, `glm-5.1` hàng chính MT | `docs/OWNER_DECISION_LEDGER.json` QD-080 |

**Lệch `DOC_SAID` ≠ `CODE_DID`:** roster ghi 4 model/miền, thực tế 25/11 chỉ 2 model (MT, MB) ra số. Nguyên nhân nằm
ngoài hệ (OpenRouter), đã trình owner ở `FU-460`.

**TanPhatAI cần làm:** cập nhật hiểu biết — từ 25/11 05:15 OpenRouter từ chối mọi lệnh gọi model từ VPS (400
`Request path cannot be relayed`), nên `gpt-oss-120b`/`glm-5.1` không ra số; MT/MB chạy 2 AI. Theo dõi `FU-460` (owner chọn
thay tạm DeepSeek hay chờ). Đừng đọc dòng `/choi` «theo khuyến nghị» làm thành tích (`FU-455`). Không có code đi trước tài
liệu trong phiên này.
