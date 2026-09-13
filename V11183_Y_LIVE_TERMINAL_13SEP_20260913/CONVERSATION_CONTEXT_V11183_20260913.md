# CONVERSATION CONTEXT — V11183 · phiên 13/09/2026

> Ghi **nguyên văn** lời Owner + Agent IDE đã làm gì + **vấp ở đâu**. Đây là tệp cho người đọc
> sau (đặc biệt TanPhatAI) để **không phải đoán** vì sao phiên này đi theo hướng đã đi.

---

## 1. Owner nói gì — nguyên văn

Phiên nhận **đúng một** prompt lớn lúc **13/09/2026 ~19:09 ICT**:

> **"PROMPT TỔNG LỰC LẦN 43 R1 · §Y — 13/09 SUNDAY LIVE TERMINAL · RETRAIN/OPTIMIZER LINEAGE ·
> OFFICIAL GENERATOR–RANKER–SELECTOR FORENSIC · REPAIR / QUARANTINE / RETIRE · NO MORE
> MEASUREMENT-ONLY LOOP"**

Các mệnh lệnh chi phối, nguyên văn:

- *"Không ngồi chờ: làm ngay toàn bộ preflight, runtime, DB, retrain, optimizer và forensic."*
- *"Không dừng ở đo: lỗi reliability rõ ⇒ sửa cùng phiên; checkpoint/weights xấu ⇒ gói
  quarantine/rollback đầy đủ; ranker miss có tính hệ thống ⇒ dựng đúng một ranker repair
  offline; generator miss ⇒ không phí thời gian sửa ranker; không có tín hiệu ⇒ retire nhánh
  trong cùng phiên."*
- *"Không hỏi Owner 'duyệt FU-430?'. Phải diễn giải vấn đề đầy đủ rồi mới xin duyệt."*
- *"Không kéo FU-430 sang checkpoint thứ tư. Ngày 13/09 là terminal đã đăng ký."*
- *"Khi daily evaluation đủ ba miền hoặc qua mốc backup 20:00 thì đóng terminal trong chính phiên."*
- *"Không sửa prediction ngày 13/09 sau khi biết kết quả. Không backfill output. Không dùng
  actual để tạo ranked list. Không ghi `output_counterfactual_rank`. Không chạy lại F1–F5.
  Không bật lại bốn cron challenger đã tắt. Không gọi thêm 19 LM/LLM."*
- *"Không mở Prompt 44. Không mở FU mới. Không mở Plan mới. Không trộn ERP. Không mở lại SC-12."*
- *"Không tô hồng. Không pass-washing. Không che blocker. Không ép số liệu khớp expectation."*
- *"Cấm tự ý thay đổi: official roster/model state; official weights; official prediction prompt;
  TOTAL; Combo; FINAL; selector/voting production; 3-càng; model checkpoint production; cutoff;
  production schedule; lịch đài; historical official rows."*

**Không có yêu cầu rời nào giữa phiên** — Owner không gửi thêm tin nhắn nào sau prompt lớn.

---

## 2. Agent IDE đã làm gì — theo thứ tự thật

1. Chạy `_v11183_pre_y_manifest.py` → `PRE_Y_MANIFEST_20260913.json`, sha `cbdf22ed4fb592d2…`
2. Phóng workflow 14 agent (8 chiều điều tra + phản biện đối kháng cho từng chiều),
   run `wf_7b6f05e7-f9b`, 0 lỗi, 1.58M token, 26 phút
3. Song song, tự đo trên DB VPS:
   - `cham1309.py` — chấm lại 13/09 từ `prizes_json` thô
   - `y9_cuaso.py` / `y9b.py` — cửa sổ 30/90/180 + cohort đầy đủ, Poisson-binomial chính xác
   - `y7b.py` — tách hai tầng generator/ranker, nền siêu bội từng ngày
   - `y5_lichsu.py` — lịch sử optimizer + diễn lại cổng
   - `y5_control.py` — đo `CONTROL` (bộ weights mặc định) — **phép so chưa từng được làm**
   - `y5_sua_nen.py` — tính lại lift với nền đúng
   - `y9_suclam.py` — sức mạnh phép đo + KTC cho delta
4. Dựng `_v11183_cong_optimizer.py`, tự kiểm **15/15**, diễn lại 6 lần chạy lịch sử
5. Chạy toàn bộ cổng thử: **177/177**
6. Chạy lại manifest → `POST_Y_MANIFEST`, so PRE/POST chứng minh không ghi

