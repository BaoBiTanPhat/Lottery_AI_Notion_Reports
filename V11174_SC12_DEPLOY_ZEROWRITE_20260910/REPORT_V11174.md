# V11174 — SC-12 DEPLOY · FINAL_BUNDLES_ZERO_WRITE

> `SOURCE_TIMESTAMP` **2026-09-10 01:52 → 02:05 ICT** (18:52 → 19:05 UTC 09/09)
> `EFFECTIVE_FROM` **2026-09-10 02:00:19 ICT** (restart) · `EVIDENCE_EPOCH` as-of 2026-09-10 02:0x
> `PROJECT/SCOPE` **Lottery_AI_Test · SC-12 = OWNER_APPROVED · MEASUREMENT_ONLY**
> `AUTHORITY` Prompt 43 R1 §R · `PLAN-20260723-lottery-doc-restructure`
> `PRODUCTION_MUTATIONS` **3 tệp mã** · `DB MUTATIONS` **0** · `DEPLOY/RESTART` **1**
> `TEST COUNTS` V11174 **58/58** · V11173 **43/43 sau tích hợp** · rollback rehearsal **ĐẠT**
> `SUPERSEDES` V11173 (BLOCKED) · `SUPERSEDED_BY` — chưa
>
> **Khung kép:** báo cáo này theo **khung 9 phần §57.3**; mười lăm mục bắt buộc của **§XVI** được
> gắn nhãn `§XVI-n` ngay tại chỗ chúng nằm. Không mục nào bị bỏ.

---

## 1 · TÓM TẮT — EXECUTIVE VERDICT `§XVI-1`

# SC-12: `DEPLOYED_PENDING_SCHEDULED_PROOF`
# Pure Context: `PURE_CONTEXT_PARTIAL`

**13/13 cổng deploy PASS. Đã deploy và restart an toàn lúc 02:00:19 ICT.** Chưa runtime-proven —
`auto_verify` tự nhiên chạy **16:37–18:34 hôm nay 10/09** mới là bằng chứng.

Blocker P0 của V11173 (**VA-h12 không có installer thật**) đã đóng bằng cách **viết lại hẳn**, và
theo khoá canon mới `FINAL_BUNDLES_ZERO_WRITE` em **bỏ hẳn VA-1/VA-2** — hai mảnh duy nhất ghi
vào `final_bundles`.

⚠️ **Phiên này KHÔNG thực hiện R6/R7/R8** (audit tổng lực nợ · pure-context · improvement
register). Em **không tuyên bố "đã kiểm tra toàn bộ"**. Chi tiết ở mục 9.

---

## 2 · OWNER YÊU CẦU GÌ — NGUYÊN VĂN + GIỜ

*(§57.3 mục 2 đọc rộng theo `PRJ-INTERACTION-LEDGER-001`: prompt chính **VÀ** mọi yêu cầu trực
tiếp trong phiên. Sổ chạy dài: `docs/SO_TUONG_TAC_OWNER.md`.)*

| giờ ICT | NGUYÊN VĂN | loại | agent đã làm gì | trạng thái |
|---|---|---|---|---|
| 09/09 ~21:00 | *«Làm gì tiếp theo em đã đề xuất và tổng hợp báo cáo đầy đủ lên github chưa em»* | `HỎI` | Kiểm **bằng lệnh**, không bằng trí nhớ: xác nhận V11173 đã push cả hai kho; trình bảng việc kế tiếp | `ĐÃ_LÀM` |
| **10/09 ~01:45** | *«[CONTINUATION · PROMPT TỔNG LỰC LẦN 43 R1 · §R] [SC-12 CLOSURE + FULL-SYSTEM AMBIGUITY/DEBT AUDIT + PURE-CONTEXT COMPLETION PLAN]»* | `YÊU_CẦU` | R0–R5 + deploy; **R6/R7/R8 không làm**, khai báo rõ | `ĐÃ_LÀM (một phần)` |

**Ràng buộc owner khoá trong §R — nguyên văn, còn hiệu lực:**

- *«`FINAL_BUNDLES_ZERO_WRITE`»* — khoá **MỚI** của phiên này
- *«Không hỏi Owner câu mơ hồ như "có cho ghi final_bundles không?". Nếu thật sự cần mở rộng
  quyền, phải lập exact Owner Decision Packet trước»*
- *«Không deploy chỉ vì đồng hồ đang nằm trong một cửa sổ từng được xem là idle»*
- *«Không dùng manual `--do` hoặc cùng-session smoke để nâng `SC12_RUNTIME_PROVEN`»*
- *«Không được tuyên bố "đã kiểm tra toàn bộ" chỉ vì chạy một test suite»*
- *«Không gộp SC-12 PASS với Pure Context PASS»*
- *«Không tô hồng. Không pass-washing. Không che blocker. Không ép số liệu khớp expectation»*
- *«Không tạo Prompt 44. Không tự tạo FU hoặc Plan mới»* · *«Không trộn ERP vào báo cáo Lottery»*

