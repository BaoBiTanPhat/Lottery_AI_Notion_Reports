# V11173 — SC-12 PRE-DEPLOY HARDENING · Q0–Q3

> **Gói:** `SC-12 = OWNER_APPROVED · MEASUREMENT_ONLY` — Prompt 43 R1 phần Q
> **Nhận lệnh:** 09/09/2026 **20:05:26 ICT** (13:05:26 UTC) · **Kết thúc:** 20:33 ICT (13:33 UTC)
> **Không deploy · không restart · production KHÔNG đổi một byte**

## ⛔ TRẠNG THÁI KẾT THÚC DUY NHẤT

# `BLOCKED_WITH_EXACT_REASONS`

**Hai lớp blocker độc lập.** Theo §VIII: *«Nếu một mục fail: KHÔNG RESTART. KHÔNG DEPLOY MỘT NỬA.»*

---

## 1 · TÓM TẮT

Q0–Q2 hoàn tất. Q3 **KHÔNG PASS** vì hai chuyện khác nhau, cả hai đều chứng minh được bằng số:

**Blocker A — cửa sổ không chứng minh được idle.** `du_doan_test_auto` chạy **mỗi 5 phút** từ
05:30 tới 23:55, **không có khoảng trống ≥30 phút nào trong cả ngày**. Nó **không nằm trong
crontab** mà đăng ký trong `scheduler.py`, tức chạy **bên trong tiến trình `lottery`** và **ghi
bảng**. `systemctl restart lottery` sẽ **giết nó giữa chừng**.

**Blocker B — VA-h12 KHÔNG CÀI ĐƯỢC.** Lớp phản biện độc lập phát hiện `--cai-dat` của
`v11165_h12_patch.py` là **no-op tự chép chính nó lên chính nó**. **Không một dòng nào** mở
`main.py` hay `database.py` để ghi. Chính tệp đó tự khai `"trang_thai": "CANDIDATE_KHONG_DEPLOY"`.

> 🔴 **Em phải nói thẳng: chính em đã viết bước `--cai-dat` đó vào runbook và đã bỏ sót.** Nếu chạy
> runbook như đã viết, nó in `DA CHEP CANDIDATE PATCH ->` rồi **thoát 0**, em restart dịch vụ và
> **báo cáo "đã deploy VA-h12" trong khi mã production không đổi một byte**. Lớp phản biện cứu
> đúng chỗ này.

---

## 2 · OWNER YÊU CẦU GÌ — NGUYÊN VĂN

| giờ ICT | NGUYÊN VĂN | loại | agent đã làm gì | trạng thái |
|---|---|---|---|---|
| ~13:00 | *«Đọc và thi hành đúng phần "MỆNH LỆNH HIỆN HÀNH · SC-12 MEASUREMENT INTEGRITY REPAIR" từ mục J đến P…»* | `YÊU_CẦU` | Tìm J–P (không có trong kho) → hỏi; owner chọn **thi hành theo phạm vi trong tin nhắn** và **viết+test giờ, deploy tối nay** | `ĐÃ_LÀM` |
| **20:05** | *«[CONTINUATION · PROMPT TỔNG LỰC 43 R1 · PHẦN Q] … V11173 PRE-DEPLOY HARDENING → DEPLOY → SCHEDULED RUNTIME PROOF»* | `YÊU_CẦU` | Q0 làm cứng · Q1 receipt tươi · Q2 chứng minh cohort · Q3 cổng idle → **BLOCKED** | `ĐÃ_LÀM` |

---

## 3 · ĐÀO BỚI / PHÁT HIỆN — Q0 · LÀM CỨNG VÀ ĐÓNG BĂNG RUNBOOK

### 3.1 · Runbook đã chuyển khỏi Windows Temp

`docs/SC12_RUNBOOK_V11173.md` (trong kho, bền vững). Bản nháp trong scratchpad **bị loại**.

**Diff so với runbook cũ — sửa đúng hai lỗi §IV nêu:**

| lỗi bản cũ | bản mới |
|---|---|
| `cd web/backend && …` rồi bước sau dùng `artifacts/…` **giải sai** thành `web/backend/artifacts/…` | **mọi đường TUYỆT ĐỐI** (`A=/root/Lottery_AI_Test/artifacts`); import chạy trong **subshell** `( cd "$B" && … )` |
| coi "sau 20:30" là **cửa xanh tự động** | thêm hẳn **mục 4 · CỔNG IDLE** phải PASS; 20:30 chỉ là **mốc sớm nhất được xét** |
| không có `set -euo pipefail`, không kiểm exit code | có `set -euo pipefail`, `test … \|\| exit 1` sau mỗi bước then chốt |
| không đóng dấu thời gian | hàm `TS()` in **ICT + UTC** cho mọi receipt |
| không neo thư mục | neo `cd /root/Lottery_AI_Test` một lần |

