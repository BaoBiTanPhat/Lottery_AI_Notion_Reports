# V11172 — KIỂM TỔNG LỰC NGÀY LIVE 08/09/2026 + TỒN ĐỌNG + MỐC ĐÃ LÊN LỊCH

> **Ngày:** 08/09/2026 (đo 21:44–22:0x giờ VN, sau khi cả ba miền đã chốt và có kết quả)
> **Tầng verdict:** `MEASURED_ONLY` — **0 ghi production · 0 deploy · 0 restart · DB READ-ONLY**
> **Cách làm:** agent chính tự đo, **không điều agent phụ** (owner không yêu cầu fan-out)

---

## 1 · TÓM TẮT

**Ngày live 08/09 chạy sạch về vận hành.** 81/81 lượt dự đoán đủ, 0 dòng rỗng, 0 dòng trễ, cả ba
miền chốt đúng mốc, health 200, `NRestarts 0`, đĩa 33%. Kết quả **1/3 miền trúng bạch thủ** — đúng
giá trị phổ biến nhất của 30 ngày.

**Điều quan trọng nhất của phiên này không phải phát hiện lỗi mới, mà là BA LẦN KHÔNG BÁO ĐỘNG SAI.**
Ba tín hiệu trông như hỏng — `pp1_live_watch_daily` ngừng ghi 2 ngày · 7 bảng im hôm nay ·
`training_history` mất 2 đêm — **cả ba đều bình thường** khi tra đến nơi. Nếu báo bừa, kho sẽ có ba
mục "lỗi" vĩnh viễn không tồn tại.

**Một con số mới đáng chú ý:** log retrain 06/09 ghi **`Precision@10: 0.2310, Lift: 0.97x`** — chính
hệ thống tự đo và tự nói nó **kém hơn nền 3%** trên tập kiểm.

---

## 2 · OWNER YÊU CẦU GÌ — NGUYÊN VĂN

| giờ (VN) | NGUYÊN VĂN | loại | agent đã làm gì | trạng thái |
|---|---|---|---|---|
| ~21:4x 08/09 | *«Kiểm tra tổng lực dự đoán hôm nay và các tồn đọng cũng như các mốc đã lên lịch»* | `YÊU_CẦU` | Chạy `_v10920_session_start`; chụp live 08/09 + 07/09; đo bạch thủ vs nền riêng 3 cửa sổ; truy 3 tín hiệu nghi vấn; đọc 3 việc đến hạn; liệt kê mốc đã lên lịch | `ĐÃ_LÀM` |

---

## 3 · ĐÀO BỚI / PHÁT HIỆN

### 3.1 · Kết quả ngày 08/09

| miền | bạch thủ | kết quả | lô2 | model_count | consensus | ranked[0] |
|---|---|---|---|---|---|---|
| **MN** | **68** | 🟢 **WIN** | PARTIAL | 15 | strong | `68` — **khớp, không bị lật** |
| MT | 15 | 🔴 LOSE | PARTIAL | 13 | strong | `15` — khớp |
| MB | 63 | 🔴 LOSE | LOSE | 15 | **moderate** | `63` — khớp |

**Nhãn WIN/LOSE kiểm lại đúng 3/3:** `68` **có** trong 41 đuôi của MN · `15` **không** có trong 29
đuôi MT · `63` **không** có trong 22 đuôi MB.

**Hôm nay KHÔNG cơ chế lật nào kích hoạt** — cả ba miền `bach_thu == ranked_numbers[0]`. Khác hẳn
06/09 (MN bị `_v10640` specialist lật 04→73).

**Ngày 07/09 hôm qua tốt hơn: 2/3.** MN `04` trúng **WIN cả bạch thủ · lô2 · xiên2 · xiên3** — ngày
mạnh nhất trong tuần. MB `64` WIN.

**7 ngày gần nhất:** 1 · 0 · 1 · 1 · 1 · 2 · 1 (trên 3 miền/ngày) — **7/21 = 33,3%**.

### 3.2 · Bạch thủ vs NỀN RIÊNG TỪNG MIỀN-NGÀY (Poisson-binomial, RM-18)

