# `NOTION_SYNC_DELTA_PACKET` — cho TanPhatAI

> **Lập:** 12/09/2026 · V11182 · Prompt 43 R1 §X13
> **Agent IDE KHÔNG ghi Notion và KHÔNG tuyên bố Notion đã sync.** §57.1 giữ nguyên.
> Chỉ sync sau khi Owner duyệt gói này.

---

## 1 · CURRENT CONTROL

| trường | giá trị mới |
|---|---|
| Version mới nhất | **V11182** (`governance_seq 497`) |
| Terminal kỹ thuật | `RETIRED_FAMILY_CRON_DISABLED_ZERO_OFFICIAL_IMPACT` + `REUSABLE_CHALLENGER_INFRA_HARDENED` |
| F4 | `F4_DIGIT_ALGEBRA_RETIRED_AFTER_VALID_MEASUREMENT` |
| F5 | `F5_RETIRED_NO_SIGNAL` + `NO_SUCCESSOR_PASSES_PREDEPLOY_GATE` |
| `PREDICTIVE_LIFT` | `NOT_PROVEN` *(không đổi)* |
| `POOL_VERDICT` | `HOLD` *(không đổi)* |
| `SC-12` | `CLOSED · DO_NOT_REOPEN` *(không đổi)* |
| Cron challenger | **ĐÃ TẮT** — 4 dòng comment-out, 0 dòng đang chạy |
| Lời gọi LM/LLM trong phiên | **0** (`v11178_attempts` 149 → 149) |
| Official zero-write | **giữ** — 6 bảng + 7 tệp + digest lịch sử không đổi |
| Restart service | **0** · PID `3870722` · health 200 |

**Câu phải sửa trên Notion nếu đang ghi:** bất kỳ chỗ nào nêu `E[RR]` ngẫu nhiên là
**0,6192 / 0,5345 / 0,4459** — đã rút bằng `RL-040`, giá trị đúng là
**0,6207 / 0,5367 / 0,4487**.

---

## 2 · PROMPT 43 R1 — tiến độ mục

| mục | trạng thái |
|---|---|
| §U | đóng, đã hạ mức (`RL-037`) |
| §V | đóng; `BASE_D1` không đạt natural-proof |
| §W | đóng; V11181 |
| **§X** | **đóng** — X0…X14 đã thực thi; báo cáo V11182 |

Không mở Prompt 44. Không mở FU mới. Không mở Plan mới. Không trộn ERP.

---

## 3 · ACTIVE PLAN

`PLAN-20260723-lottery-doc-restructure` — **không đổi**, không có checkpoint mới.

---

## 4 · PROGRAMS — challenger

**Không còn họ thống kê nào đang được đo.** Năm họ, năm lý do loại:

| họ | trục | loại bằng | con số |
|---|---|---|---|
| `F1` | identity/reverse/complement/plus1 | `G6` | BH-FDR giữ 0/5832 · 0/3888 · 0/1944 |
| `F2` | weekday×station tail frequency | `G6` | 0 qua Bonferroni cả ba miền |
| `F3` | gap/recency | `G9` | lift chỉ **+1,03pp** << 5pp |
| `F4` | digit algebra | `G6` | **0/117.270** qua BH-FDR |
| `F5` | pooled multivariate logistic | effect **ÂM** | **−4,49 / −3,76 / −5,77 pp** |

Hạ tầng challenger **giữ nguyên để dùng lại**. Shadow-only, `output_eligible=0`.

---

## 5 · RUNTIME SNAPSHOT — 12/09/2026

Không có lane nào chạy. Cron challenger đã tắt. Bảng challenger **không đổi**:
`v11178_attempts` 149 · `v11178_challenger_runs` 124 · `v11178_lane_fires` 3 ·
`v11178_challenger_runs_pre_v12` 27.

Official: `final_bundles` 588 · `predictions` 14.767 · `day_governance` 587 ·
`lottery_results` 15.462 · `model_daily_eval` 14.631 · `shadow_candidates` 39.206 —
**tất cả bằng đúng giá trị trong `PRE_X_MANIFEST`**.

---

## 6 · HOME — bốn dòng cần hiển thị

1. **Đã dừng đốt provider cho một hướng không có tín hiệu.** Cron challenger tắt; phiên này
   không gọi một lời gọi LM/LLM nào.
2. **Năm hướng thống kê đã thử và đều chết**, mỗi hướng có con số và điều kiện loại cụ thể.
   Không có hướng kế nhiệm nào vượt cổng lịch sử.
3. **Một phát hiện dùng lại được:** ranker *tập trung* vào đuôi hay ra gần đây **mất độ phủ**
   so với Top-10 trải đều — nên cả mô hình học lẫn baseline tần suất đều **âm**.
4. **Hệ thống official không bị đụng**: 0 ghi, 0 restart, health 200.

---

## 7 · SỔ CẦN CẬP NHẬT

| sổ | mục mới |
|---|---|
| `docs/SO_RUT_LAI.json` | **41 mục** — thêm `RL-040` (công thức `E[RR]`) · `RL-041` (lo3/3-càng) |
| `docs/OWNER_DECISION_LEDGER.json` | **80 mục** — thêm `QD-078` (8 mệnh đề máy kiểm được) |
| `docs/SO_TUONG_TAC_OWNER.md` | +5 mục §X, nguyên văn + giờ |
| `docs/AUTOMATION_STATE.json` | `governance_seq` **497** · `last_version` **V11182** |
| `CHANGELOG.md` · `docs/CURRENT_TRUTH_SSOT.md` | V11182 |

---

## 8 · HAI VIỆC MỞ LẠI ĐƯỢC (trước đây ghi là BỊ CHẶN)

1. **32 nhãn `lo3 WIN` sai** — V11166 ghi P1 *"bị chặn vì phải GHI vào production DB"*.
   Nay xác định được **đúng 32 dòng** (kèm `rowid`, toàn bộ tháng 03/2026) bằng phép chấm
   lại **đọc thuần**. Việc ghi DB trở thành **không cần thiết** nếu chỉ để loại khỏi cohort.
   *Nếu Owner muốn sửa nhãn trong DB thì đó là quyết định riêng, vẫn cần Owner duyệt.*
2. **3-càng chấm được** — không cần thêm cột nào; `final_bundles.lo3` chính là nó.

---

## 9 · THEO DÕI — blocker chính xác, có chủ và có hạn

| blocker | chủ | hạn |
|---|---|---|
| Không có họ challenger nào đang chạy | — | **không phải blocker**: đây là kết luận, không phải việc treo |
| Muốn mở họ mới phải có **trục khác hẳn** (không ánh xạ ô→đuôi, không tần suất/recency, không đại số chữ số, không mô hình gộp trên cùng bộ feature) | Owner quyết hướng | không hạn — chỉ mở khi có giả thuyết mới |
| 32 nhãn `lo3` trong DB vẫn sai (nếu muốn sửa trong DB) | Owner | cần Owner duyệt ghi production |
| Legacy report debt 39/258 | TanPhatAI | luồng riêng, **không chặn** |

**Không có mục nào chờ Owner phân xử kỹ thuật.**

---

TanPhatAI cần làm: cập nhật sáu trang theo đúng bảng delta này; **không** suy thêm ngoài
bảng; nếu Notion đang ghi `E[RR] = 0,6192 / 0,5345 / 0,4459` thì sửa theo `RL-040`.
Agent IDE **chưa** và **sẽ không** tự ghi Notion.
