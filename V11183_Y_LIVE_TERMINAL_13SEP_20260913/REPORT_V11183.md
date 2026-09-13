# REPORT V11183 — §Y · ĐÓNG NGÀY DỰ ĐOÁN 13/09/2026 · DÒNG DÕI RETRAIN/OPTIMIZER · PHÁP Y GENERATOR–RANKER–SELECTOR

> **Phiên:** 13/09/2026, 19:09 → 20:0x ICT · **Mã đọc §58:** `BC1309` · **Prompt:** TỔNG LỰC LẦN 43 R1 §Y
> **Khoá còn hiệu lực:** `SC12=CLOSED · DO_NOT_REOPEN` · `MATERIALIZATION_OPTION=B` ·
> `OUTPUT_COUNTERFACTUAL_RANK_PRODUCTION_WRITE=FORBIDDEN` · `FINAL_BUNDLES_ZERO_WRITE` ·
> `PREDICTIVE_LIFT=NOT_PROVEN` · `POOL_VERDICT=HOLD` · Plan `PLAN-20260723-lottery-doc-restructure`

---

## 0. SÁU TERMINAL — đọc trước, phần còn lại là bằng chứng

| # | Terminal | Kết luận | Neo bằng chứng |
|---|---|---|---|
| **A** | Hôm nay — vận hành | **`OPERATIONAL_CLEAN_WITH_PROVIDER_BILLING_OUTAGE`** | 0 dòng mức ERROR/CRITICAL, 0 traceback toàn ngày · NRestarts=0 · 81/81 prediction trước cutoff · 3/3 bundle chốt đúng hạn · hỏng hóc duy nhất là **hết số dư nhà cung cấp** (DeepSeek 402 cả ngày, OpenAI 429 từ ~16:38–16:43) |
| **B** | Hôm nay — dự báo | **`NO_LIFT_DETECTED_UNDERPOWERED`** | Bạch thủ 198 ngày × 3 miền, nền đúng grain từng ngày: MN −0.09pp · MT +1.13pp · MB −1.52pp, mọi p ≥ 0.34. **Nhưng KTC 95% vẫn cho phép lift tới +6.88 / +8.03 / +4.77pp** — chưa đủ sức để nói "không có lift" |
| **C** | Căn nguyên chính | **`GENERATOR_MISS`** (không phải ranker miss) | Pool ứng viên 13.4 đuôi/ngày, phủ kín 99–100%, nhưng số đuôi trúng **trong** pool bằng đúng kỳ vọng siêu bội: MN z=+0.32 · MT z=+1.16 · MB z=+0.14. Ranker so với **bốc ngẫu nhiên từ chính pool** cũng không thêm gì (p ≥ 0.30) |
| **D** | Retrain (FU-430) | **`RETRAIN_ACTIVATED_METRIC_NOT_COMPARABLE`** | 12/12 dòng OK, 18 artifact ghi đè 02:00:33–02:02:54, mọi prediction chạy sau đó ⇒ **đã kích hoạt**. Nhưng delta AUC **không đọc được là tốt/xấu** vì holdout trượt 7 ngày giữa hai lần đo. **`backup_path` rỗng 12/12** và chỉ `meta_learner` có `.bak` (từ 03/07) ⇒ **không rollback được** |
| **E** | Optimizer | **`OPTIMIZER_OBJECTIVE_DEFECTIVE_AND_GATE_ABSENT`** | Ba khuyết tật đo được (D1/D2/D3, §5). Cổng ghi là `best_lift > -50`, không control, không held-out, không kiểm ý nghĩa. Diễn lại: **6/6 lần chạy đều ghi; 0/6 qua được cổng đúng** |
| **F** | Hành động tiếp | **Gói quyết định `QD-079` (chưa triển khai)** + khai tử bộ thử V1.1 | §11 |

**Không terminal nào là `WAIT_DATA`.**

---

## 1. TÓM TẮT

Ngày 13/09/2026 (Chủ Nhật) đóng trọn: kết quả đủ 7/7 đài đúng lịch canonical, 3 bundle ACTIVE
chốt trước cutoff, `model_daily_eval` đủ ba miền lúc 18:45. Bạch thủ trúng **3/3 miền**
(MN 89 · MT 54 · MB 40) — chấm lại độc lập từ `prizes_json` thô khớp **9/9** nhãn production.

Nhưng 3/3 của một ngày **không phải bằng chứng**: nền đúng của ngày đó là 0.35 × 0.42 × 0.21 ⇒
P ≈ **3.1%**, n=1, và `day_governance` ghi cả ba miền **`EXCLUDE_PRIMARY`** nên ngày này vốn
không đủ tư cách primary.

Phiên này **không dừng ở đo**. Hai việc sửa/khai tử đã làm trong phiên, và một gói quyết định
đầy đủ đã dựng cho Owner:

1. **Tìm ra và chứng minh một lỗi nền thật trong `weight_optimizer.py`** khiến mọi con số lift
   của optimizer âm giả tạo 8.36–12.70 điểm (§5). Đối chứng đắt nhất: `stat_weight_optimizer.py`
   trong **cùng kho** làm đúng chỗ đó.
2. **Dựng cổng ghi weights `_v11183_cong_optimizer.py`**, tự kiểm **15/15**, có bài thử chứng
   minh cổng CHẶN được (RM-15) và chứng minh bước chỉnh-chọn thực sự đổi kết quả — **không
   triển khai**, vì đụng weights official.
3. **Khai tử `_v11178_thu.py`** (bộ thử V1.1) — đã bị `_v11178_thu_v12.py` thay thế và nay
   rc=1 do `dai_dich` đổi chữ ký từ §W2.

**Hai lần rút lại** trong chính phiên này — cả hai đều là câu của tôi, cả hai đều ở §2.

---

## 2. RÚT LẠI (`PRJ-RETRACTION-001`) — hai mục, đủ bốn phần mỗi mục

### RL-042 — "lift âm nghĩa là kém hơn ngẫu nhiên"