| cửa sổ | miền | n | trúng | tỉ lệ | nền | chênh | z | kết luận |
|---|---|---|---|---|---|---|---|---|
| 30 ngày | MN | 30 | 13 | 43,3% | 43,2% | **+0,1** | +0,01 | không tách được khỏi nền |
| 30 ngày | **MT** | 30 | 8 | 26,7% | 34,2% | **−7,6** | −0,88 | không tách được khỏi nền |
| 30 ngày | MB | 30 | 7 | 23,3% | 23,8% | −0,4 | −0,06 | không tách được khỏi nền |
| 90 ngày | MN | 90 | 39 | 43,3% | 43,1% | +0,2 | +0,05 | không tách được |
| 90 ngày | **MT** | 90 | 26 | 28,9% | 35,2% | **−6,3** | −1,26 | không tách được |
| 90 ngày | **MB** | 90 | 16 | 17,8% | 23,7% | **−5,9** | −1,32 | không tách được |
| 180 ngày | MN | 163 | 71 | 43,6% | 43,1% | +0,5 | +0,13 | không tách được |
| 180 ngày | MT | 163 | 56 | 34,4% | 35,1% | **−0,7** | −0,19 | không tách được |
| 180 ngày | MB | 163 | 30 | 18,4% | 23,7% | −5,3 | −1,59 | không tách được |

**Đọc đúng — ba điều:**

1. **KHÔNG ô nào có ý nghĩa thống kê**, cả dương lẫn âm. Theo `RM-04`, **chưa được phép kết luận**
   miền nào tốt hay kém hơn nền.
2. **MN đứng ĐÚNG nền ở cả ba cửa sổ** (+0,1 / +0,2 / +0,5). Ổn định một cách đáng chú ý — và cũng
   có nghĩa là **không có lợi thế nào**.
3. **MT có hình dạng đáng đăng ký theo dõi:** 30 ngày **−7,6** · 90 ngày **−6,3** · nhưng 180 ngày
   **−0,7**. Tức phần âm của MT **là hiện tượng GẦN ĐÂY**, không phải đặc tính cấu trúc. Chưa đủ ý
   nghĩa để kết luận, nhưng đủ hình dạng để **đăng ký trước rồi đo tiến** (`RM-03`).

### 3.3 · Hệ thống TỰ ĐO và tự nói nó kém nền — bằng chứng độc lập mới

Log retrain đêm 06/09 (`scheduler_logs`, nguyên văn):

```
✅ Retrain subprocess rc=0: Test days: 100, Precision@10: 0.2310, Lift: 0.97x, AU…
```

**`Lift = 0.97×` nghĩa là mô hình kém hơn nền 3%** trên 100 ngày kiểm. Đây là **đường đo thứ SÁU**
độc lập với năm đường của V11170, và cùng chỉ một hướng. Khác ở chỗ: **chính pipeline huấn luyện tự
tính ra con số này và tự ghi vào log**, không phải agent đi đo.

### 3.4 · 🟢 BA LẦN KHÔNG BÁO ĐỘNG SAI — phần đáng giá nhất của phiên

**① `pp1_live_watch_daily` ngừng ghi từ 06/09 13:20** trong khi bộ canh vẫn chạy 4 lần/ngày và báo
`inserted=0 events=0 regions_with_data=none regions_no_data=['MN','MT','MB']`.

Trông y hệt một writer đã chết. **Sự thật:** bảng ghi **đúng bằng số sự kiện PP-1**. PP-1 kích hoạt
**18/30 ngày**, và khoảng trống 2 ngày **đã xảy ra nhiều lần trước đó** (12–13/08 · 17–18/08 ·
20–21/08). Từ 07/09 các bundle đều ghi `pp1_convergence_dampener.events = 0` ⇒ **không có gì để
ghi**. Bộ canh đang làm đúng việc và báo cáo trung thực.

**② «7 bảng thường ghi mỗi ngày mà hôm nay im».** Tra crontab thì **6/7 chỉ là CHƯA TỚI GIỜ** — lúc
quét là **21:49 VN**:

| bảng | giờ ghi thật | tình trạng lúc quét |
|---|---|---|
| `model_latency_shadow_v11063` | **21:50** | còn **1 phút** nữa |
| `pnl_forward_track_shadow` | 22:30 | chưa tới |
| `consensus_freeshadow_shadow` | 22:35 | chưa tới |
| `rescue_candidate_shadow` | 22:45 | chưa tới |
| `rule_key_registry` | 00:30 | sau nửa đêm |
| `training_history` | ~02:00 | xem ③ |
| `pp1_live_watch_daily` | theo sự kiện | xem ① |

**③ `training_history` mất 2 đêm** (ghi 30/08 rồi 06/09). Trông như job huấn luyện chết.
**Sự thật: nó chạy HÀNG TUẦN**, không hàng đêm — 30/08 → 06/09 cách **đúng 7 ngày**. Trung bình
«1,7 dòng/ngày» mà em dùng để phát hiện là **con số gây hiểu nhầm**: thực tế là 12 dòng, mỗi tuần
một lần. Lần chạy kế tiếp dự kiến **13/09**.

