# V10945 — Dừng đặt tiền thật: hệ không hơn đánh bừa sau 90 ngày

**Ngày:** 01/08/2026 · **Loại:** quyết định lớn của owner + cơ chế thực thi
**Trạng thái:** ĐÃ DEPLOY · cổng ĐÓNG cả ba miền

---

## 1. Owner yêu cầu

> *"Hết chu kỳ live rồi em ơi? Tiến hành phân tích đánh giá, kiểm tra, đào sâu lên kế hoạch xử
> lý dứt điểm dùm anh đi em."* — 01/08 19:11

---

## 2. Hôm nay 01/08

MN trúng **16** · MB trúng **90** · MT trượt **55** → lãi **+1,2 triệu**.

Ngày đẹp. Nhưng một ngày không nói lên gì, nên phải nhìn dài.

---

## 3. Tiền thật — tính lại cho đúng

Lần đầu tính đếm "kỳ trúng". Sai, vì owner đặt **3 đài** cho MN/MT nên nếu số về ở 2 đài thì thu
gấp đôi. Phải đếm **đài trúng**. `lottery_results` lưu mỗi đài một dòng nên đếm được chính xác.

| cửa sổ | vốn | thu | lãi |
|---|---|---|---|
| 7 ngày | 52,2 triệu | 39,2 triệu | **−13,0 triệu** |
| 30 ngày | 198,5 triệu | 147,0 triệu | **−51,5 triệu** |
| 90 ngày | 579,2 triệu | 445,9 triệu | **−133,3 triệu** |

Mất khoảng **23% số vốn bỏ ra**.

---

## 4. Hệ có hơn đánh bừa không

Mặt bằng "đánh bừa" **không phải 1%**. Mỗi kỳ mỗi đài xổ nhiều giải nên một số hai chữ số bất kỳ
có xác suất về khá cao. Cách đo trung thực duy nhất: **thử cả 100 số từ 00 đến 99 trên chính kết
quả ngày hôm đó**.

### Cửa sổ 90 ngày

| miền | hệ | đánh bừa | chênh | z | kết luận |
|---|---|---|---|---|---|
| MN | 16,08% | 16,45% | −0,37pp | −0,17 | không phân biệt được |
| MT | 13,57% | 16,49% | −2,92pp | −1,17 | không phân biệt được |
| MB | 16,48% | 23,67% | −7,19pp | −1,61 | không phân biệt được |

### Cửa sổ 180 ngày — sạch hơn nữa

| miền | hệ | đánh bừa | chênh |
|---|---|---|---|
| MN | 16,60% | 16,55% | **+0,05pp** |
| MT | 16,71% | 16,50% | **+0,21pp** |
| MB | 21,94% | 23,74% | −1,81pp |

Đúng bằng ngẫu nhiên. Không hơn, không kém.

### Thử cả 5 kiểu đánh

Bạch thủ, lô 2, lô 3, xiên 2, xiên 3 × 3 miền = **15 tổ hợp**. So từng kiểu với đánh bừa cùng
kiểu (mô phỏng 200 lần mỗi ngày):

**15/15 tổ hợp không phân biệt được với ngẫu nhiên.** Không có kiểu nào là lối thoát.

### Thử giả thuyết "dở đều nhưng giỏi ngày tự tin"

Chia theo `top_score` thành bốn nhóm từ thấp tới cao:

- Không nhóm nào ở miền nào có ý nghĩa thống kê
- Nhóm điểm **cao nhất** còn **kém** nhóm áp chót ở cả MB lẫn MT

Đó là nhiễu, không phải tín hiệu. Nếu điểm tự tin thật sự có ý nghĩa thì tỉ lệ trúng phải tăng
dần theo nhóm — thực tế không.

---

## 5. Điều căn bản: ngay cả đánh bừa cũng lỗ

Owner trả **18k** để ăn **98k** → hoà vốn cần **18,37%**. Đánh bừa chỉ được **16,5%**.

MB trả **27k** ăn **98k** → cần **27,55%**. Đánh bừa được **23,8%**.

**Phần thiệt đã cài sẵn trong tỷ lệ ăn: khoảng 10% ở MN/MT và 14% ở MB.**

> ⚠ **RÚT LẠI — RL-053 (27/11/2026, V11207):** SAI — lô trả THEO NHÁY; kỳ vọng nháy của một số = số giải/100 ⇒ thu 17.640đ / giá 18.000đ (MN/MT) · 26.460đ / 27.000đ (MB) ⇒ thiệt cài sẵn **2,0%** ở cả ba miền (`_v11207_thiet_cai_san.py`). So «≥1 nháy» (16,5% · 23,8%) với 18/98 là so hai đại lượng khác nhau. Kết luận «không hơn đánh bừa» GIỮ NGUYÊN.