| phần | nội dung |
|---|---|
| **chỗ gốc** | Tin nhắn của Agent IDE gửi Owner trong phiên 13/09/2026, khoảng 19:2x ICT (trước khi đọc `backtester.get_actual_tails`) |
| **nguyên văn câu sai** | *"Hai trong ba miền có lift ÂM và vẫn ghi đè lên production"* và *"MN và MT: 69/69 tổ hợp trong lưới đều âm. Không tồn tại bộ weights nào hơn nền, và optimizer vẫn ghi 'cái ít tệ nhất' đè lên production."* |
| **điều đúng** | Các con số `−3.11` / `−6.03` / `69/69 âm` **đúng như mã tính ra**. Sai là ở **diễn giải**: chúng KHÔNG có nghĩa "kém hơn bốc ngẫu nhiên". Nền của mã bị thổi lên **+12.70pp (MN) · +12.46pp (MT) · +8.36pp (MB)** do `get_actual_tails` trả list có trùng và cộng lặp `tail_db`/`tail_g8`. Với nền đúng: MN **+10.07** · MT **+7.91** · MB **+17.92**. |
| **phép đo tái lập** | `evidence/y5_sua_nen.py` — giữ nguyên `win_rate` đo thật, chỉ thay nền bằng `1 − C(100−M,3)/C(100,3)` với M = số đuôi-2 **khác nhau** của chính ngày đó |
| **quyết định đã dựa trên số sai** | **Không có.** Con số chỉ tồn tại trong phiên, chưa vào báo cáo, chưa vào production, chưa sinh quyết định nào. |

> **Và con số mới cũng KHÔNG được đọc là thắng.** Bộ `ĐÃ_HỌC` được **chọn** từ 69 tổ hợp trên
> chính cửa sổ đó; p=0.003 của MB chưa chỉnh cho phép chọn, chỉnh Šidák cho 69 lần ⇒ ≈ **0.19**.
> `CONTROL` không qua chọn nên **+3.52 / +2.99 / −1.75** mới là ước lượng không thiên vị — cả ba
> đều không có ý nghĩa.

### RL-043 — "bằng đúng nền ngẫu nhiên"

| phần | nội dung |
|---|---|
| **chỗ gốc** | Tin nhắn của Agent IDE gửi Owner trong phiên 13/09/2026, ngay sau bảng cohort 198 ngày |
| **nguyên văn câu sai** | *"Bạch thủ bundle bằng đúng nền ngẫu nhiên ở cả ba miền."* |
| **điều đúng** | Đó là đọc *không bác bỏ được H₀* thành *đã chứng minh H₀* — đúng lỗi RM-04 cấm. Điều đúng: **không phát hiện lift**, và với n=198 phép đo **chỉ loại trừ được** lift lớn hơn **+6.88pp (MN) · +8.03pp (MT) · +4.77pp (MB)**. Để bắt +5pp với power 0.90 cần **846 / 800 / 655 ngày**. |
| **phép đo tái lập** | `evidence/y9_suclam.py` — khoảng Wilson 95% cho delta + n-cần |
| **quyết định đã dựa trên số sai** | **Không có.** `PREDICTIVE_LIFT=NOT_PROVEN` giữ nguyên và vẫn đúng; câu sai chỉ nâng nó thành "đã chứng minh vắng mặt", là nâng tầng không được phép (RM-12). |

---

## 3. OWNER YÊU CẦU GÌ (`PRJ-INTERACTION-LEDGER-001` · §62 lớp `OWNER_SAID`)

Phiên này Owner gửi **đúng một** prompt lớn (§Y), không có yêu cầu rời giữa phiên. Nguyên văn
các mệnh lệnh chi phối phiên, giờ nhận **13/09/2026 ~19:09 ICT**:

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
- *"Không tô hồng. Không pass-washing. Không che blocker. Không ép số liệu khớp expectation."*

**Điều Owner yêu cầu mà phiên này CỐ Ý không làm, kèm lý do:** *"generator miss ⇒ không phí thời
gian sửa ranker"* — §7 chứng minh căn nguyên là generator miss, nên **nhánh D
(`RANKER_V2_LINEAGE_DEDUP_CALIBRATED`) KHÔNG được mở**. Đây là thi hành đúng mệnh lệnh, không
phải bỏ sót.

---

## 4. ĐÀO BỚI / PHÁT HIỆN — liệt kê ĐỦ, kể cả phép đo ra kết quả âm

### 4.1 §Y1 — Kết quả và lịch đài

7/7 dòng `lottery_results`, tập đài khớp **đúng** `_v11180_lich_dai.cho_ngay("2026-09-13")`
(MN Kiên Giang/Tiền Giang/Đà Lạt · MT Khánh Hòa/Kon Tum/Thừa Thiên Huế · MB Thái Bình), 0 thiếu
0 thừa 0 trùng. `validate_prize_card` của production trả `valid=True` cho cả 7 đài (MN/MT 18/18
slot, MB 27/27). Cổng đối chiếu canonical × 180 ngày: **25/25 Chủ Nhật khớp cả ba miền**.

**Ba hạ cấp bắt buộc ghi** (từ phản biện độc lập):
- *"không có LATE_INGEST"* — **bỏ khỏi terminal**: chuỗi `LATE_INGEST` không tồn tại ở bất kỳ
  đâu trong kho (RM-10, kết luận theo tên đoán).
- *"không có rescrape/ghi đè"* → hạ thành ***"không có DẤU VẾT rescrape"***: `lottery_results`
  không có cột `updated_at`/`version` nên một lệnh UPDATE tại chỗ sẽ **vô hình**.
- Độ trễ ingest so với **giờ xổ thật**: **`INDETERMINATE`** — hệ thống không có bất kỳ nguồn nào
  ghi thời điểm quay số.

### 4.2 §Y2 — Ma trận official

Đúng **một** bundle ACTIVE mỗi miền (MN id=878 · MT id=880 · MB id=882). Bốn nguồn cutoff trong
mã **khớp tuyệt đối**: MN `15:45` · MT `16:58` · MB `17:58`. 0/27 prediction mỗi miền tạo sau
cutoff. 3-càng: cả ba `lo3` đúng 3 chữ số và **đều kết thúc bằng `bach_thu`** (prefix MN=1 ·
MT=8 · MB=2) — khớp phát hiện V11182.

**Một sửa quan trọng về phương pháp:** phép lọc cửa sổ chọn neo vào `bundle.created_at` là
**mốc chết** — cả ba bundle đều `bundle_version=2`, mà `ON CONFLICT` **không cập nhật**
`created_at`; nội dung thật được ghi lại lúc 15:40/16:55/17:55 bởi job `t10_chot`. Kết luận
"không rò" **vẫn đứng** nhưng vì lý do ngược: toàn bộ 27 dòng, kể cả 11 dòng shadow, đều có
**trước** lần ghi v2.

### 4.3 §Y3 — Ma trận model / provider / runtime

