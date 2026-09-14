# REPORT V11187 — DEPLOY GÓI §AB · ĐÓNG COMBO ROSTER BYPASS SAU MỘT PHẢN CHỨNG SỐNG

> **Phiên:** 14/09/2026, tiếp §AB · **Mã đọc §58:** `DP1409` · **Prompt:** 43 R1 §AB
> **Khoá giữ nguyên:** `SC12=CLOSED` · `PREDICTIVE_LIFT=NOT_PROVEN` · `POOL_VERDICT=HOLD` ·
> `MATERIALIZATION_OPTION=B` · `F1`–`F5` `RETIRED` · TOTAL formula và current weights **không đổi**

---

## 1. TÓM TẮT — EXECUTIVE TERMINAL

Ngày 14/09 chạy trọn dưới V11185 và **để lại một phản chứng sống**: `gemini-2.5-pro`, model
**ngoài roster MB**, chạm HTTP 200 lúc **17:33:43**. Nguồn đã quy được là **Combo Super** — đúng
chỗ §AB chỉ ra và đúng chỗ bản vá đã staged từ trưa. Gói §AB **đã deploy** lúc 20:05, sau khi
epoch 14/09 khép trọn.

| terminal | kết quả |
|---|---|
| `ROSTER_SYSTEM_WIDE_LIVE_PROOF` (ngày **14/09**, dưới V11185) | **`FAIL`** — MN `OK` 10/10 · MT `OK` 10/10 · **MB `FAIL` 8/10** |
| `MODEL_OUTSIDE_ROSTER_HTTP_CALLS` (14/09) | **`MB_NONZERO_LIVE_PROVEN`** — `gemini-2.5-pro` ×1 |
| `COMBO_ROSTER_BYPASS` | **`ROOT_CAUSE_CONFIRMED_AND_DEPLOYED`** |
| nguồn lượt vi phạm | **`COMBO_SUPER`**, mức **`QUY_DUOC_BANG_LONG_THOI_GIAN`** (≠ `QUY_DUOC_BANG_TRUONG_CALLER`) |
| gói §AB | **`DEPLOYED_PENDING_NATURAL_PROOF`** — PID `97754` → `169960` |
| `EPOCH_SPLIT` | **`KHONG`** — 14/09 trọn ngày V11185 · 15/09 trọn ngày V11186 |
| 4 bảng khoá · crontab | **`UNCHANGED`** — `14965/597/15483/14829` · `81efcf8de5c90c62` 90 job |
| `ROLLBACK_CAP_1` | **`EXISTS_AND_VERIFIED`** — 5 tệp, sha khớp bản trước deploy |
| `ROLLBACK_CAP_2` | **`BOUNDED_WITH_ALERT`** — hạn 24 h, hết hạn tự về trần 4 |
| `TOKEN_REDUCTION` | **`NOT_YET_MEASURED`** — cost vẫn trắng 3/3 miền ngày 14/09 |
| `COST_OBSERVABILITY` | **`CODE_DEPLOYED_PENDING_FIRST_MEASUREMENT`** |
| `OVERRIDE_LINEAGE` · `FAMILY_LINEAGE` · `RETRAIN_SAFETY` | **`EXACT_BLOCKER`** (20/09 · 20/09 · **19/09 23:00**) |
| `PURE_CONTEXT` | **`DEFERRED_PENDING_ROSTER_LIVE_PROOF`** · `ZERO_TOKEN_SPENT` |
| `TOTAL_FORMULA` · `CURRENT_WEIGHTS` | **`UNCHANGED`** |

**Điều KHÔNG được đọc sai:** deploy **không** phải chứng minh. Terminal đúng là
`DEPLOYED_PENDING_NATURAL_PROOF`. `ROSTER_SYSTEM_WIDE_LIVE_PROOF_OK` chỉ được ghi sau **ba lượt
tự nhiên ngày 15/09**.

---

## 2. OWNER YÊU CẦU GÌ (nguyên văn) — §62 lớp `OWNER_SAID`

Không có yêu cầu mới trong phiên này. Bản deploy thi hành đúng hai câu Owner đã khoá ở §AB:

