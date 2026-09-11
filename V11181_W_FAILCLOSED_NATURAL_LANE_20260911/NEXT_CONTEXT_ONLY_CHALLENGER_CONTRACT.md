# `NEXT_CONTEXT_ONLY_CHALLENGER_CONTRACT`

> **Trạng thái: `NO_SUCCESSOR_PASSES_PREDEPLOY_GATE`**
> Lập 11/09/2026 17:40–17:45 ICT · Prompt 43 R1 §W8 · V11181
> **Mọi phép đo dưới đây chỉ đọc cửa sổ discovery `2026-01-14 → 2026-07-12`** (= `[T-240, T-61]`),
> **không đọc holdout**, **không đọc kết quả 11/09**. Cửa sổ này kết thúc **61 ngày trước** ngày
> đích nên không thể chọn ngược feature theo kết quả hôm nay.

---

## 1 · Vì sao phải có hợp đồng này

Họ đang chạy — `IDENTITY_REVERSE_COMPLEMENT_PLUS1` trên trục
`(target_station × target_weekday × source_cell × lag × transform)` — **bị khai tử** vì
không có tín hiệu nào sống sót qua hiệu chỉnh đa phép:

| miền | cell đã thử | p tốt nhất | ngưỡng Bonferroni | BH-FDR α=0,10 giữ |
|---|---|---|---|---|
| MN | 5.832 | 8,685e-05 | **8,573e-06** | **0** |
| MT | 3.888 | 3,908e-04 | **1,286e-05** | **0** |
| MB | 1.944 | 5,395e-04 | **2,572e-05** | **0** |

p tốt nhất lớn hơn ngưỡng Bonferroni **10× · 30× · 21×**. Ở MN, kỳ vọng số cell có
p ≤ 8,685e-05 **thuần do ngẫu nhiên** là `5832 × 8,685e-05 ≈ 0,51` — tức quan sát được
**một** cell như vậy đúng bằng cái ngẫu nhiên sinh ra.

⇒ `IDENTITY_REVERSE_COMPLEMENT_PLUS1_FAMILY_RETIRED_NO_SIGNAL`.
**Không hạ ngưỡng để tránh khai tử.**

---

## 2 · CỔNG TIỀN-TRIỂN-KHAI — đăng ký TRƯỚC, áp cho MỌI họ kế tiếp

Một họ chỉ được đưa vào shadow live khi **đồng thời** đạt cả chín điều:

| # | điều kiện | ngưỡng |
|---|---|---|
| G1 | trục đầy đủ | `target_region × target_weekday × target_station × source_prize × source_position × lag × cutoff` |
| G2 | nền tính **cho từng thước** | nền **per target station**, **cấm** dùng nền gộp miền (RM-18) |
| G3 | discovery / holdout **không chồng lấn** | discovery `[T-240, T-61]` · holdout `[T-60, T-1]` |
| G4 | support tối thiểu | discovery ≥ 15 · holdout ≥ 20 |
| G5 | kiểm định | binomial exact một phía |
| G6 | hiệu chỉnh đa phép | BH-FDR **trên toàn bộ** cell của họ, **và** trên số họ đã thử |
| G7 | q sau hiệu chỉnh | **q ≤ 0,05** trên holdout |
| G8 | cận dưới khoảng tin cậy | Wilson 95% lower bound **> nền** |
| G9 | hiệu ứng tối thiểu | **≥ 5,0 điểm phần trăm** |

Kèm **kiểm rò rỉ bắt buộc**: `source_available_at < target_cutoff_at` tính bằng datetime
có timezone (**cấm so chuỗi thô**) · lag khớp **chính xác** · đài đích lấy từ lịch canonical
có version · loại dòng `run_source` thuộc nhóm đánh giá lại.

**Tiêu chí dừng / khai tử:** 0 cell qua G6–G9 ở **cả ba miền** ⇒ khai tử ngay, không kéo dài
đo. Một họ chỉ được đo lại nếu **trục** đổi, không phải nếu **ngưỡng** đổi.

---

## 3 · BA HỌ ĐÃ THỬ VÀ BỊ LOẠI — nêu chính xác loại bằng điều kiện nào

### `F1 · IDENTITY_REVERSE_COMPLEMENT_PLUS1` (họ đang chạy)
**Loại bằng `G6`.** BH-FDR giữ **0/5832 · 0/3888 · 0/1944**. Không có cell nào để xét tiếp
G7–G9. Đây là họ **duy nhất** trong ba họ có nền đúng ngay từ đầu (nó đã đánh giá
per target station).

### `F2 · WEEKDAY_STATION_TAIL_FREQUENCY`
Tần suất đuôi theo `(miền, thứ, đài)` trong discovery.
**Loại bằng `G6`.** 0 cell qua Bonferroni ở cả ba miền:

| miền | cell | p tốt nhất | Bonferroni | qua |
|---|---|---|---|---|
| MN | 2.182 | 5,122e-05 | 2,291e-05 | **0** |
| MT | 1.684 | 1,651e-03 | 2,969e-05 | **0** |
| MB | 698 | 2,190e-04 | 7,163e-05 | **0** |

### `F3 · GAP_RECENCY` (đuôi vắng k ngày → tỉ lệ quay lại)
**Loại bằng `G9`.** Đo **đúng thước** (per target station, nền per station):
MN **1/10** cell qua Bonferroni với lift **chỉ +1,03pp** (17,62% vs nền 16,60%,
p=4,43e-03 so với ngưỡng 5,00e-03 — sát mép) · MT **0/11** · MB **0/10**.
`+1,03pp << 5,0pp` ⇒ trượt G9. Chưa cần xét tới holdout.

### `F4 · DIGIT_ALGEBRA` (tổng / hiệu / tích chữ số của giải đặc biệt D-1)
**Loại bằng `G2` — phép đo ban đầu SAI THƯỚC, không phải họ có tín hiệu.**
Xem mục 4.

---

## 4 · MỘT SAI LẦM ĐÃ SUÝT LÀM HỎNG CHÍNH HỢP ĐỒNG NÀY (`RL-039`)

Bản khảo sát đầu của `F3` và `F4` in ra những con số như:

```
F3_GAP  MN: ('gap', 0)      hit=3329/7719 (43.1%)  p=0.000e+00
F4_DIGIT MN: ('nhan',0,'1') hit= 421/835  (50.4%)  p=7.686e-112
```

Nhìn thì đó là tín hiệu khổng lồ so với nền `0,1660`. **Không có tín hiệu nào.** Phép đo đã
gộp **cả 3 đài** của MN thành một tập ~43 đuôi rồi so với nền của **một** đài — đúng `RM-18`:
*so tỉ lệ của bộ k đuôi với nền của 1 số*.

Bằng chứng đóng đinh: `3329/7719 = 43,1%` **trùng khít** nền gộp miền MN `0,4312`, và khớp
`0,4297` đã đo độc lập từ V11170. **"Tín hiệu" chính là cái nền.**

Xác nhận thêm bằng cấu trúc: MB chỉ có **một** đài nên nền gộp = nền một đài (**1,0×**) — và
MB là miền **duy nhất** không hiện tín hiệu giả. MN lệch **2,6×**, MT lệch **2,1×** — đúng hai
miền hiện tín hiệu giả mạnh nhất.

| miền | nền một đài | nền gộp miền | lệch | có hiện tín hiệu giả |
|---|---|---|---|---|
| MN | 0,1660 | 0,4312 | 2,6× | có, rất mạnh |
| MT | 0,1647 | 0,3514 | 2,1× | có |
| MB | 0,2381 | 0,2381 | 1,0× | **không** |

Sai lầm bị bắt **trước khi** dùng làm căn cứ — bởi chính việc con số quá đẹp gây nghi, không
phải bởi một cổng máy nào. Nhưng nó **suýt** trở thành căn cứ chọn họ kế tiếp, tức suýt thay
một họ vô tín hiệu bằng một họ vô tín hiệu khác rồi gọi đó là tiến bộ.

**Hệ quả cho hợp đồng:** `G2` được nâng thành điều kiện **chặn cứng**, và mọi họ tương lai
phải in **cả hai** nền (per-station và gộp miền) cạnh nhau trong báo cáo khảo sát, để chênh
lệch không thể trôi im lặng.

---

## 5 · KẾT LUẬN

```
NO_SUCCESSOR_PASSES_PREDEPLOY_GATE
```

**Không có họ nào** trong `F1 · F2 · F3 · F4` vượt cổng tiền-triển-khai. Loại theo đúng điều
kiện: `F1` và `F2` trượt **G6** (hiệu chỉnh đa phép) · `F3` trượt **G9** (hiệu ứng tối thiểu) ·
`F4` không được tính vì phép đo **sai thước** (`G2`).

**Không trả về `WAIT_DATA`.** Việc tiếp theo là **một việc cụ thể**: nếu muốn mở họ mới thì
phải là họ có **trục khác hẳn** — không phải ánh xạ ô-nguồn → ô-đích, cũng không phải thống kê
tần suất/recency trên chính chuỗi đuôi, vì cả hai nhánh đó đã được đo và đều âm. Cho tới khi
có một họ như vậy **vượt cổng trên dữ liệu lịch sử**, challenger **giữ nguyên shadow-only** và:

```
PREDICTIVE_LIFT = NOT_PROVEN
POOL_VERDICT    = HOLD
```
