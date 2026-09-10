# V11176 — RUNTIME PROOF TỰ NHIÊN · SC-12

> `SOURCE_TIMESTAMP` **2026-09-10 13:50 → 19:05 ICT** (06:50 → 12:05 UTC)
> `EVIDENCE_EPOCH` freeze **16:16:01** → thu bằng chứng **18:41–18:58** ICT
> `AUTHORITY` Prompt 43 R1 **§S** · `PLAN-20260723-lottery-doc-restructure`
> `PRODUCTION_MUTATIONS` **0** · `DB MUTATIONS (bởi phiên)` **0** · `DEPLOY/RESTART` **0**
> `SUPERSEDES` — · `ĐÍNH CHÍNH CHO` V11174 · V11175
>
> **Khung kép:** khung 9 phần §57.3 làm xương; 23 khối bắt buộc của §XII gắn nhãn tại chỗ.

---

## 1 · TÓM TẮT — EXECUTIVE VERDICT

# SC-12 LIVE PATH: `DEPLOYED_PENDING_CONSUMER_UI_PROOF`

```
SC12_CLASSIFIER_RUNTIME_PROVEN   ✅
SC12_BACKEND_CONSUMER_PROVEN     ✅
SC12_UI_CONSUMER_PARTIAL         ⚠️
SC12_HISTORICAL_REPAIR_PENDING   ⏸
PURE_CONTEXT_PARTIAL             ⏸
PREDICTIVE_LIFT = NOT_PROVEN     ⏸
```

**Lượt `auto_verify` chạy TỰ NHIÊN, ba miền, không một lệnh tay nào.** Cả ba khớp **đúng**
kỳ vọng đã niêm phong **trước** khi có output.

**Bằng chứng quyết định — cùng input, phán quyết đổi:**

```
2026-09-05 MT   completed=13  →  DEGRADED_LIVE_DAY / EXCLUDE_PRIMARY
2026-09-06 MT   completed=13  →  DEGRADED_LIVE_DAY / EXCLUDE_PRIMARY
2026-09-07 MT   completed=13  →  DEGRADED_LIVE_DAY / EXCLUDE_PRIMARY
2026-09-08 MT   completed=13  →  DEGRADED_LIVE_DAY / EXCLUDE_PRIMARY
2026-09-10 MT   completed=13  →  VALID_LIVE_DAY    / INCLUDE          ← BẢN VÁ SỐNG
```

**Chưa `SC12_LIVE_PATH_RUNTIME_PROVEN`** vì tầng UI vẫn rơi ngược về danh sách thô —
và hôm nay đo được **đúng ca kích hoạt** lỗi đó trên dữ liệu sống.

---

## 2 · OWNER YÊU CẦU GÌ — NGUYÊN VĂN + GIỜ

| giờ ICT | NGUYÊN VĂN | loại | agent đã làm gì | trạng thái |
|---|---|---|---|---|
| **10/09 ~13:45** | *«[CONTINUATION · PROMPT TỔNG LỰC LẦN 43 R1 · §S] [V11175 GOVERNANCE CLOSEOUT + PRE-SCHEDULED RUNTIME PROOF + NATURAL CONSUMER EVIDENCE]»* | `YÊU_CẦU` | §S0→§S2 ngay · §S1 xong trước 16:20 · freeze **16:16:01** · quan sát 16:37–18:34 · §S4–§S8 | `ĐÃ_LÀM` |

**Ràng buộc §S đã tôn trọng, kiểm được:**
*«KHÔNG tạo FU-451»* → append `FU_451_INVALID_REFERENCE`, **không** tạo mục ·
*«không manual `--do`»* → 0 lệnh tay, `classification_source = auto_verify` cho cả ba miền ·
*«không force MT thành INCLUDE»* → MT `INCLUDE` là **kết quả**, kỳ vọng niêm phong lúc 16:41:00
khi output còn `null`, ghi lúc 17:30:01 — **cách nhau 49 phút** ·
*«không backfill»* → `MT EXCLUDE_PRIMARY` vẫn **98** ·
*«không sửa 1e2b546/db989aa»* → chỉ append/đính chính minh bạch.

---

## 3 · ĐÀO BỚI / PHÁT HIỆN

### 3.1 · `§XII-3` EXACT REFS VÀ BRANCH CONTAINMENT (§S0)

| REPO | BRANCH | LOCAL_SHA | REMOTE_SHA | V11174 | V11175 | CANONICAL |
|---|---|---|---|---|---|---|
| `Lottery_AI_Test` (riêng) | `fu438/admin-only-p0a` | `374e634` → xem mục 8 | khớp | ✅ `1e2b546` | ✅ `45b6bf4` | **mang canon** |
| `Lottery_AI_Test` (riêng) | `master` = `origin/HEAD` | `a4d66364` | `a4d66364` | ❌ | ❌ | default theo cấu hình |
| `Lottery_AI_Notion_Reports` | `main` = `origin/HEAD` | `bd9cf1d` → xem mục 8 | khớp | ✅ `db989aa` | ✅ `9def0ea` | ✅ |

