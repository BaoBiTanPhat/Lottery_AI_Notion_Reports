# BÁO CÁO V11180 — §W P0: action gate · lịch đài canonical · lineage thật · fail-closed

> **Ngày:** 11/09/2026 · **Prompt 43 R1 §W (W0–W7)** · **Commit:** `5d9bdb5` → `ece856f`
> **Bản này là một trong ba bản của cùng một ngày.** Bằng chứng runtime, EOD và terminal ở
> **[`REPORT_V11181.md`](../V11181_W_FAILCLOSED_NATURAL_LANE_20260911/REPORT_V11181.md)**.

---

## 1. Tóm tắt

Sau quyết định W0 (`BASE_D1_LIVE = UNFROZEN_NATURAL_RUN_DIAGNOSTIC_ONLY`), sửa **10 lỗi P0/P1**
trong 68 phút: tách ba quyết định, dựng lịch đài canonical có version, sửa lineage attempt,
gom provider theo tuyến thật, upstream completeness thật, wrapper ba mã thoát, EOD chấm riêng
từng execution class, gói freeze tự kiểm.

## 2. Owner yêu cầu gì — nguyên văn

**11/09/2026 ~13:27 ICT:** *"W1: `exact_tails` KHÔNG đồng nghĩa action-eligible… Không bao giờ
gán `diagnostic_label=ACTIONABLE` chỉ vì `model_decision=RANKED`."* · *"W2: Loại bỏ điều kiện
pre-draw `st_src == ACTUAL_FOR_DATE`."* · *"W4: Không group bằng `model_id` prefix… Không dùng
`COUNT(*)>0`… `NON_TTY_sh` không đủ."* · *"W7: Không group BASE và DELTA thành một Top-K chưa
từng tồn tại."*

Đầy đủ ở `docs/SO_TUONG_TAC_OWNER.md` mục 11/09 và `QD-077`.

## 3. Đào bới / phát hiện

- **`action_eligible` luôn 0 vì lý do SAI.** Điều kiện `st_src == "ACTUAL_FOR_DATE"` **không
  thể đạt trước giờ xổ** vì ngày đó chưa có dòng `lottery_results` nào ⇒ che mất lý do thật.
- **Không có nguồn lịch đài canonical trong backend.** MN/MT có ở `scheduler.py:1604`
  (`_expected_names`); **MB không có bản đồ nào**.
- **Gom provider theo prefix tên là sai** — đo được: 3 model prefix `gpt` đi **OpenRouter** chứ
  không đi OpenAI; `claude-opus-5-fast` cũng đi OpenRouter. Nhóm dài nhất thật sự là
  **9 model tuần tự trên OpenRouter**, không phải "5 model gpt".
- **Attempt ghi giờ **ghi DB** thay vì giờ gọi provider.**
- **`COUNT(*)>0` coi là upstream hoàn tất** — một miền về 1/3 đài cũng `complete=True`.
- **`exit $RC` chỉ mang mã nhánh LLM** — nhánh tất định hỏng thì lane vẫn `rc=0`.
- **EOD gộp BASE + DELTA** thành một Top-K chưa từng tồn tại.

## 4. Hướng xử lý và vì sao chọn

**Trích lịch đài bằng AST, không chép tay.** MN/MT đọc thẳng dict trong `scheduler.py` — chính
bản đồ production dùng để cảnh báo `STATION_INCOMPLETE`. Chép tay tạo mặt thứ hai và nó sẽ trôi.
MB khai báo kèm **xuất xứ từng thứ** và đối chiếu bắt buộc với lịch sử + chốt §W2.4.

**Fail-closed thay vì fail-open.** Wrapper từ chối chạy nếu không có gói freeze hợp lệ (exit 10);
gói freeze tự kiểm 24 trường.

## 5. Đã làm gì — trước / sau

| § | TRƯỚC | SAU |
|---|---|---|
| W1 | `ACTIONABLE if dec != ABSTAIN` | `cong_hanh_dong()` tách 3 quyết định; RANKED cần ≥3 eligible tail |
| W2 | `ACTUAL_FOR_DATE` | `CANONICAL_STATION_SCHEDULE_VERSIONED` (`_v11180_lich_dai.py`) |
| W3 | `now_ict()` lúc ghi DB | `t0`/`t1` thật + `provider_route` + `timeout_s` + `request_fingerprint` + `retry_ordinal` |
| W4.A | prefix `model_id` | `tuyen_provider()` đọc từ mã nguồn |
| W4.B | `COUNT(*)>0` | tập đài canonical + đủ giải + giờ ingest + fingerprint |
| W4.C | `exit $RC` | `llm`/`deterministic`/`composite` + cron origin 4 dấu hiệu |
| W7 | gộp BASE+DELTA | chấm riêng; `NO_CROSS_STAGE_FUSION`; chỉ đọc canonical attempt |

**Lịch đài — ba nguồn độc lập khớp 100%:** `scheduler.py` (AST) · lịch sử 180 ngày · chốt §W2.4.
MN **25/25** · MT **25/25** · MB **25/25**.