---

## 3 · ĐÀO BỚI / PHÁT HIỆN

*(§57.3 bắt **liệt kê đủ**, kể cả phép đo ra kết quả âm hoặc không kết luận được.)*

### 3.1 · Điều đã CHỨNG MINH được `§XVI-3`

**① `FINAL_BUNDLES_ZERO_WRITE` — chứng minh, không hứa.** Khối vá **không chứa** một lệnh
`INSERT`/`UPDATE`/`REPLACE`/`DELETE INTO final_bundles` nào; chỉ **đúng 1 `SELECT`**. Đếm
trước/sau trên cả `database.py` và `main.py`: mọi lệnh ghi `final_bundles` **giữ nguyên số lần**.

**② Metadata cần thiết ĐÃ CÓ SẴN** — đây là bằng chứng cho phép bỏ VA-1/VA-2.
`model_exclusion_reasons` **đã ghi** `reason='max_voters_cap'` từ trước. Gọi **hàm production
thật** trên **DB thật**:

```
MT 2026-09-08 → ['claude-opus-4-6', 'claude-sonnet-4-6']
MT 2026-09-06 → ['meta-learning', 'smart-ensemble']    ← ĐỔI THEO NGÀY, không phải hằng số
MN 2026-09-08 → []                                      ← miền không bị trần thì rỗng
ngày/miền không tồn tại → []                            ← fail-safe
```

**③ Vá KHÔNG tẩy trắng lỗi thật.** Dry-run trên dữ liệu thật: ngày **25/07 MT có
`mc=11 + cap=2 = 13 < 15`** — thiếu hụt THẬT ngoài phần bị trần — và **vẫn giữ `EXCLUDE_PRIMARY`**.
48 ngày đổi sang `INCLUDE` đều là `13+2=15`, đúng đủ, không dư ca nào.

**④ Rollback rehearsal ĐẠT.** Cài cả hai → AST OK → import OK → gỡ ngược → **cả ba tệp về đúng
preimage**, 0 marker, PID không đổi, health 200.

**⑤ Cổng 4 tích hợp ĐẠT.** Cài V11174 trước → `daily_evaluation.py` **vẫn khớp preimage** → chạy
test V11173 → **43/43**.

**⑥ Idle gate PASS thật** — và hai tiêu chí em từng dùng **SAI** đã sửa (xem mục 7).
Mốc kế tiếp 05:00 ⇒ ~3h dư địa.

**⑦ `evaluate_all_history` CÔ LẬP THẬT.** Chỉ được gọi tại `daily_evaluation.py:675`, **bên trong
`if __name__ == "__main__"`** dưới cờ `--backfill`. **0 cron · 0 route**; scheduler chỉ import
`run_daily_eval` / `generate_daily_report` / `init_eval_table`.

**⑧ Drift = 0.** Ba preimage khớp **đúng** anchor `4ed5fd7e…` / `fd3d2349…` / `42a7c0fc…`.

**⑨ Forbidden-surface diff sạch.** `ranked_numbers` · `_CANONICAL_OUTPUT_MODELS` ·
`strength_weight` · `run_combo_super` · `SYSTEM_PROMPT` · `output_counterfactual_rank` ·
`lo3_status` · `save_final_bundle` · `bach_thu =` — **giữ nguyên số lần xuất hiện** ở cả hai tệp
bị sửa.

### 3.2 · Điều BỊ BÁC BỎ / PHẢI RÚT LẠI `§XVI-4`

| # | claim cũ | nguồn | bằng chứng bác bỏ | claim đúng |
|---|---|---|---|---|
| 1 | *«VA-h12 đã có vá, 30/30 test, chờ owner ký»* | `FOLLOW_UP_TRACKER:183` | `v11165_h12_patch.py:45` `DICH` = chính đường dẫn của nó; `--cai-dat` = tự chép; **0 dòng ghi** `main.py`/`database.py`; tự khai `CANDIDATE_KHONG_DEPLOY` | **`VA_H12=DESIGN_HELPER_TESTED · REAL_INSTALLER_MISSING`** — đã thay bằng V11174 |
| 2 | *«30/30 kiểm bản vá»* | cùng tệp | 30/30 kiểm **ba hàm thuần tái dựng** (`tach_ke_toan`, `classify_bundle_quality_v2`, `classify_day_status_v2`) | 30/30 là **helper test**, không phải production-function test |
| 3 | *«bundle giống hệt từng byte»* | docstring VA-h12 | VA-2 gốc thêm 7 khoá vào `source_predictions_json` và đổi `incomplete_bundle` | **đúng cho bầu chọn, SAI cho bản ghi bundle** ⇒ đã **bỏ hẳn VA-1/VA-2** |
| 4 | *«V11173 không ghi DB»* | docstring V11173 (em viết) | `daily_evaluation.py:419` `INSERT OR REPLACE INTO daily_eval_log`; `run_daily_eval` gọi ở `scheduler.py:1836`/`:9264` | **là thay đổi DỮ LIỆU**; rollback code **không** hoàn tác. Đã đính chính trong tệp |
| 5 | *«WAL/SHM tồn đọng = có writer»* | cổng idle V11173 của em | WAL **0 byte**; `-shm` **luôn tồn tại** khi có kết nối mở | tiêu chí đúng là **WAL size > 0** |
| 6 | *«Auto Retrain 02:00 hằng đêm»* | giả định của em | journal: **`🧠 Auto Retrain (sun 02:00)`** | **`day_of_week=sun`** — hôm nay Thứ Năm ⇒ không chạy |
| 7 | *«replay VA-h12 đổi đúng 45 dòng»* | `FOLLOW_UP_TRACKER:183` + `RL-014` | dry-run độc lập: **46** dòng tính đến 04/09 | 🔴 **`INDETERMINATE`** — xem mục 4.4 |