81/81 dòng `predictions` (27 model × 3 miền), **0 TIMEOUT · 0 late · 0 DB_WRITE_FAILURE**, 100%
trước cutoff. Toàn bộ hỏng hóc quy về **một lớp duy nhất — hết số dư nhà cung cấp** (9/81 dòng):
DeepSeek `402 Insufficient Balance` cả ngày ở cả ba miền; OpenAI `429 credit_balance_exhausted`
bắt đầu trong khoảng 16:38:56–16:43:21.

Payload rỗng 30 ngày: `deepseek-reasoner` **11.4%** (10/88) · `glm-5.1` 4.6% · `gpt-oss-120b`
3.4% · `gpt-5.4` 1.1%.

**Hai phát hiện phải báo kèm:**
- **Số nguồn công bố bị phóng đại ~27–33%.** Ba tổ hợp dẫn xuất (`smart-ensemble` = meta+lstm,
  `smart-ml` = xgboost+random-forest, `combo-super`) được đếm như nguồn độc lập. Ngày 13/09
  `combo-super` đóng góp **đúng bằng 0** thông tin mới ở cả ba miền. Số **họ nguồn độc lập** thật:
  **MN 11 · MT 9 · MB 10**, không phải 14/12/13.
- **Đo được, không phải INDETERMINATE:** cặp **cùng họ** nhà cung cấp đồng thuận **0.6147**
  (n=654) vs **khác họ** **0.5253** (n=4074), chênh **+8.94pp**, bootstrap theo cụm miền-ngày
  95%CI **[+5.44, +12.45]**, z=5.00, design effect **0.72 đo trên chính thước này** (RM-21 — không
  mượn VIF=2.92; nếu mượn thì z tụt 5.00→2.49).
- **Provider chết HOÀN TOÀN CÂM với journal**: 0/9 sự cố provider có một dòng journal nào.

### 4.4 §Y4 — Dòng dõi retrain (FU-430)

Job `auto_retrain` nổ đúng CN 02:00 VN qua **APScheduler trong tiến trình** (không phải cron —
cron chỉ có `retrain_guard` 06:30). 12/12 dòng `training_history` `status=OK`, `nguon` = 8 dòng
`_retrain_all` + 4 dòng `guard`. 18 artifact ghi đè **02:00:33–02:02:54**; prediction sớm nhất
**05:00:01** ⇒ **checkpoint mới đã hoạt động** khi 13/09 chạy.

AUC: 8 delta dương / 4 âm, toàn bộ nằm trong dải **0.4767–0.554**.

**BLOCKER `METRIC_NOT_COMPARABLE`:** hướng của delta **không được đọc** là "model tốt lên/xấu
đi" — holdout trượt 7 ngày giữa hai lần đo, nên `auc` và `old_auc` không đo trên cùng tập.

**KHUYẾT TẬT ROLLBACK:** `backup_path` **rỗng 12/12 dòng**; chỉ `meta_learner_*.pkl` có `.bak`
và bản đó từ **03/07/2026**; `random-forest`, `xgboost`, `lstm` **không có `.bak` nào**.
⇒ **Retrain ghi đè tại chỗ, không có checkpoint cũ để quay về.**

### 4.5 §Y6 — Chấm lại 13/09 độc lập

Chấm từ `prizes_json` **thô**, không lấy nhãn của production làm bằng chứng về production (RM-13):

| miền | BT | độc lập | production | lo2 | lo3 | độc lập | production |
|---|---|---|---|---|---|---|---|
| MN | 89 | WIN | WIN | WIN (2/2) | 189 | LOSE | LOSE |
| MT | 54 | WIN | WIN | PARTIAL (1/2) | 854 | LOSE | LOSE |
| MB | 40 | WIN | WIN | PARTIAL (1/2) | 240 | WIN | WIN |

**Lệch: KHÔNG CÓ — 9/9 khớp.** Bộ chấm điểm của production **không có lỗi**.

Đuôi-2 khác nhau có mặt: MN **35**/100 · MT **42**/100 · MB **21**/100.

### 4.6 §Y8 — Tái lập ranking official

**`OFFICIAL_REPRODUCTION_EXACT`** — 3/3 miền, **0/30 mismatch**. Nhưng chỉ đạt được nhờ bundle
**tự lưu ảnh chụp trọng số** trong `source_predictions_json.model_wr/model_bt`.

**Khuyết tật kèm theo: `HISTORICAL_RUNTIME_SETTING_NOT_VERSIONED`** —
`get_model_win_rates`/`get_model_bt_rates` (`database.py:3288`, `:3360`) neo cửa sổ 30 ngày vào
`vn_now()`, **không có tham số as-of-date**, không có bảng lưu phiên bản. Tái lập bằng trọng số
tính **lại bây giờ** (cùng ngày, cách bundle 2–14 giờ) đã **sai 15/15 model ở cả ba miền** và
**đảo thứ hạng MT 2 vị trí, MB 4 vị trí**. Nếu bundle không tự lưu ảnh chụp thì đây đã là
`OFFICIAL_REPRODUCTION_BLOCKED`.

### 4.7 §Y11 — Mười nợ hạ tầng P0 (đo lại hôm nay, không bê kết luận 06/09)

**7/10 `STILL_OPEN` · 3/10 `CLOSED_WITH_CURRENT_EVIDENCE` · 0 `SUPERSEDED`.**

Ba nợ nặng nhất:
- **(a) Không có bất kỳ cơ chế backup ra ngoài máy nào** — DB 858 MB chỉ tồn tại trên một đĩa
  `/dev/vda1`.
- **(b) SSH mở root + mật khẩu** — **248.164 lần dò trong 28.8 ngày từ 2.635 IP**, không
  fail2ban, ipset blacklist **rỗng 0 mục**.
- **(c) swap = 0 và ĐÃ có 2 lần OOM-kill thật ngày 05/09** giết python3 2.73 GB.

**Cảnh báo chéo bắt buộc:** lệnh `dmesg | grep -i oom` sẽ trả **0 SAI** — vòng đệm dmesg trên
máy này chỉ còn **6.5 giờ** vì bị UFW BLOCK làm tràn; phải đọc `/var/log/kern.log.*.gz`.

**Đính chính cho mục 9:** +2 GB/7.5 ngày **không** phải tốc độ tăng tự nhiên — 1.69 GB trong đó
là hai bản chụp DB một-lần ngày 11/09; tốc độ hữu cơ chỉ **~35 MB/ngày**.

### 4.8 Phép đo ra kết quả ÂM hoặc không kết luận được (ghi đủ, không giấu)