⇒ **Không bảng nào hỏng.** Đây là lần thứ ba trong ba phiên liên tiếp mà kiểu bẫy này xuất hiện —
xem mục 7.

### 3.5 · MT DEGRADED — ngày thứ ba liên tiếp quan sát được, và trần đang CHE lỗi thật

`day_governance` hôm nay: MN `VALID` · MB `VALID` · **MT `DEGRADED_LIVE_DAY`, 13/15,
`degradation_reason='Thiếu 2 model (13/15)'`**.

JSON của bundle 850 ghi lý do thật: hai model bị loại là **`claude-opus-4-6`** và
**`claude-sonnet-4-6`**, `reason=max_voters_cap`, `detail=MT_top13_only_V10752_weakest_dropped` —
**trần voter CỐ Ý theo thiết kế**, đúng lỗi kế toán V11170 đã đóng nhân quả. Lưu ý: hai model bị cắt
**đổi theo ngày** (06/09 là `smart-ensemble` + `meta-learning`), nên cắt theo hạng chứ không cố định.

**Phát hiện MỚI của phiên này — trần đang CHE MẤT lỗi thật:**

Hôm nay MT **cũng có** một lỗi thật: `🚨 FAILED MODELS MT: combo-super(TIMEOUT>300s)`. Nhưng
`model_count` **vẫn là 13** — vì trần cắt xuống 13 bất kể có bao nhiêu model sống. ⇒ **Nhìn
`model_count` KHÔNG phân biệt được** MT mất model vì lỗi thật hay vì trần.

*(Ghi chú quan trọng: `combo-super` **vẫn nộp bài** lúc **16:51:15**, `status=WIN`,
`len(main_numbers)=12` — tức nó về **sau** khi timeout được tuyên bố lúc 16:50:59, chỉ **16 giây**.
Model không mất, chỉ **về trễ** so với mốc chốt bundle.)*

**MT 30 ngày:** `mc=13` **27 ngày** · `mc=12` 2 ngày · **`mc=6` 1 ngày (28/08)**.
Ngày `mc=6` **không có bất kỳ lý do loại trừ nào được ghi** — `quality_filtered=[]`,
`hard_timeout=[]`, `empty=[]`. **Chưa giải thích được** ⇒ `INDETERMINATE`, cần một phiên riêng.

### 3.6 · 🔴 `combo-super` TIMEOUT đang TĂNG TỐC

**25/30 ngày gần nhất có ít nhất một lần `combo-super TIMEOUT>300s`.** Nhịp theo ngày:

| giai đoạn | số lần/ngày |
|---|---|
| 10/08 – 30/08 | phần lớn **1–2** |
| 01/09 – 05/09 | 2 · 3 · 3 · 1 · 2 |
| **06/09** | **4** |
| **07/09** | **5** |
| **08/09** | **3** |

`combo-super` là **model gộp** — nó nằm trong pool và bỏ phiếu. Timeout của nó **đẩy nó ra khỏi
bundle** (hoặc về trễ như hôm nay). Xu hướng tăng này **chưa được đăng ký theo dõi ở đâu**.

Ngoài `combo-super`, 30 ngày còn có: `glm-5.1` (TIMEOUT 26/08, 07/09) · `deepseek-reasoner` (empty
02–03/09, TIMEOUT 22/08) · `gpt-oss-120b` (`EMPTY_PROVIDER_OUTPUT` 01/09).

### 3.7 · Chống bẫy hôm nay — quan sát, KHÔNG kết luận

| miền | bạch thủ | mức chống bẫy | đã ra ở | kết quả |
|---|---|---|---|---|
| MN | 68 | `NOT_APPLICABLE` (miền đầu ngày) | — | 🟢 **WIN** |
| MT | 15 | **`FULL_SPENT`** + có cảnh báo | MN | 🔴 LOSE |
| MB | 63 | `PARTIAL_SPENT` | MT | 🔴 LOSE |

Hai miền chơi số «đã tiêu» đều thua; miền duy nhất chơi số chưa tiêu thì thắng — **giống hệt hình
06/09**.

