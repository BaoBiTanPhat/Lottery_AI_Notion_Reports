# BÁO CÁO V11179 — §V PRE-LIVE HARDENING: 11 lỗi chặn bằng chứng live

> **Ngày:** 11/09/2026 · **Prompt 43 R1 §V** · **Commit:** `eff4a60` → `ece856f`
> **Bản này là một trong ba bản của cùng một ngày.** Bằng chứng runtime đầy đủ, EOD và
> terminal nằm ở **[`REPORT_V11181.md`](../V11181_W_FAILCLOSED_NATURAL_LANE_20260911/REPORT_V11181.md)**.
> V11179 = sửa trước lượt live · V11180 = sửa P0 §W · V11181 = closeout.

---

## 1. Tóm tắt

Sửa **11 lỗi** khiến V11178 có nguy cơ *"cron chạy exit 0 nhưng không tạo bằng chứng live mới"*.
Nặng nhất: so thời gian bằng **chuỗi thô** khiến **100% fact cùng ngày bị loại** — lane
`SAME_DAY_DELTA` về mặt cấu trúc **không bao giờ** có dữ liệu, mà vẫn `exit 0`.

## 2. Owner yêu cầu gì — nguyên văn

**11/09/2026 ~11:18 ICT:** *"Sửa các lỗi làm V11178 có nguy cơ 'cron chạy exit 0 nhưng không
tạo bằng chứng live mới'. Tách dứt khoát preliminary smoke 02:00 khỏi natural live 13:30."*
· *"Không dùng kết quả 11/09 để sửa ngược output đã seal."* · *"Nếu wrapper chỉ tồn tại trên
VPS mà không nằm trong repo: đưa bản canonical vào repo; đối chiếu byte-for-byte."*

Đầy đủ ở `docs/SO_TUONG_TAC_OWNER.md` mục 11/09 và `QD-076`.

## 3. Đào bới / phát hiện

- **§V5 · so chuỗi thô.** `avail >= cut_dt` với `avail` là ISO có offset và `cut_dt` naive.
  `'T'`(0x54) > `' '`(0x20) ⇒ cùng ngày thì ISO-T **luôn** ≥ naive. Đo trên fixture: bản cũ
  **0 fact**, bản mới **4 fact** trên *cùng* dữ liệu.
- **§V2 · smoke/live trùng identity.** `UNIQUE(...stage...)` + `INSERT OR IGNORE`; lượt 02:00
  đã ghi 27 dòng `stage=BASE_D1`, lượt 13:30 cùng khoá ⇒ mọi `INSERT` bị nuốt im lặng.
- **§V5 · `no_lookahead` luôn True** vì condition không hề có khoá `target_date`.
- **§V6 · baseline discovery trùm lên holdout** (đọc 90 ngày gần nhất).
- **§V6 · FDR giữ 0 vẫn đóng dấu `VALIDATED_ON_HOLDOUT`** qua fallback top-40.
- **§V7 · ranker thưởng `+0,05`** cho `DISCOVERY_ONLY`.
- **§V8 · prompt nói dối**: *"không có danh sách số gợi ý"* trong khi payload có `derived_tail`.
- **§V9 · `timeout_s=180` là tham số chết** — 5/5 hàm `_call_*` không nhận timeout.
- **§V3 · lệch lag mang nguyên effect của lag khác** (họ lỗi `RM-21`).
- **§V4 · condition không mang `target_weekday`/`target_station`** ⇒ gộp mù.
- **§V10 · wrapper chỉ tồn tại trên VPS**, không trong repo ⇒ không tái lập được.

**Availability lag=0 đo 120 ngày:** MN trước cutoff MT **377/377** · MT trước cutoff MB
**292/292**. Nhưng MN về **sau 16:38** ở **20/120 ngày** và MT về **sau 17:33** ở **6/120 ngày**.

## 4. Hướng xử lý và vì sao chọn

Giữ **đúng mốc giờ Owner khoá** (13:30 / 16:38 / 17:33), đưa phần **chờ upstream có deadline
cứng** vào trong lane. Dời giờ cron sẽ dễ hơn nhưng phá mốc Owner đã chốt.