🔴 **`DEFAULT_BRANCH_STATE_CONFLICT`** — `master` đứng ở **V11123 (26/08/2026)**, sau `fu438`
**54 commit** (`ahead 54 · behind 0`, fast-forward được). **Cấu hình remote** nói `master` là
default; **bằng chứng** nói `fu438` mang canon. **Không tự merge, không force-push** — để owner
quyết (mục 9.3).

**Worktree — nhãn đúng, không nói «sạch»:** riêng `TRACKED_WORKTREE_DIRTY` (1 tệp tracked:
`docs/_I2_DA_CHAY.json`, do chính cổng báo cáo ghi vết) + **212 untracked, tất cả trong
`backups/`**. Công khai `TRACKED_WORKTREE_CLEAN` (0/0).

### 3.2 · `§XII-4` GOVERNANCE CLEANUP — PRE/POST (§S1)

| mục | TRƯỚC | SAU |
|---|---|---|
| `LATEST_REPORT.json` | `452 · V11174` | **`453 · V11175`** + đúng đường dẫn report/context |
| negative test nav | — | lệch ⇒ **thoát 1** · sinh lại ⇒ **thoát 0** *(thử trên dữ liệu thật)* |
| `irissnss` trong 5 tệp điều hướng | **361** | **0** · thử tải thật **http 200** |
| `CONTEXT_V11174:132` | *«digest `396c7559…` không đổi»* | rút tại **chính câu**, thay bằng `0c5f84f8…` |
| writer-idle | *«`-shm` tồn tại»* / *«`WAL size > 0`»* | **cả hai RÚT** (`RL-033`) → hợp đồng `ACTIVE_WRITER_PROOF` W1–W4 |
| `QD-074` | `kiem_code` là **chuỗi** ⇒ **làm chết cổng sổ quyết định** | list 3 phép · **khớp 3/3** trên module production |
| `FU-451` | 4 dòng HISTORY trỏ mã không tồn tại | `FU_451_INVALID_REFERENCE` **append-only** (chứng minh bằng khớp tiền tố byte) |
| cổng mã FU | **không có** | `PRJ-FU-REFERENCE-001` · thử chặn **8/8** · chứng minh **sẽ chặn từ V11170** |
| `_v11062 --thu-chan` | `CỔNG MÙ` · `QD-062` TRÔI | sửa **bộ thử** (chọn dòng chịu lực) ⇒ `ĐẠT` · `QD-062` **4/4** |
| sổ rút lại | 32 mục | **34** (`RL-033`, `RL-034`) |

### 3.3 · `§XII-5` PRE-REGISTERED EXPECTATION (§S2)

| miền | seal | giờ | input | kỳ vọng | output lúc seal |
|---|---|---|---|---|---|
| MN | #1 | 14:07:45 | `mc=14 cap=[] eff=14` | `EXCLUDE_PRIMARY` | `null` |
| **MN** | **#2 có hiệu lực** | **16:13:58** | `mc=15 cap=[] eff=15` | **`INCLUDE`** | `null` |
| **MT** | #1 có hiệu lực | **16:41:00** | `mc=13` **`cap=2`** `eff=15` | **`INCLUDE`** | `null` |
| **MB** | #1 có hiệu lực | **17:36:34** | `mc=15 cap=[] eff=15` | **`INCLUDE`** | `null` |

🔴 **Input MN KHÔNG đứng yên** — `mc` đổi **14 → 15** lúc **15:40:06**, đúng mốc `t10_chot` MN,
trong khi `created_at` **vẫn `05:26:43`**. Đây là **bằng chứng độc lập cho `RL-018`**:
`created_at` **không phải** dấu chốt.

Việc này lộ khiếm khuyết trong bộ lấy mẫu v2 của chính em — nó chỉ niêm phong **lần đầu** thấy
bundle, tức niêm phong trên **input chưa hoàn chỉnh**. Đã nâng lên **v3** (niêm phong lại mỗi khi
`INPUT_HASH` đổi) **trước** mốc freeze. **Cả hai seal đều giữ**, không lặng lẽ thay seal #1.

### 3.4 · `§XII-10` MỌI MISMATCH / KẾT QUẢ ÂM — ghi đủ

