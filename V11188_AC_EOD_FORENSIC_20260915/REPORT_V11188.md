# REPORT V11188 — §AC · EOD 14/09 PREDICTION FORENSIC · CHANGE-IMPACT · §AB FIRST-NATURAL READINESS

> **Phiên:** 15/09/2026 02:00 → 03:xx ICT · **Mã đọc §58:** `DO1509` · **Prompt:** 43 R1 §AC
> **Hai ngày, hai epoch, KHÔNG trộn:** `TARGET_EOD_DATE=2026-09-14` chạy **trọn ngày V11185** ·
> `FIRST_NATURAL_PROOF_DATE=2026-09-15` là ngày đầu dưới **V11186/§AB** (deploy 14/09 20:05).
> **Khoá giữ nguyên:** `SC12=CLOSED` · `PREDICTIVE_LIFT=NOT_PROVEN` · `POOL_VERDICT=HOLD` ·
> `F1`–`F5` `RETIRED` · TOTAL formula · current weights · bốn override · prompt CORE **không đổi**

---

## 1. TÓM TẮT — TERMINAL DỨT ĐIỂM (§AC-U)

```
EOD_20260914_RESULT_DATA          = COMPLETE_VALID
OFFICIAL_BT_20260914              = MN_LOSE · MT_WIN · MB_LOSE                        (1/3)
OFFICIAL_LO2_20260914             = MN_PARTIAL(14 về) · MT_WIN(20,88) · MB_PARTIAL(31 về)
OFFICIAL_LO3_20260914             = MN_LOSE(424) · MT_LOSE(620) · MB_LOSE(016)
TOTAL_ROOT_CAUSE                  = MN_RANKER_MISS · MT_OFFICIAL_WIN · MB_RANKER_MISS
ROGUE_COMBO_CALL_OUTPUT_IMPACT    = NO_OUTPUT_IMPACT_AS_RUN
                                    (+ OUTPUT_CONTAMINATION_PATH_CONFIRMED — xem §7)
ROSTER_COMPRESSION_14SEP          = OPERATIONALLY_DEGRADED_WITH_EXACT_FAILURE
ROSTER_COMPRESSION_PREDICTIVE_LIFT= NOT_PROVEN
§AB_RUNTIME_14SEP                 = NOT_APPLICABLE_DEPLOYED_AFTER_EOD
§AB_DEPLOYMENT                    = DEPLOYED_PENDING_NATURAL_PROOF
V11186_FIRST_NATURAL_READY        = YES                                    (15/15 phép)
TOKEN_14SEP                       = ACTUAL_CALLS_AND_TOKENS_MEASURED  14 lượt / 424.615 token
COST_14SEP                        = UNKNOWN cho 9 lượt · TÍNH LẠI ĐƯỢC cho 5 lượt OpenRouter
OVERRIDE_LINEAGE                  = CODED_TESTED_STAGED                          (23/23)
FAMILY_LINEAGE                    = CODED_TESTED_STAGED                          (30/30)
RETRAIN_ATOMIC_PATH               = IN_PROGRESS_WITH_EXACT_MODULE                (42/42)
PURE_CONTEXT                      = DEFERRED_PENDING_FULL_LIVE_PROOF
PREDICTIVE_LIFT                   = NOT_PROVEN
POOL_VERDICT                      = HOLD
SC12                              = CLOSED_DO_NOT_REOPEN
```

**Câu trả lời ngắn cho mười câu Owner hỏi ở cuối §AC** nằm ở §17.

**Ba phát hiện nặng nhất, không phát nào nằm trong đề bài:**

1. **Nguyên nhân thua KHÔNG phải generator.** Cả ba miền, pool ứng viên đông cứng **đều chứa**
   đuôi trúng. MN và MB là **`RANKER_MISS`** — hệ xếp số trúng xuống dưới. MB còn trớ trêu hơn:
   số trúng `31` chính là **số thứ hai của đúng model đã đặt số thua `16` lên đầu**.
2. **Nén roster 8→4 làm mọi bundle bị xếp `INCOMPLETE`.** `EXPECTED_MODEL_COUNT=15` tính động từ
   `get_output_eligible_ids()` — danh sách đó **vẫn còn** `gemini-2.5-pro`, `deepseek-reasoner`,
   `gpt-5.4`, tức model ngoài mọi roster hoặc đang bị cách ly. Ngày 14/09 cả ba miền
   `model_count=11` ⇒ `classify_bundle_quality` = **`INCOMPLETE`**. Sửa chính sách gọi mà không
   sửa ngưỡng hoàn chỉnh — đúng lỗi §60 *"bỏ nửa chừng"*.
3. **Có một lớp hậu-xếp-hạng THỨ NĂM** không nằm trong bốn override đã tài liệu hoá:
   `main_number_anti_trap` / `near_miss_anti_trap` (`main.py:10441+`). **Bạch thủ DUY NHẤT thắng
   trong ngày (MT `20`) bị chính lớp này gắn cờ `FULL_SPENT`.**

---

## 1b. THƯỚC BẠCH THỦ — BÁO CÁO NÀY KHÔNG TUYÊN BỐ HIỆU QUẢ (`PRJ-SELECTION-WINDOW-001`)

Nói trước khi ai đọc nhầm: **báo cáo này không đưa ra bất kỳ tuyên bố hiệu quả nào trên thước
`TW-001` (bạch thủ vs nền đúng từng miền-ngày).** Con số `1/3` của ngày 14/09 là **biên nhận mô tả
của một ngày**, không phải phép đo hiệu quả, và `RM-04` chặn mọi kết luận ở n=1.

Đủ bộ cửa sổ của thước này đã đo ở **V11084 + V11086**, và nó **đổi dấu theo cửa sổ**:

| cửa sổ | lift so với nền |
|---|---|
| 14 ngày | xem V11084 |
| **30 ngày** | **+4,07pp** |
| **90 ngày** | **−3,18pp** |
| **180 ngày** | **+0,91pp** · CI95 `[−3,2 · +5,0]` |

**Dấu đổi theo cửa sổ** chính là lý do `PRJ-SELECTION-WINDOW-001` tồn tại: trích riêng 30 ngày sẽ
tạo ra một "lợi thế" hoàn toàn do cách vạch cửa sổ. Báo cáo này **cấm trích riêng** một cửa sổ, và
giữ `PREDICTIVE_LIFT = NOT_PROVEN` · `ROSTER_COMPRESSION_PREDICTIVE_LIFT = NOT_PROVEN`.

Mọi con số bạch thủ xuất hiện phía dưới đều là **mô tả ngày 14/09**, dùng để truy **cơ chế**
(ranker xếp sai chỗ), **không** dùng để so hiệu quả. Đủ bộ cửa sổ nằm ở V11084/V11086.

---

## 2. OWNER YÊU CẦU GÌ (nguyên văn) — §62 lớp `OWNER_SAID`

Prompt **§AC**, mức thực thi *"TỔNG LỰC · CỰC GẮT · ĐỌC CODE + DB + TRACE + LOG + GITHUB · KHÔNG
ĐOÁN · KHÔNG TÔ XANH · KHÔNG DỪNG Ở «THEO DÕI TIẾP»"*.

> *"Cấm trộn hai epoch: 14/09 trọn ngày chạy V11185. 15/09 trọn ngày phải chạy V11186/§AB. Không
> dùng kết quả 14/09 để tuyên bố §AB đã cải thiện hoặc làm xấu dự đoán: §AB chưa tồn tại trong
> các lượt sinh output ngày 14/09."* (§AC-A)

> *"MỖI NHÁNH PHẢI KẾT THÚC BẰNG: PASS / FAIL / REPAIR / RETIRE / EXACT BLOCKER / CONCRETE
> CHALLENGER."*

> *"Nếu một miền thiếu kết quả: không chấm như LOSE; ghi `UNSCORABLE_MISSING_RESULT`; sửa dữ liệu
> nguồn trước khi phân tích accuracy."* (§AC-E)

> *"Xiên: phải cùng xuất hiện tại cùng một đài. Không được lấy một số ở đài A và một số ở đài B
> rồi ghi WIN."* (§AC-F3)

> *"Cấm: gộp mọi dòng rồi nói «27 model có model trúng»; coi nhiều model cùng ngày là nhiều quan
> sát độc lập; tính thắng của model từ output sau khi biết kết quả; cho shadow/manual tham gia
> official cohort; coi model không output là LOSE."* (§AC-G)