## 5. Đã làm gì

`parse_ict()` tz-aware + `cutoff_dt()` datetime đầy đủ · `execution_class` vào khoá UNIQUE +
bảng `v11178_attempts` APPEND-ONLY + luật chuyển trạng thái · exact-lag bắt buộc · condition
mang thứ/đài đích, đánh giá per target station · nền riêng từng cửa sổ · preregistration
artifact có SHA · ranker bỏ `+0,05` · validator kiểm provenance thật · timeout cưỡng chế ở tầng
điều phối · roster lọc bằng thuộc tính (**8 → 19 model**) · wrapper canonical vào repo · payload
prompt cắt về fact được viện dẫn (**381 → 81 KB**).

## 6. Cổng kiểm

`_v11178_thu_v12.py` **51/51** (B1/B2/C5 **không còn rỗng**: MT lag0=4 · MB lag0=8 · C5 đổi 2
candidate, 11 candidate không liên quan bất biến) · `_v11178_thu_v2_ledger.py` **16/16 trên DB
thật** · §63 **ĐẠT** (seq 494) · repo↔VPS **khớp byte-for-byte**.

## 7. Vướng vấp

Gói freeze sinh lúc `12:32:54` **không hợp lệ** — chứa `sh("ssh_khong_ap_dung")`, chỗ bỏ trống
rồi quên, **và đã được trình như bằng chứng đóng băng hợp lệ**. Phát hiện ở phiên §W, xử lý
trong V11180/V11181. Thêm: heredoc nuốt `\n`; ước giờ thay vì đo (tưởng 13:10, thực tế 12:14);
`QD-076` mệnh đề kiểm đếm chuỗi thô (`RM-09`).

## 8. Gỡ về

```bash
crontab -l | grep -v _v11178_lane.sh | crontab -
# DB backup: /tmp/lottery_ai.db.pre_v11178_v12 · bảng v11178_challenger_runs_pre_v12 (27 dòng)
```

## 9. Theo dõi tiếp

Chuyển toàn bộ sang **V11181 mục 9**. Tại thời điểm V11179: `BASE_D1_LIVE` chưa chạy;
`PREDICTIVE_LIFT = NOT_PROVEN`; `POOL_VERDICT = HOLD`.

---

## §62 · NGUỒN BA LỚP

**`OWNER_SAID`** — 11/09 ~11:18: *"Tách dứt khoát preliminary smoke 02:00 khỏi natural live
13:30."*
**`CODE_DID`** — `_v11178_context_only_v11.py:parse_ict()`; migration gắn `PRELIMINARY_SMOKE`
cho 27 dòng cũ, giữ nguyên nội dung kể cả 5 dòng `ERROR`; bảng khoá trước = sau.
**`DOC_SAID`** — `CHANGELOG.md §V11179` · `docs/CURRENT_TRUTH_SSOT.md`.

**LỆCH:** `DOC_SAID` ≠ `CODE_DID` — `REPORT_V11178` nói *"mọi tiền đề kỹ thuật đều đạt"*;
kiểm máy cho ba tiền đề **không đạt** ⇒ `RL-037`.

---

TanPhatAI cần làm: ghi **`V11179`** — `governance_seq 494`, `QD-076`, `RL-037` + `RL-038`. Ghi **11 lỗi đã sửa** với lỗi nặng nhất là **so thời gian bằng chuỗi thô** (`'T'`>`' '` ⇒ 100% fact cùng ngày bị loại, lane `SAME_DAY_DELTA` không bao giờ có dữ liệu mà vẫn `exit 0`). Ghi **roster 8 → 19 model** (đổi từ lọc prefix tên sang lọc thuộc tính, `RL-038`). Ghi **availability lag=0 đo 120 ngày**: MN/MT trước cutoff 377/377 và 292/292, nhưng MN về sau 16:38 ở **20/120 ngày**. Ghi **test 51/51 + 16/16**, B1/B2/C5 **không còn đạt rỗng**. Ghi **bản này là một trong ba bản cùng ngày** — bằng chứng runtime, EOD và terminal ở **V11181**. **CHƯA sync Notion.**