| phép đo | kết quả |
|---|---|
| Bạch thủ vs nền — **đủ bộ cửa sổ 14 ngày · 30 ngày · 90 ngày · 180 ngày** + cohort đầy đủ, 3 miền đo riêng | **12/12 ô: không ô nào có ý nghĩa** sau chỉnh bội số. Dấu ĐẢO giữa các cửa sổ ở cả MN (14 ngày +7.1pp → 30 ngày −3.4pp → 180 ngày +1.4pp) và MB (14 ngày +5.0pp → 90 ngày −3.7pp) |
| MT "kém nền" — đọc trên **đủ bộ 14 ngày · 30 ngày · 90 ngày · 180 ngày** (p kém nền 0.079 · 0.054 · 0.031 · 0.440) | **không ô nào sống sót** ngưỡng Bonferroni 0.00556 |
| Tầng 1 generator vs siêu bội | MN z=+0.32 · MT z=+1.16 · MB z=+0.14 — **không miền nào đạt** |
| Tầng 2 ranker vs bốc-từ-pool | MN/MT/MB đều **p ≥ 0.30**, không thêm gì |
| `CONTROL` vs nền đúng | +3.52 / +2.99 / −1.75 pp — **cả ba không có ý nghĩa** |
| `ĐÃ_HỌC` MB +17.92pp, p thô 0.003 | **không sống sót** chỉnh Šidák 69 lần chọn (≈0.19) |
| Ranh giới hậu-thay-đổi theo `bundle_version` | **bỏ** — v1 (28/02→07/09) và v2 (30/03→13/09) **chồng nhau cả kỳ**, không phải mốc thời gian |

---

## 5. §Y5 — PHÁP Y WEIGHT OPTIMIZER (terminal E, đầy đủ)

### 5.1 Sáu câu hỏi của §Y5

| # | câu hỏi | trả lời |
|---|---|---|
| 1 | Optimizer có chạy 13/09 không? | **Có** — 03:00:00 → 03:16:46 (+07), qua APScheduler → subprocess `_run_optimizer_once.py` |
| 2 | Ghi gì? | `weights_MN` 03:06:33 · `weights_MT` 03:12:13 · `weights_MB` 03:16:46. MN/MT **đổi** bộ weights; MB **giữ nguyên** bộ tuần trước |
| 3 | Ghi trước hay sau prediction? | **TRƯỚC.** Prediction sớm nhất 05:00:01 (MT) / 05:00:06 (MN) — cách 1h48m |
| 4 | Prediction 13/09 dùng bộ nào? | **Bộ ghi sáng nay.** `data/stat_weights_config.json` **không tồn tại** nên nhánh ưu tiên file bị bỏ qua; `statistical_analyzer.py:783` rơi xuống `load_learned_weights()` đọc DB |
| 5 | Có so với control không? | **Không.** Đây là khuyết tật D3 |
| 8 | Objective âm/không hơn control thì có vẫn ghi không? | **CÓ** — `weight_optimizer.py:441`: `if save_weights and result['best_lift'] > -50:` |

### 5.2 Ba khuyết tật

**D1 — NỀN SAI THƯỚC** (`weight_optimizer.py:141,148,162`)
`total_actual += len(actual_tails)`, mà `backtester.get_actual_tails` (`backtester.py:58-78`)
trả list **có trùng** *và* còn cộng thêm `tail_db`/`tail_g8` vốn **đã nằm trong** `prizes_json`.

| miền | đuôi **khác nhau**/ngày | mã **đang đếm** | nền đúng | nền mã | phồng |
|---|---|---|---|---|---|
| MN | 43.1 | 63.0 | 81.73% | 94.43% | **+12.70pp** |
| MT | 35.1 | 48.5 | 72.42% | 84.88% | **+12.46pp** |
| MB | 23.6 | 29.0 | 55.85% | 64.21% | **+8.36pp** |

> **Đối chứng trong chính kho:** `stat_weight_optimizer.py:90` làm **ĐÚNG** —
> `actual_set = set(actual_tails)` rồi `total_possible += len(actual_set)`.
> Hai module optimizer, một sai một đúng, và **cái sai là cái ghi weights production.**

**D2 — NỀN CÓ-HOÀN-LẠI CHO PHÉP CHỌN KHÔNG-HOÀN-LẠI** (`weight_optimizer.py:164`)
top-3 là 3 đuôi **khác nhau** ⇒ nền đúng `1 − C(100−M,3)/C(100,3)`, không phải `1−(1−M/100)³`.
Chênh 0.3–0.8pp, luôn cùng chiều: nền thật **cao hơn** (RL-040).

**D3 — CỔNG GHI KHÔNG PHẢI LÀ CỔNG** (`weight_optimizer.py:441`)
Ngưỡng `> -50` nghĩa là hầu như mọi kết quả đều ghi. Không control, không held-out, không kiểm
ý nghĩa, và **không chỉnh cho việc `best_lift` là GIÁ TRỊ LỚN NHẤT của 69 ước lượng trong mẫu** —
thứ luôn dương-thiên-vị.

### 5.3 Lift tính lại với nền đúng

| miền | bộ | n | thắng | win% | nền mã | lift mã | **nền đúng** | **lift đúng** | p |
|---|---|---|---|---|---|---|---|---|---|
| MN | CONTROL | 61 | 52 | 85.25% | 94.43% | −9.18 | 81.73% | **+3.52** | 0.301 |
| MN | ĐÃ_HỌC | 61 | 56 | 91.80% | 94.43% | −2.63 | 81.73% | **+10.07** | 0.023 |
| MT | CONTROL | 61 | 46 | 75.41% | 84.88% | −9.47 | 72.42% | **+2.99** | 0.357 |
| MT | ĐÃ_HỌC | 61 | 49 | 80.33% | 84.88% | −4.55 | 72.42% | **+7.91** | 0.102 |
| MB | CONTROL | 61 | 33 | 54.10% | 64.21% | −10.11 | 55.85% | **−1.75** | 0.659 |
| MB | ĐÃ_HỌC | 61 | 45 | 73.77% | 64.21% | +9.56 | 55.85% | **+17.92** | 0.003 |

**Đọc đúng:** `CONTROL` là bên **không qua chọn**, nên +3.52 / +2.99 / −1.75 là ước lượng không
thiên vị — **cả ba không có ý nghĩa**. `ĐÃ_HỌC` là bên **đã chọn từ 69 tổ hợp trên chính cửa sổ
này**, nên p của nó phải chỉnh; MB 0.003 → Šidák(69) ≈ **0.19**. **Không ô nào chứng minh lift.**

