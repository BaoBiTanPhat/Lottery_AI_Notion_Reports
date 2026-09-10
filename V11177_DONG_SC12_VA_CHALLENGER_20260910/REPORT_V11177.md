# V11177 — ĐÓNG SC-12 · DỰNG CONTEXT-ONLY CHALLENGER

> `SOURCE_TIMESTAMP` **2026-09-10 19:45 → 20:40 ICT** · `AUTHORITY` Prompt 43 R1 **§T**
> `PLAN` `PLAN-20260723-lottery-doc-restructure` · **Không mở Prompt 44 / FU / Plan mới**
> `PRODUCTION_MUTATIONS` **2 tệp** (`du-doan.html`, `daily_evaluation.py`) · `DEPLOY/RESTART` **0 restart**
> `DB MUTATIONS` **48 dòng `day_governance`** (owner đã duyệt) + **1 dòng `shadow_candidates`**
> **0 ghi `final_bundles` · 0 ghi `predictions` · 0 ghi `output_counterfactual_rank`**

---

## 1 · TÓM TẮT — MƯỜI CÂU TRẢ LỜI NGẮN (§T7)

| # | câu hỏi | trả lời |
|---|---|---|
| **1** | 10/09 MN/MT/MB thắng hay thua | **THUA cả ba bạch thủ.** MN `95` LOSE · MT `34` LOSE · MB `01` LOSE. **Lô2 MN PARTIAL** (`82` trúng). Lô3/xiên: LOSE hết |
| **2** | Thua ở tầng nào | **`RANKING_MISS` cả ba** — số trúng **có** trong `ranked_numbers`, ở hạng **2 / 4 / 3** trên 10; hệ chọn **đúng #1 của chính nó** ⇒ **không phải SELECTOR**, **không phải GENERATOR** |
| **3** | SC-12 đã đóng hoàn toàn chưa | **RỒI** — classifier ✅ · writer ✅ · backend ✅ · **UI ✅** · **historical ✅** |
| **4** | UI đã sạch chưa | **RỒI** — `SC12_UI_CONSUMER_PROVEN`, **10/10 assertion JS thật** trên đúng bytes đang phục vụ |
| **5** | Historical 48 rows đã repair chưa | **RỒI** — 1 transaction, `MT EXCLUDE_PRIMARY` **98 → 50**, digest lịch sử **không đổi** |
| **6** | `master` đã current chưa | **RỒI** — `a4d6636` → **`d2a6586`**, fast-forward, **không force** |
| **7** | `CONTEXT_ONLY_SHADOW` chạy được chưa | **RỒI** — chạy thật end-to-end, cron **13:30 ICT** hằng ngày |
| **8** | Ngày live kế tiếp challenger sẽ ra gì | **`abstain`** — và đó là output **đúng**: 0/8.676 điều kiện sống sót sau hiệu chỉnh |
| **9** | Còn gì chưa chứng minh | **Predictive lift = NOT_PROVEN.** Ranked hôm nay **36,7%** vs nền **37,0%** |
| **10** | Commit + containment | riêng **`master` = `fu438` = `d2a6586`** → bản này · công khai `f59a5c5` → bản này |

# `SC12_LIVE_PATH_RUNTIME_PROVEN`
# `SC12_HISTORICAL_REPAIR_COMPLETE`
# `DEFAULT_BRANCH_STATE_CONFLICT_RESOLVED`
# `CONTEXT_ONLY_SHADOW_READY_FOR_NEXT_LIVE`

---

## 2 · OWNER YÊU CẦU GÌ — NGUYÊN VĂN + GIỜ

| giờ ICT | NGUYÊN VĂN | loại | agent đã làm gì | trạng thái |
|---|---|---|---|---|
| **~19:45** | *«[CONTINUATION · §T] [STOP MEASUREMENT-ONLY LOOP · CLOSE SC-12 · START PREDICTIVE CHALLENGER]» · «Xử lý dứt điểm, không tiếp tục lề mề thăm dò đo lường mỗi ngày»* | `YÊU_CẦU` | T0→T5 thi hành đủ; T6 tôn trọng; T7 đóng | `ĐÃ_LÀM` |