> *"Nếu không hoàn tất trước 03:30: giữ một epoch V11185 cho trọn ngày 14/09; **next action duy
> nhất là thu actual Combo call receipt; deploy bản hoàn chỉnh sau EOD**; không mở nhánh công
> việc khác."* (§AB-V)
>
> *"Nếu không đạt trước 03:30: không deploy patch nửa vời; không thay code giữa MN/MT/MB; giữ
> V11185 cho toàn ngày 14/09... **Cấm: deploy giữa cascade; MN một version, MT/MB version khác;
> restart khi provider job đang chạy; backdate config; ép xanh để kịp giờ.**"* (§AB-J)

Và câu chi phối toàn phiên:

> *"Biến roster từ một danh sách chỉ lọc khi bỏ phiếu thành một chính sách được thi hành ngay
> trước mọi HTTP provider call."*

§AB-U cấm kết thúc kiểu cũ, trong đó có *"«AST sạch nên live sạch»"* · *"«ước lượng token giảm»
viết thành số thật"* · *"«MN pass» viết thành ba miền pass"* · *"static proof viết thành runtime
proof"*. Báo cáo này giữ đủ: MB **FAIL** được ghi là FAIL; `TOKEN_REDUCTION` vẫn
`NOT_YET_MEASURED`; deploy vẫn là `DEPLOYED_PENDING_NATURAL_PROOF`.

**Điều Owner yêu cầu mà phiên CỐ Ý không làm:** override lineage · family lineage · retrain
atomic — §AB-U: *"Nếu P0 chưa đóng: không mở việc nghiên cứu khác"*; pure-context — §AB-Q chỉ
activate **sau** `ROSTER_SYSTEM_WIDE_LIVE_PROOF_OK`, mà hôm nay là `FAIL`.

---

## 3. ĐÀO BỚI / PHÁT HIỆN

### 3.1 Receipt ba miền 14/09 — thu từ lượt TỰ NHIÊN, không gọi provider tay (§AB-K)

| miền | thu lúc | terminal | ngoài roster | cách ly | model chạm HTTP | bundle | token | cost |
|---|---|---|---|---|---|---|---|---|
| MN | 12:53 | `OK` **10/10** | 0 | 0 | 4 | ACTIVE | 151.015 | **0/5 dòng** |
| MT | 16:47 | `OK` **10/10** | 0 | 0 | 4 | `bach_thu=20` | 113.756 | **0/4 dòng** |
| **MB** | 17:36 | **`FAIL` 8/10** | **`gemini-2.5-pro` ×1** | 0 | **5 (> trần 4)** | `bach_thu=16` | 159.844 | **0/5 dòng** |

Hai phép MB trượt: *"outside-roster HTTP = 0"* và *"số model duy nhất chạm HTTP ≤ 4"*. Tám phép
còn lại đạt: 0 cách ly · 0 dòng sau cutoff 17:58 · bundle sinh được · 0 `TOKEN_ROSTER_INVALID` ·
0 ERROR/CRITICAL · 0 traceback · health 200 · roster đọc được.

### 3.2 Truy nguồn — bốn bước, mỗi bước loại một giả thuyết

| bước | đã đào gì | kết quả |
|---|---|---|
| 1 | Dump 5 dòng trace MB | `gemini-2.5-pro` 17:33:43, `runtime_prompt_chars` **22.933** trong khi 4 model roster đều **24.7k–25.0k** |
| 2 | So bộ khoá trace hai dòng | **giống hệt** ⇒ cùng đi qua `analyze_and_predict`, không phải một đường lạ |
| 3 | Nghi Combo, tìm dòng in `UNIFIED`/`Selected` | **không có dòng nào** trong journal lẫn mọi `*.log` ⇒ **giả thuyết chưa được xác nhận**, không ép |
| 4 | Đổi sang nguồn độc lập: `scheduler_logs` mốc Combo | **chứa trọn** — xem 3.3 |

Hai giả thuyết đã **bị loại bằng dữ liệu**, không bằng suy đoán:

- **MB post-MT rerun** (`scheduler.py:5930`): vòng lặp này ghi `🔄 V9.3b MB AI: … re-predicting`
  qua `_add_log`. `scheduler_logs` ngày 14/09 **không có dòng nào** như thế ⇒ vòng rerun **không
  chạy**.