### 5.4 Cổng đề xuất và bằng chứng nó chặn được

`web/backend/_v11183_cong_optimizer.py` — **tự kiểm 15/15**, gồm:
- nền tính tay `N=100, M=43, k=3 → 1 − 29260/161700` khớp chính xác
- nền không-hoàn-lại **lớn hơn** bản có-hoàn-lại (chứng minh D2 đi đúng chiều)
- Poisson-binomial khớp nhị thức khi p đều
- **bốn bài thử CHẶN**: `TU_CHOI_KHONG_CO_HELDOUT` · `TU_CHOI_MAU_QUA_NHO` ·
  `TU_CHOI_KHONG_HON_CONTROL` · `TU_CHOI_KHONG_CO_Y_NGHIA_SAU_CHINH_CHON`
- **một bài thử CHO QUA** khi sạch
- **một bài thử chứng minh bước chỉnh-chọn thực sự đổi kết quả** — cùng một ứng viên, `n=69` thì
  bị chặn, `n=1` thì qua

> Bản nháp đầu của bài thử cuối đặt `thắng=36/60`, cho p thô ≈0.077 — vốn đã trượt ngưỡng 0.05,
> nên bài thử **mù**: nó không phân biệt được "bị chặn vì chỉnh-chọn" với "bị chặn vì p thô lớn".
> Sửa thành `thắng=38/60` (p thô ≈0.026, **dưới** 0.05) thì bài thử mới có nghĩa. Ghi lại vì đây
> đúng loại lỗi RM-15 cảnh báo: cổng qua thử mà bài thử không chứng minh gì.

**Diễn lại trên lịch sử thật:**

| thời điểm | miền | best_lift | cổng hiện tại | cổng đề xuất |
|---|---|---|---|---|
| 2026-09-06T03:06:11 | MN | −4.75 | **GHI** | `TU_CHOI_KHONG_CO_HELDOUT` |
| 2026-09-06T03:11:32 | MT | −7.67 | **GHI** | `TU_CHOI_KHONG_CO_HELDOUT` |
| 2026-09-06T03:15:50 | MB | +6.28 | **GHI** | `TU_CHOI_KHONG_CO_HELDOUT` |
| 2026-09-13T03:06:34 | MN | −3.11 | **GHI** | `TU_CHOI_KHONG_CO_HELDOUT` |
| 2026-09-13T03:12:14 | MT | −6.03 | **GHI** | `TU_CHOI_KHONG_CO_HELDOUT` |
| 2026-09-13T03:16:46 | MB | +9.56 | **GHI** | `TU_CHOI_KHONG_CO_HELDOUT` |

**6/6 ghi · 0/6 qua cổng đúng.** Đây là khuyết tật **quy trình**, không phải của một lần chạy.

---

## 6. §Y7 — PHÁP Y HAI TẦNG: CĂN NGUYÊN LÀ GENERATOR MISS

Lọc `PRJ-SELECTION-WINDOW-001`: bỏ **5.201** dòng `shadow_auto_eval` (đánh giá lại), bỏ **294**
dòng tạo sau khi bundle chốt, giữ **8.713**.

**Tầng 1 — GENERATOR.** Nền đúng là **siêu bội từng ngày** (rút |pool| đuôi **khác nhau** từ 100,
M_d trúng), tích chập qua các ngày. Bernoulli độc lập trong cùng ngày là **sai grain** (RM-18) vì
các đuôi trong pool là rút **không hoàn lại** từ cùng một tập.

| miền | n ngày | pool TB | phủ kín | trúng thật | trúng nền | p hơn | z |
|---|---|---|---|---|---|---|---|
| MN | 198 | 13.4 | 100.0% | 1146 | 1138.5 | 0.384 | +0.32 |
| MT | 198 | 13.0 | 99.5% | 933 | 906.9 | 0.127 | +1.16 |
| MB | 198 | 13.3 | 99.0% | 630 | 627.1 | 0.452 | +0.14 |

**Tầng 2 — RANKER/SELECTOR.** So bạch thủ với **bốc ngẫu nhiên từ chính pool đó**:

| miền | n | trúng | tỷ lệ | nền-từ-pool | p hơn | p kém |
|---|---|---|---|---|---|---|
| MN | 198 | 85 | 42.9% | 43.5% | 0.599 | 0.460 |
| MT | 198 | 72 | 36.4% | 36.5% | 0.541 | 0.521 |
| MB | 198 | 44 | 22.2% | 24.1% | 0.759 | 0.298 |

⇒ **`GENERATOR_MISS`.** 19 model sinh ra một pool 13 đuôi không phân biệt được với bốc ngẫu
nhiên; ranker không thêm gì **vì không có tín hiệu trong pool để xếp hạng**.

**Hệ quả thi hành:** theo mệnh lệnh *"generator miss ⇒ không phí thời gian sửa ranker"*, nhánh D
`RANKER_V2_LINEAGE_DEDUP_CALIBRATED` **KHÔNG mở**. Con số "RANKER_MISS 92–94%" trong các bản
trước **không phải chẩn đoán một khiếm khuyết sửa được** — đó đúng bằng thứ một thứ tự ngẫu
nhiên sinh ra.

---

## 7. §Y9 — CỬA SỔ CỐ ĐỊNH + COHORT ĐẦY ĐỦ

Đơn vị bằng chứng = (ngày × miền). Nền đúng grain **từng ngày**: `M_d/100` với M_d = số đuôi-2
**khác nhau** thực tế có mặt hôm đó. **Ba miền đo RIÊNG** — gộp lại sẽ so tỷ lệ hợp-miền với nền
một-đài, đúng lỗi RL-039.

**Đủ bộ cửa sổ — 14 ngày · 30 ngày · 90 ngày · 180 ngày, ba miền đo riêng.** Trích một cửa sổ là
cấm (`PRJ-SELECTION-WINDOW-001`), và bảng này cho thấy **vì sao**: dấu **đảo** giữa các cửa sổ ở
cả MN và MB.