> ⚠️ **CẤM kết luận từ quan sát này.** Dự án **đã có phép đo ĐĂNG KÝ TRƯỚC** cho đúng câu hỏi đó:
> bảng **`anti_trap_shadow_v11058`** (`FU-397`, đăng ký 10/08/2026), ngưỡng **n(FULL_SPENT) ≥ 90 và
> |z_MH| ≥ 1,96**, ghi rõ **«chưa đủ n ⇒ cấm đọc sớm (RM-04)»**. Bảng có **423 dòng**, chạy liên tục
> **21/04 → 08/09**, **ghi cả hôm nay**. Phiên này **KHÔNG đọc hướng kết quả**.
> Nhắc lại từ V11171: trục anti-trap **từng được cắm thành cơ chế ghi đè thật và ĐÃ TẮT** sau khi đo
> tiến cứu ra **−29,4 triệu / 60 ngày**.

### 3.8 · Ba việc ĐẾN HẠN HÔM NAY

**🔴 `FU-446` · DO0809 · `OWNER_DECISION_NEEDED` — bảng hiệu chỉnh sức mạnh lạc hậu**

Xác minh lại bằng cách **nạp thẳng module trên VPS**: `strength_calibrator.MODEL_STRENGTH_DISCOUNT`
có **15 khoá**, `DEFAULT_DISCOUNT = 0.7`; **27 model** sinh dự đoán trong 30 ngày ⇒ **12 model không
có khoá**.

**Nhưng quy mô thật NHỎ HƠN ticket viết, và hậu quả CHƯA chứng minh được:**

- Đối chiếu `_CANONICAL_OUTPUT_MODELS` (`main.py:9693`, 15 model bỏ phiếu): trong 12 model thiếu
  khoá, **chỉ 2 là model OFFICIAL** — `glm-5.1` và `gpt-oss-120b`. **10 cái còn lại là shadow**,
  không bỏ phiếu vào bundle.
- Quan trọng hơn: đo `strength_weight` **thực tế trong bundle hôm nay** ⇒ **0/15 model** có giá trị
  đúng bằng `0.7`. Giá trị quan sát được trải từ **0,26 đến 1,0** và **đổi theo từng số**, kể cả
  `glm-5.1` (0,26 / 0,6 / 0,92) và `gpt-oss-120b` (0,51 / 0,6).

⇒ `MODEL_STRENGTH_DISCOUNT` **không phải** thứ quyết định `strength_weight` lúc chạy — hoặc chỉ là
một thừa số. **Ticket đúng về sự kiện (bảng lạc hậu), nhưng mệnh đề «12 model rơi về 0,70» KHÔNG
quan sát được ở runtime.** Mức đề nghị hạ từ 🔴 xuống 🟡, và phải **đo lại tác động thật** trước khi
xin owner quyết.

**🟡 `FU-447` · BC0809 · `MEASURED_BUT_NOT_FIXED` — 16 báo cáo đặt tiêu đề ngoài khung**

Nội dung **có đủ**, chỉ tiêu đề lệch khung 9 phần nên cổng không nhận ra. Ticket tự ghi:
*«Đây là lỗi của agent khi viết báo cáo, không phải lỗi cổng»* và **không cần owner quyết**.
⇒ **Đây là việc agent tự sửa được**, đang chờ một phiên nhận làm.

**🔴 `FU-448` · DO0809-2 · `OWNER_DECISION_NEEDED` — MN mất khối `🎯 RULE TAILS` trong prompt**

Gốc thật đã tìm ra: **lỗi THỨ TỰ TRONG NGÀY**, không phải chất lượng luật. Chuỗi bảy mắt xích đã
truy xong (`mined_rule_eval.py:165-180` không lọc tier/miền · `:311` là writer duy nhất).
**Chờ owner chọn phương án A/B/C.**

### 3.9 · Các mốc ĐÃ LÊN LỊCH

| hạn | mã | việc | trạng thái | ai chặn |
|---|---|---|---|---|
| **13/09** | `FU-430` · DO1309 | đo tiến đang chạy | `DO_TIEN_DANG_CHAY` | tự chạy |
| **13/09** | — | **lần retrain hàng tuần kế tiếp** (30/08 → 06/09 → 13/09) | tự động 02:00 | tự chạy |
| **14/09** | `FU-351` · DO0914 | MN trượt đúng MỘT BẬC — nghi bộ xếp hạng | `MEASURED_BUT_NOT_FIXED` | agent |
| **18/09** | `FU-376` · DD0918 | bốn món nợ tháng 7 chưa trả | `AWAITING_OWNER_OK` | **owner** |
| **19/09** | `FU-235` · HT0919 | B3 gỡ ép chọn từ list (sau B1+B2) | `OWNER_LOCK` | **owner** |
| **22/09** | `FU-358` · DO2209 | `/nghiem-thu` — cửa sổ TRƯỚC đã đóng băng | `WAIT_LIVE` | chờ dữ liệu |
| **07/10** | `FU-367` · DO0710 | chấm lane G2-MB sau đủ 60 ngày đo tiến | `WAIT_LIVE` | chờ dữ liệu |
| **chưa có hạn** | `FU-397` | anti-trap đủ **n ≥ 90** mới được đọc | đang tích luỹ | chờ dữ liệu |