- **Diversity pass** (`scheduler.py:4898`): đã dùng `_AA_MODELS` từ §AA ⇒ không thể chọn model
  ngoài roster.

### 3.3 Lồng thời gian — bằng chứng quy nguồn

`scheduler_logs.log_time` là **naive và là UTC** (§55) ⇒ cộng 7 giờ. Combo Super là bước **cuối
cùng** của `_run_ai_models_predict` (`scheduler.py:5114`, *"COMBO SUPER (cuối cùng, sau 5 AI
models + diversity pass)"*).

| miền | cửa sổ Combo Super | lượt nằm trọn trong cửa sổ | ngoài roster? |
|---|---|---|---|
| MN | 05:16:35 → 05:17:32 (**57 s**) | `claude-opus-4-6` 05:16:37→05:17:31 | không — **may, không phải nhờ cổng** |
| MT | 16:43:58 → 16:44:02 (**4 s**) | không có | — |
| MB | 17:33:05 → 17:33:43 (**38 s**) | **`gemini-2.5-pro` 17:33:07→17:33:43** | **CÓ** |

Bốn lượt chuỗi chính mỗi miền khởi động **trong vòng 1–2 giây của nhau** (song song); hai lượt
Combo khởi động **sau khi chuỗi chính kết thúc**. Không lượt nào chờm cửa sổ.

Bằng chứng ngoại vi thứ hai, **độc lập với DB** — `scraper.log` 14/09:

```
17:30:24  AFC is enabled …                 <- client Google #1 (chuỗi chính)
17:31:10  POST … gemini-2.5-flash  200 OK
17:33:07  AFC is enabled …                 <- client Google #2, KHỞI TẠO RIÊNG
17:33:43  POST … gemini-2.5-pro    200 OK
17:33:44  Job "Tự động cào MT + Dự đoán MB (17:30)" executed successfully
```

**Mức bằng chứng ghi đúng tầng:** `QUY_DUOC_BANG_LONG_THOI_GIAN`, **không phải**
`QUY_DUOC_BANG_TRUONG_CALLER`. Lồng thời gian là bằng chứng ngoại vi rất mạnh nhưng vẫn là ngoại
vi. Dứt điểm chỉ có từ 15/09, khi mỗi lượt mang `caller` + `execution_class` +
`request_fingerprint`. Tái lập: `evidence/_v11187_quy_nguon_combo.py`.

### 3.4 Đối chiếu mã — pool Combo trên bản ĐANG CHẠY lúc đó

`combo_super.py` V11185, `AI_MODELS` **9 model**, trong đó `gemini-2.5-pro` và
`deepseek-reasoner` không thuộc roster miền nào hoặc đang bị cách ly. Chọn top-3 theo win-rate
(`:1286`–`:1302`) **không qua roster**. Đây đúng là cấu trúc §AB-D nhắm.

### 3.5 Ba điều phép đo này đổi

1. **`MODEL_OUTSIDE_ROSTER_HTTP_CALLS` KHÔNG phải ZERO toàn hệ thống.** Việc `RL-044` hạ xuống
   `STATIC_SCHEDULER_PROOF_ONLY` là **đúng**; nếu vẫn giữ `ZERO` thì hôm nay đã là một lời nói
   dối có bằng chứng ngược.
2. **§AA đóng đúng đường nó nhắm, và chỉ đường đó.** Cả **12** lượt chuỗi chính ở ba miền đều
   trong roster.
3. **"MN sạch" là may.** Combo ở MN cũng gọi ngoài kiểm soát, chỉ tình cờ bốc trúng
   `claude-opus-4-6` vốn trong roster MN. Cùng lỗ hổng, khác kết quả.

---

## 4. HƯỚNG XỬ LÝ VÀ VÌ SAO CHỌN

**Chọn DEPLOY, không chọn gỡ về.** Ba lý do, theo thứ tự sức nặng:

1. **Lỗi thuộc về bản đang chạy, không phải bản vá.** `combo_super.py` của **V11185** là nơi
   sinh lỗi. Bản vá §AB-D giao pool với roster **trước khi chấm điểm** và đóng fallback
   `else AI_MODELS`.
2. **Gỡ về làm nặng thêm.** CẤP 2 đưa ngược về hành vi trước §AA — **8 model**, tức mở rộng đúng
   thứ vừa đo được là đang rò.