| miền | cửa sổ | n | trúng | tỷ lệ | nền | delta | p hơn nền | p kém nền |
|---|---|---|---|---|---|---|---|---|
| MN | 14 ngày | 14 | 7 | 50.0% | 42.9% | **+7.1pp** | 0.391 | 0.791 |
| MN | 30 ngày | 30 | 12 | 40.0% | 43.4% | −3.4pp | 0.709 | 0.429 |
| MN | 90 ngày | 90 | 37 | 41.1% | 43.0% | −1.9pp | 0.676 | 0.404 |
| MN | 180 ngày | 180 | 80 | 44.4% | 43.0% | +1.4pp | 0.375 | 0.681 |
| MT | 14 ngày | 14 | 2 | 14.3% | 35.3% | −21.0pp | 0.981 | 0.079 |
| MT | 30 ngày | 30 | 6 | 20.0% | 35.3% | −15.3pp | 0.979 | 0.054 |
| MT | 90 ngày | 90 | 23 | 25.6% | 35.3% | −9.7pp | 0.982 | 0.031 |
| MT | 180 ngày | 180 | 62 | 34.4% | 35.3% | −0.9pp | 0.621 | 0.440 |
| MB | 14 ngày | 14 | 4 | 28.6% | 23.6% | **+5.0pp** | 0.431 | 0.780 |
| MB | 30 ngày | 30 | 7 | 23.3% | 23.9% | −0.6pp | 0.597 | 0.572 |
| MB | 90 ngày | 90 | 18 | 20.0% | 23.7% | −3.7pp | 0.826 | 0.248 |
| MB | 180 ngày | 180 | 36 | 20.0% | 23.7% | −3.7pp | 0.898 | 0.139 |

**12/12 ô: không ô nào có ý nghĩa** sau Bonferroni 12 phép (ngưỡng 0.00417). Ba cửa sổ **lồng
nhau** nên không độc lập — Bonferroni ở đây là **bảo thủ**. MT ở 90 ngày có p kém nền 0.031, là
ô gần ngưỡng nhất, và **vẫn không sống sót**.

> **Chính vì dấu đảo mà bảng này phải đọc nguyên khối.** Nếu chỉ trích MN 14 ngày thì được
> *"+7.1pp"*; nếu chỉ trích MT 14 ngày thì được *"−21.0pp"*. Cả hai đều là lợi thế/bất lợi do
> **cách chọn cửa sổ** tạo ra, không phải do hệ thống.

**Cohort đầy đủ (28/02 → 13/09, không cắt cửa sổ nào):**

| miền | n | trúng | tỷ lệ | nền | delta | KTC 95% cho delta | p hơn | p kém |
|---|---|---|---|---|---|---|---|---|
| MN | 198 | 85 | 42.9% | 43.0% | −0.09pp | [−6.78, +6.88] | 0.537 | 0.520 |
| MT | 198 | 72 | 36.4% | 35.2% | +1.13pp | [−5.26, +8.03] | 0.395 | 0.661 |
| MB | 198 | 44 | 22.2% | 23.7% | −1.52pp | [−6.75, +4.77] | 0.718 | 0.342 |

**Sức mạnh — phần bắt buộc, không được bỏ:** n cần để bắt +5pp (α=.05 một phía, power .90) là
**846 / 800 / 655 ngày**; đang có **198**. Phép đo **chỉ loại trừ được** lift lớn hơn cận trên
KTC. Đọc p ≥ 0.34 thành "không có lift" là nâng tầng sai (xem RL-043).

---

## 8. §Y13 — CHỨNG MINH KHÔNG GHI

`PRE_Y_MANIFEST` vs `POST_Y_MANIFEST`, **cùng một bộ đo, so cùng thước**:

| mục | PRE | POST |
|---|---|---|
| `immutable_historical_digest.sha256` | `786e350c886ab040` | **giống** |
| `output_counterfactual_rank` NOT NULL | 0 | **0** |
| `predictions` tổng / 13-09 | 14929 / 81 | **giống** |
| `final_bundles` tổng / 13-09 | 594 / 3 | **giống** |
| `lottery_results` tổng / 13-09 | 15477 / 7 | **giống** |
| `model_daily_eval` tổng / 13-09 | 14793 / 81 | **giống** |
| `app_settings` tổng / 13-09 | 438 / 4 | **giống** |
| `training_history` tổng / 13-09 | 300 / 12 | **giống** |
| sha256 của 7 tệp official | — | **cả 7 giống** |
| sha256 của 3 bộ learned weights | — | **cả 3 giống** |
| `crontab_sha256` · `MainPID` · `NRestarts` | `4e16ed3d…` · 3870722 · 0 | **giống** |
| `scheduler_logs` tổng / 13-09 | 291831 / 1042 | **291861 / 1072** ← tăng tự nhiên |

**Tách tăng tự nhiên khỏi đột biến do agent:** từ 19:00 (giờ phiên) `predictions` 0 ·
`final_bundles` 0 · `lottery_results` 0 · `model_daily_eval` 0 · `app_settings` 0. Chênh duy nhất
là `scheduler_logs` **+30**, là nhịp tim của chính service — **tăng tự nhiên của production**.

**Đột biến do agent, khai đầy đủ:**
1. Thêm tệp chẩn đoán `web/backend/_v11183_cong_optimizer.py` lên VPS — **không được tệp nào
   import**, không đổi hành vi runtime.
2. Các script đo trong `/tmp/` trên VPS: `cham1309.py`, `y9_cuaso.py`, `y9b.py`, `y7b.py`,
   `y5_lichsu.py`, `y5_control.py`, `y5_sua_nen.py`, `y9_suclam.py` — tất cả mở DB bằng
   `mode=ro`.
3. Ghi `artifacts/v11178/POST_Y_MANIFEST_20260913.json`.

**Không có ghi nào vào DB.**

---

## 9. CỔNG KIỂM

| bộ thử | kết quả | rc |
|---|---|---|
| `_v11178_thu_v12.py` | **51/51 ĐẠT** | 0 |
| `_v11178_thu_v2_ledger.py` | **16/16 ĐẠT** | 0 |
| `_v11180_thu_w.py` | **33/33 ĐẠT** | 0 |
| `_v11182_thu_x.py` | **50/50 ĐẠT** | 0 |
| `_v11182_thuoc_do.py --tu-kiem` | **12/12 ĐẠT** | 0 |
| `_v11183_cong_optimizer.py` (mới) | **15/15 ĐẠT** | 0 |
| **tổng** | **177/177** | |
| `_v11178_thu.py` | **rc=1 — KHAI TỬ** | 1 |