### 3.10 · Bức tranh tồn đọng tổng thể

| chỉ số | số |
|---|---|
| mục theo dõi **còn treo** | **200** |
| trong đó **quá hạn** | **155** |
| **đến hạn hôm nay** | **3** |
| không ghi hạn | 34 |
| thiếu mã đọc (§58) | 3 |
| **quyết định tới hạn rà soát** | **24** |

**24 quyết định quá hạn rà soát**, cái cũ nhất từ **08/08** (`OD-20260801-B`, `QD-015` … `QD-017`) —
tức **một tháng**. Phần lớn mang dạng *«sau khi hết đóng băng 08/08 thì làm X»* — cửa sổ đóng băng
đã qua từ lâu mà chưa ai đóng sổ.

---

## 4 · HƯỚNG XỬ LÝ VÀ VÌ SAO CHỌN

**Không điều agent phụ.** Owner yêu cầu *«kiểm tra tổng lực»* — đó là yêu cầu về **độ kỹ**, không
phải yêu cầu fan-out nhiều agent. Phiên trước (V11170) đã dùng 24 agent cho một câu hỏi mở; câu hỏi
lần này **có phạm vi rõ** (ngày live + tồn đọng + mốc), agent chính tự đo đủ và rẻ hơn nhiều.

**Tra crontab TRƯỚC khi gọi một bảng là chết.** Bài học `RM-20` + hai ca hụt của V11170/V11171. Nhờ
vậy tránh được **ba báo động sai** trong một phiên.

**Không đọc phép đo đăng ký trước.** `anti_trap_shadow_v11058` chưa đạt ngưỡng n≥90 ⇒ chỉ ghi quan
sát, **không suy hướng**. V11170 đã vi phạm đúng chỗ này và đã ghi nhận.

**Hạ mức `FU-446` thay vì trình owner ngay.** Ticket ghi 🔴 và 12 model, nhưng đo runtime cho thấy
chỉ **2 model official** liên quan và **0/15 model** thực sự ở mức `0.7`. Trình owner một P0 chưa
chứng minh được hậu quả là **làm mất thời gian của owner** — đúng thứ `§56` cấm.

---

## 5 · ĐÃ LÀM GÌ

| việc | kết quả |
|---|---|
| khởi động phiên | `_v10920_session_start.py` — nêu ngay 3 việc đến hạn hôm nay |
| chụp live 08/09 + 07/09 | 3 bundle · 6 dòng kết quả · 81 dự đoán · `day_governance` · 1.151 dòng scheduler |
| bạch thủ vs nền riêng | 9 ô (3 miền × 3 cửa sổ), Poisson-binomial từng miền-ngày |
| truy 3 tín hiệu nghi vấn | **cả 3 đều bình thường** — không báo động sai |
| kiểm nhãn WIN/LOSE | **3/3 đúng** khi chấm lại từ `prizes_json` |
| xác minh `FU-446` | nạp thẳng module trên VPS + đo `strength_weight` thật trong bundle |
| đọc 3 việc đến hạn + mốc lịch | 8 mốc từ 13/09 đến 07/10 |
| production | **0 ghi · 0 deploy · 0 restart** |

---

## 6 · CỔNG KIỂM

| cổng | kết quả |
|---|---|
| `_v10920_session_start.py` | ✅ chạy đầu phiên |
| `_v11044_cong_so_hieu.py` | ✅ `SO_HIEU_V11044=KHỚP` — cấp V11172 |
| `_v11062_nang_version.py --kiem` | ✅ `NANG_VERSION_V11062=ĐẠT` |
| `_v11085_cong_rut_lai.py` | ✅ `PRJ_RETRACTION=SẠCH` |
| `_v11088_cong_cua_so_chon.py` | ✅ `PRJ_WINDOW=SẠCH` |
| `_v10921_report_gate.py V11172` | ✅ đủ 9 phần, đã commit |
| nhãn `bach_thu_status` hôm nay | ✅ chấm lại **3/3 khớp** |
| DB production | ✅ **READ-ONLY** — 0 lệnh ghi |
| VPS | ✅ PID `3370750` · `NRestarts 0` · health 200 · đĩa 33% (còn 26 G) · load 0,00 |