### 3.2 · Đóng băng SHA-256 đầy đủ

**Preimage (bản LF trên VPS, đo 20:0x ICT):**

| tệp | sha256 | byte |
|---|---|---|
| `main.py` | `4ed5fd7ebaee8d232177df2e371ca7ad7fc57d829dde503c560ac511a83781cf` | 1.010.551 |
| `database.py` | `fd3d2349ab917c6f36ee8d0a2aa6b82841a963811ba716bc58090c3be566eb16` | 210.868 |
| `daily_evaluation.py` | `42a7c0fcf04450bdf09c604b8f47bd576abfde413daa3edeb31534cac51ca603` | 25.568 |

**Installer:**

| tệp | sha256 | byte | test |
|---|---|---|---|
| `artifacts/v11165_h12_patch.py` | `50383fc724dc23fccd9accbe372ba101905493d68807df09da58c3288482f3cb` | 23.924 | 30/30 *(xem 5.2 — test này KHÔNG kiểm bản vá thật)* |
| `artifacts/v11173_sc12_cohort_patch.py` | `704cde8880e0449bd54853368cd45ff3b02f456443f9323f358ae35ee70b979b` | 20.385 | **43/43** |

*(V11173 qua ba lần đóng băng trong phiên: `c4eef9e9…` r1 → `7434412f…` r2 → `704cde88…` r2 +
đính chính docstring. Chỉ bản cuối là bản chính thức.)*

**Provenance:** kho local `fu438/admin-only-p0a` @ `20140b6`, worktree **sạch**.
Kho VPS `master` @ `68f0ea6` (15/06/2026), **sau 259 commit**.

### 3.3 · Fail-closed của V11173

| chốt | giá trị | kết quả |
|---|---|---|
| sha256 nguồn trong danh sách nhận diện | `42a7c0fc…ca603` | ✅ |
| preimage khối `conn` / khối `WHERE` | **đúng 1 lần** mỗi khối | ✅ |
| số lần thay thế | **đúng 2** | ✅ |
| marker `V11173` sau vá | **đúng 3** | ✅ |
| `NOT EXISTS` thêm vào | **đúng 1** (gốc 0 → 1) | ✅ |
| `JOIN final_bundles` sau vá | **0** | ✅ |
| idempotent (áp lại lần hai) | không đổi gì | ✅ |
| biên dịch AST | qua | ✅ |

**r2 đổi `LEFT JOIN` → `NOT EXISTS`** theo §VII.3: vị từ thuần, **không bao giờ nhân bản dòng**,
và **không có bẫy áp hai lần** (khối `SAU_JOIN` cũ chứa nguyên văn `TRUOC_JOIN`).

---

## 4 · HƯỚNG XỬ LÝ VÀ VÌ SAO CHỌN

**Không chạy nguyên văn runbook cũ.** §IV cấm tường minh, và hoá ra lệnh đó đúng: bước
`--cai-dat` của VA-h12 là no-op (mục 6.2). Nếu chạy, phiên này đã kết thúc bằng một báo cáo
deploy giả.

**Đổi `LEFT JOIN` → `NOT EXISTS`** thay vì giữ JOIN rồi dựa vào phép đo "0 cặp trùng". Đo đúng
hôm nay không bảo đảm đúng mai; vị từ thuần thì **không bao giờ** nhân bản dòng, bất kể dữ liệu.

**Chốt fail-closed theo sha256 nguồn** thay vì theo số dòng. Vá theo số dòng mù là thứ §V.5 cấm,
và tệp đích còn có bản CRLF ở local — chốt bằng hash loại hẳn rủi ro áp nhầm bản.

**Dừng ở cổng idle thay vì deploy cho kịp giờ.** §IV nói rõ 20:30 là mốc sớm nhất được xét. Đo ra
không có khoảng trống ≥30 phút nào trong ngày ⇒ dừng, không co kiểm tra lại cho vừa cửa sổ.

**Cho một lớp phản biện độc lập soi trước khi deploy.** Bốn góc chạy song song, chỉ đọc. Chính
lớp này bắt được blocker P0 mà agent chính bỏ sót — đó là lý do nó tồn tại.