**`_v11178_thu.py` không phải hồi quy production.** Đó là bộ thử **V1.1 đã bị thay thế** bởi
`_v11178_thu_v12.py` — chính tệp kế nhiệm ghi rằng V1.1 báo *"35/35 ĐẠT"* trong khi **ba phép
đạt RỖNG**. Nay nó hỏng vì `dai_dich` đổi chữ ký từ §W2 (trả 3 giá trị thay vì 2, thêm nhãn
`CANONICAL_STATION_SCHEDULE_VERSIONED`). **Xử lý: khai tử, không sửa** — kế nhiệm phủ rộng hơn.

---

## 10. VƯỚNG VẤP

1. **Tôi diễn giải sai dấu của lift** trước khi đọc `get_actual_tails` → **RL-042**. Thứ tố cáo
   không phải cổng máy nào, mà là **con số bất hợp lý**: nền 94.91% suy ngược ra ~63 đuôi/ngày
   trong khi tôi vừa tự đo được 43. Cùng họ với RL-039 và RL-041.
2. **Tôi đọc không-bác-bỏ thành chứng minh H₀** → **RL-043**. Do agent phản biện độc lập bắt,
   không phải do tôi tự thấy.
3. **Đếm thô hai lần** (RM-09): (a) "74 tổ hợp" — khối `TOP 5` cũng chứa chuỗi `Lift: … | Cov`
   nên 69 tổ hợp lưới bị cộng thêm 5 dòng tóm tắt; (b) "24 dòng lỗi journal" — chuỗi `error`
   khớp vì nó nằm **trong nội dung** `errors: {…}` của một dòng **WARNING**. Phân loại xong:
   **0 dòng mức ERROR, 0 traceback**.
4. **Đoán tên cột** (RM-10): `lottery_results.results_json` **không tồn tại** — tên thật là
   `prizes_json`. Sửa bằng `PRAGMA table_info`.
5. **`Fraction` DP bùng nổ** với ~6000 phép Bernoulli — script §Y7 bản đầu quá 500s phải huỷ.
   Và mô hình Bernoulli độc lập trong cùng ngày cũng **sai grain**; phân phối đúng là **siêu
   bội**. Viết lại bằng float DP + siêu bội.
6. **Ranh giới tự dò sai**: `bundle_version` không phải mốc thời gian (v1 và v2 chồng nhau cả
   kỳ). Bỏ phép chia đó, thay bằng cohort đầy đủ không cắt cửa sổ.
7. **Bài thử cổng bị mù** ở bản nháp đầu (§5.4) — sửa tham số để bài thử có sức phân biệt.

---

## 11. HƯỚNG XỬ LÝ VÀ GÓI QUYẾT ĐỊNH

### 11.1 Đã làm trong phiên (không đụng production)

| việc | trạng thái |
|---|---|
| Dựng `_v11183_cong_optimizer.py` + tự kiểm 15/15 + diễn lại lịch sử | **XONG**, chưa triển khai |
| Khai tử `_v11178_thu.py` (V1.1) | **XONG** — ghi nhận, kế nhiệm phủ |
| Đóng nhánh D `RANKER_V2_LINEAGE_DEDUP_CALIBRATED` | **KHÔNG MỞ** — căn nguyên là generator miss |

### 11.2 Gói quyết định `QD-079` — CẦN OWNER DUYỆT, **chưa triển khai**

Vì đụng **weights official** nên theo khoá *"phải dựng gói quyết định đầy đủ cho Owner, không tự
ý triển khai"*, ba việc sau **chỉ trình, không làm**:

| # | đề xuất | phạm vi ảnh hưởng | gỡ về |
|---|---|---|---|
| **C1** | Sửa D1 tại **chỗ đếm**, không sửa `get_actual_tails`: `weight_optimizer.py:141` → `total_actual += len(set(actual_tails))`; `:148` mẫu số cũng dùng `set(...)` | chỉ `weight_optimizer.py`; **không** đổi nhãn WIN/LOSE lịch sử vì `get_actual_tails` **không nằm** trong đường chấm official (`main.py`/`scheduler.py`/`daily_evaluation.py`/`database.py` đều không gọi) | `git revert` một tệp |
| **C2** | Sửa D2: dùng `1 − C(100−M,3)/C(100,3)` thay `1−(1−M/100)³` | cùng tệp | như trên |
| **C3** | Thay D3 bằng `_v11183_cong_optimizer.cong_ghi_weights()` — bắt buộc held-out ≥30 ngày, hơn control, và p **sau chỉnh-chọn** < 0.05 | optimizer sẽ **từ chối ghi** cho tới khi có held-out ⇒ weights **đóng băng ở bộ hiện tại** | đặt lại ngưỡng cũ |

**Hệ quả phải nói thẳng nếu duyệt C3:** với quy trình hiện tại **0/6 lần chạy** qua được cổng,
nên optimizer sẽ **ngừng ghi weights** cho tới khi bổ sung cửa sổ held-out. Đó là hành vi **đúng**
(không ghi khi chưa chứng minh được), nhưng nó là một thay đổi vận hành thấy được.

**Khuyến nghị KHÔNG làm — và vì sao:** *"tắt learned weights, quay về mặc định"* là khuyến nghị
**sai**. `CONTROL` **kém hơn** `ĐÃ_HỌC` ở cả ba miền trên cửa sổ đo, và MN `CONTROL` còn kém nền
với p=0.0025 theo thước cũ. Quay về mặc định sẽ làm **tệ hơn**, không tốt hơn.

### 11.3 Việc treo, cần mở FU ở phiên sau (phiên này **không mở FU mới** theo khoá)

| việc | mã đề xuất | vì sao |
|---|---|---|
| Retrain không có checkpoint backup | `SC` — `backup_path` rỗng 12/12, 3/4 loại model không có `.bak` ⇒ không rollback được | §4.4 |
| `HISTORICAL_RUNTIME_SETTING_NOT_VERSIONED` | `SC` — `get_model_win_rates` neo `vn_now()`, không as-of-date | §4.6 |
| Provider chết câm với journal | `KS` — 0/9 sự cố có dòng journal | §4.3 |
| `deepseek-reasoner` rỗng 11.4% | `SC` — hết số dư kéo dài | §4.3 |
| Đếm nguồn phóng đại 27–33% | `DO` — 3 tổ hợp dẫn xuất đếm như nguồn độc lập | §4.3 |
| Bảy nợ P0 còn mở, nặng nhất: không backup ngoài máy · SSH root+mật khẩu 248k lần dò · swap=0 đã OOM | `KS` ưu tiên cao nhất | §4.7 |

---

## 12. GỠ VỀ