**Ràng buộc đã tôn trọng, kiểm được:** không mở Prompt 44/FU/Plan · không đổi official prediction
policy · không đổi roster/weights/TOTAL/Combo/FINAL · **số MN/MT/MB sau mọi thao tác vẫn
`95` / `34` / `01`** · không dùng kết quả 10/09 để viết ngược cho 11/09 · không đếm
*«có model nào đó trúng»* làm KPI.

---

## 3 · ĐÀO BỚI / PHÁT HIỆN

### 3.1 · T0 — BẢNG EOD 10/09, TRẢ LỜI ĐÚNG VÌ SAO LIVE TỆ

| | MN | MT | MB |
|---|---|---|---|
| số đài · cutoff | 3 · 15:40 | 3 · 16:55 | 1 · 17:55 |
| **đuôi trúng thực tế** | **40** | **47** | **24** |
| nền ngẫu nhiên 1 số | **40%** | **47%** | **24%** |
| FINAL bạch thủ | `95` **LOSE** | `34` **LOSE** | `01` **LOSE** |
| lô2 | `95,82` **PARTIAL** | `34,60` LOSE | `01,20` LOSE |
| lô3 · xiên2 · xiên3 | `095` · LOSE · LOSE | `034` · LOSE · LOSE | `001` · LOSE · LOSE |
| bundle | mc=15 · moderate · 0.0754 | mc=13 · strong · 0.1484 | mc=15 · strong · 0.0887 |
| **ranked #1 của hệ** | `95` (0.0754) | `34` (0.1484) | `01` (0.0887) |
| **hệ chọn đúng #1?** | ✅ | ✅ | ✅ |
| **đuôi trúng đầu tiên trong ranked** | **hạng 2** (`82`) | **hạng 4** (`40`) | **hạng 3** (`34`) |
| candidate union (trước cutoff) | 22 số | 18 số | 22 số |
| prediction trước / sau cutoff | 27 / **0** | 27 / **0** | 27 / **0** |
| `main_selection_reason` | \multicolumn — `max_ranked_score_after_gate_and_lane_weight` cả ba | | |

**ROOT CAUSE: `RANKING_MISS` cả ba miền.** Số trúng **có mặt** trong `ranked_numbers`; hệ chọn
**đúng #1 của chính nó** ⇒ loại `SELECTOR_MISS`; số trúng nằm trong candidate ⇒ loại
`GENERATOR_MISS`; bundle ráp đúng ⇒ loại `BUNDLE_MISS`; đủ input, 0 bản ghi sau cutoff ⇒ loại
`DATA_OR_RUNTIME_FAILURE`.

**🔴 NHƯNG PHẦN QUAN TRỌNG HƠN — phải nói thẳng, không được đọc `RANKING_MISS` thành «có lỗi kỹ
thuật cần vá»:**

| miền | ranked K | trúng/K | tỉ lệ | nền | chênh |
|---|---|---|---|---|---|
| MN | 10 | 4 | 40,0% | 40% | **+0,0** |
| MT | 10 | 4 | 40,0% | 47% | **−7,0** |
| MB | 10 | 3 | 30,0% | 24% | **+6,0** |
| **TỔNG** | **30** | **11** | **36,7%** | **37,0%** | **−0,3 điểm** |

Bảng xếp hạng đạt **đúng bằng nền ngẫu nhiên**. Ở tầng thống kê đây là
**`RANDOM_MISS_WITHOUT_IDENTIFIED_DEFECT`**: mọi tầng đúng contract, không khiếm khuyết nào được
nhận diện ngoài *«xếp hạng không có lợi thế»*. Với **n=3** bạch thủ, ngày này **không chứng minh
được gì mới** (`RM-04`) — nó chỉ nhất quán với V11170.

### 3.2 · T5 — KẾT QUẢ ĐO LƯỜNG ĐÁNG GIÁ NHẤT CỦA PHIÊN

Bộ đào điều kiện thuần-ngữ-cảnh chạy trên dữ liệu thật, **không shortlist số**:

```
so_phep_thu_da_chay   : 8.676        (2 scope × 4 cửa sổ × 3 miền nguồn × 4 lag × nhiều vị trí giải)
z_nguong_bonferroni   : 4.53         (α = 0,05 chia cho 8.676)
so_dieu_kien_song_sot : 0            ← cả BA miền
```

| miền | nền đo độc lập hôm nay | V11170 đã công bố | cell tốt nhất | sống sót |
|---|---|---|---|---|
| MN | **0,4297** | 43,1% | `sup=40 stab=0,65` **z=2,8** | **0** |
| MT | **0,3497** | 35,2% | `sup=40 stab=0,60` **z=3,3** | **0** |
| MB | **0,2365** | 23,8% | `sup=40 stab=0,45` **z=3,2** | **0** |

**Hai điều đáng ghi:**
1. Nền em đo lại **hoàn toàn độc lập** hôm nay **khớp gần như tuyệt đối** với V11170 — một phép
   kiểm chéo ngoài dự kiến, củng cố kết luận cũ.
2. **Không một điều kiện nào vượt nền sau hiệu chỉnh so sánh bội.** Nếu chỉ nhìn z thô, top-20
   đều có z ≈ 3–3,8 và trông như bằng chứng mạnh. Sau khi chia cho 8.676 phép thử thì **không còn
   gì**. Đây chính là bẫy mà bản đầu của em suýt rơi vào — xem mục 7 vấp #3.

---

## 4 · HƯỚNG XỬ LÝ VÀ VÌ SAO CHỌN

**T1 — vì sao vá được mà không cần restart:** `/du-doan` phục vụ bằng
`FileResponse(STATIC_DIR / "du-doan.html")` với `Cache-Control: no-store` ⇒ đọc từ đĩa **mỗi
request**. Đổi tệp có hiệu lực ngay, **không cắt ngang `du_doan_test_auto`**.

**T3 — vì sao chọn B (cho nghỉ) chứ không A (sửa thành công cụ tốt):** đo code-use thật —
`evaluate_all_history` chỉ xuất hiện ở **3 chỗ** (1 chú thích, 1 định nghĩa, 1 lời gọi trong
`__main__`), **0 cron · 0 route · 0 module import**. Sửa nó là đầu tư vào đường không ai đi, và
vẫn để lại nguy cơ một CLI cũ sinh kết quả **khác classifier canon**. Việc sửa lịch sử đã được
làm đúng cách ở T2.

**T4 — vì sao fast-forward an toàn:** `master` **là tổ tiên** của `fu438` (ahead 59, behind 0),
nên đây là fast-forward thuần, **không rewrite commit nào**.

**T5 — vì sao `abstain` là kết quả ĐÚNG, không phải thất bại:** hợp đồng output cho phép abstain
khi bằng chứng không đủ. Với 0/8.676 điều kiện sống sót, **bất kỳ ranked list nào cũng sẽ là bịa**.
Abstain là câu trả lời trung thực duy nhất — và nó **được ghi thành bản ghi** để mỗi ngày đều có
dữ liệu đối chiếu.

---

## 5 · ĐÃ LÀM GÌ

| T | việc | TRƯỚC | SAU |
|---|---|---|---|
| **T1** | `du-doan.html` | `76599f6a` · 3 điểm rơi ngược | **`23f1ca69`** · 6 marker `V11177` · phân biệt `FIELD_ABSENT` / `FIELD_PRESENT_EMPTY` |
| **T2** | `day_governance` | `MT EXCLUDE_PRIMARY` **98** | **50** · 48 dòng trong **1 transaction** |
| **T3** | `daily_evaluation.py` | `dab6bf14` · `ISOLATED_NOT_REPAIRED` | **`3c91aba8`** · **`RETIRED_FAIL_CLOSED`** |
| **T4** | `origin/master` | `a4d6636` = V11123 | **`d2a6586`** = canon hiện hành |
| **T5** | challenger | không tồn tại | `web/backend/_v11177_context_only_challenger.py` · cron **13:30** · đã chạy thật |