**Không tự quyết câu hỏi phạm vi `final_bundles`.** Owner khoá "CẤM sửa Combo/FINAL"; VA-1/VA-2
ghi vào `final_bundles`. Agent **không** được tự diễn giải cho qua.

---

## 5 · ĐÃ LÀM GÌ — Q1 · XÁC MINH TRÊN EXACT CURRENT STATE

**Receipt tươi, đo 20:05:26 ICT / 13:05:26 UTC:**

| mục | giá trị |
|---|---|
| MainPID | `3370750` |
| PID start | `Fri 2026-09-04 01:08:40 +07` |
| NRestarts | `0` |
| ActiveState / SubState | `active` / `running` |
| health | `200` |
| cwd của PID | `/root/Lottery_AI_Test/web/backend` |
| FragmentPath | `/etc/systemd/system/lottery.service` |

**Drift — GIẢI THÍCH ĐƯỢC, không phải drift lạ:**

`git status` trên VPS báo `M main.py`, `M database.py`. **Nhưng checkout VPS đứng ở commit
15/06/2026, sau 259 commit** — vì deploy làm bằng **chép tệp**, không `git pull` (V11171 đã chứng
minh 0 cron `git pull`/`fetch`). ⇒ **`git diff` trên VPS KHÔNG phải thước dò drift.**

Thước đúng — so hash VPS với kho local HEAD `20140b6`:

| tệp | local raw | local LF | VPS | kết luận |
|---|---|---|---|---|
| `main.py` | `4ed5fd7e…` | `4ed5fd7e…` | `4ed5fd7e…` | ✅ **khớp** |
| `database.py` | `fd3d2349…` | `fd3d2349…` | `fd3d2349…` | ✅ **khớp** |
| `daily_evaluation.py` | `357641b7…` | **`42a7c0fc…`** | `42a7c0fc…` | ✅ **khớp sau chuẩn hoá LF** (bản Windows là CRLF — ca `RL-023` đã biết) |

⇒ **Không có drift chưa rà.** Tested preimage == current.

**Test chạy lại trên exact current target:** V11173 **43/43 ĐẠT** · VA-h12 **30/30 ĐẠT**
*(nhưng xem 5.2 — 30/30 đó không kiểm cái mà nó tự nhận là đang kiểm)*.

---

## 6 · CỔNG KIỂM — Q2 · QUERY / COHORT / DB PROOF

### 6.1 · Bốn kịch bản, `as_of=2026-09-09`, tái lập độc lập

| kịch bản | dòng | ngày | MT | MN | MB |
|---|---|---|---|---|---|
| current | 270 | **157** | 83 *(cũ)* | 145 | 42 |
| chỉ V11173 | **113** | 83 | **12** ⚠️ | 79 | **22** |
| chỉ VA-h12 | 163 | 87 | 62 | 80 | 21 |
| gộp cả hai | 161 | 86 | 61 | 79 | 21 |

**Membership diff so với số handoff (chụp ~13:00) — chỉ MỘT dòng, giải thích được:**

```
+ ADDED  2026-09-09  MB  status=LOSE
  lý do: auto_verify chấm ngày 09/09 (verified_at 18:32:34) SAU khi handoff chụp
  grain: (date, region) · không phải lỗi tính, là DB lớn tự nhiên
```

handoff `112/82 · MB 21` → live `113/83 · MB 22`. Mọi ô khác **y hệt**.

### 6.2 · Kiểm bắt buộc theo §VII