> *"Không restart chỉ để «cho chắc». Không deploy thêm change vào official path trước MN."* (§AC-M)

> *"Được code/test offline ngay. Không deploy vào official giữa các lượt MN/MT/MB ngày 15/09."* (§AC-O)

> *"KHÔNG ĐƯỢC KẾT THÚC BẰNG: «TIẾP TỤC THEO DÕI»."*

**Không có yêu cầu rời nào giữa phiên.**

**Điều Owner yêu cầu mà phiên CỐ Ý không làm, kèm lý do:** không sửa lớp anti-trap vừa phát hiện
và không sửa `EXPECTED_MODEL_COUNT` (§AC-C khoá *"không sửa bốn override legacy trong bước đánh
giá"* và §AC-M cấm đưa thay đổi vào official path trước MN — cả hai đã ghi thành việc treo có hạn
ở §14); không bù backup off-machine (đó là thao tác ghi, ngoài phạm vi phiên read-only).

---

## 3. MANIFEST NGUỒN / EPOCH (§AC-D)

`FORENSIC_INPUT_EPOCH_OK` — DB và trace **cùng epoch**, cùng dừng ở 2026-09-14.

| | |
|---|---|
| đo lúc | **2026-09-15T02:26:36 ICT** (= 2026-09-14T19:26 UTC) |
| service | PID **169960** · NRestarts **0** · `active` từ 2026-09-14 20:06:21 · health **200** |
| row counts | `predictions` 14.965 · `final_bundles` 597 · `lottery_results` 15.483 · `model_daily_eval` 14.829 · `scheduler_logs` 293.428 |
| max date | cả bốn bảng = **2026-09-14** |
| trace | 7.076 dòng · ts cuối **2026-09-14 17:33:43** · sha16 `89c7db7a931150e6` |
| DB | `quick_check=ok` · journal `wal` · **WAL 0 byte** · 863.191.040 B |
| crontab | `81efcf8de5c90c62` · **90 dòng job** |
| sha 5 tệp §AB | khớp bản deploy cả 5 |

Artifact: `evidence/FORENSIC_MANIFEST_20260915.json`. **Không** đưa DB/jsonl/log/secret lên public.

---

## 4. ĐÀO BỚI / PHÁT HIỆN — liệt kê ĐỦ, kể cả nhánh đo ra kết quả âm

§57.3 buộc mục này **liệt kê đủ**, không tóm lược, kể cả việc đo ra kết quả âm hoặc không kết luận
được. Bảy nhánh chạy song song, mỗi nhánh có một agent riêng được giao việc **cố bác bỏ** và bắt
buộc **chạy lại truy vấn** thay vì đọc lại lời. 14 agent, 0 lỗi, 491 lượt gọi công cụ.

| # | đã đào gì | kết quả |
|---|---|---|
| 1 | Kết quả xổ ba miền, trích **chỉ từ `prizes_json`** | `COMPLETE_VALID` cả ba · tail_db khớp 6/6 đài — §4.1 |
| 2 | Chấm lại official từ đầu, 15 trường bundle | khớp stored **100%** — không có `LIVE_SCORING_DEFECT` |
| 3 | Chấm lại **36/36 dòng model** | khớp stored **100%**, 0 sai lệch |
| 4 | Quét dòng sau cutoff | **0/36** |
| 5 | Dựng lại điểm TOTAL ba miền | khớp **100%**, 10/10 vị trí, 4 chữ số — §7.1 |
| 6 | Bốn lớp override | **không lớp nào nổ** — `OVERRIDE_HURT/HELPED` bị loại |
| 7 | Tìm lớp hậu-xếp-hạng chưa tài liệu hoá | **tìm thấy lớp thứ NĂM** — §7.3 |
| 8 | Phản tưởng "bỏ phiếu combo-super" | **kết quả ÂM** — không miền nào đổi số |
| 9 | Phản tưởng "bỏ chiết khấu vị trí" | **kết quả ÂM** — MN và MB vẫn miss |
| 10 | Truy lượt Combo ngoài roster vào bundle | không đổi số, **nhưng đường lan có thật** — §8 |
| 11 | Đếm lại token/cost từ trace thô | trùng từng chữ số với V11187 — §10 |
| 12 | Tìm cost trong journal/log | **0/14 dòng có cost**; 5 lượt OpenRouter **tính lại được** |
| 13 | So `EXPECTED_MODEL_COUNT` với `model_count` thật | **cả ba bundle `INCOMPLETE`** — §9.1 |
| 14 | Đo họ gốc của roster | MN 4 model = **2,67 voter hiệu dụng** — §6.4 |
| 15 | Cohort chọn của V10640 | **41,7% là `shadow_auto_eval`** ⇒ vi phạm `PRJ-SELECTION-WINDOW-001` mục 2 |
| 16 | Hạ tầng P0 (chỉ đọc) | 5/13 blocker — §15 |
| 17 | Phân loại 12 mục tracker quá hạn | §14 |
| 18 | Kiểm `partial_bonus_shadow` có nhân vào score không | **KHÔNG** — chỉ ghi vào trace, §7.1 |
| 19 | Băm `generate_final_bundle` trước/sau deploy | **byte-identical** ⇒ đo đúng mã đã chạy (`RM-13`) |
| 20 | Preflight lượt tự nhiên 15/09 | 15/15 sau khi sửa **false blocker của chính tôi** — §11 |

### 4.1 Kết quả xổ 14/09 (§AC-E) — `COMPLETE_VALID` cả ba miền

Trích **chỉ từ `prizes_json`**, mỗi số một lần. **Không** cộng `tail_db`/`tail_g8` — hai cột đó đã
nằm sẵn trong `prizes_json`; cộng vào là đếm hai lần (`RL-042`, từng gây lift âm giả).

| miền | đài | số giải | đuôi 2 chữ số phân biệt | đuôi 3 chữ số | terminal |
|---|---|---|---|---|---|
| MN | 3/3 — TP. HCM · Đồng Tháp · Cà Mau | 18 mỗi đài | **42** | 49 | `RESULT_COMPLETE_VALID` |
| MT | 2/2 — Phú Yên · Thừa Thiên Huế | 18 mỗi đài | **31** | 34 | `RESULT_COMPLETE_VALID` |
| MB | 1/1 — Hà Nội | 27 | **26** | 22 | `RESULT_COMPLETE_VALID` |

Không đài trùng tên, không đài rỗng, không dòng hỏng. **Kiểm chéo độc lập:** cột `tail_db` so với
hai chữ số cuối của Giải Đặc Biệt trong `prizes_json` — **khớp toàn bộ 6/6 đài**.

`UNSCORABLE_MISSING_RESULT`: **không miền nào** rơi vào.

---

## 5. OFFICIAL SCORECARD 14/09 (§AC-F) — chấm lại từ đầu

| miền | BT | BT status | lô2 | status | lô3 | status | xiên2 | xiên3 |
|---|---|---|---|---|---|---|---|---|
| MN | `24` | **LOSE** | `24,14` | **PARTIAL** (14 về) | `424` | LOSE | **LOSE** | **LOSE** |
| MT | `20` | **WIN** | `20,88` | **WIN** | `620` | LOSE | **WIN** (Thừa Thiên Huế) | **LOSE_KHÁC_ĐÀI** |
| MB | `16` | **LOSE** | `16,31` | **PARTIAL** (31 về) | `016` | LOSE | **LOSE** | **LOSE** |

| | MN row 884 | MT row 886 | MB row 888 |
|---|---|---|---|
| bundle_version · tạo · verified | 2 · 05:17:32 · 16:39:39 | 2 · 16:44:02 · 17:30:00 | 2 · 17:33:44 · 18:30:32 |
| policy · method | `v1_aggregated_top1` · `weighted_voting_wr` | như MN | như MN |
| consensus · model_count · top_score | moderate · **11** · 0,1276 | moderate · **11** · 0,0859 | moderate · **11** · 0,0945 |

**`LIVE_SCORING_DEFECT`: KHÔNG CÓ.** Status đã lưu khớp bản tính lại độc lập **100%**, ở cả tầng
bundle (15/15 trường) lẫn tầng từng model (**36/36** dòng `predictions`, 0 sai lệch).