| # | phát hiện | phân loại |
|---|---|---|
| 1 | `forbidden surface` báo *«CÓ ĐỔI»* | 🟢 **BÁO ĐỘNG GIẢ do script của em** — `grep -c ... \|\| echo n/a` làm giá trị preimage thành `"0\nn/a"`. Đo lại: `output_counterfactual_rank` **0=0** (main.py) · **1=1** (database.py). `RM-09` |
| 2 | journal *«23 dòng lỗi»* | 🟢 **BÁO ĐỘNG GIẢ do mẫu của em** — **0 Traceback · 0 CRITICAL · 0 mức `ERROR` thật**. 22 dòng là `WARNING SCRAPE_FAIL` (scraper thử lại trước khi có kết quả); 11 dòng chứa chữ *«errors:»* nên khớp nhầm `-i ERROR`. `RM-09` |
| 3 | MT/MB **không có** dòng journal `[DAY-GOV]`/`[SCHEDULER]` | 🟡 **BẤT ĐỐI XỨNG LOG THẬT** — chỉ đường MN in hai dòng đó. DB `classification_source` mới là tín hiệu đáng tin. Nếu chỉ đọc journal sẽ **báo thiếu 2/3 miền** |
| 4 | MT row: `completed=13 · failed=0 · expected=15` | 🟡 **TỰ NÓ TRÔNG MÂU THUẪN** — `completed` giữ số **thô**, phần trần nằm trong `failed`. Đúng thiết kế nhưng dễ đọc nhầm |
| 5 | `/api/final-bundle` trả **401** | 🟡 endpoint admin có bảo vệ (tốt), nhưng ⇒ **không đọc payload trực tiếp được** trong epoch này |
| 6 | `RL-034` `dau_hieu` viết **không dấu** | 🔴 **lỗi của em** — cổng không bắt được chữ có dấu. Bổ sung (5→13) thì cổng lập tức bắt thêm **một chỗ thật** (`REPORT_V11174.md:211`) |
| 7 | tệp dry-run: `giu 532 + doi 49 = 581 ≠ tong 582` | 🔴 lỗi số học nội bộ, cùng gốc với đếm dư (mục 4.2) |

---

## 4 · HƯỚNG XỬ LÝ VÀ VÌ SAO CHỌN

### 4.1 · Vì sao KHÔNG tạo `FU-451`

Owner khoá *«không tạo FU mới»*; §63 luật 3 khoá `HISTORY` **chỉ APPEND**. Hai ràng buộc kẹp
nhau ⇒ đường duy nhất còn lại: **append một sự kiện khai tử**, giữ nguyên 4 dòng cũ làm dấu vết,
và ánh xạ công việc về **Prompt 43 R1 §R/§S + SC-12**, không về mã FU nào. Cổng mới chấp nhận
**đúng hai** đường hợp lệ: mã có thật trong sổ, **hoặc** đã khai tử đúng dạng.

### 4.2 · Vì sao `INDETERMINATE` được gỡ (§S7)

Đối chiếu **từng dòng** dry-run × tính lại độc lập trên DB:

```
dry-run 49 dòng · thật sự đổi 48 dòng · hiệu = {('2026-07-25','MT')}
chiều ngược («đổi thật nhưng thiếu trong dry-run») = RỖNG
phân rã đúng: 45 (đến 04/09) + 3 (05, 06, 08/09) = 48
```

Dòng thừa `25/07 MT` — **chính tệp dry-run** ghi `cu_status = moi_status` và
`cu_policy = moi_policy`, tức **không đổi gì**. ⇒ **«45» trong sổ ĐÚNG TỪ ĐẦU · `RL-014` ĐÚNG ·
«46» của V11174 mới là số sai.**

Hai ca từng ghi *«vắng mặt chưa rõ»* cũng đã truy ra: `07/09 MT` có **`cap=0`** (không phải ứng
viên); `09/09 MT` có `cap=2` nhưng `mc=12` ⇒ `eff=14 < 15` ⇒ vẫn `INCOMPLETE`.

**Bài học:** tiền đề *«không có script gốc để tái lập»* là **SAI** — chỉ cần đối chiếu từng dòng.
`INDETERMINATE` phải kèm **đã thử phép đo nào**, nếu không nó thành chỗ trú cho việc chưa đo đủ.

### 4.3 · Vì sao KHÔNG vá UI trong epoch này (§S6)

`du-doan.html` là **mặt official đang phục vụ**; vá nó trong/trước lượt tự nhiên sẽ **trộn evidence
epoch**. §S6 cấm tường minh. Đã làm **đặc tả chạy được** thay vì bản vá — mục 9.2.

---

## 5 · ĐÃ LÀM GÌ — BẰNG CHỨNG NĂM TẦNG

### 5.1 · `§XII-6` TẦNG 1 — SCHEDULER TỰ NHIÊN