Muốn có lời, hệ phải hơn ngẫu nhiên ít nhất **1,9pp** (MN/MT) hoặc **3,8pp** (MB) — chỉ để hoà
vốn, chưa nói tới lãi.

---

## 6. Vấn đề đo lường — chỗ khiến không thể hứa hẹn

Cần bao nhiêu dữ liệu mới **chứng minh** được một lợi thế (95% tin cậy, 80% khả năng phát hiện):

| miền | 2pp | 3pp | 5pp |
|---|---|---|---|
| MN | 873 ngày | 388 ngày | 139 ngày |
| MT | 1.125 ngày | 500 ngày | 180 ngày |
| MB | 3.551 ngày | 1.578 ngày | 568 ngày |

Kể cả hệ **có** lợi thế vừa đủ hoà vốn (1,9pp), cũng phải chờ **hơn hai năm** mới biết chắc.

### Hệ quả thẳng thắn

Mọi việc làm suốt mấy tháng qua — thêm model, cắt model, đổi bộ lọc, sửa prompt — đều xoay quanh
những khác biệt **nhỏ hơn mức có thể đo được** với lượng dữ liệu hiện có.

Nghĩa là không có cách nào biết việc nào có ích, việc nào có hại. Đó chính là lý do owner nói
*"cứ lẩn quẩn mãi"*.

---

## 7. Owner chốt hai việc

1. **Dừng đặt tiền thật.** Giữ hệ chạy để đo (chỉ tốn token). Đặt lại khi chứng minh được lợi thế.
2. **Dừng thêm/cắt model vặt.** Cổng thống kê viết sẵn: hơn ngẫu nhiên **≥3pp** và **z ≥2** mới
   được động vào tiền.

---

## 8. Biến quyết định thành cơ chế chạy được

Quyết định kiểu này **rất dễ trôi**. Vài tuần nữa có một tuần đẹp là lại muốn đặt lại. Nên ngưỡng
phải nằm trong code, tự chấm mỗi ngày, hiện lên màn hình.

| | |
|---|---|
| module | `_v10945_edge_gate.py` — `NGUONG_LOI_THE_PP = 3.0`, `NGUONG_Z = 2.0` |
| API | `/api/admin/edge-gate` (chỉ admin, `Cache-Control: no-store`) |
| UI | `/monitoring` panel `sectionEdgeGate`, tự làm mới 60 giây |
| bảng | `edge_gate_daily` (`diagnostic_only=1`, `shadow_only=1`, `owner_approved=0`) |

### Xác minh sau deploy

```
md5 ba file                          khớp
PID dịch vụ                          575903 → 591144   (đổi thật)
/api/health                          200
/api/admin/edge-gate chưa đăng nhập  401   (chặn đúng)
băm 4 bảng trước/sau                 Y NGUYÊN

cổng chấm:
  MB   hệ 16,48% · bừa 23,67% · lợi thế −7,19pp · z −1,61 · ĐÓNG
  MN   hệ 16,08% · bừa 16,45% · lợi thế −0,36pp · z −0,17 · ĐÓNG
  MT   hệ 13,57% · bừa 16,49% · lợi thế −2,92pp · z −1,17 · ĐÓNG
```

---

## 9. Vẫn làm gì, và không làm gì nữa

**Vẫn làm:** giữ hệ chạy, giữ đo lường, sửa lỗi kỹ thuật rõ ràng (như V10933 lối thoát 503),
giữ tài liệu và hồ sơ.

**Không làm nữa:** tỉa tót model, đổi bộ lọc, sửa prompt để mong nhích vài phần trăm — vì vài
phần trăm đó không đo được.

**Chỉ động vào model khi** có giả thuyết dự kiến tạo lợi thế **≥5pp** (đo được trong ~139 ngày ở
MN), hoặc khi sửa một lỗi kỹ thuật rõ ràng.

---

## 10. Cảnh báo tự đặt cho tương lai

**KHÔNG được hạ ngưỡng khi sốt ruột.** Hạ ngưỡng để cổng mở sớm là tự lừa mình — và lần này sẽ
mất tiền thật.

Ghi ở `FU-208` (`OWNER_LOCK`) và `QD-013` trong `docs/OWNER_DECISION_LEDGER.json` với trường
`kiem_code` để máy tự đối chiếu ngưỡng trong code mỗi phiên.