**Bẫy xiên đã bắt được và chấm đúng:** MT xiên3 = `20,88,30`. **Cả ba số đều về trong miền MT** —
nhưng `30` ở **Phú Yên** còn `20,88` ở **Thừa Thiên Huế**. Gộp miền sẽ chấm nhầm thành WIN. Bản
tính lại ra `LOSE_KHÁC_ĐÀI`, và **status production cũng ghi LOSE** — bộ chấm live đúng ở điểm này.

**Nền ngẫu nhiên CHÍNH XÁC từng miền** (`P = 1 − C(100−M,K)/C(100,K)`, K=1 cho bạch thủ):

| | MN (M=42) | MT (M=31) | MB (M=26) | tổng kỳ vọng |
|---|---|---|---|---|
| nền BT | **0,4200** | **0,3100** | **0,2600** | **0,99 / 3 miền** |
| thực tế | 0 | 1 | 0 | **1 / 3** |

🛑 **n = 1 ngày/miền.** Độ lệch chuẩn của **một** phép Bernoulli tại nền là **0,49 · 0,46 · 0,44**
— lớn hơn mọi "lệch" quan sát được. Theo `RM-04`, **chưa được phép kết luận** bất cứ điều gì về
chất lượng hệ từ con số 1/3 này. Nó là **descriptive receipt**, không phải bằng chứng.

---

## 6. BẢNG ĐIỂM TỪNG MODEL (§AC-G) — `HON_HOP_THEO_MIEN`

36 dòng `predictions`, **0 dòng sau cutoff** (MN muộn nhất 05:17:32 / cutoff 15:45 · MT 16:44:01 /
16:58 · MB 17:33:43 / 17:58). **0 output rỗng · 0 parse failure.**

### 6.1 Model nào tạo giá trị — bảy dòng WIN 2/2 trong ngày

| miền | model | role | số | verdict | vào bundle? |
|---|---|---|---|---|---|
| MN | `claude-opus-4-6` | **CORE** | `36`+`14` | CHOT_HA | có — nhưng 36 chỉ hạng 3 |
| MN | `lstm` | ML | `25`+`20` | CHOT_HA | có |
| MT | `smart-ensemble` | ENSEMBLE | `01`+`52` | **SKIP** (overlap=0) | **bị chặn** |
| MT | `meta-learning` | ML | `52`+`20` | CHOT_HA | có |
| MT | `random-forest` | ML | `30`+`20` | CHOT_HA | có |
| MT | `combo-no-token` | COMBO | — | — | bị guard output-eligible loại |
| MB | `smart-ml` | ENSEMBLE | `71`+`08` | **SKIP** `[GUARD-SKIP] WR=36% < 40%` | **bị chặn** |

**HAI dòng WIN 2/2 bị cổng chặn**: MT `smart-ensemble` và MB `smart-ml`. Riêng số `71` của
`smart-ml`@MB **không xuất hiện một lần nào** trong bảng vote MB.

### 6.2 Model nào chỉ đốt token

| model | miền | số | trúng? | token | ghi chú |
|---|---|---|---|---|---|
| **`gemini-2.5-pro`** | MB | `16`,`46` | **0/2** | **26.784** | **NGOÀI roster** — lượt rò |
| `gemini-2.5-flash` | MN | `26`,`64` | 0/2 | 6.819 | CORE |
| `gpt-oss-120b` | MN | `26`,`42` | 0/2 | 3.020 | CORE |
| `claude-sonnet-4-6` | MN | `86`,`62` | 0/2 | — | CHALLENGER, verdict SKIP |

### 6.3 Ba câu bắt buộc

- **Direct LLM yếu ở MN/MB, ML cứu ở MT.** MN: 1/4 direct LLM có số trúng (`claude-opus-4-6`),
  3/4 trượt sạch. MT: toàn bộ 6 model ML/ensemble đều có ít nhất một số trúng. MB: `glm-5.1`
  (CHALLENGER) ra `93` **trúng** nhưng xếp **hạng 10 — bét bảng**, score 0,0246 = 26% điểm của số
  đứng đầu, đúng 1 voter.
- **CHALLENGER có diversity THẬT:** cả ba miền, CHALLENGER đóng góp **2/2 đuôi MỚI** mà không CORE
  nào đề xuất (6/6 số, 100%). Và 2/3 miền số mới đó **trúng**: MT `gpt-oss-120b`→`30`,
  MB `glm-5.1`→`93`. Nhưng **cả hai đều bị hệ thống dìm**: `30` bị AUTO-SKIP (strength<5,0),
  `93` xếp bét bảng. `RM-04`: n=3 miền/1 ngày, **chưa được phép kết luận** về giá trị khe
  CHALLENGER.
- **Coverage roster-4:** MN 7/8 ô là đuôi phân biệt (trùng `26`) · **MT 6/8 — co cụm nhất** (trùng
  `88` và `29`) · MB 7/8 (trùng `16`). Phủ so với đuôi thực tế: MN 2/42 = 4,8% · MT 2/31 = 6,5% ·
  MB 3/26 = 11,5%.

### 6.4 Phụ lục họ gốc — "4 model" không phải "4 quan sát độc lập"

Đo bằng `_v11188_family_lineage.py` (30/30):

| roster | số model | **số họ gốc độc lập** | **voter hiệu dụng (1/HHI)** | họ lớn nhất |
|---|---|---|---|---|
| **MN** | 4 | **3** | **2,67** | `ANTHROPIC_CLAUDE` 50% (`claude-opus-4-6` + `claude-sonnet-4-6`) |
| MT | 4 | 4 | 4,00 | — |
| MB | 4 | 4 | 4,00 | — |
| bundle 11 voter | 11 | 8 | 8,00 | `smart-ensemble`/`smart-ml` là DERIVED, `combo-super` là COMBO ⇒ không tính độc lập |

`model_registry` có `provider` nhưng **không có họ gốc**, và `provider` đánh lừa hai chiều:
`provider='openrouter'` gộp chung **16 họ gốc khác nhau**; còn `gpt-5.4` (openai) và `gpt-5.5`
(openrouter) **cùng một họ**.

---

## 7. GIẢI PHẪU TOTAL (§AC-H) — `MN_RANKER_MISS · MT_OFFICIAL_WIN · MB_RANKER_MISS`

### 7.1 Dựng lại điểm — khớp 100%, và công thức có một chỗ phải đính chính

Công thức **thật** đọc từ `main.py:9959–10004`:

```
score = effective_weight × strength_weight × verdict_weight × lane_weight × position_weight
```

⚠️ **`partial_bonus_shadow` CHỈ được ghi vào trace, KHÔNG nhân vào score.** `main.py:10004` là
`score = model_weight * position_weight`. Mô tả công thức ở các bản trước có thừa cấu phần này.

`generate_final_bundle` **byte-identical trước và sau deploy 20:05** (md5
`b2639f9f45ce8a20b634281d86ab2c1b`, 954 dòng) ⇒ đo đúng mã đã chạy (`RM-13`).
Dựng lại **khớp 100%** cả ba miền, 10/10 vị trí, 4 chữ số thập phân, khớp cả danh sách voters.

### 7.2 Bốn lớp override — CẢ BỐN KHÔNG ĐỔI SỐ

| miền | ranked[0] | BT cuối | V10640 | V10767 | V10789 | V10790 |
|---|---|---|---|---|---|---|
| MN | **24** | **24** | **CHẠY** → trả `24`, `specialist_votes=3 rank=1` → **không đổi** | không gọi | không gọi | không gọi |
| MT | **20** | **20** | disabled | không gọi | không gọi | `FLAG=False` |
| MB | **16** | **16** | disabled | `FLAG=False` | `FLAG=False` | không gọi |

Kiểm độc lập: **0 dòng** mang dấu `🎯 [V106xx/V107xx-OVERRIDE]` ngày 14/09, và `xien2[0] == bach_thu`
ở cả ba miền.

`main_selection_reason` (`main.py:10383`) **vẫn gán cứng vô điều kiện** sau cả bốn lớp. Ngày 14/09
giá trị lưu ra **tình cờ đúng** vì không lớp nào đổi số — **không** phải vì trường này đã lành.

### 7.3 🔴 LỚP THỨ NĂM — chưa từng được tài liệu hoá

`main_number_anti_trap` + `near_miss_anti_trap` (`main.py:10441+`) chạy **trong cùng hàm**
`generate_final_bundle`, **sau** bốn lớp trên. Bốn lớp override không phải danh sách vét cạn.

