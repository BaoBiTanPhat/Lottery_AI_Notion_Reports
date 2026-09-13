# NOTION_SYNC_DELTA_PACKET — V11183 · 13/09/2026

> **Agent IDE KHÔNG ghi Notion** (§57.1 khoá chỉ-đọc) và **không tuyên bố Notion đã sync**.
> Gói này là **đầu vào cho TanPhatAI**. Mọi dòng dưới đây là delta so với trạng thái sau V11182.

---

## A. TRẠNG THÁI KHOÁ — giữ nguyên, không đổi

| khoá | giá trị | đổi? |
|---|---|---|
| `SC12` | `CLOSED · DO_NOT_REOPEN` | không |
| `MATERIALIZATION_OPTION` | `B` | không |
| `OUTPUT_COUNTERFACTUAL_RANK_PRODUCTION_WRITE` | `FORBIDDEN` | không |
| `FINAL_BUNDLES_ZERO_WRITE` | còn hiệu lực | không |
| `PREDICTIVE_LIFT` | `NOT_PROVEN` | không |
| `POOL_VERDICT` | `HOLD` | không |

**Cảnh báo dùng từ:** `NOT_PROVEN` ≠ `PROVEN_ABSENT`. Phiên này chứng minh **không phát hiện
lift** trên 198 ngày, nhưng cũng chứng minh phép đo **chỉ loại trừ được** lift > +6.88 (MN) /
+8.03 (MT) / +4.77 (MB) điểm. Đừng nâng nhãn.

---

## B. SÁU TERMINAL MỚI — ghi vào trang trạng thái

| # | terminal | giá trị |
|---|---|---|
| A | hôm nay, vận hành | `OPERATIONAL_CLEAN_WITH_PROVIDER_BILLING_OUTAGE` |
| B | hôm nay, dự báo | `NO_LIFT_DETECTED_UNDERPOWERED` |
| C | căn nguyên chính | **`GENERATOR_MISS`** |
| D | retrain (FU-430) | `RETRAIN_ACTIVATED_METRIC_NOT_COMPARABLE` |
| E | optimizer | `OPTIMIZER_OBJECTIVE_DEFECTIVE_AND_GATE_ABSENT` |
| F | hành động tiếp | `QD-079` chờ duyệt + khai tử bộ thử V1.1 |

**`FU-430` ĐÓNG** bằng terminal D. Không kéo sang checkpoint thứ tư.

---

## C. NHÁNH BỊ ĐÓNG — quan trọng nhất của gói này

**`RANKER_V2_LINEAGE_DEDUP_CALIBRATED` — KHÔNG MỞ.**

Lý do: căn nguyên đã chứng minh là **generator miss**, không phải ranker miss. Pool 13.4
đuôi/ngày không phân biệt được với bốc ngẫu nhiên (MN z=+0.32 · MT z=+1.16 · MB z=+0.14 trên 198
ngày, nền siêu bội đúng grain), và ranker so với **bốc từ chính pool** cũng không thêm gì
(p ≥ 0.30 cả ba miền).

Con số **"RANKER_MISS 92–94%"** trong các bản trước **không phải chẩn đoán một khiếm khuyết sửa
được** — đó đúng bằng thứ một thứ tự ngẫu nhiên sinh ra. **Đừng mở lại nhánh này ở phiên sau.**

---

## D. HAI MỤC RÚT LẠI → `docs/SO_RUT_LAI.json`

| mã | câu bị rút | điều đúng |
|---|---|---|
| **RL-042** | *"Hai trong ba miền có lift ÂM và vẫn ghi đè lên production"* / *"69/69 tổ hợp đều âm, không tồn tại bộ weights nào hơn nền"* | Con số đúng như mã tính; **diễn giải** sai. Nền của mã phồng +12.70/+12.46/+8.36pp. Nền đúng cho MN **+10.07** · MT **+7.91** · MB **+17.92**. Nhưng không ô nào chứng minh lift (bên `ĐÃ_HỌC` đã qua chọn 69 lần) |
| **RL-043** | *"Bạch thủ bundle bằng đúng nền ngẫu nhiên ở cả ba miền"* | Đọc không-bác-bỏ thành chứng minh H₀ (RM-04). Đúng: **không phát hiện lift**, chỉ loại trừ được lift > +6.88/+8.03/+4.77pp; cần 846/800/655 ngày để bắt +5pp |

Cả hai đều là câu của **Agent IDE trong phiên 13/09**, chưa vào báo cáo nào, chưa sinh quyết định
nào.

---

## E. `QD-079` → `docs/OWNER_DECISION_LEDGER.json`, trạng thái **`CHỜ_OWNER`** (KHÔNG phải ACTIVE)

**Tiêu đề:** Sửa objective và dựng cổng ghi cho weight optimizer

**Ba đề xuất:**

| # | nội dung | tệp |
|---|---|---|
| C1 | `total_actual += len(set(actual_tails))` — khử trùng tại **chỗ đếm**, không sửa `get_actual_tails` (20 nơi gọi) | `weight_optimizer.py:141,148` |
| C2 | nền `1 − C(100−M,3)/C(100,3)` thay `1−(1−M/100)³` | `weight_optimizer.py:164` |
| C3 | thay cổng `best_lift > -50` bằng `_v11183_cong_optimizer.cong_ghi_weights()` — bắt buộc held-out ≥30 ngày, hơn control, p **sau chỉnh-chọn** < 0.05 | `weight_optimizer.py:441` |

