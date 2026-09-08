# CONVERSATION CONTEXT — V11172 · 08/09/2026

> Nguyên văn lời owner · agent làm gì · vấp ở đâu (§57.2). Giờ **Việt Nam (UTC+07:00)**.
> `CURRENT_ACTOR = CLAUDE_CODE` · **Prompt 43 R1 giữ `PARTIAL` — không mở Prompt 44.**

---

## 1 · Owner nói gì — NGUYÊN VĂN

| giờ (VN) | NGUYÊN VĂN | loại | agent đã làm gì | trạng thái |
|---|---|---|---|---|
| ~21:4x | *«Kiểm tra tổng lực dự đoán hôm nay và các tồn đọng cũng như các mốc đã lên lịch»* | `YÊU_CẦU` | Khởi động phiên; chụp live 08/09 + 07/09; đo bạch thủ vs nền riêng 9 ô; truy 3 tín hiệu nghi vấn; đọc 3 việc đến hạn + 8 mốc lịch | `ĐÃ_LÀM` |

---

## 2 · Điều đáng nói nhất — phiên này giá trị ở chỗ KHÔNG báo động

Ba tín hiệu trông y hệt hỏng:

| tín hiệu | trông như | sự thật |
|---|---|---|
| `pp1_live_watch_daily` **im 2 ngày** | writer chết | ghi **đúng bằng số sự kiện PP-1**; PP-1 kích hoạt 18/30 ngày, khoảng trống 2 ngày **đã từng xảy ra** (12–13/08 · 17–18/08 · 20–21/08) |
| **7 bảng im hôm nay** | pipeline gãy | **6/7 CHƯA TỚI GIỜ CRON** — quét lúc **21:49**, `model_latency` chạy **21:50**, `pnl_forward` 22:30, `consensus_free` 22:35, `rescue` 22:45, `rule_key` 00:30 |
| `training_history` **mất 2 đêm** | job huấn luyện chết | chạy **HÀNG TUẦN** — 30/08 → 06/09, **đúng 7 ngày**; kế tiếp 13/09 |

**Nếu báo bừa, kho sẽ có ba mục «lỗi» vĩnh viễn không tồn tại**, và phiên sau đi tìm chúng.

**Bẫy phương pháp đã gây ra cả ba:** dùng **«trung bình dòng/ngày»** để phát hiện bảng chết. Bảng
chạy **theo tuần** (12 dòng/tuần → «1,7 dòng/ngày») hoặc **theo sự kiện** đều cho **dương tính giả**.
**Phải tra crontab và nhịp thật trước khi gọi một bảng là chết** — mở rộng `RM-20`.

Đây là **phiên thứ ba liên tiếp** kiểu bẫy này xuất hiện: V11170 (đọc sớm thí nghiệm đăng ký trước) ·
V11171 (`ls-remote` hỏng tạm + `credential.helper` giả ẩn danh) · V11172 (ba bảng «chết» giả).

---

## 3 · Điều đáng nói thứ hai — hệ thống TỰ nói nó kém nền

Log retrain đêm 06/09, nguyên văn trong `scheduler_logs`:

```
✅ Retrain subprocess rc=0: Test days: 100, Precision@10: 0.2310, Lift: 0.97x, AU…
```

**`Lift = 0.97×` ⇒ kém nền 3%** trên 100 ngày kiểm. Đây là **đường đo thứ SÁU** cùng hướng với năm
đường của V11170 — và là đường **duy nhất do chính pipeline tự tính**, không phải agent đi đo.

---

## 4 · Điều đáng nói thứ ba — trần MT đang CHE MẤT lỗi thật

Hôm nay MT bị dán `DEGRADED` (ngày thứ **ba liên tiếp**) vì trần `max_voters_cap` cố ý — hôm nay cắt
`claude-opus-4-6` + `claude-sonnet-4-6` (**đổi theo ngày**; 06/09 là `smart-ensemble` + `meta-learning`).

**Nhưng hôm nay MT CÒN có một lỗi thật:** `🚨 FAILED MODELS MT: combo-super(TIMEOUT>300s)`.
`model_count` **vẫn là 13** — vì trần cắt xuống 13 bất kể có bao nhiêu model sống.
⇒ **Nhìn `model_count` KHÔNG phân biệt được** MT mất model vì lỗi thật hay vì trần.