**Bạch thủ DUY NHẤT thắng trong ngày — MT `20` — bị chính lớp này gắn cờ `FULL_SPENT`.**

### 7.4 Nguyên nhân từng miền

| miền | nhãn | cơ chế đo được |
|---|---|---|
| **MN** | **`RANKER_MISS`** | Đuôi trúng `14` **không được model nào xếp vị trí 1** — cả 3 phiếu đều top2 (`pw=0,80`). `smart-ml` và `smart-ensemble` cùng ra đúng cặp `["24","14"]` theo đúng thứ tự đó; ranker chỉ tôn trọng thứ tự nội bộ của chính hai model ấy. **24 = 0,1362 vs 14 = 0,1350 — biên 0,0012** |
| **MT** | **`OFFICIAL_WIN`** | `ranked[0]=20` ∈ đuôi trúng. BT WIN · lô2 WIN · xiên2 WIN. *(kèm cờ `FULL_SPENT` ở §7.3)* |
| **MB** | **`RANKER_MISS`** | Đuôi trúng `31` là **số THỨ HAI của chính model đã đặt số thua `16` lên đầu** (`gemini-2.5-flash` → `["16","31"]`). 16 = 0,0945 (3 phiếu top1) vs 31 = 0,0415 (1 phiếu top2) |

**Loại trừ CÓ BẰNG CHỨNG, không suy đoán:** `GENERATOR_MISS` ✗ (pool cả ba miền **đều chứa** đuôi
trúng) · `OVERRIDE_HURT/HELPED` ✗ (bốn lớp no-op) · `SELECTOR_OR_GATE_MISS` ✗ (gate lọc **0 model**,
cap không kích hoạt, PP-1 **0 sự kiện**, PP-5 tắt cứng) · `OUTPUT_OR_SCORING_DEFECT` ✗.

### 7.5 Hai phản tưởng hấp dẫn — cả hai đều BỊ BÁC

| phản tưởng (chỉ dùng dữ liệu TRƯỚC kết quả) | MN | MT | MB |
|---|---|---|---|
| **Bỏ phiếu `combo-super`** (kênh mà lượt rò đi vào) | 24 giữ 0,1276 → **không đổi** | 20 giữ 0,0859 → **không đổi** | 16: 0,0945 → 0,0846, **vẫn #1** (31 chỉ 0,0415) |
| **Bỏ chiết khấu vị trí** (`pw` top2 = 1,0) | 24 → 0,1362 vs 14 → 0,1350 · **vẫn MISS** | vẫn WIN | 16 giữ 0,0945 vs 31 → 0,0477 · **vẫn MISS** |

⇒ **Lượt rò `gemini-2.5-pro`@MB KHÔNG phải nguyên nhân MB thua.** Nó góp `0,0099/0,0945 = 10,5%`
điểm của số `16`. Là lỗi quản trị thật, nhưng gán làm nguyên nhân thua hôm nay là **kết luận sai**.

### 7.6 Hit@K và MRR — tách riêng, trên `ranked` đầy đủ

| miền | vị trí trúng | **MRR** | @1 | @2 | @3 | @5 | @10 |
|---|---|---|---|---|---|---|---|
| MN | 2, 3, 6, 11, 12 | **0,5000** | 0/1 | 1/2 | 2/3 | 2/5 | 3/10 |
| MT | 1, 2, 3, 4, 7, 10 | **1,0000** | 1/1 | 2/2 | 3/3 | 4/5 | 6/10 |
| MB | 2, 3, 5, 6, 10, 17 | **0,5000** | 0/1 | 1/2 | 2/3 | 3/5 | 5/10 |

| K | thẻ sản phẩm | nền MN | nền MT | nền MB | quan sát (MN·MT·MB) |
|---|---|---|---|---|---|
| 1 | bạch thủ | 0,4200 | 0,3100 | 0,2600 | 0 · 1 · 0 |
| 2 | lô 2 số | 0,6661 | 0,5261 | 0,4543 | 1 · 1 · 1 |
| 3 | xiên 3 | 0,8092 | 0,6760 | 0,5991 | 1 · 1 · 1 |

Công thức **có hoàn lại** `1−(1−b)^K` (bị cấm) luôn cho số **thấp hơn** — MN K=3: 0,8049 thay vì
0,8092.

---

## 8. LƯỢT COMBO NGOÀI ROSTER (§AC-I) — `NO_OUTPUT_IMPACT_AS_RUN`

| | |
|---|---|
| lượt | `gemini-2.5-pro` @ MB, 17:33:07 → 17:33:43, latency **35,90 s**, **26.784 token** |
| trả về | `["16","46"]` — **0/2 trúng** (16 và 46 đều không thuộc 26 đuôi MB) |
| dòng `predictions` riêng | **0** — pha AI nội bộ của Combo **không bao giờ** được persist thành dòng model riêng |
| đổi ranking? | **không** |
| đổi bạch thủ? | **không** |

**Nhưng đường lan là CÓ THẬT và phải nói rõ.** Lượt rò **không mồ côi** — nó là **pha AI của chính
`combo-super`**, và `combo-super` là **một trong ba voter** của số top-1 `16` trong bundle MB
official. `predictions.analysis_text` id=30751 ghi thẳng:

```
dual_pool_v596.selected_ai = ["gemini-2.5-pro", "glm-5.1"]
ai_models      = {"gemini-2.5-pro": ["16","46"]}
weighted_scores= {"16": 0.802, "46": 0.599, "31": 0.2, ...}
model_win_rates= {"meta-learning": 13.1, "gemini-2.5-pro": 26.8}   dynamic_wr_used = true
```

⇒ Terminal đúng: **`NO_OUTPUT_IMPACT_AS_RUN` + `OUTPUT_CONTAMINATION_PATH_CONFIRMED`**. Hôm nay số
không đổi; **đường đi thì đã mở**. Đúng thứ bản vá §AB đóng.

**Nguyên nhân gốc, đọc từ bản mã CHẠY LÚC 17:33** (`backups/combo_super.py.pre_v11186`, vì bản hiện
tại có mtime 20:05 = sau khi chạy):

```
:1270  all_ai_ids = [m['id'] for m in AI_MODELS]     # 9 model, KHÔNG giao roster
:1291  allowed_models = [m for m, _ in all_sorted[:3]]
```

Pool vừa là *danh mục ứng viên* vừa là *quyền được gọi* ⇒ Combo gọi được model mà scheduler đã khoá.

**Chấm hồi cứu — KHÔNG phải bằng chứng predictive:** `gemini-2.5-pro`@MB 0/2 (nền `P(Hit@2)` MB =
45,43%); lượt Combo thứ hai `claude-opus-4-6`@MN 05:17:31 `["62","36"]` 31.121 token, 1/2 (nền MN =
66,61%). `RM-04`: n=1 lượt/miền ⇒ **chưa được phép kết luận**, theo cả hai chiều.

---

## 8b. HƯỚNG XỬ LÝ VÀ VÌ SAO CHỌN

**Chọn ĐO và ĐÓNG BĂNG, không chọn SỬA.** Ba lý do, theo thứ tự sức nặng:

1. **Lượt MN 05:15 cách thời điểm phân tích 3 giờ.** §AC-M cấm tường minh *"deploy thêm change vào
   official path trước MN"* và *"restart chỉ để cho chắc"*. Mọi thứ tìm được hôm nay — kể cả
   `EXPECTED_MODEL_COUNT` lệch và lớp anti-trap thứ năm — đều **không** khẩn tới mức đánh đổi
   epoch đầu tiên của §AB. Sửa bây giờ là phá đúng phép đo mà cả §AB sinh ra để có.
2. **Ba phát hiện mới đều là lỗi QUAN SÁT, không phải lỗi SINH SỐ.** Bundle vẫn sinh đúng hạn ba
   miền, status chấm đúng 100%, công thức khớp 100%. Không có gì đang chảy máu cần cầm ngay.
3. **Nguyên nhân thua đã truy được, và nó bác luôn phản xạ tự nhiên.** `RANKER_MISS` ở hai miền —
   không phải thiếu model, không phải lượt rò. Nếu sửa theo phản xạ (thêm model, chặn Combo, bỏ
   chiết khấu vị trí) thì phản tưởng cho thấy **không cái nào lật được ngày 14/09**.

