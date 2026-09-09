# SC-12 · RUNBOOK ĐÃ LÀM CỨNG — V11173 + VA-h12

> **Gói:** `SC-12 = OWNER_APPROVED · MEASUREMENT_ONLY` · Prompt 43 R1 phần Q
> **Lập:** 09/09/2026 · **Thay thế** bản nháp trong scratchpad Windows (đã bị loại theo Q0 mục 1)
> **Trạng thái khi lập:** `CODED_AND_TESTED_NOT_RUNTIME_PROVEN`
>
> ⚠️ **KHÔNG chạy nguyên văn runbook cũ.** Bản cũ có hai lỗi đã được sửa ở đây:
> ① `cd web/backend && …` làm lệch thư mục cho các bước sau ⇒ đường tương đối
> `artifacts/…` giải thành `web/backend/artifacts/…`; ② coi "sau 20:30" là cửa xanh tự động.

---

## 0 · HAI LUẬT CỦA RUNBOOK NÀY

1. **20:30 chỉ là mốc SỚM NHẤT ĐƯỢC XÉT, không phải cửa xanh.** Phải **chứng minh idle**
   (mục 4). Không chứng minh được thì chuyển sang cửa **00:00–05:00** sau khi chạy lại preflight.
   **Không chạy đua cho kịp giờ.**
2. **Không dùng lại receipt cũ.** Ngay trước `--cai-dat` phải **thu lại toàn bộ** PID / start time /
   NRestarts / hash / scheduler snapshot. Phiên chờ lâu ⇒ receipt hết hạn.

---

## 1 · NEO BẤT BIẾN — đóng băng lúc 09/09/2026 20:0x ICT

**Dịch vụ:** PID `3370750` · `NRestarts 0` · `active/running` · health `200` ·
`ExecMainStartTimestamp` = `Fri 2026-09-04 01:08:40 +07` · cwd `/root/Lottery_AI_Test/web/backend`

**Preimage (sha256 đầy đủ, bản LF trên VPS):**

| tệp | sha256 | byte |
|---|---|---|
| `main.py` | `4ed5fd7ebaee8d232177df2e371ca7ad7fc57d829dde503c560ac511a83781cf` | 1.010.551 |
| `database.py` | `fd3d2349ab917c6f36ee8d0a2aa6b82841a963811ba716bc58090c3be566eb16` | 210.868 |
| `daily_evaluation.py` | `42a7c0fcf04450bdf09c604b8f47bd576abfde413daa3edeb31534cac51ca603` | 25.568 |

**Installer (sha256 đầy đủ):**

| tệp | sha256 | byte | test |
|---|---|---|---|
| `artifacts/v11165_h12_patch.py` | `50383fc724dc23fccd9accbe372ba101905493d68807df09da58c3288482f3cb` | 23.924 | **30/30** |
| `artifacts/v11173_sc12_cohort_patch.py` | `7434412ffd3cf76d4c18be55ea4dd6a8e3ae446bce782f786837eae1af91ef6a` | 19.777 | **43/43** |

**Git:** kho local `fu438/admin-only-p0a` @ `20140b6` · kho VPS `master` @ `68f0ea6` (15/06/2026,
**sau 259 commit**).

> **Vì sao `git status` trên VPS báo `M main.py`, `M database.py` mà KHÔNG phải drift lạ:**
> deploy của dự án làm bằng **chép tệp**, không `git pull` (V11171 đã chứng minh: 0 cron
> `git pull`/`fetch`). Checkout VPS là ảnh chụp cũ. **Thước drift đúng là so hash VPS với kho
> local** — đã so: cả ba tệp **khớp** kho local HEAD (`daily_evaluation.py` khớp sau chuẩn hoá LF;
> bản Windows là CRLF nên hash thô khác — đây là ca `RL-023` đã biết).

---

## 2 · FAIL-CLOSED CỦA INSTALLER

`v11173_sc12_cohort_patch.py` **từ chối chạy** nếu bất kỳ điều nào sai:

| chốt | giá trị |
|---|---|
| sha256 nguồn phải nằm trong danh sách nhận diện | `42a7c0fc…ca603` |
| preimage khối `conn` khớp | **đúng 1 lần** |
| preimage khối `WHERE` khớp | **đúng 1 lần** |
| số lần thay thế | **đúng 2** |
| marker `V11173` sau vá | **đúng 3** |
| `NOT EXISTS` thêm vào | **đúng 1** (gốc 0 → sau 1) |
| `JOIN final_bundles` sau vá | **0** |
| biên dịch AST | phải qua |

Idempotent: đã có marker thì **không áp lại**. `r2` dùng **`NOT EXISTS`** thay `LEFT JOIN` —
vị từ thuần, **không bao giờ nhân bản dòng**, và **không có bẫy áp hai lần** như JOIN.

---

## 3 · THỨ TỰ BẮT BUỘC — VA-h12 TRƯỚC, V11173 SAU