---

## 3. Vấp ở đâu — ghi đủ, không giấu

### 3.1 Vấp NẶNG NHẤT: diễn giải sai dấu của lift (→ RL-042)

Tôi đọc `weight_optimizer.py:441` thấy cổng `best_lift > -50`, thấy MN `-3.11` / MT `-6.03`, và
**báo ngay cho Owner** rằng *"hai trong ba miền có lift ÂM và vẫn ghi đè lên production"*, rồi
*"69/69 tổ hợp đều âm"*.

**Cái tố cáo tôi không phải cổng máy nào — mà là một con số bất hợp lý.** Khi đọc
`backtest_with_weights` để biết `lift` so với cái gì, tôi thấy `random_chance` của MN là
**94.91%**; suy ngược `1-(1-b)³ = 0.9491` cho b ≈ **0.63**, tức ~63 đuôi/ngày. Nhưng chính tôi
vừa đo được MN chỉ có **43.1** đuôi-2 **khác nhau** mỗi ngày. 63 vs 43 là chênh không giải thích
nổi ⇒ đào tiếp ⇒ tìm ra `get_actual_tails` trả list **có trùng** và còn cộng lặp
`tail_db`/`tail_g8`.

Với nền đúng, dấu đảo: MN **+10.07** · MT **+7.91** · MB **+17.92**.

**Đây là lần thứ ba trong bốn phiên gần đây một kết luận sai bị bắt bởi *con số quá bất hợp lý*
chứ không bởi cổng máy** — cùng họ với **RL-039** (43.1% vs nền 16.6%, hoá ra gộp 3 đài MN so
với nền một-đài) và **RL-041** (57/57 lo3 WIN false, hoá ra so `lo3` 3 chữ số với đuôi 2 chữ số).

### 3.2 Đọc không-bác-bỏ thành chứng minh H₀ (→ RL-043)

Sau bảng cohort 198 ngày tôi viết *"bạch thủ bundle bằng đúng nền ngẫu nhiên ở cả ba miền"*.
**Agent phản biện độc lập bắt** — đó là nâng "không bác bỏ được" thành "đã chứng minh", đúng lỗi
RM-04 cấm.

Phép đo này chạy trên **đủ bộ cửa sổ 14 ngày · 30 ngày · 90 ngày · 180 ngày** cộng cohort đầy đủ,
ba miền đo riêng — **12/12 ô không ô nào có ý nghĩa**, và dấu **đảo** giữa các cửa sổ ở cả MN
(14 ngày +7.1pp → 30 ngày −3.4pp → 180 ngày +1.4pp) và MB (14 ngày +5.0pp → 90 ngày −3.7pp).
Chính vì dấu đảo mà **cấm trích một cửa sổ** cho bất kỳ tuyên bố hiệu quả nào; bộ số đầy đủ ở
`REPORT_V11183.md` §7 và `evidence/y9b.py`.

Với n=198 phép đo chỉ loại trừ được lift **> +6.88 / +8.03 / +4.77pp**; cần
**846/800/655 ngày** mới bắt được +5pp.

**Ghi rõ để lần sau nhớ:** cái này tôi **không tự thấy**. Nếu không có tầng phản biện, câu sai đã
vào báo cáo.

### 3.3 Đếm thô hai lần (RM-09)

- **"74 tổ hợp trong lưới"** — tôi `grep` chuỗi `Lift: … | Cov` rồi đếm. Nhưng khối `TOP 5` cũng
  chứa đúng chuỗi đó, nên 69 tổ hợp lưới bị cộng thêm 5 dòng tóm tắt. Sửa: phân loại dòng lưới
  (`[i/n]`) khác dòng tóm tắt (`#k`).
- **"24 dòng lỗi journal"** — manifest đếm chuỗi `error|traceback|critical|exception`. Phân loại
  xong: **4 lớp, tất cả mức `WARNING`**, và chuỗi `error` khớp chỉ vì nó nằm **trong nội dung**
  `errors: {…}` của chính dòng WARNING đó. Số dòng mức **ERROR/CRITICAL thật = 0**, traceback = 0.

### 3.4 Đoán tên cột (RM-10)

Truy vấn đầu tiên dùng `lottery_results.results_json` — **không tồn tại**. Tên thật là
`prizes_json`. Sửa bằng `PRAGMA table_info` trước khi viết truy vấn tiếp.

### 3.5 Hai lỗi kỹ thuật trong script §Y7