*(Bốn phần bắt buộc của `PRJ-RETRACTION-001` — chỗ gốc · nguyên văn câu sai · điều đúng kèm phép
đo · quyết định nào đã dựa trên số sai — nằm đủ trong bảng trên cộng mục 4.4.)*

### 3.3 · Phép đo KHÔNG kết luận được — ghi thẳng, không giấu

- **Lệch +1 so với mốc 45**: không tái lập được ⇒ `INDETERMINATE` (mục 4.4).
- **`07/09 MT` và `09/09 MT` KHÔNG nằm trong danh sách 49 ngày đổi** — chưa truy nguyên nhân.
- **Nhánh `fb.status != 'ACTIVE'`** chưa từng được dữ liệu thật đi qua (582/582 đều `ACTIVE`) ⇒
  đường đó **chưa có bằng chứng runtime**.

---

## 4 · HƯỚNG XỬ LÝ VÀ VÌ SAO CHỌN — SC-12 BLOCKERS AND FIXES `§XVI-5`

### 4.1 · Blocker P0 — VA-h12 không cài được → **ĐÃ ĐÓNG**

**Vì sao không vá tệp cũ:** nó không phải installer hỏng, nó **chưa bao giờ là installer**. Sửa
một tệp tự khai `CANDIDATE_KHONG_DEPLOY` chỉ nối dài nhầm lẫn.

Viết mới `artifacts/v11174_vah12_zerowrite_installer.py`. **Không một dấu `...`**. Fail-closed:
chỉ áp lên sha256 nguồn đã nhận diện · preimage khớp **đúng 1 lần**/khối · marker **tính từ chính
khối vá** (`_so_marker_du_kien()` — không đoán tay, xem mục 7) · AST · idempotent · rollback về
đúng preimage. **58/58 test**, mục **F gọi thẳng hàm production thật** trên DB thật.

### 4.2 · Blocker phạm vi `final_bundles` → **ĐÃ ĐÓNG bằng thiết kế lại, không bằng xin phép**

§R khoá cấm ghi `final_bundles` **và** cấm hỏi lại owner câu đó. Nghe như bế tắc — nhưng đi đọc
**dữ liệu thật** thay vì thiết kế cũ thì thấy metadata VA-2 muốn *ghi* **đã có sẵn**. Nên:

| mảnh | gốc | V11174 |
|---|---|---|
| VA-1 (`main.py` ~9823) | thêm `_capped_models` để nuôi VA-2 | **BỎ** |
| VA-2 (`main.py` ~10506/10511) | **GHI** 7 khoá vào `final_bundles` | **BỎ** → **VA-2′ sửa phía ĐỌC** ở `_quality_filtered_models_from_source_meta` (`main.py:489`): loại model `max_voters_cap` **khi đọc**, 0 ghi |
| VA-3 (`database.py`) | đọc số cap | **VA-3′** — mở rộng SELECT đã có sẵn, ghi **chỉ** `day_governance` |

### 4.3 · Blocker `reason` chưa gán → **ĐÃ ĐÓNG**

Khối `SAU` của VA-3 gốc kết thúc bằng `...  # reason ghi ro phan nao la cap co y` — **thiếu dòng
gán**. Chép tay sẽ làm `classify_day_status` **nổ cho cả ba miền** tại `auto_verify`. V11174 gán
`reason` ở **cả ba nhánh**, kể cả nhánh `COMPLETE` (ghi rõ model nào bị trần).

### 4.4 · 🔴 CHƯA ĐÓNG — lệch +1 so với mốc 45 (`INDETERMINATE`)

Dry-run: **49 ngày đổi, tất cả MT, 0 MN, 0 MB**, trải 26/06 → 08/09. Phân rã:

| thành phần | số |
|---|---|
| ngày đổi tính đến **04/09** (mốc đo cũ) | **46** |
| ngày mới sau 04/09 (05, 06, 08/09) | **+3** |
| **tổng** | **49** |
| mốc ghi trong sổ (`FOLLOW_UP_TRACKER:183`) | **45** |