3. **Bản vá đã được thử ngược trên chính sự cố thật**, 17/17 — xem §6.

**Vì sao 20:05 chứ không phải 13:00 hay 03:00:** §AB-J cấm chẻ epoch. MN đã chạy 05:17 dưới
V11185; deploy trước 17:33 sẽ làm MB chạy bản khác MN/MT trong cùng ngày. 20:05 là sau khi cả ba
bundle ACTIVE, sau khi kết quả MB về (~18:31) và các job settle 19:00 xong, và trace đã im
**151 phút**.

**Vì sao không chờ tới 15/09:** mỗi ngày chờ là thêm một ngày Combo có thể bốc trúng model ngoài
roster. Hôm nay nó đã bốc trúng một lần.

---

## 5. ĐÃ LÀM GÌ

| # | việc | bằng chứng |
|---|---|---|
| 1 | Thu receipt MN/MT/MB từ lượt **tự nhiên** | `evidence/ROSTER_RECEIPTS.jsonl` · 0 lượt gọi provider tay |
| 2 | Truy nguồn lượt vi phạm về Combo Super | `evidence/QUY_NGUON_COMBO_20260914.txt` |
| 3 | Thử ngược bản vá trên **chính sự cố thật** | `evidence/THU_CHAN_SU_CO_MB_20260914.txt` — **17/17** |
| 4 | Lập backup CẤP 1 trên VPS (5 tệp) | sha256 đối chiếu bản đang chạy: **khớp cả 5** |
| 5 | CẤP 2 có hạn 24 h + ALERT stderr | `_v11186_thu_khan_cap.py` **45/45** |
| 6 | Preflight 7 phép, chạy thật hai lần | 13:46 **NO_GO** (C1/C2/C4) → 20:05 **GO** cả bảy |
| 7 | Chép 8 tệp lên VPS, đối chiếu sha từng tệp | khớp cả 8, `CR=0` |
| 8 | Chạy bộ thử **trên VPS trước khi restart** | §6 |
| 9 | Restart, so PID | **97754 → 169960**, NRestarts 0, health 200 |
| 10 | Xác minh sau restart | 0 traceback · 4 bảng khoá y nguyên · crontab không đổi · `/monitoring`=401 |
| 11 | Đặt bộ thu receipt ba miền cho 15/09 | PID **170282**, truy vấn đã thử trên dữ liệu thật |
| 12 | Bốn mặt quản trị | `governance_seq → 502`, cổng `NANG_VERSION_V11062=ĐẠT` |

Tệp đã deploy: `combo_super.py` · `gpt_analyzer.py` · `scheduler.py` · `main.py` ·
`_v11185_roster_goi_token.py` · `_v11186_thu_ab.py` · `_v11186_thu_khan_cap.py` ·
`_v11187_thu_chan_su_co_mb.py`.

---

## 6. CỔNG KIỂM

**Trên VPS, trên mã đã chép, TRƯỚC khi restart:**

| bộ thử | kết quả |
|---|---|
| `_v11186_thu_ab.py` | **102/102** |
| `_v11186_thu_khan_cap.py` (§AB-L) | **45/45** |
| `_v11187_thu_chan_su_co_mb.py` (thử ngược sự cố thật) | **17/17** |
| `_v11185_thu_aa.py` | **45/45** |
| `_v11184_thu_z.py` | **65/65** |
| tự-kiểm `_v11185_roster_goi_token` · `_v11184_cach_ly_provider` · `_v11184_retrain_an_toan` · `_v11184_intake_model` | **32/32** · **23/23** · **16/16** · **19/19** |

**Thử ngược sự cố thật** — mạnh hơn bài thử tổng hợp vì nó dựng lại **đúng lượt đã xảy ra trong
sản xuất**:

| phép | kết quả |
|---|---|
| `uy_quyen_goi('gemini-2.5-pro','MB','combo_super')` | **`DENY_OUTSIDE_ROSTER`** |
| lý do là *ngoài roster*, không phải *cách ly* | ✓ |
| pool Combo 9 model ∩ roster MB | **4 model**, không còn `gemini-2.5-pro`, **không rỗng** |
| lượt Combo @MN (`claude-opus-4-6`, trong roster) | vẫn **`ALLOW`** |
| cả 4 model chuỗi chính MB | vẫn **`ALLOW`** |
| model bị cách ly | **`DENY_QUARANTINED`** |
| thiếu `target_region`/`execution_class` | **`DENY_INVALID_CONTEXT`** (§AB-E3) |