**Migration** `_v11180_migrate_w.py` — chỉ `ADD COLUMN`; 86 run / 102 attempt giữ nguyên.

## 6. Cổng kiểm

`_v11180_thu_w.py` **33/33** (16 mục §W5) · `_v11178_thu_v12.py` **51/51** ·
`_v11178_thu_v2_ledger.py` **16/16** · `_v11180_lich_dai.py` **ĐẠT** · §63 **ĐẠT** (seq 495) ·
repo↔VPS **11/11 khớp byte-for-byte**.

**Phép quan trọng nhất:** `W5-3b` bơm điều kiện `VALIDATED_ON_HOLDOUT` ⇒ 3 eligible tail ⇒
`system_action_decision = RANKED`. Nếu thiếu phép này thì `W5-1` vô nghĩa: một cổng luôn trả
`ABSTAIN` cũng sẽ "đạt".

## 7. Vướng vấp

**`RM-10` hai lần, cổng bắt cả hai:** `getattr(gpt_analyzer, "OPENROUTER_MODELS", [])` — tên
không tồn tại, mặc định `[]` khiến nó **trượt im lặng** (tên thật `OPENROUTER_MODELS_SET` dòng
125 và `model_registry.OPENROUTER_MODELS` dòng 1051); cột `final_bundles.final_numbers_json` —
không tồn tại, script sập.

**`RM-09` hai lần:** hai phép test đếm chuỗi `EXEC_LIVE`/`would_save` trên cả tệp, kể cả
docstring mô tả lỗi cũ — sửa bằng `ma_thuan()`/`ma_thuan_sh()`.

**Fixture sai ba lần, cổng đúng cả ba:** 40 ngày → 5 ngày cùng thứ < `MIN_MAU_LICH_SU=8`; đài
giả không khớp lịch canonical; mỗi đài 4 số < `TOI_THIEU_SO_MOI_DAI=10`. **Nới fixture, không
nới ngưỡng.**

**Heredoc nuốt `\n` lần thứ ba**, làm hỏng `_v11180_thu_w.py`.

**`docs/_I2_DA_CHAY.json`** do chính hook cổng commit ghi ra **trong lúc** commit ⇒ worktree
bẩn ngay sau mỗi commit. Xử bằng khai báo `worktree_exclusions` tường minh kèm hash, **không**
nới định nghĩa "sạch".

## 8. Gỡ về

```bash
crontab -l | grep -v _v11178_lane.sh | crontab -
# DB backup truoc migration: /tmp/lottery_ai.db.pre_w
```

## 9. Theo dõi tiếp

Chuyển sang **V11181 mục 9**. Blocker phát hiện giữa lượt chạy và **không sửa vì đã freeze**:
circuit breaker `COST_HIGH` chưa vào tiêu chí roster · `phan_loai_loi` retry vô ích khi circuit
đang đếm ngược · `gpt-oss-120b` trả `RANKED`+`uncertainty=low`+confidence toàn 0.

---

## §62 · NGUỒN BA LỚP

**`OWNER_SAID`** — 11/09 ~13:27: *"Không bao giờ gán `diagnostic_label=ACTIONABLE` chỉ vì
`model_decision=RANKED`."*
**`CODE_DID`** — `cong_hanh_dong()`; đo thật: model đòi RANKED tail `07` confidence 0,9 ⇒
`diagnostic_tails=['07']`, `action_tails=[]`, `system_action_decision=ABSTAIN`.
**`DOC_SAID`** — `CHANGELOG.md §V11180` · `docs/CURRENT_TRUTH_SSOT.md`.

**LỆCH:** `OWNER_SAID` = `CODE_DID` ở cả bốn mục W1/W2/W4/W7 — không còn lệch sau khi vá.

---

TanPhatAI cần làm: ghi **`V11180`** — `governance_seq 495`, `QD-077` với 7 mệnh đề máy kiểm được. Ghi **10 lỗi P0/P1 đã sửa**, trọng tâm là **`action_eligible` trước đây luôn 0 vì một lý do SAI** (`ACTUAL_FOR_DATE` không thể đạt trước giờ xổ), nay chỉ còn **hai lý do THẬT**: `NOT_VALIDATED_ON_HOLDOUT:EXPLORATORY_DISCOVERY_ONLY`=30 và `HOLDOUT_SUPPORT_BELOW_PREREG`=30. Ghi **lịch đài canonical `lottery_station_schedule/2026.09.11-1`** — MN/MT trích **AST** từ `scheduler.py`, MB khai báo kèm xuất xứ; ba nguồn độc lập khớp **25/25** cả ba miền. Ghi **bản đồ tuyến provider thật**: openrouter **9** · google 4 · anthropic 2 · deepseek 2 · openai 2 — gom theo prefix tên là **sai**, 3 model prefix `gpt` đi OpenRouter. Ghi **33/33 test §W5**, trong đó `W5-3b` chứng minh cổng hành động **không phải hằng-số-ABSTAIN**. Ghi **`RM-10` hai lần và `RM-09` hai lần, cổng bắt được**. Ghi **bản này là một trong ba bản cùng ngày** — runtime/EOD/terminal ở **V11181**. **CHƯA sync Notion.**