**T1 — kiểm sau khi cài:** health **200** · `/du-doan` **200** · PID **`3870722` KHÔNG ĐỔI** ·
NRestarts **0** · journal từ 20:30 **0 lỗi** · endpoint phục vụ **byte-identical** với tệp đã vá.

**T2 — bất biến kiểm TRƯỚC khi ghi (lệch một dòng là ROLLBACK toàn bộ):**
candidate 74 · mutation **đúng 48** · chỉ `MT` · **45** đến 04/09 **+ 3** ngày (05,06,08/09) ·
`25/07 MT` **KHÔNG** trong mutation (old = new) · `07/09 MT` **không** là candidate (`cap=0`) ·
`09/09 MT` **giữ** `EXCLUDE` (`eff=14<15`) · 0 MN · 0 MB · `BEGIN IMMEDIATE` · verify post-values
**trong** transaction · digest `final_bundles` kiểm **trong** transaction.

**T2 — cohort sạch, và tin xấu nói thẳng:** 7 lượt `INCLUDE` gần nhất của MT nay là **01–10/09**
(trước đây **19–25/06**, trễ **71 ngày**) — đây mới là **điều T2 chứng minh**: cohort đã hết trễ.
Chỉ số quan sát được: `wr7` bạch thủ MT = 1/7 = **14,3%**. *(Sổ dự báo `14,3% → 0,0%`; thực tế
**14,3%** — con số dự báo đó cũng sai.)*

> ⚠️ **`PRJ-SELECTION-WINDOW-001` — `wr7` KHÔNG PHẢI TUYÊN BỐ HIỆU QUẢ.**
> `wr7` là **một cửa sổ 7 ngày, n = 7**. Trích riêng nó để nói *«MT tốt/xấu»* chính là
> **chọn cửa sổ cho khớp kết quả**. Bộ cửa sổ đầy đủ đã đo ở **V11084 + V11086** cho thấy
> **DẤU ĐỔI**: **30 ngày +4,07pp · 90 ngày −3,18pp · 180 ngày +0,91pp** (CI95 **[−3,2 ; +5,0]**).
> Vì vậy `wr7 = 14,3%` ở đây chỉ dùng để **chứng minh cohort đã hết trễ 71 ngày**, **KHÔNG**
> dùng làm bằng chứng về chất lượng dự đoán của MT. Với **n = 7**, `RM-04`: **chưa được phép
> kết luận**.


---

## 6 · CỔNG KIỂM

| cổng | kết quả |
|---|---|
| `v11177_ui_patch.py --test` | **19/19 ĐẠT** |
| **DOM/JS-level trên bytes đang phục vụ** | **10/10 ĐẠT** — trích nguyên văn `_v11177_canon` từ `/du-doan`, chạy trong `node vm` |
| `v11177_retire.py --test` | **12/12 ĐẠT** |
| `v11177_backfill.py` (bất biến) | **ĐẠT** — mutation đúng 48 |
| `ACTIVE_WRITER_PROOF` W1–W4 | **KHÔNG thành lập** ⇒ cửa sổ an toàn |
| digest lịch sử `final_bundles` | **`0c5f84f8…` KHÔNG ĐỔI** |
| số dự đoán MN/MT/MB | **`95` / `34` / `01` — KHÔNG ĐỔI** |
| `output_counterfactual_rank` | **0** |
| `_v10921_report_gate.py` ① toàn dải | 🔴 **39/253 KHÔNG ĐẠT** — `LEGACY_ADMIN_DEBT`, **không dùng để trì hoãn** (§T6) |

---

## 7 · VƯỚNG VẤP — BÀI HỌC