```
classification_source = auto_verify   ← cho CẢ BA miền (trường máy đọc trong day_governance)
PID trong journal      = python3[3870722]  ← ĐÚNG PID dịch vụ production, không đổi
16:36:37  [SCHEDULER] 🔄 Bắt đầu auto-update MN cho ngày 2026-09-10
16:36:40  [DAY-GOV] MN 2026-09-10: VALID_LIVE_DAY | COMPLETE | 15/15 | eval=INCLUDE
17:30:00  Running job "Tự động cào MT + Dự đoán MB (17:30)"  → SCRAPE_OK MT 17:30:00.533
17:30:01  → day_governance MT được ghi
18:31:03  → day_governance MB được ghi
```

**0 lệnh tay.** Agent ở trạng thái freeze từ **16:16:01**, chỉ đọc.

### 5.2 · `§XII-7` TẦNG 2/3/4 — CLASSIFIER · WRITER · CONSUMER

| tầng | miền | input thật | output thật | khớp preregistration |
|---|---|---|---|---|
| **2+3** | MN | `mc=15 cap=[] eff=15` | `VALID_LIVE_DAY / INCLUDE` @16:36:37 | ✅ |
| **2+3** | **MT** | `mc=13` **`cap=['claude-opus-4-6','claude-sonnet-4-6']`** `eff=15` | `VALID_LIVE_DAY / INCLUDE` @17:30:01 | ✅ |
| **2+3** | MB | `mc=15 cap=[] eff=15` | `VALID_LIVE_DAY / INCLUDE` @18:31:03 | ✅ |

`day_governance` **581 → 584** (3 dòng mới, đúng 3 miền).

**`reason` ở nhánh `COMPLETE` — dòng mà gói VA-h12 gốc ĐÃ BỎ SÓT — nay chạy thật:**
> *«Đủ 15/15 model hợp lệ · **2 model bi TRAN CO Y (V10752), KHONG tinh la thieu**:
> claude-opus-4-6, claude-sonnet-4-6»*

**`§XII-8` TẦNG 4a — BACKEND CONSUMER: ĐÃ CHỨNG MINH.**
`daily_eval_log` **432 → 435**, ba dòng mới cho 10/09 (MB/MN/MT), `MAX(date) = 2026-09-10`.

**`§XII-9` TẦNG 4b — API: hàm production thật trên dữ liệu thật** *(endpoint trả 401 nên không
đọc payload trực tiếp; thay vì bịa, trích **nguyên văn** `_json_list_or_empty` và
`_quality_filtered_models_from_source_meta` từ chính `main.py` đang chạy — sha256
`d59a6ae9…` — rồi chạy trên `source_predictions_json` thật)*:

```
MT   wr_gate_filtered trong DB (THÔ) : ['claude-opus-4-6', 'claude-sonnet-4-6']
     model bị TRẦN CỐ Ý              : ['claude-opus-4-6', 'claude-sonnet-4-6']
     HÀM API trả về (sau VA-2′)      : []          ← sạch
MN / MB                              : [] → []
```

**`§XII-9` TẦNG 4c — UI: `CONSUMER_UI_PARTIAL`.** Ba điểm rơi ngược **vẫn nguyên**
(`du-doan.html:1354`, `:1438-1439`, `:1443-1444`). Và **MT hôm nay chính là ca kích hoạt**:
API trả `[]` (`FIELD_PRESENT_EMPTY`) trong khi `wr_gate_filtered` có **2** phần tử ⇒ điều kiện
`!length` thành đúng ⇒ **UI lấy lại đúng hai model bị trần và hiện chúng như «trượt quality»**.
**Không còn là suy đoán — đo được trên dữ liệu sống hôm nay.**

### 5.3 · `§XII-11` TẦNG 5 — AN TOÀN / NO-DRIFT

| mục | kết quả |
|---|---|
| digest **phạm vi khoá** | `0c5f84f8de9bbada94abe2b665dc53c5ab4044f07e64f2ebe796efff6278ffb2` · **582 dòng** · **KHỚP** |
| dòng từ 10/09 (tách riêng) | `860 MN 05:26:43 mc=15` · `861 MT 16:40:46 mc=13` · `862 MB 17:36:19 mc=15` — **tăng trưởng tự nhiên** |
| PID / NRestarts | `3870722` / **0** — **không đổi suốt phiên** |
| health | **200** |
| journal | **0 Traceback · 0 CRITICAL · 0 ERROR** · **0** Started/Stopping/Stopped ⇒ **không restart ngoài dự kiến** |
| `output_counterfactual_rank` | **0 dòng ghi bởi phiên** (cột, không phải bảng) |
| `MT EXCLUDE_PRIMARY` | **98 — KHÔNG ĐỔI** (backfill chưa chạy, đúng lệnh) |