| # | phép kiểm | kết quả |
|---|---|---|
| 1 | grain khai báo của metric query | **metric row** = 1 dòng `predictions` của `combo-super` sau lọc status + `day_governance` |
| 2 | nhân bản dòng do `final_bundles` nhiều version/status | **0** — `LEFT JOIN` cho `join=376 = base=376`; `final_bundles` có `UNIQUE(date,region)`; **582/582 dòng đều `ACTIVE`** |
| 3 | ưu tiên `NOT EXISTS` | ✅ **r2 đã đổi sang `NOT EXISTS`** |
| 4 | row count trước/sau JOIN | 376 → 376 (không tăng); `NOT EXISTS` **chỉ loại bớt**: 376 → 336 |
| 5 | biên lịch | **D0 trong · D89 trong · D90 ngoài** · `Asia/Ho_Chi_Minh` · ngày hỏng **ném lỗi (fail-closed)** · `days_back=0` không nổ · năm nhuận OK · qua nửa đêm VN OK |
| 6 | đối soát «90 bundle» vs «40 metric row» | **không mâu thuẫn** — 90 = grain **BUNDLE** (90 cặp `(date,region)` riêng biệt); 40 = grain **METRIC ROW** |
| 7 | `days_back=90` loại 0 dòng backfill | ✅ **0** — mốc chặn 90 ngày đã tự bỏ qua backfill 28/02–29/03 |
| 8 | `days_back=9999` → 375→335, loại 40 | ✅ **376 → 336, loại 40** (376 chứ không 375: +1 dòng ngày 09/09) |
| 9 | MT `wr7` đang dùng 19/06–25/06 | ✅ **tái lập đúng** — 7 lượt gần nhất: 25/06 · 24/06 · 23/06 · 22/06 · 21/06 · 20/06 · **19/06** |
| 10 | 7 ngày MT hợp lệ sau vá gộp | ⛔ **chưa xuất được** — xem 6b.3, con số này **không tự xuất hiện** từ deploy |

**Kế hoạch truy vấn (`EXPLAIN QUERY PLAN`, phản biện chạy độc lập):** bản SAU dùng
`SEARCH p (date>?)` + tra 1 điểm trên `UNIQUE index` của `final_bundles` — **không sinh
full-table-scan**, và **RẺ HƠN** bản TRƯỚC (bản cũ phải `SCAN` toàn bộ 14.605 dòng).

**`LIMIT 270` sau khi khoá ngày là trần không bao giờ chạm** — được **schema** bảo đảm:
`UNIQUE(date, target_region, ai_model)` ⇒ tối đa 3 dòng/ngày. Kiểm 0/14.605 dòng vi phạm.

---

## 6b · Q3 — CỔNG PRE-DEPLOY: KHÔNG PASS

### 6b.1 · Blocker A — cửa sổ không chứng minh được idle

Đo lúc **20:14:46 ICT**:

| phép | kết quả |
|---|---|
| tiến trình python nặng ngoài service | ✅ 0 |
| **job chạy trong 5 phút qua** | ❌ **`du_doan_test_auto` lúc 20:10** |
| mốc cron trong 15 phút tới | ✅ 0 |
| **WAL/SHM tồn đọng** | ❌ **`-shm` 32 KB sửa lúc 20:14 — writer đang giữ DB** |
| health / ActiveState | ✅ 200 / active |

**Vì sao không thể chờ tới lúc idle trong ngày:**

`du_doan_test_auto` có **178 mốc riêng biệt hôm nay**, từ **05:30 tới 20:15**, đều **cách nhau đúng
5 phút**. Quét toàn ngày: **KHÔNG có khoảng trống ≥30 phút nào**. Nó **không nằm trong crontab** —
đăng ký trong `scheduler.py:7196-7236`, tức **chạy bên trong tiến trình `lottery`** và **ghi bảng**
(`_materialize_adaptive_exploit_v1`). ⇒ `systemctl restart lottery` **giết nó giữa chừng**.

Khung 00:00–05:00 ngày 08/09 chỉ có **1 dòng log**. ⇒ **Cửa sổ khả thi duy nhất: 00:35–04:45**
(sau `rule_key_registry` 00:30, trước `free_predict` 05:00).

### 6b.2 · Blocker B — VA-h12 KHÔNG CÀI ĐƯỢC (P0)

Bằng chứng đọc thẳng từ `v11165_h12_patch.py`:

```python
DICH = "/root/Lottery_AI_Test/artifacts/v11165_h12_patch.py"   # chính đường dẫn của nó
ap.add_argument("--cai-dat", help="chep chinh no vao artifacts/v11165_h12_patch.py")
if a.cai_dat:
    src = io.open(os.path.abspath(__file__)).read()
    io.open(DICH, "w").write(src)          # ← TỰ CHÉP LÊN CHÍNH MÌNH
    print("DA CHEP CANDIDATE PATCH ->", DICH)
KQ = {"trang_thai": "CANDIDATE_KHONG_DEPLOY", ...}   # ← tự khai KHÔNG để deploy
```

Quét toàn tệp: **0 dòng** mở `main.py` hoặc `database.py` để ghi.

**Ba hệ quả, đều xác minh được:**