**Vì sao vẫn code ba blocker §AC-O ngay trong phiên:** §AC-O cho phép tường minh
*"được code/test offline ngay"*. Ba module đứng độc lập, **không tệp nào lên VPS**, nên chúng không
chạm đường official. Làm sớm để khi cửa deploy mở (sau ba receipt 15/09) thì chỉ còn việc nối.

**Vì sao dùng bảy nhánh song song có agent phản biện riêng:** bốn con số sai đã **bị bắt** trước
khi vào báo cáo — "MN chỉ có một dòng WIN 2/2" (thật ra hai), "5 dòng SKIP" (thật ra 10), "OOM = 0"
(thật ra 2), "cost không khôi phục được" (khôi phục được). Không có lớp phản biện, cả bốn đã công bố.

---

## 9. MA TRẬN THAY ĐỔI (§AC-J)

| # | thay đổi | mục tiêu | static proof | runtime 14/09 | predictive impact | stability | **verdict** |
|---|---|---|---|---|---|---|---|
| 1 | §AA roster scheduler 8→4 | cắt lượt gọi ngoài roster ở scheduler | AST 0 tham chiếu | **12/12 lượt chuỗi chính đúng roster** | **N/A** | 3/3 bundle sinh đúng hạn | **`OPERATIONALLY_STABLE_ONE_DAY`** |
| 2 | Shadow pause 11→1 | `UNBOUNDED_SHADOW=0` | có | **0 lượt shadow** cả ba miền | N/A | ổn | `LIVE_PROVEN_ZERO` |
| 3 | Tắt `_v11059_lane_ab_3tang` | dừng lane không truy vết | có | 0 lượt | N/A | ổn | `LIVE_PROVEN_ZERO` |
| 4 | Provider quarantine | chặn model hỏng | 23/23 | **0 lượt model bị cách ly** | N/A | ổn | `LIVE_PROVEN_ZERO` |
| 5 | Deterministic no-retry | không thử lại lỗi tất định | có | **0 retry** | N/A | ổn | `LIVE_PROVEN_ZERO` |
| 6 | Optimizer C1+C2+C3 (QD-079) | cổng ghi weights | 15/15 | **chưa chạy lần nào** | N/A | — | **`DEPLOYED` — KHÔNG phải `RUNTIME_PROVEN`**; lượt đầu là CN 20/09 03:00 |
| 7 | Combo roster gate §AB | đóng bypass | 102/102 + 17/17 | **N/A — deploy 20:05, sau EOD** | N/A | — | `DEPLOYED_PENDING_NATURAL_PROOF` |
| 8 | Uỷ quyền dispatcher §AB | chặn tại điểm cuối | như trên | **N/A** | N/A | — | như trên |
| 9 | Request fingerprint/reuse | không gọi trùng | 11 bài | **N/A** | N/A | — | như trên |
| 10 | Cost normalization | không biến UNKNOWN thành 0 | có | **N/A** | N/A | — | như trên |
| 11 | Rollback CẤP 1 | có đường về | sha khớp 5/5 | không dùng tới | — | — | `EXISTS_AND_VERIFIED` |
| 12 | Emergency cap CẤP 2 + expiry | không giữ mãi | 45/45 | TẮT | — | — | `DEPLOYED_OFF_BY_DEFAULT` |
| 13 | Current weights | — | — | **không đổi** | — | — | `UNCHANGED` |
| 14 | TOTAL formula | — | — | **không đổi**, byte-identical | — | — | `UNCHANGED` |
| 15 | Prompt CORE | — | — | **không đổi** | — | — | `UNCHANGED` |

### 9.1 🔴 Lỗi chính xác của nén roster — KHÔNG phải chuyện output

`EXPECTED_MODEL_COUNT = len(get_output_eligible_ids())` = **15**, và danh sách 15 đó **vẫn còn**
`gemini-2.5-pro`, `deepseek-reasoner`, `gpt-5.4` — model **ngoài mọi roster hoặc đang bị cách ly**.

| ngày | MN | MT | MB |
|---|---|---|---|
| 03–11/09 (trước nén) | 14–15 | 12–13 | 15 |
| 12/09 | 14 | 12 | 14 |
| 13/09 | 14 | 12 | 13 |
| **14/09** (ngày đầy đủ đầu tiên dưới roster 4) | **11** | **11** | **11** |

`classify_bundle_quality(11)` = **`INCOMPLETE`** cho **cả ba miền**. Từ 14/09 trở đi **mọi bundle
đều bị xếp INCOMPLETE theo thiết kế**, vì ngưỡng hoàn chỉnh vẫn trỏ vào thế giới trước khi nén.
Sửa chính sách gọi mà không sửa ngưỡng — đúng lỗi §60 *"bỏ nửa chừng"*.

⇒ **`ROSTER_COMPRESSION_14SEP = OPERATIONALLY_DEGRADED_WITH_EXACT_FAILURE`**, hai lỗi chính xác:
(a) một lượt HTTP ngoài roster ở MB; (b) `EXPECTED_MODEL_COUNT` không được cập nhật sau 8→4.

⇒ **`ROSTER_COMPRESSION_PREDICTIVE_LIFT = NOT_PROVEN`.** Một ngày không cho phép nói gì về chất
lượng dự đoán, theo cả hai chiều.

---

## 10. TOKEN / COST THẬT 14/09 (§AC-L) — `ACTUAL_CALLS_AND_TOKENS_MEASURED`

Tính lại **từ trace thô**, và **xác nhận trùng từng chữ số** với V11187 sau khi một agent độc lập
chạy lại:

| | lượt HTTP | token |
|---|---|---|
| MN | 5 | 151.015 |
| MT | 4 | 113.756 |
| MB | 5 | 159.844 |
| **tổng** | **14** | **424.615** |

| tách nguồn | lượt | token |
|---|---|---|
| scheduler main chain | **12** | 366.710 |
| **Combo** | **2** | **57.905** |
| shadow · retry · denied · untraced | **0 · 0 · 0 · 0** | 0 |
| reused | 1 (Combo MT — **0 lượt gọi**) | 0 |

**Chênh 14 lượt gọi vs 12 dòng model AI trong `predictions`** = đúng 2 lượt Combo nội bộ, **không
phải** lỗ hổng ghi nhận: pha AI nội bộ của `combo-super` **theo thiết kế** không persist thành dòng
model riêng.

### COST

**`COST_14SEP = UNKNOWN cho 9 lượt · TÍNH LẠI ĐƯỢC cho 5 lượt OpenRouter`.**

- **0/14 dòng** trace có trường cost khác `None`. **Không được ghi 0.**
- 5 lượt qua OpenRouter **khôi phục được** vì `cost_est = round(tokens/1000 × cost_per_1k, 4)` là
  **hàm tất định** của token và bảng đơn giá: `gpt-oss-120b`@MN 26.939 tok → **$0,0269** ·
  `gpt-oss-120b`@MT 25.825 → **$0,0258** · `glm-5.1`@MT 28.742 → **$0,0086** · (+2 lượt còn lại).
- 9 lượt còn lại (Anthropic/Google trực tiếp) **`UNKNOWN`** — mã chuẩn hoá cost vừa deploy 20:05,
  số đo đầu tiên sẽ có từ 15/09.
- **`−74,7%` KHÔNG được dùng lại như số thật** — đó là ước lượng đã rút lại (`RL-047`).

**Baseline:** so 4 ngày Thứ Hai trước khi nén. Nếu chỉ tính tập **được phép** (5 model roster), nền
4 ngày = 15+17+12+13 lượt. Phần giảm phần lớn đến từ **13 model rời hẳn** (9 dừng hẳn + 4 cách ly),
không phải từ việc mỗi miền gọi ít đi.

---

## 11. PREFLIGHT 15/09 (§AC-M) — `V11186_FIRST_NATURAL_READY = YES`

`_v11188_preflight_natural.py`, **15/15**, chạy 02:12 ICT. **Không restart. Không deploy gì vào
official path.**