**`§XII-12` FORBIDDEN SURFACE — đếm hiện tại × preimage:**
`ranked_numbers` 9=9 · `_CANONICAL_OUTPUT_MODELS` 3=3 · `run_combo_super` 2=2 ·
`save_final_bundle` 1=1 · `bach_thu =` 8=8 · `INTO final_bundles` 1=1 ·
`UPDATE final_bundles` 1=1 · `output_counterfactual_rank` 0=0 (main) · 1=1 (database).
**Không bề mặt cấm nào đổi.**

---

## 6 · CỔNG KIỂM — `§XII-13`

| cổng | kết quả |
|---|---|
| `_v10921_report_gate.py V11176` | xem mục 8 |
| `_v10921_report_gate.py` ① toàn dải | 🔴 **KHÔNG ĐẠT — 39/251** · nợ có sẵn (22 bản thiếu, tất cả ≤ V11087B) · **phiên này không xử** |
| `_v11062_nang_version.py --kiem` | **ĐẠT** |
| `_v11062_nang_version.py --thu-chan` | **ĐẠT** *(sau khi sửa bộ thử — trước đó báo `CỔNG MÙ`)* |
| `_v11085_cong_rut_lai.py` | **SẠCH** (34 mục) |
| `_v11085 --thu-chan` | **ĐẠT 10/10** |
| `_v11176_cong_ma_fu.py` | **`PRJ_FU_REFERENCE=SẠCH`** · 3 mã cảnh báo văn xuôi (`FU-214`, `FU-902`, `FU-999`) |
| `_v11176_cong_ma_fu.py --thu-chan` | **ĐẠT 8/8** |
| `_v11176_thu_va2p_ui.py` | **ĐẠT 8/8** *(đặc tả, không phải bản vá)* |
| `_v11088_cong_cua_so_chon.py` | **SẠCH** |
| `_v11027_so_muc_quan_tri.py` | **ĐẠT** |
| `_v11044_cong_so_hieu.py` | **KHỚP** |
| `_v11083_sinh_dieu_huong.py --thu` | **ĐẠT** + negative test hai chiều |
| `_v10920_decision_ledger.py` | **KHÔNG quyết định nào TRÔI** · `QD-074` **3/3** · `QD-062` **4/4** |
| — | ⛔ `QD-056` = **`KHÔNG_KẾT_LUẬN_ĐƯỢC`** 1/4 (RM-01, DB local cũ). **Không đọc thành TRÔI, cũng không thành ĐẠT.** Tồn đọng từ trước |

---

## 7 · VƯỚNG VẤP — BÀI HỌC

| # | vấp | ai bắt |
|---|---|---|
| 1 | 🔴 **`QD-074` của em sai schema và làm CHẾT cổng sổ quyết định** — 75/76 mục dùng `list[dict]`, riêng của em là chuỗi ⇒ probe ném `AttributeError` ⇒ cổng trả *«KHÔNG ĐO ĐƯỢC»*. Một cổng chết lặng vì một mục mới | cổng, khi chạy lại |
| 2 | 🔴 **Bộ lấy mẫu v2 niêm phong trên input CHƯA HOÀN CHỈNH** — MN `mc` đổi 14→15 lúc `t10_chot`. Nếu không phát hiện, «preregistration» đã sai đối tượng | snapshot B |
| 3 | 🔴 **`dau_hieu` của `RL-034` viết KHÔNG DẤU** ⇒ cổng rút lại mù với chữ có dấu | chính cổng, sau khi sửa |
| 4 | 🟠 **Hai báo động giả do đếm chuỗi thô của em** (`RM-09` lần thứ hai trong hai phiên): `\|\| echo n/a` làm hỏng phép so preimage; `-i ERROR` khớp chữ *«errors:»* trong dòng WARNING | tự kiểm khi thấy kết quả vô lý |
| 5 | 🟠 **Em ước lượng giờ thay vì đo** — báo «15:50» khi thực tế **14:37**. Sửa: đo bằng lệnh mỗi lần | tự phát hiện |
| 6 | 🟡 SSH rớt (255) nhiều lần vì `pkill -f 's2_mon'` **khớp chính shell của lệnh ssh** ⇒ tự giết mình | truy nguyên |
| 7 | 🟡 Heredoc mangling `\n` trong Python — đúng lỗi đã ghi trong bộ nhớ, vẫn tái phạm | assert của chính script |

**Bài học lớn nhất:** năm trong bảy vấp là **phép đo của em sai**, không phải hệ thống sai. Ba lần
suýt báo cáo một điều không có thật (forbidden-surface drift · 23 lỗi journal · «45» sai). Cách
duy nhất bắt được: **thấy kết quả vô lý thì đo lại có phân loại**, đừng chép con số ra báo cáo.