**① `30/30 test` không kiểm cái nó tự nhận là đang kiểm.** Nó kiểm **ba hàm thuần tái dựng lại**
(`tach_ke_toan`, `classify_bundle_quality_v2`, `classify_day_status_v2`) — **không** kiểm bản vá
thật vào `main.py`/`database.py`, vì bản vá đó **không tồn tại**.

**② Khối `TRƯỚC/SAU` là mô tả, không phải mã dán được.** **6 dòng chứa `...`**. Riêng khối `SAU`
của VA-3 kết thúc bằng `...  # reason ghi ro phan nao la cap co y` — **thiếu hẳn dòng gán `reason`**
mà `database.py:5113-5115` sau đó dùng để ghi `day_governance.degradation_reason`.
⇒ **Chép tay theo đúng văn bản đó sẽ khiến `classify_day_status` nổ** — và nó được gọi **đồng bộ
cho cả ba miền** tại `auto_verify` (`scheduler.py:1670/1739/1811`).

**③ `--replay` không tái lập được nữa.** Clone `artifacts/v11165_immutable.db` mà nó tham chiếu
**đã bị xoá** (đợt dọn đĩa V11166). Mọi con số «replay lịch sử» của VA-h12 hiện là **NOT PROVEN**.

### 6b.3 · Blocker B phụ — thiếu bước backfill, số «161/86/MT 61» sẽ KHÔNG xuất hiện

`classify_day_status` chỉ được gọi với **`today`**:

```
scheduler.py:1670  _cds(today, "MN", source='auto_verify')
scheduler.py:1739  _cds(today, "MT", source='auto_verify')
scheduler.py:1811  _cds(today, "MB", source='auto_verify')
```

Production **không bao giờ xếp loại lại ngày quá khứ**. Con số **161/86/MT 61** là **mô phỏng
offline** áp logic mới cho toàn bộ 156 ngày lịch sử. Muốn nó thành thật phải chạy
**`web/backend/backfill_day_governance.py`** (tệp **có tồn tại**, 1.713 byte) — và **runbook 6 bước
của em KHÔNG có bước này**. ⇒ Nếu deploy rồi công bố 161/86, đó sẽ là **con số sai**.

### 6b.4 · Blocker B phụ — câu hỏi phạm vi cần owner phân xử

VA-1/VA-2 nằm trong `generate_final_bundle()` và **ghi 6–7 khoá mới** vào
`final_bundles.source_predictions_json`, đồng thời **đổi giá trị `incomplete_bundle`** cho ngày MT
bị cap. `final_bundles` là **1 trong 4 bảng khoá**, và **"Combo/FINAL"** nằm trong danh sách
**CẤM** của SC-12.

Số dự đoán công bố **không đổi** (bầu chọn giữ nguyên), nhưng **bản ghi bundle thì đổi**.
⇒ **Không thể tự suy diễn là "chấp nhận được"**. Cần owner phân xử tường minh.

---

## 7 · VƯỚNG VẤP

| # | vấp | ai bắt | gỡ |
|---|---|---|---|
| 1 | 🔴 **Runbook của em có bước `--cai-dat` là NO-OP** — sẽ tạo ảo giác deploy thành công | **lớp phản biện (góc 3 + góc 4, độc lập)** | dừng deploy; VA-h12 phải viết lại thành installer thật kiểu V11173 |
| 2 | 🔴 Em coi "sau 20:30" là cửa khả thi | §IV của prompt + phép đo | đo nhịp job: **không có khoảng trống ≥30 phút** trong cả ngày |
| 3 | 🟠 Bản nháp V11173 viết `datetime.timezone(...)` — `daily_evaluation.py:16` chỉ có `from datetime import datetime, timedelta`, `datetime` là **lớp không phải module** ⇒ **sẽ nổ lúc chạy** | test B6 của chính em | dùng đúng idiom tệp đang dùng ở `:547`/`:629` |
| 4 | 🟠 Docstring V11173 ghi **"không ghi DB"** — **KHÔNG chính xác** | phản biện góc 4 | **đã đính chính trong tệp**: `evaluate_day()` (`:419`) `INSERT OR REPLACE INTO daily_eval_log` theo cohort mới; `run_daily_eval` được scheduler gọi (`:1836`, `:9264`) ⇒ **là thay đổi DỮ LIỆU** |
| 5 | 🟡 Ba hằng số kỳ vọng trong test của em sai (marker=5, `NOT EXISTS`=1 tuyệt đối, idempotent bằng replace thô) | chính bộ test | sửa thành 3 · đo **delta** · chốt bằng marker |
| 6 | 🟡 Chú thích của em chứa chuỗi `NOT EXISTS (` làm phép đếm tự dính | test B6 | đổi lời chú thích |