| phép | kết quả |
|---|---|
| M1 service + PID đúng bản deploy | `active` · **169960** · NRestarts 0 · từ 20:06:21 |
| M2 health | **200** |
| M3 sha 5 tệp = gói §AB | khớp cả 5 |
| M4 **không tệp nào ghi SAU khi service khởi động** | mọi tệp cũ hơn mốc 20:06:21 |
| M5 roster ba miền trong trần 4 | `token_call_roster/2026.09.14-1` · MN 4 · MT 4 · MB 4 |
| M6 cửa khẩn cấp CẤP 2 | **TẮT** |
| M7 uỷ quyền chặn đúng, không chặn oan | `DENY_OUTSIDE_ROSTER` · `ALLOW` · `DENY_QUARANTINED` · `DENY_INVALID_CONTEXT` |
| M8 Combo gate có mặt (AST, giải bí danh) | gọi tại `combo_super.py:1290` |
| M9 uỷ quyền dispatcher có mặt | gọi tại `gpt_analyzer.py:6807` |
| M10 bộ thu receipt 15/09 | PID **170282** sống |
| M11 không provider job đang bay | trace im **519 phút** |
| M12 scheduler đã xếp lịch 15/09 | 20 mốc |
| M13 đĩa / RAM | 23,82 GB · 2.863 MB khả dụng |
| M14 DB lành, chưa có bản ghi ngày mới | `quick_check=ok` · `predictions[2026-09-15]=0` |
| M15 trạng thái cách ly đọc được | 4 model |

🔴 **M8/M9 ban đầu báo CHẶN — và đó là FALSE BLOCKER của chính tôi.** Phép kiểm tìm lời gọi mang
đúng tên `get_token_call_roster`/`uy_quyen_goi`, trong khi mã thật import dưới **bí danh**
(`as _v11186_gtcr`, `as _uqg`). Tên trong nút `ast.Call` là bí danh, nên phép kiểm luôn trượt. Đã
sửa: **giải bí danh** trước khi tìm. Nếu tin bản đầu, tôi đã có thể kích hoạt **rollback vô cớ**
cho một cổng đang chạy đúng.

---

## 12. RECEIPT TỰ NHIÊN 15/09 (§AC-N) — CHƯA ĐẾN GIỜ

Thời điểm chốt báo cáo: **03:xx ICT 15/09**. Lượt MN chạy **05:15**. Bộ thu (PID 170282, chỉ đọc)
đã chờ sẵn cho **cả ba miền**, và sau mỗi miền sẽ chạy thêm `_v11187_quy_nguon_combo.py` để quy
nguồn bằng lồng thời gian.

`MN_V11186_NATURAL_OK/FAIL` · `MT_…` · `MB_…` — **chưa có miền nào**.
`ROSTER_SYSTEM_WIDE_LIVE_PROOF_OK` **chỉ được ghi ở EOD 15/09**, và **không được** dùng MN đại diện
ba miền.

---

## 13. BA BLOCKER CÓ THỂ ĐI TIẾP (§AC-O) — ĐÃ CODE + THỬ XONG OFFLINE

**Không tệp nào được đưa lên VPS. Không đổi đường official.**

| blocker | module | bài thử | terminal |
|---|---|---|---|
| Override lineage | `_v11188_override_lineage.py` | **23/23** | **`CODED_TESTED_STAGED`** |
| Family lineage | `_v11188_family_lineage.py` | **30/30** | **`CODED_TESTED_STAGED`** |
| Atomic retrain | `_v11188_atomic_retrain.py` | **42/42** | **`IN_PROGRESS_WITH_EXACT_MODULE`** |

**Override lineage** ghi vào **bảng riêng** `v11188_override_lineage`: `pre_override_ranked0` /
`_score` / `_topk`, `override_applied`, `override_rule_id`, `override_input_hash` (băm tất định),
**cả câu đã ghi lẫn câu thật**, `final_bach_thu`, `roster_version`, và `xien2_lech_bach_thu`.
Fail-safe tuyệt đối: mọi lỗi bị nuốt — lineage hỏng **không được** làm hỏng một lượt dự đoán. Ghi
lại cùng bundle **không đẻ dòng mới** ⇒ không backfill. `rule_id` tự bịa **bị từ chối**, không quy
về `NONE`.

**Atomic retrain** — blocker đã xác minh lại nguyên văn: `ml_models.py:27` · `lstm_model.py:29` ·
`meta_learner.py:48` dùng **một** hằng `MODEL_DIR` cho **cả save lẫn load**, và `_retrain_all.py`
chạy như **tiến trình con** nên phải truyền qua **môi trường**. Hợp đồng:
`LOTTERY_ML_WRITE_DIR` / `LOTTERY_ML_READ_DIR`; **không đặt biến ⇒ hành vi byte-identical hôm nay**.
Kích hoạt nguyên tử theo **đơn vị model × miền** (một model xgboost có **ba** tệp; thay lần lượt mà
sập giữa chừng sẽ để model mới đi với scaler cũ — **sai lặng lẽ, tệ hơn hỏng hẳn**): chép dưới hậu
tố `.dang_vao` → ghi **nhật ký** → `os.replace` từng tệp → xoá nhật ký. Nhật ký còn sót = lần trước
sập; `tu_sua()` dọn và **báo cáo**, **không tự gỡ về**.
**Hạn 19/09 23:00 còn nguyên.** Còn lại đúng: vá ba module + truyền env cho tiến trình con.

---

## 14. THEO DÕI TIẾP + PHÂN LOẠI TRACKER (§AC-Q)

`TRACKER_CLASSIFIED = 12 mục` · `CLOSED_OR_SUPERSEDED_BUT_INDEXED_WRONG:3` ·
`TECHNICALLY_EXECUTABLE_NOW:3` · `WAIT_LIVE:0` · `OWNER_DECISION_NEEDED:1` ·
`STALE_REQUIRES_REWRITE:3` · `BLOCKED_WITH_EXACT_DEPENDENCY:2`

### Việc MỚI sinh từ phiên này

| # | việc | hạn | terminal bắt buộc |
|---|---|---|---|
| 1 | **Receipt ba miền 15/09** (bộ thu PID 170282 đã chờ) | 15/09 EOD | `ROSTER_SYSTEM_WIDE_LIVE_PROOF_OK` hoặc `AUTO_ROLLBACK_WITH_EXACT_REASON` |
| 2 | **`EXPECTED_MODEL_COUNT` không khớp roster 4** ⇒ mọi bundle `INCOMPLETE` | **16/09** | `EXPECTED_COUNT_ALIGNED_WITH_ROSTER` hoặc `OWNER_DECISION_NEEDED` |
| 3 | **Lớp thứ NĂM `main_number_anti_trap`** chưa tài liệu hoá; BT thắng duy nhất bị gắn `FULL_SPENT` | **17/09** | `ANTI_TRAP_DOCUMENTED_AND_MEASURED` |
| 4 | `PRJ-SELECTION-WINDOW-001` mục 2 bị vi phạm **trong đường chọn đang chạy**: cohort roster "đặc sản" của V10640 gồm **41,7% dòng `shadow_auto_eval`** (MN 60 ngày: 941 `auto_daily` + 672 shadow) | **17/09** | `SELECTION_COHORT_CLEANED` hoặc `EXACT_BLOCKER` |
| 5 | Công bố cost THẬT sau 15/09 | 15/09 EOD | `COST = ACTUAL` |
| 6 | Vá ba module cho atomic retrain | **19/09 23:00** | `RETRAIN_ATOMIC_PATH = READY` |
| 7 | Nối override lineage + family lineage vào production (sau khi có full natural proof) | 20/09 | `LINEAGE_DEPLOYED_ZERO_OUTPUT_CHANGE` |
| 8 | Pure-context preregistration + activate | sau `ROSTER_SYSTEM_WIDE_LIVE_PROOF_OK` | `BOUNDED_SHADOW_PREREGISTERED` |
| 9 | Cổng `_v10921_report_gate` đọc dòng `#` trong khối code như tiêu đề | chưa đặt hạn | `GATE_HEADING_FALSE_POSITIVE_GHI_NHAN` |
| 10 | 39/264 bản thiếu báo cáo (tồn đọng lịch sử) | chưa đặt hạn | `A55_BACKLOG_GHI_NHAN` |

---

## 15. HẠ TẦNG P0 (§AC-R) — `EXACT_BLOCKER`, 5/13 blocker · 8/13 đạt