---

## 7 · VƯỚNG VẤP

| # | vấp | gỡ |
|---|---|---|
| 1 | 🟢 **Ba tín hiệu trông như hỏng** — `pp1_live_watch_daily` im 2 ngày · 7 bảng im hôm nay · `training_history` mất 2 đêm | **Cả ba đều bình thường.** PP-1 không kích hoạt (18/30 ngày, khoảng trống 2 ngày đã từng xảy ra) · 6/7 bảng **chưa tới giờ cron** (quét lúc 21:49, `model_latency` chạy **21:50**) · `training_history` chạy **hàng tuần**, không hàng đêm |
| 2 | Dùng **«trung bình dòng/ngày»** để phát hiện bảng im | Sai với bảng chạy **theo tuần** hoặc **theo sự kiện**: 12 dòng mỗi tuần ra «1,7 dòng/ngày», trông như ghi hằng ngày rồi đứt. **Phải tra crontab và nhịp thật trước.** |
| 3 | `FU-446` ghi 🔴 với «12 model rơi về 0,70» | Đo runtime: chỉ **2/12 là model official**, và **0/15 model** có `strength_weight` đúng bằng `0.7`. Hạ 🔴 → 🟡, ghi rõ hậu quả **chưa chứng minh được** |
| 4 | Suýt đọc sớm `anti_trap_shadow_v11058` lần nữa | Ghi **quan sát** (2 miền chơi số «đã tiêu» đều thua) nhưng **không suy hướng** — ngưỡng n≥90 chưa đạt |
| 5 | MT `mc=6` ngày 28/08 **không có lý do loại trừ nào** | **Chưa giải thích được** ⇒ ghi `INDETERMINATE`, cần phiên riêng. Không đoán |

---

## 8 · GỠ VỀ

**Không có gì để gỡ.** Phiên này **chỉ đọc**: không ghi production, không deploy, không restart,
không đụng DB, không sửa tệp nào trong `web/backend`. Thay đổi duy nhất là tài liệu quản trị và kho
báo cáo công khai — gỡ bằng `git revert <commit>` trên hai kho.

---

## 9 · THEO DÕI TIẾP

### Chờ owner quyết

| # | việc | vì sao |
|---|---|---|
| 1 | **`FU-448`** — chọn phương án A/B/C cho lỗi thứ-tự-trong-ngày làm MN mất khối `🎯 RULE TAILS` | gốc thật đã truy xong, chỉ chờ chọn |
| 2 | **`SC-12` / `VA-h12`** — vá kế toán MT (test 30/30, đã có vá) | mỗi ngày trôi thêm 1 ngày trễ; hôm nay là ngày thứ ba liên tiếp MT bị dán `DEGRADED` sai |
| 3 | Ba việc kỹ thuật **V11170**: `main.py:10491`/`:10511` · `LIMIT 270` ra trước bộ lọc | `MB` đang bị báo thấp 23,4pp |
| 4 | **`FU-376`** (hạn 18/09) · **`FU-235`** (hạn 19/09) | `AWAITING_OWNER_OK` / `OWNER_LOCK` |
| 5 | **24 quyết định quá hạn rà soát**, cũ nhất từ 08/08 | phần lớn dạng «sau đóng băng 08/08 thì làm X» — cửa sổ đã qua một tháng |
| 6 | Năm P0 hạ tầng **V11166** | vẫn nguyên |

### Agent làm được, chưa ai nhận

| # | việc | ghi chú |
|---|---|---|
| 7 | **`FU-447`** — sửa tiêu đề 16 báo cáo về đúng khung 9 phần | ticket ghi rõ **không cần owner quyết** |
| 8 | Truy **MT `mc=6` ngày 28/08** — không có lý do loại trừ nào được ghi | `INDETERMINATE` |
| 9 | Đo lại **tác động thật** của `MODEL_STRENGTH_DISCOUNT` trước khi trình `FU-446` | 2 model official liên quan |

### Ứng viên ĐĂNG KÝ TRƯỚC (RM-03) — chưa được phép kết luận