---

## 8 · GỠ VỀ — `§XII-14`

**KHÔNG có runtime mutation nào để gỡ.** Phiên này `PRODUCTION_MUTATIONS = 0` ·
`DB MUTATIONS (bởi phiên) = 0` · `DEPLOY/RESTART = 0`. Mọi thứ chạm VPS đều là **đọc**
(`sqlite3 mode=ro`, `journalctl`, `systemctl show`, `grep`) cộng một cây tạm trong `/tmp`.

Ba dòng `day_governance` mới **KHÔNG do agent ghi** — do `auto_verify` tự nhiên
(`classification_source = auto_verify`). Muốn hoàn nguyên: `evidence/v11174_day_governance_snapshot.json`
(581 dòng, ở thư mục báo cáo V11174).

**Sao lưu tài liệu trước khi sửa:** `backups/SO_RUT_LAI.json.pre_v11176` ·
`.pre_rl034` · `FOLLOW_UP_TRACKER.md.pre_v11174b` · `.pre_rl034` ·
`OWNER_DECISION_LEDGER.json.pre_v11176` · `SC12_RUNBOOK_V11173.md.pre_v11176` ·
`_v11062_nang_version.py.pre_v11176` · `00_PUBLIC_RAW_LINKS.md.pre_v11174b`.

**Artifact** (`evidence/`): `v11176_snapshot_A.json` · `v11176_snapshot_B.json` ·
`v11176_preregister_v3.json` · `v11176_evidence.json` · `v11176_mau_lay_mau.jsonl` (bộ lấy mẫu
45s/lần, 240 KB).

---

## 9 · THEO DÕI TIẾP

### 9.1 · `§XII-19` NỢ MỞ

| mức | nợ |
|---|---|
| 🔴 P1 | **UI fallback chưa vá** — `du-doan.html:1354,1438-1444`; đã có đặc tả + 8/8 test, **chưa deploy** |
| 🔴 P1 | **`SC12_HISTORICAL_REPAIR_PENDING`** — 48 dòng MT lịch sử vẫn `EXCLUDE_PRIMARY`, `MT EXCLUDE_PRIMARY = 98` |
| 🔴 P1 | **`DEFAULT_BRANCH_STATE_CONFLICT`** — `master` sau `fu438` 54 commit |
| 🔴 P1 | **R6 · R7 · R8 vẫn `NOT_PERFORMED`** |
| P1 | cổng báo cáo toàn dải **39/251 KHÔNG ĐẠT** |
| P2 | `evaluate_all_history` = **`ISOLATED_NOT_REPAIRED`** — *«0 cron/0 route»* **không phải** kết luận ngữ nghĩa vĩnh viễn |
| P2 | nhánh `fb.status != 'ACTIVE'` **vẫn chưa có dữ liệu thật đi qua** (583/583 `ACTIVE`) |
| P2 | **bất đối xứng log** — chỉ đường MN in `[DAY-GOV]`/`[SCHEDULER]`; MT/MB không |
| P2 | `completed_model_count` giữ số thô ⇒ dòng `13/15 · failed=0` **tự nó trông mâu thuẫn** |
| P2 | `--out` của installer không ghi số test và **ghi đè** artifact cũ |
| P2 | snapshot `daily_eval_log` (1,8 MB) vẫn chỉ trên VPS |
| P3 | 3 mã FU chỉ nằm trong văn xuôi: `FU-214`, `FU-902`, `FU-999` |
| ⛔ | `QD-056` `KHÔNG_KẾT_LUẬN_ĐƯỢC` (RM-01) |

### 9.2 · `§XII-20` VIỆC KẾ TIẾP CHÍNH XÁC

> **Vá UI theo đúng đặc tả `web/backend/_v11176_thu_va2p_ui.py`** (8/8 đã đạt):
> phân biệt `FIELD_ABSENT` với `FIELD_PRESENT_EMPTY`; chỉ fallback khi trường **thật sự vắng**;
> `quality_filtered_model_count` tính từ danh sách canonical.
> Deploy **ở một safe window MỚI**, có pre/post hash · rollback · consumer proof riêng —
> **KHÔNG** trong epoch này. Ánh xạ về **Prompt 43 R1 §S9**, **không mở FU, không mở Plan**.

### 9.3 · CHẶN Ở OWNER — đúng một việc