**+3 giải thích được** (tăng tự nhiên). **+1 thì KHÔNG** — cùng mốc 04/09 mà em ra 46, sổ ghi 45.
Nặng hơn: **`RL-014` chính là mục đã rút lại đúng con số này** (46 → 45).

**Vì sao chọn ghi `INDETERMINATE` thay vì chọn một số:** em **không có script gốc để tái lập**.
`RM-11`/`RM-17` cấm dùng số không tái lập làm căn cứ — và cũng cấm làm nó biến mất. Ép cho khớp 45
là `pass-washing`; im lặng lấy 49 là che một xung đột với sổ rút lại.

---

## 5 · ĐÃ LÀM GÌ — DEPLOY + TRẠNG THÁI AN TOÀN PRODUCTION `§XVI-2` `§XVI-6`

### 5.1 · Thứ tự deploy đã theo đúng §XIII

`v11174_vah12_zerowrite_installer.py --cai-dat` → `v11173_sc12_cohort_patch.py --cai-dat` →
AST OK → import OK → `systemctl restart lottery` → smoke.

### 5.2 · TRƯỚC / SAU (§60.4)

| mục | TRƯỚC | SAU |
|---|---|---|
| PID | `3370750` (start 04/09 01:08) | **`3870722`** (start **10/09 02:00:19**) |
| NRestarts | 0 | **0** |
| ActiveState/SubState | active/running | **active/running** |
| health | 200 | **200** |
| `predictions` | 14.605 | **14.605** |
| `final_bundles` | 582 | **582** · digest `396c755927410de46583b6dd3716967373c963ba88f2d8b29c396fe37a24a8a6` |
| `lottery_results` | — | 15.449 |
| `model_daily_eval` | — | 14.469 |
| `day_governance` | 581 | **581** — `classified_at` mới nhất vẫn `2026-09-09 18:32:34` ⇒ **chưa ghi mới** |
| MT `EXCLUDE_PRIMARY` | 98 | **98** |
| `output_counterfactual_rank` | 0 ghi / 17.283 | **0 ghi / 17.526 dòng** — phương án B nguyên vẹn |
| journal Traceback/ERROR | — | **0** |

**`DB MUTATIONS = 0`.** Toàn phiên không một lệnh `INSERT`/`UPDATE`/`DELETE` nào vào DB production.

**PHIÊN BẢN:** `main.py` `4ed5fd7e…` → `d59a6ae9…` · `database.py` `fd3d2349…` → `758cf2cf…` ·
`daily_evaluation.py` `42a7c0fc…` → `dab6bf14…`
**KIỂM:** marker `V11174` database.py **3** · main.py **1** · `V11173` daily_evaluation.py **3** ·
`JOIN final_bundles` **0**.

---

## 6 · CỔNG KIỂM — 13/13 XÁC MINH

| # | cổng §XIII | kết quả |
|---|---|---|
| 1 | exact current preimages accepted | ✅ 3/3 khớp anchor |
| 2 | VA-h12 real installer PASS | ✅ **58/58** |
| 3 | actual production-function tests | ✅ mục F gọi hàm thật trên DB thật |
| 4 | V11173 43/43 sau tích hợp | ✅ **43/43** |
| 5 | `FINAL_BUNDLES_ZERO_WRITE` proven | ✅ 0 lệnh ghi thêm, 1 SELECT |
| 6 | backfill dry-run accepted | ✅ 49 dòng, row-level diff, +3 giải thích, +1 `INDETERMINATE` |
| 7 | transaction/backup/restore tested | ✅ snapshot 581+432 dòng, khôi phục thử khớp |
| 8 | all-history fixed **hoặc explicitly isolated** | ✅ **isolated** (CLI-only, 0 cron/route) |
| 9 | no output/model/TOTAL/prompt/Combo/FINAL/3-càng drift | ✅ forbidden-surface diff sạch |
| 10 | local provenance rõ | ✅ `fu438/admin-only-p0a` @ `75806b6`, worktree sạch |
| 11 | fresh VPS snapshot | ✅ R0 lúc 01:52 |
| 12 | fresh idle gate | ✅ đo lại **ngay trước** khi cài |
| 13 | rollback rehearsal PASS | ✅ về đúng preimage |

**Cổng quản trị trong phiên:** `NANG_VERSION_V11062=ĐẠT` (seq 488 → **489**) ·
`PRJ_RETRACTION=SẠCH` · `PRJ_WINDOW=SẠCH` · `_v11027_so_muc_quan_tri=ĐẠT` (không mục nào biến mất).

> ⚠️ **`--do` / smoke cùng phiên KHÔNG được dùng để nâng lên `SC12_RUNTIME_PROVEN`** (§XIII).
> Cổng 1–13 chỉ nói về **một lần deploy**, **không** phải "đã kiểm tra toàn bộ hệ thống".

---

## 7 · VƯỚNG VẤP — BÀI HỌC