| ứng viên | số hiện có | ghi chú |
|---|---|---|
| **MT âm gần đây** | 30 ngày −7,6 · 90 ngày −6,3 · **180 ngày −0,7** | hình dạng «gần đây», không cấu trúc; **z chưa đạt** |
| **`combo-super` timeout tăng tốc** | 25/30 ngày; 06/09 **4** · 07/09 **5** · 08/09 **3** | **chưa được đăng ký theo dõi ở đâu** |
| anti-trap `FULL_SPENT` | `anti_trap_shadow_v11058` 423 dòng, ghi tới hôm nay | **CẤM đọc sớm** — ngưỡng n≥90 |

### Mốc tự chạy

`13/09` retrain hàng tuần · `13/09` `FU-430` · `14/09` `FU-351` · `22/09` `FU-358` · `07/10` `FU-367`.

---

## §62 — NGUỒN BA LỚP

### `OWNER_SAID`
> *«Kiểm tra tổng lực dự đoán hôm nay và các tồn đọng cũng như các mốc đã lên lịch»*
> — ~21:4x ngày 08/09/2026, IDE.

Chỉ thị đứng từ các phiên trước còn hiệu lực: *«nếu kết luận là "không hơn ngẫu nhiên" thì phải nói
thẳng»* · *«trường hợp nào không thông báo anh xử lý luôn để lâu quên»*.

### `CODE_DID`
- 3 bundle hôm nay: `848` MN `BT=68` **WIN** · `850` MT `BT=15` LOSE · `852` MB `BT=63` LOSE;
  cả ba `bach_thu == ranked_numbers[0]` ⇒ **không cơ chế lật nào kích hoạt**.
- `scheduler_logs` 08/09: `🚨 FAILED MODELS MT: combo-super(TIMEOUT>300s)` lúc 16:50:59; nhưng
  `predictions` có dòng `combo-super` MT lúc **16:51:15**, `status=WIN` ⇒ **về trễ 16 giây**, không mất.
- `t10_chot` ba miền: **15:40 · 16:55 · 17:55** — đúng mốc thiết kế.
- Retrain 06/09: `Precision@10: 0.2310, Lift: 0.97x` trên 100 ngày kiểm.
- `strength_calibrator.MODEL_STRENGTH_DISCOUNT` = **15 khoá**, `DEFAULT_DISCOUNT = 0.7`; nhưng
  `score_breakdown` hôm nay: **0/15 model** có `strength_weight == 0.7`.
- `crontab`: `rescue` **22:45** · `pnl_forward` **22:30** · `consensus_free` **22:35**;
  `model_latency` ghi **21:50**; quét lúc **21:49**.
- `training_history`: 30/08 và 06/09 — **cách đúng 7 ngày**.
- VPS: PID `3370750` · `NRestarts 0` · `ActiveEnterTimestamp` **04/09 01:08:40** · health 200.

### `DOC_SAID`
- `docs/FOLLOW_UP_TRACKER.md:1815` — `FU-446` ghi 🔴 «15 khoá / 24 model», «12 model còn lại vẫn rơi
  về `DEFAULT_DISCOUNT = 0.70`».
- `docs/FOLLOW_UP_TRACKER.md:1699` — `FU-447`, *«lỗi của agent khi viết báo cáo, không phải lỗi cổng»*.
- `docs/FOLLOW_UP_TRACKER.md:1625` — `FU-448`, `AGENT_DA_DO_XONG`, chờ owner.
- `docs/CURRENT_TRUTH_SSOT.md:68` — MT `EXCLUDE_PRIMARY` 72/90 vì kế toán trần V10752.
- `docs/GITHUB_KHO_VA_QUYEN.md` (V11171) — địa chỉ kho chính thức, đã dùng để push bản này.

**LỆCH GIỮA BA LỚP — phải báo:**
1. `DOC_SAID` ≠ `CODE_DID`: `FU-446` ghi «12 model rơi về 0,70», nhưng runtime cho **0/15 model** ở
   mức `0.7` và **10/12 model đó là shadow, không bỏ phiếu**. **Ticket cần đo lại trước khi trình owner.**
2. `DOC_SAID` ≠ `CODE_DID`: `day_governance` ghi MT *«Thiếu 2 model»*, JSON bundle ghi
   `reason=max_voters_cap` — **chính sách CỐ Ý bị kế toán thành thất bại**, ngày thứ ba liên tiếp.
3. `CODE_DID` mâu thuẫn nội bộ: log tuyên `combo-super TIMEOUT>300s` (16:50:59) trong khi
   `predictions` có dòng của chính nó lúc 16:51:15 — **nhãn «FAILED» không phân biệt «hỏng» với
   «về trễ»**.

---