> **`DEFAULT_BRANCH_STATE_CONFLICT`.** `origin/HEAD → master` = `a4d66364` = **V11123 (26/08)**;
> toàn bộ V11124–V11176 chỉ nằm trên `fu438/admin-only-p0a` (**ahead 54, behind 0**).
> Người mở kho theo đường mặc định sẽ thấy một kho **lạc hậu 15 ngày**.
> **Owner chọn:** **(a)** fast-forward `master` về `fu438`; **(b)** đổi default branch sang
> `fu438/admin-only-p0a`; hoặc **(c)** giữ nguyên có chủ ý và ghi rõ vào tài liệu.
> Em **không tự merge, không force-push**.

### 9.4 · `§XII-15..18` TRẠNG THÁI TÁCH DÒNG

`SC12_LIVE_PATH_STATUS` = **`DEPLOYED_PENDING_CONSUMER_UI_PROOF`**
`SC12_HISTORICAL_STATUS` = **`SC12_HISTORICAL_REPAIR_PENDING`**
`PURE_CONTEXT_STATUS` = **`PURE_CONTEXT_PARTIAL`**
`PREDICTIVE_LIFT_STATUS` = **`NOT_PROVEN`** — SC-12 chỉ sửa **phép đo**; kết luận V11170
*«hệ không hơn ngẫu nhiên»* **vẫn đứng nguyên**.

---

## §62 — NGUỒN BA LỚP · `§XII-21`

### `OWNER_SAID`
> *«[CONTINUATION · §S] … Không manual `--do` de gia lap scheduled proof … Khong force MT 10/09
> thanh INCLUDE … KHONG tao FU-451 … Khong tu merge/force-push … Khong to hong»* — 10/09 ~13:45 ICT.

### `CODE_DID`
- `day_governance` 10/09: cả ba miền `classification_source = **auto_verify**`,
  `classified_at` 16:36:37 / 17:30:01 / 18:31:03.
- journal `python3[**3870722**]` — đúng PID dịch vụ; `[DAY-GOV] MN … eval=INCLUDE` @16:36:40.
- `main.py` sha256 `d59a6ae9…` — hàm API trích từ chính tệp này trả `[]` cho MT.
- `du-doan.html:1354/1438/1439/1443/1444` — **5 điểm rơi ngược còn nguyên**.
- `final_bundles` 583 dòng; digest phạm vi khoá `0c5f84f8…` trên 582 dòng — **khớp**.
- `grep -c 'FU-451' docs/FOLLOW_UP_TRACKER.md` → **0**; HISTORY `theo_doi` → **4**.

### `DOC_SAID`
- `FOLLOW_UP_TRACKER` (bản V11175) — *«replay 45 dòng là SAI»* → **bản rút lại đó SAI**, đã sửa (`RL-034`).
- `REPORT_V11174` — *«49 = 46 + 3, `INDETERMINATE`»* → **đã rút**, đúng là **48 = 45 + 3**.
- `docs/SC12_RUNBOOK_V11173.md` mục 4.3 — nay mang hợp đồng `ACTIVE_WRITER_PROOF`.

**LỆCH BA LỚP:**
1. `OWNER_SAID` = `CODE_DID`: *«không manual»* — `classification_source = auto_verify` cho **cả ba**.
2. `DOC_SAID` ≠ `CODE_DID` **đã đảo chiều**: sổ ghi **45**, đo lại đúng cách cũng **45**.
   Chỗ lệch là **phép đếm của agent**, không phải giữa hai lớp nguồn.
3. `CODE_DID` ≠ `CODE_DID` (**trong cùng một hệ**): API trả `[]` trong khi UI hiện 2 model —
   đó chính là `CONSUMER_UI_PARTIAL`.

---