**Sau restart, trên VPS:**

| phép | kết quả |
|---|---|
| journal 3 phút | **0** dòng traceback/CRITICAL/ImportError |
| `/api/health` · `/monitoring` | **200** · **401** |
| 4 bảng khoá | `14965 / 597 / 15483 / 14829` — **khớp từng con số** với ảnh chụp preflight |
| crontab | `81efcf8de5c90c62`, **90 job** — không đổi |
| `gemini-2.5-pro` @MB và @MN lớp `combo_super` | **`DENY_OUTSIDE_ROSTER`** |
| cửa khẩn cấp CẤP 2 | **TẮT mặc định** |

**Cổng dự án:** `NANG_VERSION_V11062=ĐẠT` · `SO_HIEU_V11044=KHỚP` ·
`_v10921_report_gate` (toàn dải + bản này).

---

## 7. VƯỚNG VẤP

1. **Tôi suýt ép một giả thuyết đúng bằng bằng chứng sai.** Nghi Combo từ sớm và đi tìm dòng in
   `UNIFIED`/`🏆 Selected` của nó. **Không có dòng nào** — trong journal lẫn mọi `*.log`. Nếu coi
   "không tìm thấy" là "đã loại", tôi đã bỏ qua thủ phạm đúng. Phải đổi sang một nguồn khác
   (`scheduler_logs` mốc Combo) mới quy được. *Vắng bằng chứng không phải bằng chứng vắng mặt.*
2. **Dấu vân tay prompt tôi tưởng là mạnh, hoá ra yếu.** Lượt rogue có `runtime_prompt_chars`
   22.933 so với 24,7k–25,0k của bốn model roster, và tôi đọc thành *"đường dựng prompt khác"*.
   So bộ khoá trace hai dòng thì **giống hệt** — cùng `analyze_and_predict` — và chênh lệch giải
   thích được bằng `selected_source_prizes` (4 prize vs 5). Đã hạ nó xuống đúng vai: gợi ý, không
   phải bằng chứng.
3. **RM-10 chặn hai lần trong phiên.** `scheduler_logs` **không có cột `status`** (chỉ
   `id/log_time/log_level/message/job_name/region/date_str`) — tín hiệu "job đang bay" phải lấy
   từ độ im lặng của trace. `predictions` **không có cột `model_name`** (là `ai_model`). Cả hai
   đều bị bắt **trước khi** viết kết luận.
4. **§55 suýt làm sai toàn bộ phép lồng thời gian.** `scheduler_logs.log_time` naive **là UTC**;
   đọc thẳng sẽ lệch 7 giờ và mọi cửa sổ Combo sẽ trượt khỏi mọi lượt gọi.
5. **Lệnh kiểm sau deploy của tôi vỡ vì quoting** (`grep -vcE` lồng trong ssh). Ba phép đầu đã in
   ra đúng nên không mất gì; làm lại bằng script trên máy đích thay vì inline.
6. **Endpoint admin tôi đoán là `/api/admin/stats` — trả 404.** Nó không tồn tại. Phép smoke đúng
   là `/monitoring` = **401**. Lại là RM-10, lần này ở tên endpoint.

---

## 8. GỠ VỀ

**CẤP 1 — mặc định, GIỮ trần 4** (5 tệp đã lập và đối chiếu sha **trước** deploy):

```bash
ssh root@14.225.224.89 'cd /root/Lottery_AI_Test
for f in combo_super.py gpt_analyzer.py scheduler.py main.py _v11185_roster_goi_token.py; do
  cp -p backups/$f.pre_v11186 web/backend/$f
done
systemctl restart lottery'
# -> về V11185: roster 4 GIỮ · shadow bounded GIỮ · cách ly GIỮ · KHÔNG biến môi trường nào
# CẢNH BÁO: V11185 là bản ĐÃ ĐƯỢC ĐO LÀ CÒN RÒ ở Combo (MB 14/09). Chỉ dùng khi V11186 hỏng nặng hơn.
```