Đo trên DB thật, `as_of=2026-09-09` (chỉ đọc):

| kịch bản | dòng | ngày | MT | MN | MB |
|---|---|---|---|---|---|
| hiện nay | 270 | **157** | 83 *(cũ)* | 145 | 42 |
| **chỉ V11173** | 113 | 83 | **12** ⚠️ | 79 | 22 |
| chỉ VA-h12 | 163 | 87 | 62 | 80 | 21 |
| **gộp cả hai** ✅ | 161 | 86 | **61** | 79 | 21 |

**Deploy V11173 một mình kéo cohort MT xuống 12 dòng.** Phải VA-h12 trước để trả lại **49 ngày**
bị loại oan chỉ vì trần cố ý.

---

## 4 · CỔNG IDLE — phải PASS mới được sang mục 5

Lịch trong ngày: `ai_predict` 05:15–17:42 · `t10_chot` 15:40/16:55/17:55 ·
`auto_update`(=`auto_verify`) 16:30–18:34 · `v77`–`v95` 19:00–19:20 ·
`measurement_materialize` tới 20:20 · `du_doan_test_auto` **tới 23:55** ·
cron đêm: `pnl_forward` 22:30 · `consensus_free` 22:35 · `rescue` 22:45 ·
`model_latency` 21:50 · `rule_key` 00:30 · retrain tuần ~02:00.

```bash
set -euo pipefail
cd /root/Lottery_AI_Test

echo "ICT $(TZ=Asia/Ho_Chi_Minh date '+%F %T') · UTC $(TZ=UTC date '+%F %T')"
# 4.1 không có tiến trình python nào ngoài service đang bận
ps -eo pid,etimes,pcpu,cmd --sort=-pcpu | grep -i '[p]ython' | head -10
# 4.2 không job nào vừa chạy trong 5 phút qua và không job nào sắp chạy trong 15 phút tới
sqlite3 -readonly data/lottery_ai.db \
  "SELECT job_name, datetime(log_time,'+7 hours') FROM scheduler_logs \
   WHERE datetime(log_time,'+7 hours') >= datetime('now','+7 hours','-5 minutes') ORDER BY id DESC;"
# 4.3 không writer nào đang giữ DB
ls -la data/lottery_ai.db-wal data/lottery_ai.db-shm 2>/dev/null || echo "khong co wal/shm"
# 4.4 dịch vụ khoẻ
systemctl show -p MainPID,NRestarts,ActiveState,SubState --value lottery
curl -s -o /dev/null -w '%{http_code}\n' http://127.0.0.1:8000/api/health
```

**PASS khi:** không job nào chạy trong 5 phút qua · không mốc cron nào trong 15 phút tới ·
không tiến trình python nặng ngoài service · health 200.
**FAIL ⇒ dừng, chuyển cửa sổ 00:00–05:00.**

---

## 5 · DEPLOY — mọi đường đều TUYỆT ĐỐI, không `cd` rò rỉ

```bash
set -euo pipefail
cd /root/Lottery_AI_Test
PY=/root/Lottery_AI_Test/venv/bin/python3
A=/root/Lottery_AI_Test/artifacts
B=/root/Lottery_AI_Test/web/backend
TS() { echo "[$(TZ=Asia/Ho_Chi_Minh date '+%F %T') ICT | $(TZ=UTC date '+%F %T') UTC]"; }

# 5.0 · receipt TƯƠI ngay trước khi cài
TS; PID0=$(systemctl show -p MainPID --value lottery); echo "PID truoc = $PID0"
systemctl show -p NRestarts,ActiveState,SubState --value lottery
sha256sum "$B/main.py" "$B/database.py" "$B/daily_evaluation.py"

# 5.1 · VA-h12 TRƯỚC — test rồi cài
TS; "$PY" "$A/v11165_h12_patch.py" --test
TS; "$PY" "$A/v11165_h12_patch.py" --cai-dat
sha256sum "$B/main.py" "$B/database.py"
grep -c 'V11165' "$B/main.py" "$B/database.py"
test "$(systemctl show -p MainPID --value lottery)" = "$PID0" || { echo "PID TU DOI — DUNG"; exit 1; }

# 5.2 · V11173 SAU — test rồi cài
TS; "$PY" "$A/v11173_sc12_cohort_patch.py" --test
TS; "$PY" "$A/v11173_sc12_cohort_patch.py" --cai-dat
sha256sum "$B/daily_evaluation.py"
grep -c 'V11173' "$B/daily_evaluation.py"          # phai = 3
grep -c 'JOIN final_bundles' "$B/daily_evaluation.py" || true   # phai = 0
test "$(systemctl show -p MainPID --value lottery)" = "$PID0" || { echo "PID TU DOI — DUNG"; exit 1; }

# 5.3 · cú pháp + import THẬT (subshell — không đổi cwd của bước sau)
TS; "$PY" -c "import ast,io; [ast.parse(io.open(p,encoding='utf-8').read()) for p in ['$B/main.py','$B/database.py','$B/daily_evaluation.py']]; print('AST OK')"
( cd "$B" && "$PY" -c "import daily_evaluation, database; print('import OK')" )

# 5.4 · restart — TÊN SERVICE LÀ `lottery`
TS; systemctl restart lottery
sleep 5
PID1=$(systemctl show -p MainPID --value lottery); echo "PID sau = $PID1"
test "$PID1" != "$PID0" || { echo "PID KHONG DOI — restart that bai"; exit 1; }
systemctl show -p NRestarts,ActiveState,SubState,ExecMainStartTimestamp --value lottery
curl -s -o /dev/null -w 'health=%{http_code}\n' http://127.0.0.1:8000/api/health
journalctl -u lottery --since "2 minutes ago" --no-pager | grep -iE 'traceback|error|importerror' || echo "journal SACH"

# 5.5 · smoke (MANUAL_SMOKE — KHÔNG phải bằng chứng production path)
TS; "$PY" "$A/v11173_sc12_cohort_patch.py" --do --as-of 2026-09-09
```