| # | mục | số thật | terminal |
|---|---|---|---|
| 1 | **Off-machine backup** | lần cuối **2026-04-17 — 150 ngày trước**. Hai tarball ở máy Windows local **chứa CÙNG MỘT ảnh chụp DB** (24.604.672 B, mtime trùng) ⇒ **một điểm khôi phục, không phải hai**. DB đang chạy 863.191.040 B ⇒ **97,15% khối lượng không có bản sao ngoài máy**. Không cron, không timer, không rclone/restic/borg | **`EXACT_BLOCKER`** |
| 2 | **Mất theo BẢNG, không chỉ theo dòng** | **233/257 bảng (90,7%) KHÔNG TỒN TẠI** trong backup, chiếm **482.418.688 B = 55,9%** tệp DB. Theo dòng: `predictions` 80,2% · `model_daily_eval` 80,3% · `final_bundles` 75,4% | **`EXACT_BLOCKER`** |
| 3 | **Restore proof** | Chưa từng thử trên VPS. **Nhưng thử được offline**: rút một thành viên bằng `tar --occurrence=1` (24,6 MB, 4 giây) → `integrity_check = ok`, `page_count 6007 × 4096 = 24.604.672` khớp kích thước. **Không còn là blocker "không thử được"** | `HA_XUONG_THUC_HIEN_DUOC` |
| 4 | **OOM** | **2 sự kiện ngày 2026-09-05** (00:19:09 và sau đó), *không phải 0*. Con số "0" trước đó là **artifact của journal xoay vòng** — journal chỉ giữ từ 2026-09-10 trong khi uptime từ 2026-04-18 | **`EXACT_BLOCKER`** |
| 5 | **SSH brute-force** | ~**25.246** lượt `Failed password` trong `auth.log` hiện hành | **`EXACT_BLOCKER`** |
| 6 | Mã nguồn | **CÓ** bản sao ngoài máy: `origin git@github.com:BaoBiTanPhat/Lottery_AI_Test.git` + cây local Windows | `DAT` |
| 7 | Đĩa / RAM / DB | 23,82 GB trống · 2.863 MB RAM khả dụng · DB 863 MB · WAL 0 | `DAT` |

**Câu đúng phải ghi:** *"**DỮ LIỆU** thời gian thực không có bản sao ngoài máy từ 18/04"* — **không**
phải "toàn hệ không có bản sao". Mã nguồn có. Ghi sai câu này là định cỡ sai vùng thiệt hại.

**Không dùng P0 hạ tầng để trì hoãn phân tích dự đoán** — mục này chỉ báo trạng thái. **Không tự
sửa SSH giữa live.**

---

## 16. CỔNG KIỂM VÀ ZERO-WRITE (§AC-S)

### Bộ thử

| bộ | kết quả |
|---|---|
| `_v11188_override_lineage.py` | **23/23** |
| `_v11188_family_lineage.py` | **30/30** |
| `_v11188_atomic_retrain.py` | **42/42** |
| `_v11188_preflight_natural.py` | **15/15** trên VPS |
| `_v11186_thu_ab.py` · `_v11186_thu_khan_cap.py` · `_v11187_thu_chan_su_co_mb.py` | 102/102 · 45/45 · 17/17 |
| `_v11185_thu_aa.py` · `_v11184_thu_z.py` | 45/45 · 65/65 |
| tự-kiểm roster · cách ly · retrain · intake | 32/32 · 23/23 · 16/16 · 19/19 |

### Zero-write

| | trước (02:11) | sau (02:26) |
|---|---|---|
| `predictions` · `final_bundles` · `lottery_results` · `model_daily_eval` | 14.965 · 597 · 15.483 · 14.829 | **y hệt** |
| crontab | `81efcf8de5c90c62`, 90 job | **y hệt** |
| service PID | 169960 | **y hệt** |
| WAL | 0 byte | 0 byte |

Toàn phiên **chỉ SELECT** và đọc tệp. **Không** ghi counterfactual, **không** sửa status lịch sử,
**không** bundle thay thế, **không** predictions tổng hợp, **không** replay vào bảng official.
Hai tệp đưa lên VPS (`_v11188_eod_ground_truth.py`, `_v11188_preflight_natural.py`) là **chỉ đọc**
và **không ai import** — đã kiểm bằng `grep -rln`.

---

## 16b. GỠ VỀ

**Phiên này KHÔNG có gì để gỡ về** — read-only, zero-write đã chứng minh ở §16. Không deploy,
không restart, không ghi DB. Ba module §AC-O nằm trong repo riêng và **không tệp nào lên VPS**.

**Gỡ về mã nguồn của phiên:** `git revert <commit V11188>` — chỉ bỏ ba module độc lập và hai script
chỉ đọc; không chạm production.

**Đường gỡ về của bản đang chạy (V11186/§AB) vẫn nguyên và đã xác minh:**

```bash
# CẤP 1 — mặc định, GIỮ trần 4. 5 tệp .pre_v11186 trên VPS, sha khớp bản trước deploy cả 5.
ssh root@14.225.224.89 'cd /root/Lottery_AI_Test
for f in combo_super.py gpt_analyzer.py scheduler.py main.py _v11185_roster_goi_token.py; do
  cp -p backups/$f.pre_v11186 web/backend/$f
done
systemctl restart lottery'
# CẢNH BÁO: V11185 là bản ĐÃ ĐƯỢC ĐO LÀ CÒN RÒ ở Combo (MB 14/09).

# CẤP 2 DISASTER — chỉ khi roster 4 không ra output VÀ ML-only cũng hỏng.
ssh root@14.225.224.89 'systemctl set-environment LOTTERY_ROSTER_KHAN_CAP=1 && systemctl restart lottery'
# Có hạn 24 h từ lần bật đầu tiên · hết hạn tự về trần 4 · ALERT stderr · viết sai biến => TỪ CHỐI mở.
```

```bash
python web/backend/_v11185_roster_goi_token.py --go-ve    # in đủ hai cấp + trạng thái hiện tại
python web/backend/_v11188_preflight_natural.py           # 15 phép READY/NO-GO
python web/backend/_v11188_atomic_retrain.py --ban-va     # bản vá ba module, STAGED
```

**Ngưỡng kích hoạt gỡ về trong ngày 15/09:** chỉ khi receipt tự nhiên cho `FAIL` **có nguyên nhân
thuộc §AB** (roster authorization sai · overblock · thiếu ngữ cảnh · duplicate). **Không** gỡ về vì
dự đoán thua — ngày 14/09 đã chứng minh nguyên nhân thua nằm ở **ranker**, không ở số lượng model.

---

## 17. MƯỜI CÂU OWNER HỎI — TRẢ LỜI DỨT ĐIỂM

1. **Ngày 14/09 thắng/thua cái gì?** Bạch thủ **1/3** (MT `20` WIN; MN `24`, MB `16` LOSE). Lô 2
   số: MT WIN, MN và MB PARTIAL — **4/6 số trúng**. Lô 3 càng **0/3**. Xiên 2: MT WIN, hai miền
   kia LOSE. Xiên 3 **0/3**, riêng MT là `LOSE_KHÁC_ĐÀI`.
2. **TOTAL sai ở đâu?** **Ở RANKER**, không phải generator. MN và MB `RANKER_MISS`; MT
   `OFFICIAL_WIN`. Pool cả ba miền **đều chứa** đuôi trúng.
3. **Model nào tạo giá trị, model nào chỉ đốt token?** Tạo giá trị: `claude-opus-4-6`@MN (WIN 2/2),
   `lstm`@MN, và ở MT gần như toàn bộ khối ML. Đốt token: `gemini-2.5-pro`@MB (26.784 token, 0/2,
   **ngoài roster**), `gemini-2.5-flash`@MN, `gpt-oss-120b`@MN, `claude-sonnet-4-6`@MN.
   **Hai dòng WIN 2/2 bị cổng chặn**: MT `smart-ensemble`, MB `smart-ml`.
4. **Lượt Combo ngoài roster có đổi output không?** **Không đổi** — bỏ phiếu `combo-super` thì
   `16` vẫn #1 ở MB. Nhưng **đường lan đã mở**: lượt đó là pha AI của `combo-super`, và
   `combo-super` là một trong ba voter của chính số `16`.
5. **Roster 8→4 có vận hành ổn định không?** **Không hoàn toàn.** Output sinh đủ và đúng hạn ba
   miền, nhưng có **hai lỗi chính xác**: một lượt HTTP ngoài roster ở MB, và
   `EXPECTED_MODEL_COUNT=15` không được cập nhật ⇒ **cả ba bundle bị xếp `INCOMPLETE`**.