| tệp `.pre_v11186` | sha256 (16) |
|---|---|
| `combo_super.py` | `47047b1dc0b7e0b9` |
| `gpt_analyzer.py` | `20f3bb5305ad13d2` |
| `scheduler.py` | `732e302a57e299fb` |
| `main.py` | `d59a6ae94f9c3666` |
| `_v11185_roster_goi_token.py` | `294ec64572e5cd9d` |

**CẤP 2 DISASTER — CHỈ khi roster 4 không ra output VÀ ML-only cũng hỏng:**

```bash
ssh root@14.225.224.89 'systemctl set-environment LOTTERY_ROSTER_KHAN_CAP=1 && systemctl restart lottery'
```

| | |
|---|---|
| hạn mặc định | **24 giờ**, đo từ **lần bật đầu tiên** (`data/roster_khan_cap.json`) ⇒ restart **không** reset đồng hồ |
| đổi hạn | `LOTTERY_ROSTER_KHAN_CAP_GIO=<số giờ>` hoặc `LOTTERY_ROSTER_KHAN_CAP_HET_HAN=<ISO>` |
| viết sai hai biến trên | **TỪ CHỐI mở cửa** (§AB-E3) |
| hết hạn | **tự động về roster bình thường (trần 4)**, *không* fail-closed |
| cờ còn bật sau hạn | chạy bình thường **nhưng** để lại `canh_bao_khan_cap` + **ALERT stderr** |
| tắt | `systemctl unset-environment LOTTERY_ROSTER_KHAN_CAP && systemctl restart lottery` |

```bash
python web/backend/_v11185_roster_goi_token.py --go-ve    # in đủ hai cấp + trạng thái hiện tại
python web/backend/_v11186_thu_khan_cap.py                # 45/45 — RM-15
python web/backend/_v11187_preflight_deploy.py            # 7 phép GO/NO-GO
```

**Gỡ về mã nguồn:** `git revert 0a8d7f6 0ea1439 9de5afc` (V11186a · V11186b · V11186e).

---

## 9. THEO DÕI TIẾP

| # | việc | hạn | terminal bắt buộc |
|---|---|---|---|
| 1 | **Receipt ba miền 15/09 dưới V11186** (bộ thu PID 170282 đã chạy) | 15/09 EOD | `ROSTER_SYSTEM_WIDE_LIVE_PROOF_OK` **hoặc** `AUTO_ROLLBACK_WITH_EXACT_REASON` |
| 2 | Xác nhận `caller`/`execution_class`/`fingerprint` **có mặt** trong trace 15/09 ⇒ nâng `QUY_DUOC_BANG_LONG_THOI_GIAN` → `QUY_DUOC_BANG_TRUONG_CALLER` | 15/09 EOD | `ATTRIBUTION_BY_CALLER_FIELD_OK` |
| 3 | Công bố token/cost **THẬT** (cost 14/09 trắng 3/3 miền) | 15/09 EOD | `TOKEN_REDUCTION = ACTUAL_MEASURED` |
| 4 | Kiểm Combo ở ba miền 15/09 **có bị chặn đúng** và **không bị chặn oan** (pha AI của Combo vẫn ra output) | 15/09 EOD | `COMBO_GATED_NO_OVERBLOCK` |
| 5 | Override lineage (additive, bundle mới) | 20/09 | `CORRECT_FOR_NEW_BUNDLES` hoặc `STAGED_NOT_DEPLOYED_WITH_REASON` |
| 6 | Family lineage observability | 20/09 | `OBSERVABILITY_FIXED_NO_SCORING_CHANGE` |
| 7 | Retrain atomic candidate path | **19/09 23:00** | `ATOMIC_..._READY` hoặc `RETRAIN_ABORTED_FAIL_CLOSED_WITH_EXACT_MODULE` |
| 8 | Pure-context preregistration + activate | sau `ROSTER_SYSTEM_WIDE_LIVE_PROOF_OK` | `BOUNDED_SHADOW_PREREGISTERED` |
| 9 | **Cổng `_v10921_report_gate` đọc dòng `#` trong khối code như tiêu đề** ⇒ có thể báo đủ 9 phần cho báo cáo thật sự thiếu | chưa đặt hạn — **không mở FU mới** theo khoá §AB | `GATE_HEADING_FALSE_POSITIVE_GHI_NHAN` |
| 10 | 39/263 bản thiếu báo cáo (tồn đọng lịch sử, **không** sinh từ phiên này) | chưa đặt hạn | `A55_BACKLOG_GHI_NHAN` |