> ⚠️ Nếu dịch vụ **tự restart** khi mới cài một gói ⇒ **sự cố half-applied**: gỡ về theo mục 6,
> xác minh health + import, **dừng và báo bằng chứng chính xác**.

---

## 6 · GỠ VỀ — thứ tự ngược

```bash
set -euo pipefail
cd /root/Lottery_AI_Test
PY=/root/Lottery_AI_Test/venv/bin/python3
A=/root/Lottery_AI_Test/artifacts
"$PY" "$A/v11173_sc12_cohort_patch.py" --rollback     # kiểm hash == preimage gốc
"$PY" "$A/v11165_h12_patch.py" --rollback
systemctl restart lottery
systemctl show -p MainPID,NRestarts --value lottery
curl -s -o /dev/null -w 'health=%{http_code}\n' http://127.0.0.1:8000/api/health
sha256sum web/backend/main.py web/backend/database.py web/backend/daily_evaluation.py
```

Sao lưu: `daily_evaluation.py.pre_v11173` (V11173 tự tạo) · VA-h12 tự tạo bản sao của nó.

> 🔴 **Gỡ mã KHÔNG phải gỡ dữ liệu.** Nếu `auto_verify` đã chạy tự nhiên sau khi cài, nó **đã ghi
> `day_governance`** bằng logic mới. Gỡ tệp **không** hoàn nguyên các dòng đó. Muốn hoàn nguyên
> đầy đủ phải **khôi phục/tính lại `day_governance`** từ ảnh chụp. **Cấm tuyên bố "rollback hoàn
> chỉnh" nếu mới chỉ khôi phục tệp.**

---

## 7 · BA ĐIỀU PHẢI GHI TRUNG THỰC TRONG BÁO CÁO

1. **Hạng mục 4 loại 0 dòng ở cửa sổ 90 ngày.** Chỉ `evaluate_all_history` (`days_back=9999`)
   mới bị: **376 → 336, loại 40 dòng**. Cấm nói nó sửa được nhiều hơn thế.
2. **Số MT sẽ XẤU ĐI và đó là ĐÚNG.** Hiện "7 lượt gần nhất của MT" là **19/06–25/06** (trễ 76
   ngày). `FOLLOW_UP_TRACKER:194` dự báo `wr7 14,3% → 0,0%` · `top1_7 57,1% → 28,6%`.
   **Không rollback vì số xấu đi** — chỉ rollback vì lỗi kỹ thuật/runtime/no-drift/toàn vẹn dữ liệu.
3. **270 → 161 KHÔNG phải "mất dữ liệu"** — đó là loại bỏ cohort bị kéo lùi sai thời gian.
   **Cấm gộp 161 dòng thành một mẫu dự báo duy nhất**; phải báo n **riêng từng miền**.
4. **`90` bundle vs `40` metric row không mâu thuẫn** — khác grain: 90 là **bundle**
   (90 cặp `(date,region)`), 40 là **metric row** (chỉ `combo-super`, sau lọc status + `day_governance`).

---

## 8 · TRẠNG THÁI KẾT THÚC HỢP LỆ

`BLOCKED_WITH_EXACT_REASONS` · `DEPLOYED_PENDING_SCHEDULED_PROOF` ·
`DEPLOYED_PENDING_CONSUMER_PROOF` · `SC12_RUNTIME_PROVEN`

**`SC12_RUNTIME_PROVEN` chỉ được ghi sau natural `auto_verify` 16:37–18:34 ngày 10/09**, khi
chứng minh được bằng trace/log thật rằng production PID gọi `classify_day_status` đã vá **và**
consumer thật chạy cohort query đã vá. Nếu VA-h12 qua mà consumer V11173 chưa được production path
chạm tới ⇒ ghi `DEPLOYED_PENDING_CONSUMER_PROOF`, **không đóng SC-12**.