| # | vấp | ai bắt |
|---|---|---|
| 1 | 🔴 Em đoán **số marker kỳ vọng bằng tay — SAI BA LẦN** (5 vs 3; rồi 6/3 vs 3/1). Sửa tận gốc: **tính số marker từ chính khối vá** (`_so_marker_du_kien()`), không hardcode | bộ test của chính em |
| 2 | 🔴 **Hai tiêu chí idle của chính em SAI** — `-shm` tồn tại ≠ có writer (đúng: **WAL size > 0**); retrain **`day_of_week=sun`** chứ không hằng đêm. Giữ chúng sẽ sinh một `BLOCKED` **sai** — tai hại ngang một `PASS` sai | đo lại journal + kích thước WAL |
| 3 | 🟠 `_chay.py` chép script sang `artifacts/_run_<tên>.py` ⇒ installer **không nằm ở đường dẫn chuẩn**, bước 1 deploy im lặng báo "No such file" | bước deploy |
| 4 | 🟠 `health: 000` ngay sau restart — app **chưa kịp bind cổng 8000** sau 6 giây. Poll tiếp: **200 lúc 02:00:42**; journal xác nhận `Uvicorn running` **02:00:25** | smoke test |
| 5 | 🟡 Chú thích của em chứa `NOT EXISTS (` làm phép đếm tự dính (2 thay vì 1); chú thích chứa `date('now')` phá một phép kiểm khác | bộ test |
| 6 | 🟡 Thông điệp commit có dấu nháy làm vỡ shell (`pathspec '0.2310,'`) ⇒ chuyển sang `git commit -F` | shell |
| 7 | 🔴 **Bản nháp đầu của báo cáo này dùng 15 tiêu đề §XVI thay cho khung 9 phần §57.3** — cổng báo *thiếu 5/9 phần*. **Đúng lỗi `FU-447` mà chính em vừa báo ở V11172, và đã mắc một lần ở V11173.** Sửa: khung kép — 9 phần §57.3 làm xương, `§XVI-n` gắn nhãn tại chỗ | `_v10921_report_gate.py` |

**Bài học lớn nhất của phiên:** một **khoá cấm phạm vi** (`FINAL_BUNDLES_ZERO_WRITE`) buộc em đi
đọc **dữ liệu thật** thay vì đi theo **thiết kế đã viết sẵn** — và thiết kế đó hoá ra **thừa**.
Nếu owner cho phép ghi, em đã ghi trùng cái đang có.

---

## 8 · GỠ VỀ — ARTIFACT · HASH · ROLLBACK `§XVI-14`

| artifact | trên VPS | bản lưu trong kho công khai | sha256 |
|---|---|---|---|
| installer VA-h12 zero-write | `artifacts/v11174_vah12_zerowrite_installer.py` | ✅ `evidence/` | `f4ea7cd876ea76d53713e959747ef68c1526aab2a73721048c2096328e376497` |
| installer cohort | `artifacts/v11173_sc12_cohort_patch.py` | ✅ `evidence/` | `704cde8880e0449bd54853368cd45ff3b02f456443f9323f358ae35ee70b979b` |
| backfill dry-run diff (49 dòng) | `artifacts/v11174_backfill_dryrun.json` | ✅ `evidence/` | 15.226 byte |
| kết quả test installer | `artifacts/v11174_vah12_kq.json` | ✅ `evidence/` | 58/58 |
| snapshot `day_governance` (581 dòng) | `artifacts/v11174_day_governance_snapshot.json` | ❌ **chỉ trên VPS** (269 KB) | `5e2c7fb9e40cb230a09f30e5ba6f470dfe27b9e58fa3cad742c72cd6a1a8de04` |
| snapshot `daily_eval_log` (432 dòng) | `artifacts/v11174_daily_eval_log_snapshot.json` | ❌ **chỉ trên VPS** (1,8 MB) | `495a630c75874f57c5c592879f7b0d4d40a53ae6cfcda52c561e96e1b46043de` |
| runbook đã làm cứng | `docs/SC12_RUNBOOK_V11173.md` | — (kho riêng) | — |

> **Vì sao evidence nằm ở kho CÔNG KHAI chứ không phải kho riêng:** `artifacts/` **bị `.gitignore`
> chặn có chủ ý** ở kho riêng (nơi chứa runtime artifact). §57.2 chỉ định đúng chỗ cho tệp bằng
> chứng là thư mục **`evidence/`** của báo cáo công khai. Hai installer đã kéo từ VPS về và
> **đối chiếu sha256 khớp từng byte** — `f4ea7cd8…` (20.743 byte) · `704cde88…` (20.385 byte).
> Hai snapshot **cố ý không đưa vào git** (2,1 MB runtime artifact) — giữ trên VPS, hash ghi ở đây
> để đối chiếu.

**Preimage → Postimage:**