| # | vấp | ai bắt |
|---|---|---|
| 1 | 🔴 **Bản EOD đầu của em kết luận `GENERATOR_MISS` cả ba miền — SAI HOÀN TOÀN.** `main_numbers` là **JSON array text**; em tách bằng dấu phẩy nên sinh token rác `["76"` ⇒ `union` là rác. Bằng chứng phản: MN lô2 `PARTIAL` mà `82` **có** trong đuôi trúng | em, khi thấy Top-K in ra `('["76"', 5)` |
| 2 | 🔴 **Bản thứ hai kết luận `SELECTOR_MISS` — cũng SAI.** Em xếp hạng bằng **đếm phiếu thô**, còn hệ dùng `weighted_voting_wr`. Thước đúng nằm sẵn trong `source_predictions_json.ranked_numbers`. Dùng sai thước ⇒ đổ oan cho selector | em, khi tự hỏi «hệ xếp hạng thế nào» |
| 3 | 🔴 **Bộ đào điều kiện đầu tiên báo 20/20 `du_manh=True` với z≈3,8** — trong khi em vừa **tự cảnh báo** về bẫy n-nhỏ ở đúng đoạn trên. Đào **8.676** cell rồi **sắp theo z lấy top** thì z cao là **định nghĩa** của bẫy so sánh bội, không phải bằng chứng | em, ngay sau khi in bảng |
| 4 | 🟠 **Đoán số marker sai — LẦN THỨ TƯ** (đoán 9, thực tế 6). Sửa tận gốc: tính từ chính khối vá | bộ test |
| 5 | 🟠 Preimage viết bằng `\n` nhưng `du-doan.html` dùng **CRLF** ⇒ không bao giờ khớp | assert fail-closed |
| 6 | 🟡 Heredoc mangling `\r\n` — **đúng lỗi đã ghi trong bộ nhớ**, vẫn tái phạm | lỗi cú pháp |

**Bài học xuyên suốt:** **ba lần liên tiếp em suýt công bố một nguyên nhân không có thật**
(`GENERATOR_MISS` → `SELECTOR_MISS` → *«20 điều kiện mạnh»*). Cả ba đều do **dùng sai thước đo**,
không phải do hệ thống hỏng. Điều cứu được cả ba lần là **nhìn kết quả thấy vô lý thì đo lại**,
chứ không phải một cổng máy nào.

---

## 8 · GỠ VỀ

| việc | cách gỡ |
|---|---|
| T1 UI | `venv/bin/python3 /tmp/v11177_ui_patch.py --rollback` → về `76599f6a`; sao lưu `du-doan.html.pre_v11177` |
| T3 retire | `venv/bin/python3 /tmp/v11177_retire.py --rollback` → về `dab6bf14`; sao lưu `daily_evaluation.py.pre_v11177` |
| T2 backfill | khôi phục 48 dòng từ `backups/v11177/v11177_backfill_preimage.json`; ảnh chụp **toàn bộ** `day_governance` 584 dòng ở `v11177_day_governance_FULL_pre.json` (sha256 `a824fb6e…`) — **để NGOÀI VPS** |
| T4 master | `git push origin a4d66364…:refs/heads/master` *(chỉ khi owner yêu cầu — đây là lùi trạng thái)*; `fu438` **giữ nguyên** làm điểm gỡ về |
| T5 cron | `crontab /tmp/cron_pre_v11177.bak` (143 dòng) |

**Không cần gỡ runtime:** **0 restart**, PID `3870722` không đổi suốt phiên.

---

## 9 · THEO DÕI TIẾP

### 9.1 · Việc kế tiếp chính xác

> **Ngày live kế tiếp (11/09), lúc 13:30 ICT, cron chạy challenger cho MN/MT/MB.**
> Kỳ vọng: **`abstain`** cả ba (0 điều kiện sống sót). Mỗi miền sẽ có **một bản ghi
> `output_type='abstain'`** trong `shadow_candidates` kèm `so_phep_thu_da_chay`,
> `z_nguong_bonferroni`, `so_dieu_kien_song_sot` — đủ để đối chiếu `CURRENT_OFFICIAL` vs
> `CONTEXT_ONLY_CHALLENGER` mà không cần thêm phiên đo nào.

**Cổng dừng cứng (§T5-E) — đã cài sẵn ý nghĩa, không cần chờ hàng tháng:**
nếu challenger tiếp tục `abstain` vì `so_dieu_kien_song_sot = 0`, đó **không phải lỗi runtime** mà
là **câu trả lời**: không gian điều kiện này không chứa tín hiệu vượt nền. Muốn đi tiếp phải **mở
rộng không gian điều kiện** (thêm loại điều kiện, không phải thêm ngày đo).