---

## 8 · GỠ VỀ

**Không có gì để gỡ.** Phiên này **không cài, không restart, không ghi DB, không sửa tệp nào trong
`web/backend`**. `PID 3370750` · `NRestarts 0` · health `200` **không đổi** suốt phiên (đo lại lúc
20:33 ICT).

> 🔴 **Ghi để lần sau không nhầm:** gỡ **mã** không phải gỡ **dữ liệu**. Nếu `auto_verify` hoặc
> `run_daily_eval` đã chạy tự nhiên sau khi cài, chúng **đã ghi** `day_governance` / `daily_eval_log`
> bằng logic mới. Gỡ tệp **không** hoàn nguyên các dòng đó. **Cấm tuyên bố "rollback hoàn chỉnh"
> nếu mới chỉ khôi phục tệp.**

---

## 9 · THEO DÕI TIẾP — MA TRẬN NỢ CÒN LẠI

### Chặn deploy (phải xử trước khi có thể sang Q4)

| # | việc | mức | ai |
|---|---|---|---|
| 1 | **Viết lại VA-h12 thành installer THẬT** kiểu V11173: văn bản `TRƯỚC/SAU` đầy đủ **không elide**, chốt sha256 nguồn, đếm khớp, compile-check, backup, rollback | **P0** | agent |
| 2 | **Bổ sung dòng gán `reason`** còn thiếu trong khối `SAU` của VA-3 | **P0** | agent |
| 3 | **Owner phân xử**: VA-1/VA-2 ghi khoá mới vào `final_bundles.source_predictions_json` (bảng khoá; "FINAL" trong danh sách CẤM) — có nằm trong phạm vi SC-12 không? | **P0** | **owner** |
| 4 | **Thêm bước `backfill_day_governance.py`** vào runbook, kèm ảnh chụp `day_governance` trước khi chạy | **P1** | agent |
| 5 | Dời deploy sang **00:35–04:45**, thu **receipt tươi** ngay trước khi cài | **P1** | agent |

### Đã biết, không chặn deploy

| # | việc | mức |
|---|---|---|
| 6 | `LIKE '%Phase 1.5 backfill%'` **rộng hơn** ngữ nghĩa `notes=`; hiện 90/90 khớp chính xác nên chưa hại | P3 latent |
| 7 | Nhánh `fb.status != 'ACTIVE'` **chưa từng được dữ liệu thật đi qua** (582/582 đều ACTIVE) — hành vi là suy luận, chưa có bằng chứng runtime | P3 `INDETERMINATE` |
| 8 | `evaluate_all_history` (**chỉ CLI thủ công**, không cron/route) sẽ mất phủ từ ~87% xuống ~46% lịch sử, vì `evaluate_day()` **hardcode `days_back=90`** | P2 |
| 9 | Clone `v11165_immutable.db` đã bị xoá ⇒ số «replay lịch sử» của VA-h12 **NOT PROVEN** | P3 |

---

## 10 · BẢNG BẰNG CHỨNG

| hạng mục | DIRECT_GITHUB | HANDOFF | VPS_RUNTIME | INFERENCE |
|---|---|---|---|---|
| V11173 43/43 test | — | ✅ | ✅ chạy trên exact current target | — |
| VA-h12 30/30 test | — | ✅ | ✅ chạy được | ⚠️ **chỉ kiểm hàm thuần, không kiểm bản vá thật** |
| preimage 3 tệp | ✅ khớp local HEAD `20140b6` | ✅ | ✅ | — |
| cohort 4 kịch bản | — | ✅ | ✅ tái lập độc lập trên DB thật | — |
| membership diff +1 dòng | — | — | ✅ | — |
| `EXPLAIN QUERY PLAN` | — | — | ✅ (phản biện chạy độc lập) | — |
| `--cai-dat` là no-op | — | — | ✅ **đọc thẳng mã nguồn** | — |
| `classify_day_status(today)` | — | — | ✅ `scheduler.py:1670/1739/1811` | — |
| cửa sổ idle | — | — | ✅ 178 mốc, cách 5 phút | — |
| **runtime proof SC-12** | — | — | ❌ **CHƯA CÓ** | — |

> Theo §III: V11173 ghi **`HANDOFF_PROVIDED · GITHUB_NOT_INDEXED`** cho tới khi đọc được exact
> artifact trên GitHub. Bản này **chưa** nâng bất kỳ claim nào thành GitHub-verified.