**`kiem_code` (mệnh đề máy kiểm được):**
`grep -c "len(set(actual_tails))" weight_optimizer.py` ≥ 1 **và**
`grep -c "best_lift'\] > -50" weight_optimizer.py` = 0 **và**
`python _v11183_cong_optimizer.py` trả rc=0 với 15/15.

**Hệ quả phải nói thẳng nếu duyệt C3:** diễn lại lịch sử cho **0/6 lần chạy** qua được cổng, nên
optimizer sẽ **ngừng ghi weights** cho tới khi bổ sung cửa sổ held-out. Hành vi đó **đúng**, nhưng
là thay đổi vận hành thấy được.

**Khuyến nghị KHÔNG làm:** *"tắt learned weights, quay về mặc định"*. `CONTROL` **kém hơn**
`ĐÃ_HỌC` ở cả ba miền; MN `CONTROL` còn kém nền với p=0.0025 theo thước cũ. Quay về mặc định làm
**tệ hơn**.

---

## F. SÁU VIỆC TREO → `docs/FOLLOW_UP_TRACKER.md`

> Phiên này **không mở FU mới** theo khoá. Sáu mục dưới đây là **đề xuất mã**, chờ phiên sau mở.

| việc | mã đề xuất §58 | mức |
|---|---|---|
| Bảy nợ P0 còn mở — nặng nhất: **không có backup ngoài máy** (DB 858 MB một đĩa) · **SSH root+mật khẩu, 248.164 lần dò/28.8 ngày từ 2.635 IP, không fail2ban, ipset rỗng** · **swap=0 và đã OOM-kill thật 05/09** | `KS` | **cao nhất** |
| Retrain không có checkpoint backup — `backup_path` rỗng 12/12; chỉ `meta_learner` có `.bak` (từ 03/07); rf/xgb/lstm **không có** | `SC` | cao |
| `HISTORICAL_RUNTIME_SETTING_NOT_VERSIONED` — `get_model_win_rates`/`get_model_bt_rates` (`database.py:3288,:3360`) neo `vn_now()`, không as-of-date | `SC` | cao |
| Provider chết **câm với journal** — 0/9 sự cố có dòng journal nào | `KS` | trung bình |
| `deepseek-reasoner` payload rỗng **11.4%** (10/88 lượt/30 ngày) — hết số dư kéo dài | `SC` | trung bình |
| Đếm nguồn **phóng đại 27–33%** — `smart-ensemble`/`smart-ml`/`combo-super` là tổ hợp dẫn xuất, không phải nguồn độc lập. Họ nguồn thật: **MN 11 · MT 9 · MB 10** | `DO` | trung bình |

---

## G. BỘ THỬ — một tệp KHAI TỬ

`web/backend/_v11178_thu.py` (bộ thử V1.1) → **`KHAI_TỬ`**.
Đã bị `_v11178_thu_v12.py` thay thế; nay `rc=1` vì `dai_dich` đổi chữ ký từ §W2 (trả 3 giá trị,
thêm nhãn `CANONICAL_STATION_SCHEDULE_VERSIONED`). **Không sửa** — kế nhiệm phủ rộng hơn và chính
nó ghi rằng V1.1 báo *"35/35 ĐẠT"* trong khi ba phép **đạt rỗng**.

Cổng thử sống: **177/177** (51 + 16 + 33 + 50 + 12 + 15 mới).

---

## H. SỐ LIỆU 13/09 — cho trang ngày

| miền | bạch thủ | lo2 | lo3 (3-càng) | model | policy |
|---|---|---|---|---|---|
| MN | **89 WIN** | WIN (2/2) | 189 LOSE | 14/15 | `EXCLUDE_PRIMARY` |
| MT | **54 WIN** | PARTIAL (1/2) | 854 LOSE | 14/15 | `EXCLUDE_PRIMARY` |
| MB | **40 WIN** | PARTIAL (1/2) | **240 WIN** | 13/15 | `EXCLUDE_PRIMARY` |

**Bạch thủ 3/3 — nhưng KHÔNG phải bằng chứng.** Nền đúng hôm đó 0.35 × 0.42 × 0.21 ⇒ P ≈ **3.1%**,
n=1. Và cả ba miền đều `EXCLUDE_PRIMARY` nên ngày này **vốn không đủ tư cách primary**. Chấm lại
độc lập từ `prizes_json` thô khớp **9/9** nhãn production.

---

## I. ĐIỀU TANPHATAI KHÔNG ĐƯỢC LÀM VỚI GÓI NÀY

- Không nâng `PREDICTIVE_LIFT` khỏi `NOT_PROVEN`.
- Không ghi `QD-079` ở trạng thái `ACTIVE` — nó là **`CHỜ_OWNER`**.
- Không mở lại `RANKER_V2_LINEAGE_DEDUP_CALIBRATED`.
- Không trích con số `+10.07 / +7.91 / +17.92` như bằng chứng lift — chúng là ước lượng **trong
  mẫu, bên đã qua chọn 69 lần**.
- Không trích `3/3 bạch thủ WIN` như bằng chứng hiệu quả (`PRJ-SELECTION-WINDOW-001`: một ngày,
  và là ngày `EXCLUDE_PRIMARY`).