### 9.2 · Nợ mở

| mức | nợ |
|---|---|
| 🔴 P1 | **`PREDICTIVE_LIFT = NOT_PROVEN`** — chưa có edge ex-ante · `POOL_VERDICT` giữ **HOLD** |
| 🔴 P1 | **R6 · R7 · R8 vẫn `NOT_PERFORMED`** · `PURE_CONTEXT_PARTIAL` |
| P1 | Bonferroni là **bảo thủ**; chưa thử FDR (Benjamini–Hochberg) — có thể đổi kết luận «0 sống sót» |
| P1 | cổng báo cáo toàn dải **39/253** — `LEGACY_ADMIN_DEBT` |
| P2 | không gian điều kiện challenger còn hẹp (chỉ `station×prize×position×lag×scope`) |
| P2 | `completed_model_count` giữ số thô ⇒ dòng `13/15 · failed=0` tự trông mâu thuẫn |
| P2 | bất đối xứng log: chỉ đường MN in `[DAY-GOV]` |
| P2 | nhánh `fb.status != 'ACTIVE'` vẫn chưa có dữ liệu thật đi qua |
| ⛔ | `QD-056` `KHÔNG_KẾT_LUẬN_ĐƯỢC` (RM-01) |

### 9.3 · Không có việc nào chặn ở owner

Owner đã chỉ thị dứt điểm cho cả bốn nhánh (UI · historical · branch · challenger). Không có
lựa chọn mơ hồ nào cần owner phân xử (§T6).

---

## §62 — NGUỒN BA LỚP

### `OWNER_SAID`
> *«Xử lý dứt điểm, không tiếp tục lề mề thăm dò đo lường mỗi ngày» · «Không được dùng thêm một
> báo cáo "đo lường" làm sản phẩm cuối nếu không tạo ra hành động sửa, loại bỏ hoặc triển khai
> cụ thể» · «Chọn phương án A: FAST-FORWARD master» · «Không đổi official chỉ vì kết quả 10/09
> tệ»* — 10/09/2026 ~19:45 ICT.

### `CODE_DID`
- `final_bundles` 10/09 — `ranked_numbers[0]` = `95`/`34`/`01`, **đúng bằng** `bach_thu` đã chọn;
  `main_selection_reason = max_ranked_score_after_gate_and_lane_weight`.
- `du-doan.html` `23f1ca69` — `/du-doan` phục vụ **byte-identical**; `_v11177_canon` chạy thật
  trong `node vm`: fixture MT 10/09 cho `[]`, **không** hiện 2 model bị trần.
- `day_governance` — 48 dòng đổi trong 1 transaction; `MT EXCLUDE_PRIMARY` **98 → 50**.
- `daily_evaluation.py` `3c91aba8` — `evaluate_all_history` ném `RuntimeError`,
  `--backfill` `sys.exit(2)`.
- `origin/master` = `origin/HEAD` = `d2a6586`.
- `shadow_candidates` — 1 dòng `output_type='abstain'`, `shadow_only=1`, `output_eligible=0`.
- `crontab` 143 → **148 dòng**.

### `DOC_SAID`
- `FOLLOW_UP_TRACKER:194` — dự báo `wr7 14,3% → 0,0%`. **Đo thật sau backfill: 14,3%** ⇒ dự báo sai.
- V11176 — `SC12_UI_CONSUMER_PARTIAL`, `SC12_HISTORICAL_REPAIR_PENDING`. **Cả hai nay đã đóng.**

**LỆCH BA LỚP:**
1. `DOC_SAID` ≠ `CODE_DID`: sổ dự báo `wr7 → 0,0%`; đo thật **14,3%**. Cả hai đều **dưới nền
   35,2%**, nhưng con số dự báo không đúng.
2. `OWNER_SAID` = `CODE_DID`: *«không đổi official chỉ vì 10/09 tệ»* — số MN/MT/MB **không đổi
   một ký tự** sau toàn bộ phiên.