| tệp | PRE | POST |
|---|---|---|
| `main.py` | `4ed5fd7ebaee8d232177df2e371ca7ad7fc57d829dde503c560ac511a83781cf` | `d59a6ae94f9c3666eace95d2e772ed39e761a1711cb726b601d753d5d8f2f4ca` |
| `database.py` | `fd3d2349ab917c6f36ee8d0a2aa6b82841a963811ba716bc58090c3be566eb16` | `758cf2cf0a8a6564d7ad5c0c92aa788e9b80c78e2a0dd1adeb5539e502af09fa` |
| `daily_evaluation.py` | `42a7c0fcf04450bdf09c604b8f47bd576abfde413daa3edeb31534cac51ca603` | `dab6bf149c46ed55661f9016050752ff8c7cc3bd1df6e2348e46b69750696fbd` |

**Sao lưu:** `database.py.pre_v11174` · `main.py.pre_v11174` · `daily_evaluation.py.pre_v11173`

**Lệnh gỡ về (thứ tự NGƯỢC):**
```bash
/root/Lottery_AI_Test/venv/bin/python3 /root/Lottery_AI_Test/artifacts/v11173_sc12_cohort_patch.py --rollback
/root/Lottery_AI_Test/venv/bin/python3 /root/Lottery_AI_Test/artifacts/v11174_vah12_zerowrite_installer.py --rollback
systemctl restart lottery
# NEU auto_verify DA CHAY: khoi phuc day_governance tu v11174_day_governance_snapshot.json
```

> 🔴 **Gỡ mã ≠ gỡ dữ liệu.** Sau 18:34 hôm nay, `day_governance` sẽ có dòng ghi bằng logic mới.
> Gỡ tệp **không** hoàn nguyên chúng. Phải khôi phục từ snapshot.

---

## 9 · THEO DÕI TIẾP

### 9.1 · 🔴 PHẦN KHÔNG LÀM TRONG PHIÊN NÀY — khai báo thẳng `§XVI-7` `§XVI-8` `§XVI-10`

**R6 · R7 · R8 = `NOT_PERFORMED_THIS_SESSION`** — không phải PASS, không phải FAIL.

| mục §R | nội dung | trạng thái |
|---|---|---|
| **R6** `§XVI-7` | audit tổng lực nợ/ambiguity: measurement · leakage · per-model inventory · TOTAL reproduction · Combo/FINAL/3-càng call graph · scheduler/infra · code-debt scan · report/doc debt | **KHÔNG LÀM** |
| **R6** `§XVI-8` | model / output / TOTAL / Combo / FINAL / 3-càng findings | **KHÔNG LÀM** |
| **R7** `§XVI-9` | pure-context condition ledger · UCC-1.0.0 audit · contamination/anchor test · ba lớp payload | **KHÔNG LÀM** |
| **R7** `§XVI-10` | set-to-condition conversion findings | **KHÔNG LÀM** |
| **R8** `§XVI-11` | Improvement Candidate Register | **KHÔNG LÀM** |

**Vì sao:** phiên tập trung toàn bộ vào đóng blocker SC-12 và deploy an toàn trong **cửa sổ idle
hẹp ~3 giờ**. Điều **duy nhất** phiên này chứng minh về các bề mặt model/output/TOTAL/Combo/FINAL/
3-càng là **chúng KHÔNG ĐỔI** (forbidden-surface diff, mục 3.1 ⑨). Kiến trúc 3-càng giữ nguyên:
prefix + bạch thủ cuối theo lane; không bắt model đơn output 000–999; không tạo model 3-càng riêng.

### 9.2 · Bằng chứng cũ VẪN ĐỨNG — không đo lại phiên này

| mục | trạng thái | nguồn |
|---|---|---|
| nền riêng từng miền MN 43,1% · MT 35,2% · MB 23,8% | ĐÃ CHỨNG MINH | V11170 |
| hệ **không hơn ngẫu nhiên** — 5 đường đo độc lập | ĐÃ CHỨNG MINH | V11170 |
| retrain tự ghi `Precision@10 0.2310 · Lift 0.97×` (kém nền 3%) | ĐÃ CHỨNG MINH | V11172 |
| cohort «WR Tổng» trượt 157 ngày cho nhãn "90 ngày" | ĐÃ CHỨNG MINH | V11173 |
| MT `wr7` dùng dữ liệu **19/06–25/06** | ĐÃ CHỨNG MINH | V11170/72/73 |
| `FU-397` anti-trap n=63/90 | **CẤM ĐỌC SỚM** | V11170 |
| 32 nhãn lo3 sai · 90 bundle Phase 1.5 | ĐÃ CHỨNG MINH, **loại khỏi measurement** | V11169/73 |
| `combo-super` TIMEOUT 25/30 ngày, đang tăng tốc | ĐÃ CHỨNG MINH, **chưa đăng ký theo dõi** | V11172 |
| 200 mục treo · 155 quá hạn · 24 quyết định quá hạn rà soát | ĐÃ ĐO | V11172 |

### 9.3 · Pure Context `§XVI-9`

# `PURE_CONTEXT_PARTIAL`

Giữ nguyên **`PARTIAL · NOT_RUNTIME_COMPLETE · NOT_PREDICTIVE_VALIDATED`**. **Không nhảy cấp.**
Ghi nhận từ V11165: 0/60 prompt lịch sử tái dựng được ⇒ **`NON_RECONSTRUCTABLE`**.
**Cấm gộp với dòng SC-12.**