---

## 11 · RESUME RECEIPT — cho lượt tiếp theo cùng Prompt 43 R1

```
TRANG THAI      : BLOCKED_WITH_EXACT_REASONS
MOC             : 2026-09-09 20:33 ICT / 13:33 UTC
PRODUCTION      : PID 3370750 · NRestarts 0 · active/running · health 200 · KHONG DOI
PREIMAGE        : main.py 4ed5fd7e… · database.py fd3d2349… · daily_evaluation.py 42a7c0fc…
INSTALLER SAN   : artifacts/v11173_sc12_cohort_patch.py sha256 704cde8880e0449bd54853368cd45ff3b02f456443f9323f358ae35ee70b979b (20385 byte, 43/43)
INSTALLER THIEU : VA-h12 CHUA CO installer that — PHAI VIET LAI
RUNBOOK         : docs/SC12_RUNBOOK_V11173.md (da lam cung, CHUA co buoc backfill)
CUA SO DEPLOY   : 00:35–04:45 ICT (duy nhat chung minh duoc idle)
CHAN O OWNER    : VA-1/VA-2 ghi vao final_bundles.source_predictions_json — "FINAL" trong danh sach CAM
VIEC KE TIEP    : (1) viet lai VA-h12 thanh installer that + bu dong `reason`
                  (2) owner phan xu pham vi final_bundles
                  (3) them buoc backfill_day_governance.py vao runbook
                  (4) thu receipt TUOI roi moi cai trong cua so 00:35–04:45
CAM             : khong deploy mot nua · khong restart khi chua PASS het cong
```

---

## §62 — NGUỒN BA LỚP

### `OWNER_SAID`
> *«[CONTINUATION · PROMPT TỔNG LỰC 43 R1 · PHẦN Q] … DO_NOT_EXECUTE_THE_PASTED_RUNBOOK_UNCHANGED
> … 20:30 là earliest consideration, không phải automatic green gate … Nếu một gate kỹ thuật không
> đạt, tự dừng và báo BLOCKED_WITH_EXACT_REASONS»* — 09/09/2026 20:05 ICT.

### `CODE_DID`
- `v11165_h12_patch.py:45` `DICH` = chính đường dẫn của nó; `--cai-dat` = `io.open(DICH,"w").write(src)`
  ⇒ **no-op**. `"trang_thai": "CANDIDATE_KHONG_DEPLOY"`.
- `scheduler.py:1670/1739/1811` — `_cds(today, …)`, **không bao giờ ngày quá khứ**.
- `scheduler.py:7196-7236` — `du_doan_test_auto` đăng ký trong service, **không** ở crontab.
- `daily_evaluation.py:419` — `INSERT OR REPLACE INTO daily_eval_log`;
  `scheduler.py:1836`/`:9264` gọi `run_daily_eval`.
- `web/backend/backfill_day_governance.py` **tồn tại** (1.713 byte) — **thiếu trong runbook**.
- `final_bundles`: `UNIQUE(date,region)`, **582/582 dòng `ACTIVE`** ⇒ `LEFT JOIN` không nhân bản
  (`join=376 = base=376`).
- VPS 20:33 ICT: PID `3370750` · `NRestarts 0` · health `200`.

### `DOC_SAID`
- `docs/FOLLOW_UP_TRACKER.md:183` — *«`SC-12` kế toán MT (**VA-h12**, 30/30 test, replay đổi đúng
  45 dòng)»* trong **NHÓM A — đã có vá, chờ owner ký**.
- `docs/FOLLOW_UP_TRACKER.md:194` — dự báo `wr7 14,3%→0,0%` · `top1_7 57,1%→28,6%`.
- `docs/SC12_RUNBOOK_V11173.md` (bản này lập) — runbook đã làm cứng.

**LỆCH BA LỚP — phải báo:**
1. `DOC_SAID` ≠ `CODE_DID`: sổ ghi VA-h12 **"đã có vá, chờ owner ký"**, hàm ý chỉ cần ký là cài
   được. `CODE_DID`: **không có bản vá nào cài được** — chỉ có phân tích ứng viên tự khai
   `CANDIDATE_KHONG_DEPLOY`. **Sổ đang mô tả một thứ không tồn tại ở dạng đó.**
2. `DOC_SAID` ≠ `CODE_DID`: docstring V11173 (do em viết) ghi **"không ghi DB"**; `CODE_DID`:
   `evaluate_day()` **ghi** `daily_eval_log`. **Đã đính chính trong tệp.**