---

TanPhatAI cần làm: ghi **`V11177`** — `governance_seq 492`, công khai bản này cùng `CONVERSATION_CONTEXT_V11177_20260910.md`. Ghi **BỐN TRẠNG THÁI KẾT THÚC**: `SC12_LIVE_PATH_RUNTIME_PROVEN` · `SC12_HISTORICAL_REPAIR_COMPLETE` · `DEFAULT_BRANCH_STATE_CONFLICT_RESOLVED` · `CONTEXT_ONLY_SHADOW_READY_FOR_NEXT_LIVE`. Ghi **EOD 10/09: THUA cả ba bạch thủ** (`95`/`34`/`01`), **lô2 MN PARTIAL** (`82`); **root cause `RANKING_MISS` cả ba** — số trúng ở hạng **2/4/3** trên 10, hệ chọn **đúng #1 của chính nó** nên **KHÔNG phải SELECTOR/GENERATOR/BUNDLE**. Ghi **phần quan trọng hơn: ranked Top-10 đạt 36,7% vs nền 37,0% = −0,3 điểm — ĐÚNG BẰNG NGẪU NHIÊN**; ở tầng thống kê là **`RANDOM_MISS_WITHOUT_IDENTIFIED_DEFECT`**, và với **n=3** thì **chưa được phép kết luận**. Ghi **UI ĐÃ SẠCH**: `du-doan.html` `76599f6a`→`23f1ca69`, **10/10 assertion JS thật** chạy trên **đúng bytes endpoint phục vụ**, fixture MT 10/09 cho `[]`, **0 restart**, PID `3870722` không đổi. Ghi **historical repair XONG**: **đúng 48 dòng** trong 1 transaction, `MT EXCLUDE_PRIMARY` **98 → 50**, `25/07` không tính là mutation, `07/09` không là candidate, `09/09` giữ EXCLUDE, **digest `final_bundles` lịch sử KHÔNG ĐỔI**. Ghi **cohort sạch cho tin xấu**: 7 lượt MT nay là **01–10/09** (trước là **19–25/06**, trễ 71 ngày), **`wr7` = 14,3% vs nền 35,2% = −20,9 điểm** — **không tô hồng**; sổ dự báo `→ 0,0%` cũng sai. Ghi **`evaluate_all_history` = `RETIRED_FAIL_CLOSED`** (0 cron · 0 route · 0 import), bỏ hẳn nhãn mơ hồ `ISOLATED_NOT_REPAIRED`. Ghi **`master` fast-forward `a4d6636` → `d2a6586`, không force**, `fu438` giữ làm điểm gỡ về. Ghi **CHALLENGER CHẠY THẬT**: payload chỉ gồm **điều kiện có cấu trúc**, cron **13:30 ICT** hằng ngày, ghi `shadow_candidates` với `shadow_only=1 · output_eligible=0`, **0 ghi `final_bundles`/`predictions`**. Ghi **KẾT QUẢ ĐO ĐÁNG GIÁ NHẤT: 8.676 phép thử · ngưỡng Bonferroni z≥4,53 · 0 điều kiện sống sót ở CẢ BA MIỀN** ⇒ challenger `abstain`, và **abstain là output ĐÚNG**. Ghi **nền đo độc lập hôm nay (MN 0,4297 · MT 0,3497 · MB 0,2365) KHỚP gần tuyệt đối với V11170** — kiểm chéo ngoài dự kiến. Ghi **`PREDICTIVE_LIFT = NOT_PROVEN`, `POOL_VERDICT` giữ HOLD**. Ghi **agent ba lần suýt công bố nguyên nhân không có thật** (`GENERATOR_MISS` do parse JSON sai → `SELECTOR_MISS` do dùng đếm phiếu thô thay `ranked_numbers` → «20 điều kiện mạnh» do chưa hiệu chỉnh so sánh bội), **cả ba đều do dùng SAI THƯỚC ĐO**. **Không mở Prompt 44. Không mở Plan mới. Không mở FU mới. Không trộn ERP. Notion KHÔNG cập nhật lượt này.**