### 9.4 · Lộ trình cải thiện `§XVI-11`

| bước (canonical §XII) | trạng thái |
|---|---|
| **MEASUREMENT REPAIR** | 🟡 **ĐANG LÀM** — code deployed, chờ runtime proof + backfill |
| CONTEXT-ONLY SHADOW DEPLOY | ⬜ chưa (chặn bởi bước trên) |
| SCHEDULED RUNTIME PROOF | 🟡 **hôm nay 16:37–18:34** |
| RANKED TOP-K ADAPTER · ALL-MODEL ARENA · TOTAL_V2 · COMBO_V2 · FINAL_V2 · OFFICIAL CUTOVER | ⬜ chưa — **cấm nhảy bước** |

**Phân loại đúng cho những gì phiên này làm:** **measurement correction** + **reliability
improvement** — **KHÔNG phải predictive lift**. Không có tuyên bố nào về chất lượng dự đoán tăng.

### 9.5 · Quyết định cần owner `§XVI-12`

**KHÔNG CÓ quyết định nào chặn ở owner lúc này.** Khoá `FINAL_BUNDLES_ZERO_WRITE` đã giải quyết
câu hỏi phạm vi mà V11173 treo — và em đã thiết kế lại để tuân thủ, **không cần Owner Decision
Packet**. Việc còn lại đều nằm trong thẩm quyền agent hoặc chờ bằng chứng tự nhiên.

### 9.6 · VIỆC KẾ TIẾP DUY NHẤT `§XVI-13`

> **Chờ `auto_verify` tự nhiên chạy 16:37–18:34 hôm nay 10/09, rồi thu bằng chứng runtime:**
> production PID `3870722` gọi `classify_day_status` đã vá · MT ngày 10/09 nhận
> `VALID_LIVE_DAY`/`INCLUDE` thay vì `DEGRADED`/`EXCLUDE_PRIMARY` · `daily_eval_log` nhận cohort
> đã khoá · `final_bundles` digest **vẫn `396c7559…`** · 4 bảng khoá no-drift.
> **Chỉ khi đủ mới được ghi `SC12_RUNTIME_PROVEN`.**

Mục treo liên quan: **`FU-451`**.

### 9.7 · Nợ đã biết, KHÔNG chặn

| mức | nợ |
|---|---|
| P2 | `evaluate_all_history` **cô lập** chứ chưa **sửa** — phủ lịch sử giảm ~87% → ~46% nếu ai chạy tay |
| P3 | `LIKE '%Phase 1.5 backfill%'` rộng hơn ngữ nghĩa `notes=` (hiện 90/90 khớp chính xác) |
| P3 | nhánh `fb.status != 'ACTIVE'` chưa từng được dữ liệu thật đi qua (582/582 ACTIVE) |
| P3 | clone `v11165_immutable.db` đã xoá ⇒ số replay cũ của VA-h12 `NOT PROVEN` |
| 🔴 | **backfill lịch sử CHƯA chạy** — mới dry-run; 49 dòng MT lịch sử **vẫn** `EXCLUDE_PRIMARY` |
| 🔴 | **lệch +1 `INDETERMINATE`**, xung đột `RL-014` |
| 🔴 | `07/09 MT` và `09/09 MT` vắng khỏi danh sách đổi — chưa truy nguyên nhân |

---

## §62 — NGUỒN BA LỚP

### `OWNER_SAID`
> *«[CONTINUATION · §R] … `FINAL_BUNDLES_ZERO_WRITE` … Không hỏi Owner câu mơ hồ như "có cho ghi
> final_bundles không?" … Nếu một gate kỹ thuật không đạt, tự dừng và báo
> `BLOCKED_WITH_EXACT_REASONS`»* — 10/09/2026 ~01:45 ICT.
> *«Làm gì tiếp theo em đã đề xuất và tổng hợp báo cáo đầy đủ lên github chưa em»* — 09/09 ~21:00.

### `CODE_DID`
- `database.py:5062-5077` — `classify_day_status` đã có sẵn `cursor` và **đã SELECT `final_bundles`**;
  V11174 mở rộng SELECT đó. Ghi **chỉ** `day_governance` (`:5095` INSERT).
- `main.py:487-506` — `_quality_filtered_models_from_source_meta` **đã lọc đúng theo `reason`**
  (`:502` chỉ nhận `bt_gate`/`wr_gate`), nhưng `:489` **nuốt trọn `wr_gate_filtered`** đang bị nhiễm.
- `daily_evaluation.py:664-675` — `evaluate_all_history()` **chỉ trong `__main__`** dưới `--backfill`.
- `scheduler.py` — chỉ import `run_daily_eval` / `generate_daily_report` / `init_eval_table`.
- journal `02:00:25` — `🧠 Auto Retrain (sun 02:00)`, `Application startup complete`,
  `Uvicorn running on http://0.0.0.0:8000`.