TanPhatAI cần làm: ghi **`V11176`** — `governance_seq 491`, công khai bản này cùng `CONVERSATION_CONTEXT_V11176_20260910.md`. Ghi **BỐN DÒNG TRẠNG THÁI RIÊNG, CẤM GỘP**: `SC12_LIVE_PATH_STATUS = DEPLOYED_PENDING_CONSUMER_UI_PROOF` · `SC12_HISTORICAL_STATUS = SC12_HISTORICAL_REPAIR_PENDING` · `PURE_CONTEXT_STATUS = PURE_CONTEXT_PARTIAL` · `PREDICTIVE_LIFT_STATUS = NOT_PROVEN`. Ghi **lượt `auto_verify` chạy TỰ NHIÊN cho cả ba miền, `classification_source = auto_verify`, 0 lệnh tay**, agent freeze từ **16:16:01**. Ghi **BẰNG CHỨNG QUYẾT ĐỊNH: cùng `completed=13`, MT ngày 05–08/09 đều `EXCLUDE_PRIMARY`, ngày 10/09 ra `INCLUDE`** — bản vá sống trong production. Ghi **kỳ vọng NIÊM PHONG TRƯỚC OUTPUT**: MT seal **16:41:00** (`mc=13 cap=2 eff=15` → `INCLUDE`), output ghi **17:30:01** — **cách 49 phút**, `TRUOC_KHI_CO_OUTPUT: true`. Ghi **`reason` nhánh `COMPLETE` — dòng VA-h12 gốc BỎ SÓT — nay chạy thật**: *«Đủ 15/15 model hợp lệ · 2 model bi TRAN CO Y (V10752), KHONG tinh la thieu»*. Ghi **backend consumer ĐÃ CHỨNG MINH**: `daily_eval_log` **432 → 435**, `MAX(date) = 2026-09-10`. Ghi **API: endpoint trả 401 nên không đọc payload trực tiếp; thay vì bịa, trích NGUYÊN VĂN hàm từ `main.py` đang chạy (`d59a6ae9…`) và chạy trên dữ liệu thật → MT trả `[]` trong khi DB thô có 2 model**. Ghi **`CONSUMER_UI_PARTIAL` — MT hôm nay CHÍNH LÀ ca kích hoạt lỗi**: API `[]` + `wr_gate_filtered` 2 phần tử ⇒ `du-doan.html:1438` rơi ngược ⇒ **UI hiện đúng hai model bị trần như «trượt quality»**; **KHÔNG vá** vì ngoài phạm vi và sẽ trộn evidence epoch. Ghi **no-drift**: digest phạm vi khoá `0c5f84f8…` trên **582 dòng KHỚP**; ba dòng 10/09 là **tăng trưởng tự nhiên**; **0 bề mặt cấm nào đổi**; PID `3870722` NRestarts **0**, health 200, **0 Traceback/CRITICAL/ERROR**, **0 restart**. Ghi **`MT EXCLUDE_PRIMARY` vẫn 98 — backfill CHƯA chạy, đúng lệnh**. Ghi **§S7 GỠ `INDETERMINATE`: đúng 48 = 45 + 3; dòng thừa là `25/07 MT` mà chính dry-run ghi `cu_status = moi_status`; «45» trong sổ ĐÚNG TỪ ĐẦU; `RL-014` ĐÚNG; bản rút lại mà agent viết ở V11175 là bản rút lại SAI, nay rút lại chính nó (`RL-034`)**. Ghi **`FU-451` KHÔNG được tạo** — append `FU_451_INVALID_REFERENCE`, giữ 4 dòng HISTORY, ánh xạ về §R/§S + SC-12. Ghi **cổng mới `PRJ-FU-REFERENCE-001` (8/8) sẽ chặn từ V11170**. Ghi **CHẶN Ở OWNER: `DEFAULT_BRANCH_STATE_CONFLICT`** — `master` ở **V11123**, sau `fu438` **54 commit**; owner chọn (a) fast-forward, (b) đổi default branch, hay (c) giữ nguyên có chủ ý. Ghi **bảy vấp, năm trong đó là PHÉP ĐO CỦA AGENT SAI** — hai báo động giả (`RM-09` lần hai), `QD-074` sai schema làm chết cổng, niêm phong trên input chưa hoàn chỉnh, `dau_hieu` không dấu. **Không mở Prompt 44. Không mở Plan mới. Không mở FU mới. Không trộn ERP. Notion KHÔNG cập nhật trong lượt này.**

---

## 🔴 ĐÍNH CHÍNH APPEND-ONLY — V11178 §U13-1 (11/09/2026)

**Ba row ID ở mục 5.3 bị CHÉP SAI.** Bản gốc ghi `860 / 861 / 862`; **ID thật là
`860 / 862 / 864`**.

```sql
SELECT id,date,region,status,created_at,model_count
  FROM final_bundles WHERE date>='2026-09-10' ORDER BY id;
-- 860 | 2026-09-10 | MN | ACTIVE | 05:26:43 | 15
-- 862 | 2026-09-10 | MT | ACTIVE | 16:40:46 | 13
-- 864 | 2026-09-10 | MB | ACTIVE | 17:36:19 | 15
```

**Tệp `evidence/v11176_evidence.json` kèm theo bản này GHI ĐÚNG từ đầu**
(`T5_no_drift.rows_tu_10_09` = `860 / 862 / 864`). ⇒ Lỗi nằm ở **văn bản báo cáo**, không nằm ở
dữ liệu hay ở phép đo. Mọi trường khác (`date`, `region`, `status`, `created_at`,
`model_count`) đều đúng.

**Kết luận không bị lật:** ba dòng này vẫn là **tăng trưởng tự nhiên** và vẫn nằm **ngoài** phạm
vi digest khoá (`date ≤ 2026-09-09`) — điều đó dựa vào `date`, không dựa vào giá trị ID. `RL-036`.

*Bản gốc phía trên giữ nguyên, không xoá.*