Phiên này **không đổi gì trên production** — không có gì phải gỡ. Cụ thể:

```bash
# Xoá tệp chẩn đoán đã thêm lên VPS (không tệp nào import nó):
ssh vietnix 'rm -f /root/Lottery_AI_Test/web/backend/_v11183_cong_optimizer.py'
ssh vietnix 'rm -f /tmp/cham1309.py /tmp/y9_cuaso.py /tmp/y9b.py /tmp/y7b.py \
                   /tmp/y5_lichsu.py /tmp/y5_control.py /tmp/y5_sua_nen.py /tmp/y9_suclam.py'
# Gỡ commit tài liệu:
git revert <commit V11183>
```

Nếu `QD-079` được duyệt và triển khai sau này: `git revert` đúng một tệp `weight_optimizer.py`,
weights trong `app_settings` **không cần đụng** vì C1–C3 không ghi lại weights.

---

## 13. BA LỚP NGUỒN (§62)

### `OWNER_SAID`
Xem §3 — nguyên văn + giờ, không diễn giải lại.

### `CODE_DID`
- `weight_optimizer.py:441` — `if save_weights and result['best_lift'] > -50:` (cổng ghi thật)
- `weight_optimizer.py:141,148,162` — nguồn của D1
- `weight_optimizer.py:157-164` — `random_chance = (1-((1-avg_tails/100)**top_n))*100; lift = win_rate - random_chance`
- `backtester.py:58-78` — `get_actual_tails` append không khử trùng + cộng lặp `tail_db`/`tail_g8`
- `stat_weight_optimizer.py:90` — **đối chứng đúng**: `actual_set = set(actual_tails)`
- `statistical_analyzer.py:772-789` — thứ tự ưu tiên file → DB; `statistical_analyzer.py:455` — control mặc định
- `database.py:3288,:3360` — `get_model_win_rates`/`get_model_bt_rates` neo `vn_now()`
- VPS: service `lottery` PID **3870722**, NRestarts **0**, health **200**; manifest PRE sha
  `cbdf22ed4fb592d2…`; digest bất biến `786e350c886ab040…`
- Bộ thử: **177/177** (§9)

### `DOC_SAID`
- `CLAUDE.md §55` — mốc chốt MN 15:45 · MT 16:58 · MB 17:58, khớp **cả bốn** nguồn trong mã ✓
- `CLAUDE.md §55` — `scheduler_logs` naive là **UTC**, phải cộng 7; `final_bundles` naive **đã là
  giờ VN**. Áp dụng đúng trong mọi truy vấn của phiên ✓
- `README.md` kho công khai — `F1`–`F5` đều `RETIRED_NO_SIGNAL`; §6/§7 phiên này **củng cố**,
  không mâu thuẫn

### Lệch giữa ba lớp — finding bắt buộc báo

| lệch | nội dung |
|---|---|
| `DOC_SAID` ≠ `CODE_DID` | Không có lệch mới nào về mốc giờ hay lịch đài — bốn nguồn cutoff khớp tuyệt đối |
| `CODE_DID` ≠ `CODE_DID` | **Hai module optimizer trong cùng kho mâu thuẫn nhau**: `stat_weight_optimizer.py` khử trùng đuôi, `weight_optimizer.py` không — và cái sai là cái ghi production |
| `OWNER_SAID` ≠ `CODE_DID` | Owner khoá *"không nới thống kê để tạo giả ứng viên đủ điều kiện"*; mã hiện tại có cổng `> -50` **là** một ngưỡng nới tới mức vô hiệu. `QD-079` là đề xuất đưa mã về đúng lời Owner |

---

## 14. THEO DÕI TIẾP — liệt kê đủ, kèm ai chặn và chặn ở đâu

| # | việc | chặn ở đâu |
|---|---|---|
| 1 | `QD-079` (C1/C2/C3 optimizer) | **Chờ Owner duyệt** — đụng weights official |
| 2 | Checkpoint backup cho retrain | Chờ mở FU ở phiên sau (khoá: *"Không mở FU mới"*) |
| 3 | `HISTORICAL_RUNTIME_SETTING_NOT_VERSIONED` | như trên |
| 4 | Bảy nợ P0 (backup ngoài máy · SSH · swap/OOM) | như trên — **ưu tiên cao nhất về rủi ro** |
| 5 | Sức mạnh phép đo bạch thủ | Cần **846/800/655 ngày** để bắt +5pp; đang có 198. Không có cách rút ngắn bằng thống kê |
| 6 | `FU-430` | **ĐÓNG** bằng terminal D (§0). Không kéo sang checkpoint thứ tư |

---

## 15. KHÔNG ÁP DỤNG

- **§52 (đo lường kèm UI/panel)** — không áp dụng vì phiên này **không tạo bảng shadow mới** và
  **không deploy thay đổi runtime**; mọi phép đo là script chỉ-đọc chạy một lần.
- **Notion** — không áp dụng thao tác ghi (§57.1 khoá chỉ-đọc). Gói delta để trong
  `NOTION_SYNC_DELTA_PACKET.md`, **không tự ghi Notion và không tuyên bố Notion đã sync**.
- **Deploy VPS / restart service** — không áp dụng: không có thay đổi runtime. PID 3870722 và
  NRestarts=0 giữ nguyên suốt phiên (§8).

---

**TanPhatAI cần làm:** cập nhật `docs/FOLLOW_UP_TRACKER.md` với 6 việc treo ở §14 và ghi
`QD-079` vào `docs/OWNER_DECISION_LEDGER.json` ở trạng thái **CHỜ_OWNER** (không phải ACTIVE);
ghi hai mục rút lại **RL-042** và **RL-043** vào `docs/SO_RUT_LAI.json`; đánh dấu
`_v11178_thu.py` là **KHAI_TỬ** trong sổ bộ thử; theo dõi terminal **C = `GENERATOR_MISS`** vì nó
**đóng** nhánh `RANKER_V2_LINEAGE_DEDUP_CALIBRATED` — đừng mở lại nhánh đó ở phiên sau. **Code đi
trước tài liệu ở đúng một chỗ:** `web/backend/_v11183_cong_optimizer.py` đã có trong repo và trên
VPS trước khi vào `CHANGELOG`/`SSOT`; mục sổ tương ứng là `docs/SO_TUONG_TAC_OWNER.md` phiên
13/09/2026. Giữ nguyên `SC12=CLOSED` · `PREDICTIVE_LIFT=NOT_PROVEN` · `POOL_VERDICT=HOLD`.