TanPhatAI cần làm: ghi **`V11172`** — `governance_seq 487`, công khai bản này cùng `CONVERSATION_CONTEXT_V11172_20260908.md`. Ghi **ngày live 08/09 SẠCH về vận hành** (81/81 lượt, 0 rỗng, 0 trễ, 3 miền chốt đúng mốc) và **1/3 miền trúng — đúng giá trị phổ biến nhất 30 ngày**; **07/09 hôm trước được 2/3, MN thắng cả bạch thủ + lô2 + xiên2 + xiên3**. Ghi **hôm nay KHÔNG cơ chế lật nào kích hoạt** — cả ba miền `bach_thu == ranked[0]`, khác 06/09. Ghi **bạch thủ vs NỀN RIÊNG TỪNG MIỀN: KHÔNG ô nào trong 9 ô có ý nghĩa thống kê** (RM-04 — chưa được phép kết luận); **MN đứng ĐÚNG nền cả ba cửa sổ** (+0,1/+0,2/+0,5); **MT có hình dạng ÂM GẦN ĐÂY** (30 ngày −7,6 · 90 ngày −6,3 · **180 ngày chỉ −0,7**) ⇒ ứng viên **đăng ký trước rồi đo tiến**. Ghi **ĐƯỜNG ĐO THỨ SÁU độc lập: log retrain 06/09 tự ghi `Precision@10 0.2310, Lift 0.97x`** — chính pipeline huấn luyện tự nói nó **kém nền 3%** trên 100 ngày kiểm. Ghi **BA LẦN KHÔNG BÁO ĐỘNG SAI**: `pp1_live_watch_daily` ghi **đúng bằng số sự kiện PP-1** (PP-1 kích hoạt 18/30 ngày, khoảng trống 2 ngày đã từng xảy ra) · **6/7 bảng «im» chỉ là CHƯA TỚI GIỜ CRON** (quét 21:49, `model_latency` chạy 21:50) · `training_history` chạy **HÀNG TUẦN** (30/08 → 06/09, đúng 7 ngày). Ghi **bài học: cấm dùng «trung bình dòng/ngày» để phát hiện bảng chết** — bảng chạy theo tuần hoặc theo sự kiện sẽ ra dương tính giả. Ghi **MT DEGRADED ngày thứ BA liên tiếp** vì trần `max_voters_cap` cố ý (hôm nay cắt `claude-opus-4-6` + `claude-sonnet-4-6`, đổi theo ngày), và **PHÁT HIỆN MỚI: trần đang CHE MẤT lỗi thật** — hôm nay MT vừa bị trần vừa có `combo-super TIMEOUT` nhưng `model_count` vẫn 13, nhìn con số đó **không phân biệt được** hai nguyên nhân. Ghi **`combo-super` TIMEOUT ĐANG TĂNG TỐC: 25/30 ngày, 06/09 bốn lần · 07/09 NĂM lần · 08/09 ba lần — chưa được đăng ký theo dõi ở đâu**. Ghi **`combo-super` hôm nay VẪN NỘP BÀI lúc 16:51:15 (`status=WIN`), tức về TRỄ 16 giây chứ không hỏng** — nhãn «FAILED» không phân biệt «hỏng» với «về trễ». Ghi **`FU-446` phải HẠ MỨC 🔴 → 🟡**: chỉ **2/12 model thiếu khoá là OFFICIAL**, và **0/15 model** có `strength_weight` đúng bằng `0.7` ⇒ mệnh đề «12 model rơi về 0,70» **không quan sát được ở runtime**. Ghi **`FU-447` agent tự sửa được, không cần owner**. Ghi **MT `mc=6` ngày 28/08 KHÔNG có lý do loại trừ nào — `INDETERMINATE`**. Ghi **TỒN ĐỌNG: 200 mục treo · 155 quá hạn · 3 đến hạn hôm nay · 24 quyết định quá hạn rà soát, cũ nhất từ 08/08 (một tháng)**. Ghi **MỐC ĐÃ LÊN LỊCH: 13/09 retrain tuần + FU-430 · 14/09 FU-351 · 18/09 FU-376 · 19/09 FU-235 · 22/09 FU-358 · 07/10 FU-367**. Ghi **phép đo đăng ký trước `anti_trap_shadow_v11058` (423 dòng, ghi tới hôm nay) VẪN CẤM ĐỌC SỚM** — ngưỡng n≥90. **Code KHÔNG đi trước tài liệu** — 0 ghi production, 0 deploy, 0 restart, DB chỉ đọc. **Không mở Prompt 44. Không mở FU mới. Không mở Plan mới.**