Và bản thân nhãn «FAILED» cũng không chính xác: `combo-super` **vẫn nộp bài lúc 16:51:15**,
`status=WIN` — tức **về trễ 16 giây** sau khi timeout được tuyên bố, **không hỏng**.

---

## 5 · Vấp ở đâu

| # | vấp | gỡ |
|---|---|---|
| 1 | Dùng **«trung bình dòng/ngày»** phát hiện bảng chết ⇒ **3 dương tính giả** | tra **crontab + nhịp thật** trước khi kết luận |
| 2 | `FU-446` ghi 🔴 «12 model rơi về 0,70» | đo runtime: chỉ **2/12 là official**, **0/15 model** có `strength_weight` đúng `0.7` ⇒ hạ 🔴 → 🟡, hậu quả **chưa chứng minh được** |
| 3 | Suýt đọc sớm `anti_trap_shadow_v11058` lần nữa | ghi **quan sát**, **không suy hướng** — ngưỡng n≥90 chưa đạt |
| 4 | MT `mc=6` ngày 28/08 **không có lý do loại trừ nào** | ghi `INDETERMINATE`, **không đoán**; cần phiên riêng |

---

## 6 · Cho TanPhatAI đọc tiếp

**Con số dễ trích sai:** «MT kém nền 7,6 điểm» — **z = −0,88, KHÔNG có ý nghĩa**. Và **180 ngày chỉ
−0,7**, tức phần âm của MT là **hiện tượng gần đây**, không phải đặc tính. **Cấm** dùng riêng cửa sổ
30 ngày.

**Việc rẻ nhất agent tự làm được, chưa ai nhận:** `FU-447` — sửa tiêu đề 16 báo cáo về đúng khung 9
phần. Ticket ghi rõ **không cần owner quyết**.

**Việc gấp nhất chờ owner:** ký **`SC-12`** (vá kế toán MT — hôm nay là ngày thứ ba liên tiếp MT bị
dán nhãn sai) và chọn **A/B/C cho `FU-448`**.

**Đang tích luỹ, chưa được đọc:** `anti_trap_shadow_v11058` — 423 dòng, ghi tới hôm nay, ngưỡng
**n ≥ 90**.

---

TanPhatAI cần làm: ghi **`V11172`** — công khai bản này cùng `REPORT_V11172.md`. Ghi **ngày 08/09 SẠCH vận hành, 1/3 miền trúng (đúng mode 30 ngày); 07/09 được 2/3, MN thắng cả bạch thủ + lô2 + xiên2 + xiên3**. Ghi **KHÔNG ô nào trong 9 ô (3 miền × 3 cửa sổ) có ý nghĩa thống kê** — RM-04, chưa được phép kết luận; **MN đứng ĐÚNG nền cả ba cửa sổ**; **MT âm GẦN ĐÂY** (30 ngày −7,6 · 90 ngày −6,3 · 180 ngày **chỉ −0,7**). Ghi **đường đo thứ SÁU: retrain 06/09 tự ghi `Lift 0.97x`** — pipeline tự nói kém nền 3%. Ghi **BA LẦN KHÔNG BÁO ĐỘNG SAI** và **bài học: cấm dùng «trung bình dòng/ngày» để phát hiện bảng chết**. Ghi **trần MT đang CHE MẤT lỗi thật** — `model_count=13` không phân biệt được «bị trần» với «model hỏng». Ghi **`combo-super` TIMEOUT tăng tốc 25/30 ngày, 07/09 NĂM lần, chưa đăng ký theo dõi ở đâu**, và **hôm nay nó VẪN nộp bài, chỉ TRỄ 16 giây**. Ghi **`FU-446` hạ 🔴 → 🟡**. Ghi **200 mục treo · 155 quá hạn · 24 quyết định quá hạn rà soát cũ nhất từ 08/08**. **Code KHÔNG đi trước tài liệu** — 0 ghi production. **Không mở Prompt 44. Không mở FU mới. Không mở Plan mới.**