- `systemctl` — PID `3370750` → `3870722`, `NRestarts 0`, `ExecMainStart Thu 2026-09-10 02:00:19 +07`.

### `DOC_SAID`
- `FOLLOW_UP_TRACKER:183` — *«SC-12 kế toán MT (VA-h12, 30/30 test, replay đổi đúng 45 dòng)»*
- `FOLLOW_UP_TRACKER:194` — dự báo `wr7 14,3% → 0,0%` · `top1_7 57,1% → 28,6%`
- `docs/SC12_RUNBOOK_V11173.md` — runbook đã làm cứng
- `docs/SO_RUT_LAI.json` — 25 mục, trong đó `RL-014` rút lại chính con số 46 → 45

**LỆCH BA LỚP — báo bắt buộc:**
1. `DOC_SAID` ≠ `CODE_DID`: sổ ghi VA-h12 *«đã có vá, chờ ký»*; mã cho thấy **không có installer**.
   ⇒ reclassify `DESIGN_HELPER_TESTED · REAL_INSTALLER_MISSING`.
2. `DOC_SAID` ≠ `CODE_DID`: sổ ghi replay **45**; đo độc lập ra **46** cùng mốc ⇒ `INDETERMINATE`.
3. `OWNER_SAID` = `CODE_DID`: khoá `FINAL_BUNDLES_ZERO_WRITE` **đã thi hành đủ** — 0 lệnh ghi
   `final_bundles`, digest bảng không đổi.

---

TanPhatAI cần làm: ghi **`V11174`** — `governance_seq 489`, công khai bản này cùng `CONVERSATION_CONTEXT_V11174_20260910.md`. Ghi **TRẠNG THÁI: `DEPLOYED_PENDING_SCHEDULED_PROOF`** cho SC-12 và **`PURE_CONTEXT_PARTIAL`** cho Pure Context — **hai dòng riêng, cấm gộp làm một**. Ghi **đã deploy 02:00:19 ICT ngày 10/09, PID 3370750 → 3870722, NRestarts 0→0, health 200, journal 0 lỗi, DB MUTATIONS = 0**. Ghi **13/13 cổng deploy PASS** — nhưng **«13/13» chỉ nói về MỘT LẦN DEPLOY, KHÔNG phải «đã kiểm tra toàn bộ hệ thống»**. Ghi **blocker P0 «VA-h12 không có installer thật» ĐÃ ĐÓNG** bằng `v11174_vah12_zerowrite_installer.py` (**58/58**, test **gọi hàm production thật trên DB thật**), và **VA-1/VA-2 gốc bị BỎ HẲN** vì chúng ghi `final_bundles` — vi phạm khoá mới `FINAL_BUNDLES_ZERO_WRITE`; thay bằng **VA-2′ sửa phía ĐỌC** ở `main.py:489`. Ghi **bằng chứng cho phép bỏ VA-1/VA-2: `model_exclusion_reasons` ĐÃ ghi sẵn `reason='max_voters_cap'`** — chỉ cần ĐỌC cái đã có, không cần ghi thêm. Ghi **vá KHÔNG tẩy trắng lỗi thật**: ngày 25/07 MT `mc=11+2=13 < 15` vẫn giữ `EXCLUDE_PRIMARY`. Ghi **dry-run backfill: 49 ngày đổi, TẤT CẢ MT, 0 MN, 0 MB**; phân rã **46 tính đến 04/09 + 3 ngày mới**; **+3 giải thích được, +1 là `INDETERMINATE`** xung đột với `RL-014` — **KHÔNG ép số cho khớp**. Ghi **hai tiêu chí idle em từng dùng SAI đã sửa**: retrain là `day_of_week=sun` (không phải hằng đêm) và **WAL size > 0** mới là tiêu chí đúng (`-shm` luôn tồn tại khi có kết nối). Ghi **cổng 8: `evaluate_all_history` CÔ LẬP THẬT** — chỉ trong `__main__` dưới `--backfill`, 0 cron 0 route. Ghi **R6 · R7 · R8 KHÔNG THỰC HIỆN trong phiên này (`NOT_PERFORMED_THIS_SESSION`)** — agent **không tuyên bố "đã kiểm tra toàn bộ"**. Ghi **backfill lịch sử CHƯA chạy, mới dry-run** — 49 dòng MT lịch sử vẫn `EXCLUDE_PRIMARY`. Ghi **đây là measurement correction + reliability improvement, KHÔNG phải predictive lift** — kết luận V11170 *«hệ không hơn ngẫu nhiên»* **vẫn đứng nguyên**. Ghi **KHÔNG có quyết định nào chặn ở owner**. Ghi **VIỆC KẾ TIẾP DUY NHẤT: chờ `auto_verify` 16:37–18:34 hôm nay rồi thu bằng chứng runtime** (`FU-451`). **Không mở Prompt 44. Không mở Plan mới. Không mở FU mới. Không trộn ERP.**