Bản đầu dùng `Fraction` cho DP Poisson-binomial với ~6000 phép Bernoulli → **quá 500s phải huỷ**.
Và mô hình "mỗi đuôi trong pool là một Bernoulli độc lập" cũng **sai grain** (RM-18): các đuôi
trong pool là rút **không hoàn lại** từ cùng tập 100, nên phân phối đúng là **siêu bội** từng
ngày rồi tích chập qua các ngày. Viết lại bằng float DP + siêu bội.

### 3.6 Ranh giới tự dò sai

Tôi để script tự tìm "ranh giới hậu-thay-đổi" bằng `bundle_version`, nó chọn `bundle_version=3`
— chỉ có **2 bản ghi**. Đọc kỹ hơn: `v1` chạy 28/02→07/09 và `v2` chạy 30/03→13/09, **chồng nhau
cả kỳ** ⇒ `bundle_version` **không phải mốc thời gian**. Bỏ phép chia đó, thay bằng cohort đầy đủ
không cắt cửa sổ nào.

### 3.7 Bài thử cổng bị mù

Bản nháp đầu của `_v11183_cong_optimizer.tu_kiem` có bài *"chỉnh chọn THỰC SỰ đổi kết quả"* đặt
`thắng=36/60`, cho p thô ≈ **0.077** — vốn đã trượt ngưỡng 0.05. Nên bài thử **không phân biệt
được** "bị chặn vì thiếu chỉnh-chọn" với "bị chặn vì p thô lớn": nó FAIL, và nếu tôi sửa cổng
thay vì sửa bài thử thì đã hỏng cổng. Sửa thành `thắng=38/60` (p thô ≈0.026, **dưới** 0.05) →
15/15. **Đúng loại lỗi RM-15 cảnh báo: cổng qua thử mà bài thử không chứng minh gì.**

---

## 4. Điều Owner yêu cầu mà phiên CỐ Ý không làm

| yêu cầu | không làm vì |
|---|---|
| *"ranker miss có tính hệ thống ⇒ dựng đúng một ranker repair offline"* | §Y7 chứng minh căn nguyên là **generator miss**, không phải ranker miss. Chính prompt ghi *"generator miss ⇒ không phí thời gian sửa ranker"*. Nhánh `RANKER_V2_LINEAGE_DEDUP_CALIBRATED` **không mở** |
| *"lỗi reliability rõ ⇒ sửa cùng phiên"* với ba khuyết tật optimizer | Khuyết tật **đã chứng minh và đã dựng bản sửa tham chiếu**, nhưng nó đụng **weights official** — khoá cứng bắt *"phải dựng gói quyết định đầy đủ cho Owner, không tự ý triển khai"*. Nên trình `QD-079`, **không deploy** |

---

## 5. Code đi trước tài liệu — khai theo `PRJ-INTERACTION-LEDGER-001`

`web/backend/_v11183_cong_optimizer.py` đã có **trong repo và trên VPS** trước khi vào
`CHANGELOG.md` / `docs/CURRENT_TRUTH_SSOT.md`. Đây là **được phép** (Owner đã cho phép tường
minh để giữ mạch xử lý nhanh trong IDE), nhưng phải khai — và đây là chỗ khai.

Tệp đó **không được tệp nào import**, **không đổi hành vi runtime**, và **không ghi `app_settings`**.
Nó tồn tại để dựng gói quyết định, không để chạy trong production.

---

## 6. Điều quan trọng nhất cho người đọc sau

Nếu chỉ đọc một đoạn, đọc đoạn này:

**Căn nguyên là `GENERATOR_MISS`, không phải ranker miss.** Pool 13 đuôi/ngày do 19 model sinh ra
không phân biệt được với 13 đuôi bốc ngẫu nhiên (MN z=+0.32 · MT z=+1.16 · MB z=+0.14 trên 198
ngày, nền siêu bội đúng grain). Ranker không thêm gì **vì không có gì để xếp hạng**. Mọi nỗ lực
sửa ranker, sửa selector, hay đổi trọng số voting đều **không chạm tới vấn đề**.

Và **không được đọc ngược lại thành "đã chứng minh không có tín hiệu"** — với 198 ngày, phép đo
chỉ loại trừ được lift lớn hơn ~+5 đến +8 điểm. Một lift thật +3pp sẽ **vô hình** ở cỡ mẫu này.
`PREDICTIVE_LIFT = NOT_PROVEN` là đúng chữ; `PROVEN_ABSENT` là **sai chữ**.