---

## 10. BA LỚP NGUỒN (§62)

| lớp | nội dung | bằng chứng |
|---|---|---|
| **`OWNER_SAID`** | §AB-V: *"next action duy nhất là thu actual Combo call receipt; deploy bản hoàn chỉnh sau EOD; không mở nhánh công việc khác"* · §AB-J: *"Cấm: deploy giữa cascade; MN một version, MT/MB version khác; restart khi provider job đang chạy"* | prompt §AB, 14/09 |
| **`CODE_DID`** | Combo Super gọi `gemini-2.5-pro` @MB 17:33:07→17:33:43 (`scheduler.py:5114` → `combo_super.py:1134`); pool `AI_MODELS` 9 model chọn top-3 theo WR không qua roster (`combo_super.py:1286`–`:1302`); §AA đã gate diversity pass (`:4898`) và chuỗi chính (`:4708`) | `prediction_trace.jsonl` · `scheduler_logs` · `scraper.log` · PID `97754`→`169960` |
| **`DOC_SAID`** | `docs/CURRENT_TRUTH_SSOT.md §V11187` · `CHANGELOG.md §V11187` · `REPORT_V11186.md §4c` | `governance_seq=502` |

**Lệch giữa ba lớp — báo đủ:** `DOC_SAID` của **V11185** từng ghi
`MODEL_OUTSIDE_ROSTER_HTTP_CALLS = ZERO` trong khi `CODE_DID` ngày 14/09 cho **1 lượt ngoài
roster ở MB**. Lệch này đã được rút lại ở `RL-044` **trước khi** phép đo hôm nay xác nhận —
tức bản rút lại là đúng, và đúng sớm hơn bằng chứng.

---

## 11. KHÔNG ÁP DỤNG

- **§52 (panel UI)** — không tạo bảng shadow mới, không đụng `/monitoring`.
- **Notion** — chỉ đọc (§57.1). Gói delta ở `NOTION_SYNC_DELTA_PACKET.md`; **không tự tuyên bố
  Notion đã sync**.
- **Thay đổi thuật toán** — không đụng TOTAL formula · current weights · bốn override ·
  prompt CORE · 3-càng · bộ chọn top-N của Combo (chỉ thu hẹp **đầu vào** của nó).

---

**TanPhatAI cần làm:** ghi ngày 14/09 là **`ROSTER_SYSTEM_WIDE_LIVE_PROOF_FAIL`** (MN/MT `OK`,
**MB `FAIL`**) và **cấm ghi `MODEL_OUTSIDE_ROSTER_HTTP_CALLS = ZERO`** dưới mọi dạng cho ngày đó —
đã có phản chứng sống; ghi gói §AB là **`DEPLOYED_PENDING_NATURAL_PROOF`**, PID `169960`,
**không** được nâng thành `ROSTER_SYSTEM_WIDE_LIVE_PROOF_OK` cho tới khi có ba receipt tự nhiên
ngày 15/09; ghi nguồn lượt vi phạm là **Combo Super** ở mức **`QUY_DUOC_BANG_LONG_THOI_GIAN`**,
**không** phải bằng trường `caller`; **đừng** ghi `TOKEN_REDUCTION` bằng bất kỳ con số nào —
vẫn `NOT_YET_MEASURED`, cost trắng 3/3 miền; giữ ba mục `EXACT_BLOCKER` (override lineage 20/09 ·
family lineage 20/09 · retrain atomic **19/09 23:00**); giữ `PURE_CONTEXT = DEFERRED`;
giữ `SC12=CLOSED` · `PREDICTIVE_LIFT=NOT_PROVEN` · `POOL_VERDICT=HOLD`. **Code đi trước tài liệu**
ở `_v11187_*`; mục sổ tương ứng là `docs/SO_TUONG_TAC_OWNER.md` phiên 14/09/2026.