3. `OWNER_SAID` ≠ khả thi: owner khoá scope **CẤM sửa "Combo/FINAL"**, nhưng VA-1/VA-2 **ghi vào
   `final_bundles`**. Hai điều này **không thể cùng đúng** — cần owner phân xử.

---

TanPhatAI cần làm: ghi **`V11173`** — `governance_seq 488`, công khai bản này cùng `CONVERSATION_CONTEXT_V11173_20260909.md`. Ghi **TRẠNG THÁI DUY NHẤT = `BLOCKED_WITH_EXACT_REASONS`**, **KHÔNG deploy, KHÔNG restart, production KHÔNG đổi một byte** (PID 3370750 · NRestarts 0 · health 200 suốt phiên). Ghi **BLOCKER A: cửa sổ không chứng minh được idle** — `du_doan_test_auto` **178 mốc, cách nhau 5 phút, 05:30→23:55, KHÔNG có khoảng trống ≥30 phút nào**, và nó **chạy TRONG tiến trình `lottery`** (`scheduler.py:7196`, không ở crontab) nên restart sẽ giết giữa chừng ⇒ cửa sổ duy nhất là **00:35–04:45**. Ghi **BLOCKER B (P0): `v11165_h12_patch.py --cai-dat` là NO-OP tự chép chính nó** (`DICH` = chính đường dẫn của nó), **0 dòng ghi vào `main.py`/`database.py`**, và tệp **tự khai `CANDIDATE_KHONG_DEPLOY`** ⇒ **VA-h12 KHÔNG CÀI ĐƯỢC**; **`30/30 test` chỉ kiểm ba hàm thuần tái dựng, KHÔNG kiểm bản vá thật**; khối `TRƯỚC/SAU` **có 6 dòng `...` elide** và khối `SAU` của VA-3 **thiếu dòng gán `reason`** — chép tay sẽ làm `classify_day_status` nổ cho **cả ba miền** tại `auto_verify`. Ghi **agent TỰ NHẬN chính mình đã viết bước `--cai-dat` đó vào runbook và bỏ sót; lớp phản biện độc lập bắt được**. Ghi **số «gộp cả hai 161/86/MT 61» SẼ KHÔNG tự xuất hiện** — `classify_day_status` chỉ được gọi với `today` (`scheduler.py:1670/1739/1811`), production **không xếp loại lại ngày quá khứ**; phải chạy **`backfill_day_governance.py`** (tệp CÓ tồn tại) mà **runbook đang thiếu bước này**. Ghi **CÂU HỎI PHẠM VI CHẶN Ở OWNER: VA-1/VA-2 ghi 6–7 khoá mới vào `final_bundles.source_predictions_json`** — bảng khoá, và **"Combo/FINAL" nằm trong danh sách CẤM của SC-12**; số dự đoán không đổi nhưng bản ghi bundle thì đổi ⇒ **không tự suy diễn là chấp nhận được**. Ghi **ĐÍNH CHÍNH: docstring V11173 nói "không ghi DB" là SAI** — `evaluate_day()` (`daily_evaluation.py:419`) `INSERT OR REPLACE INTO daily_eval_log` theo cohort mới, `run_daily_eval` được scheduler gọi (`:1836`, `:9264`) ⇒ **là thay đổi DỮ LIỆU**, và **rollback CODE không hoàn tác dòng đã ghi**. Ghi **V11173-r2 đã làm cứng**: đổi `LEFT JOIN` → **`NOT EXISTS`**, fail-closed theo sha256 nguồn, **43/43 test ĐẠT**, biên lịch **D0 trong · D89 trong · D90 ngoài**, ngày hỏng **fail-closed**. Ghi **drift GIẢI THÍCH ĐƯỢC**: `git status` VPS báo `M` vì checkout đứng ở commit 15/06, **sau 259 commit** (deploy bằng chép tệp); thước đúng là so hash — **cả ba tệp khớp kho local HEAD `20140b6`**. Ghi **membership diff chỉ MỘT dòng** (`2026-09-09 MB`), **90 bundle vs 40 metric row KHÔNG mâu thuẫn** (khác grain), **`days_back=90` loại 0 dòng · `days_back=9999` 376→336 loại 40**. **Code KHÔNG đi trước tài liệu.** **Không mở Prompt 44. Không mở Plan mới. Không mở FU mới. Không trộn ERP.**