6. **Có bằng chứng predictive tốt hơn không?** **KHÔNG.** `PREDICTIVE_LIFT = NOT_PROVEN`. n=1
   ngày, độ lệch chuẩn của một phép Bernoulli tại nền (0,49/0,46/0,44) lớn hơn mọi lệch quan sát.
7. **§AB mới deploy hay đã live-proven?** **Mới deploy.**
   `§AB_DEPLOYMENT = DEPLOYED_PENDING_NATURAL_PROOF`. Runtime 14/09 = **`NOT_APPLICABLE`**.
8. **Còn đúng những blocker nào?** Hạ tầng: backup off-machine 150 ngày · 233/257 bảng không có
   bản sao · 2 sự kiện OOM · 25.246 lượt SSH brute-force. Sản phẩm: `EXPECTED_MODEL_COUNT` lệch
   roster · lớp anti-trap thứ năm chưa tài liệu hoá · cohort V10640 lẫn 41,7% shadow ·
   `RETRAIN_ATOMIC_PATH` còn ba module · cost thật chưa có.
9. **Việc nào làm ngay mà không làm bẩn live 15/09?** Ba blocker §AC-O — **đã làm xong offline**
   (23/23 · 30/30 · 42/42), không tệp nào lên VPS.
10. **Một next action duy nhất?** **Thu natural receipt MN → MT → MB ngày 15/09.** Xem §19.

---

## 18. BA LỚP NGUỒN (§62)

| lớp | nội dung | bằng chứng |
|---|---|---|
| **`OWNER_SAID`** | §AC-A cấm trộn epoch · §AC-M cấm restart/deploy trước MN · §AC-O cho code offline · *"KHÔNG ĐƯỢC KẾT THÚC BẰNG «TIẾP TỤC THEO DÕI»"* | prompt §AC, 15/09 |
| **`CODE_DID`** | `score = eff × strength × verdict × lane × position` (`main.py:9959–10004`), `partial_bonus_shadow` **chỉ vào trace** · bốn override no-op 14/09 · lớp thứ năm `main.py:10441+` · `EXPECTED_MODEL_COUNT=15` (`database.py:5023`) vs `model_count=11` · Combo pool không giao roster (`combo_super.py.pre_v11186:1270`) | DB VPS `mode=ro` · `prediction_trace.jsonl` · `scraper.log` · md5 `b2639f9f45ce8a20b634281d86ab2c1b` |
| **`DOC_SAID`** | `CHANGELOG §V11188` · `docs/CURRENT_TRUTH_SSOT.md §V11188` · `REPORT_V11187.md` | `governance_seq` |

**Lệch giữa ba lớp — báo đủ:**
① `DOC_SAID` mô tả công thức TOTAL có `partial_bonus_shadow` **nhân vào score**; `CODE_DID` cho
thấy nó **chỉ ghi vào trace**. Đã đính chính ở §7.1.
② `DOC_SAID` liệt kê **bốn** lớp override; `CODE_DID` có **năm**. Đã báo ở §7.3.
③ `DOC_SAID` (QD-079) được đọc thành "đang thi hành"; `CODE_DID` cho thấy optimizer **chưa chạy
lần nào** kể từ khi vá — tầng đúng là `DEPLOYED`, không phải `RUNTIME_PROVEN` (`RM-12`).

---

## 19. NEXT ACTION DUY NHẤT (§AC-V)

EOD 14/09 **sạch** (không defect dữ liệu, không defect chấm điểm) và preflight V11186 **đạt 15/15**.
⇒ **Giữ nguyên production. KHÔNG restart. KHÔNG deploy.**

> **Một next action duy nhất: thu natural receipt MN → MT → MB ngày 15/09** (bộ thu chỉ đọc PID
> 170282 đã chờ sẵn cho cả ba miền).

- **Nếu ba receipt đạt:** chốt roster 4 thành last-known-good · kích hoạt bounded pure-context theo
  preregistration · hoàn thành override/family/retrain theo hạn.
- **Nếu thất bại:** phân loại `roster authorization / overblock / missing context / duplicate /
  provider / bundle / data` → repair hoặc rollback **CẤP 1**. **Không quay về 8 model chỉ vì dự
  đoán thua** — 14/09 đã chứng minh nguyên nhân thua nằm ở **ranker**, không ở số lượng model.

---

## 20. VƯỚNG VẤP

1. **False blocker của chính tôi (M8/M9).** Phép kiểm AST tìm theo tên gốc trong khi mã import
   dưới bí danh ⇒ báo "cổng không tồn tại" cho một cổng đang chạy đúng. Nếu tin, tôi đã kích hoạt
   rollback vô cớ. Đã sửa thành **giải bí danh**.
2. **Bảy nhánh forensic chạy song song đều bị một agent phản biện chạy lại truy vấn để bác bỏ — và
   phản biện bắt được lỗi thật ở CẢ BẢY.** Những chỗ bị lật đáng kể: "MN chỉ có một dòng WIN 2/2"
   (thật ra **hai**) · "24 gom ba phiếu cùng một họ" (**sai** — `smart-ensemble` = Meta + LSTM, không
   phải xgboost; khử trùng cả hai vế thì 24 vẫn thắng) · "5 dòng bị SKIP" (thật ra **10**, 7 trong
   đó có số trúng) · "OOM 30 ngày = 0" (thật ra **2**, con số 0 là artifact journal xoay vòng) ·
   "cost không khôi phục được" (**khôi phục được** cho 5 lượt OpenRouter).
3. **`grep -c '[COST]'` không thoát ngoặc** là **lớp ký tự regex**, khớp bất kỳ ký tự nào trong
   `COST` — một agent công bố số 0 từ lệnh đó; chạy lại đúng cách (`grep -cF`) mới ra số thật.
   Đúng họ `RM-09`, và nó lọt vào tận khâu công bố.
4. **Heredoc + quoting lồng qua `ssh` làm hỏng hai lệnh kiểm** (`'` bị nuốt, `no such column: ACTIVE`).
   Phải chuyển sang ghi script ra tệp rồi `scp`.
5. **`get_output_eligible_ids` không nằm trong `database.py`** — nó được import từ `model_registry`
   dưới bí danh `_goe`. Lại là `RM-10`, và lần này tôi mắc.

---

**TanPhatAI cần làm:** ghi ngày 14/09 là **`EOD_20260914_RESULT_DATA = COMPLETE_VALID`** với bạch
thủ **1/3** (MT WIN) và **`TOTAL_ROOT_CAUSE = MN_RANKER_MISS · MT_OFFICIAL_WIN · MB_RANKER_MISS`** —
**không** được ghi là generator miss; ghi **`ROGUE_COMBO_CALL_OUTPUT_IMPACT = NO_OUTPUT_IMPACT_AS_RUN`**
kèm **`OUTPUT_CONTAMINATION_PATH_CONFIRMED`**, hai vế đi cùng nhau; ghi
**`ROSTER_COMPRESSION_14SEP = OPERATIONALLY_DEGRADED_WITH_EXACT_FAILURE`** với **hai** lỗi chính xác
(lượt HTTP ngoài roster ở MB · `EXPECTED_MODEL_COUNT=15` không khớp roster 4 ⇒ cả ba bundle
`INCOMPLETE`); **giữ** `§AB_DEPLOYMENT = DEPLOYED_PENDING_NATURAL_PROOF` và **cấm** nâng thành
`ROSTER_SYSTEM_WIDE_LIVE_PROOF_OK` cho tới khi có đủ ba receipt ngày 15/09; ghi
**`COST_14SEP = UNKNOWN cho 9 lượt`**, **không** ghi 0 và **không** dùng lại `−74,7%`; ghi
**`TOKEN_14SEP = 14 lượt / 424.615 token`**; hạ **QD-079** về tầng **`DEPLOYED`** (chưa
`RUNTIME_PROVEN`, lượt chạy đầu là CN 20/09 03:00); thêm **lớp override thứ NĂM**
(`main_number_anti_trap`) vào sổ cơ chế; thêm **10 việc treo ở §14**; giữ `PREDICTIVE_LIFT=NOT_PROVEN`
· `POOL_VERDICT=HOLD` · `SC12=CLOSED`. **Code đi trước tài liệu** ở `_v11188_*`; mục sổ tương ứng là
`docs/SO_TUONG_TAC_OWNER.md` phiên 15/09/2026.
