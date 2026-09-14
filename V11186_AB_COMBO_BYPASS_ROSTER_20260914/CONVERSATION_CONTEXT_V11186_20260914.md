# CONVERSATION CONTEXT — V11186 · phiên §AB, 14/09/2026 12:49 → 13:xx ICT

## 1. Owner nói gì — nguyên văn

Prompt **§AB**, mức thực thi *"CỰC GẮT · CỰC MẠNH · KHÔNG TÔ XANH · KHÔNG ĐOÁN · KHÔNG GIA HẠN MƠ HỒ"*.

Điều quan trọng nhất: **Owner tự soi nguồn và chỉ đúng chỗ V11185 báo quá.**

> *"V11185 đã đóng scheduler chính nhưng chưa chứng minh toàn hệ thống vì:
> 1. `combo_super.py` còn pool `AI_MODELS` riêng.
> 2. Combo tự chọn Top-N và gọi `analyze_and_predict`.
> 3. Pool Combo còn model ngoài roster từng miền.
> 4. `gpt_analyzer._invoke_model_api` hiện có quarantine guard nhưng chưa có roster authorization
>    bắt buộc cho model khỏe nhưng ngoài roster.
> 5. Ước lượng giảm 74,7% chưa tách đầy đủ Combo calls.
> 6. Natural receipt chưa xảy ra.
>
> Do đó, trước khi có §AB: `MODEL_OUTSIDE_ROSTER_HTTP_CALLS=ZERO` chỉ là PREDEPLOY/STATIC CLAIM,
> chưa phải runtime fact toàn hệ thống."*

Và §AB-B bắt đính chính **trước khi làm tiếp**:

> *"Không được để tài liệu dẫn người sau đọc sai."*

Cùng §AB-U cấm kết thúc kiểu cũ, trong đó có: *"«AST sạch nên live sạch»"* · *"«đếm riêng Combo nên
không cần roster-gate»"* · *"«ước lượng token giảm» viết thành số thật"* · *"«MN pass» viết thành ba
miền pass"* · *"static proof viết thành runtime proof"* · *"pure-context chưa chạy viết thành
retired"*.

Và §AB-J về mốc deploy:

> *"Nếu không đạt trước 03:30: không deploy patch nửa vời; không thay code giữa MN/MT/MB; giữ
> V11185 cho toàn ngày 14/09... Cấm: MN một version, MT/MB version khác."*

**Không có yêu cầu rời nào giữa phiên.**

---

## 2. Điều đầu tiên tôi làm, và vì sao nó đổi cả kế hoạch

§AB viết như thể phiên bắt đầu ~00:15 ngày 14/09 (*"Thời điểm prompt bắt đầu khoảng 00:15 ICT ngày
14/09"*), với mốc deploy 03:30/04:00.

Tôi chạy `date` trên VPS: **12:49 ngày 14/09**.

Nghĩa là:
- Lượt MN sáng nay **đã chạy xong** (05:00–05:17) dưới V11185;
- MT (~16:38) và MB (~17:30) **chưa chạy**;
- Deploy lúc này ⇒ **MN một version, MT/MB version khác trong cùng một ngày** — điều §AB-J cấm
  tuyệt đối.

⇒ Kế hoạch đổi ngay: **không deploy hôm nay**, hoàn tất mã và **staged**, thu receipt, deploy sau EOD.

**Nếu tôi làm theo chữ trong prompt mà không kiểm đồng hồ, tôi đã phá epoch ngày 14/09.**

---

## 3. Agent IDE đã làm gì — theo thứ tự thật

1. Preflight §AB-C1 + inventory provider call-site toàn repo (24 tệp, 7 call-site sống).
2. **Thu receipt MN** — bằng chứng sống đầu tiên: `MN_ROSTER_LIVE_PROOF_OK` 10/10.
3. Đo lịch sử 30 ngày: model ngoài roster từng vào bundle bao nhiêu ngày.
4. Đóng Combo bypass ở `combo_super.py` (giao pool với roster + đóng fallback).
5. Thêm `uy_quyen_goi()` vào module SSOT, chèn guard vào `_invoke_model_api`.
6. Truyền `execution_class` + `caller` từ **cả 7 call-site sống**.
7. Thêm request fingerprint + reuse cùng lượt; chuẩn hoá cost.
8. Bộ thử `_v11186_thu_ab.py` **102/102**.
9. Đính chính bốn mục V11185 (RL-044..047) tại **chính chỗ đã công bố**.
10. Đặt bộ thu receipt nền trên VPS cho MT/MB.

---

## 4. Vấp ở đâu

### 4.1 Bộ thu receipt của tôi báo FAIL OAN

Receipt MN đầu tiên ra `MN_ROSTER_LIVE_PROOF_FAIL` với 3 phép trượt. Nhưng nhìn chi tiết thì
`ERROR/CRITICAL` in ra `"0\n0"` — hai dòng.

Nguyên nhân: `grep -c` trả **mã thoát 1** khi đếm ra 0, nên `... || echo 0` làm **cả hai** cùng chạy.
Sửa bằng `; true` + ép `int`. Và thêm **`−1 = KHÔNG ĐỌC ĐƯỢC`**, khác hẳn 0 — để không bao giờ biến
"thiếu dữ liệu" thành "sạch". Sau sửa: **10/10**.

Đây là đúng loại lỗi §AB-U cấm (*"thiếu data viết thành zero"*), và nó xảy ra trong **chính bộ thu
bằng chứng của tôi**.

### 4.2 Script sửa của tôi hỏng vì escape trong chú thích tiếng Việt

Một `\n` trong chuỗi chú thích bị diễn giải trong heredoc, làm hỏng cú pháp. `ast.parse` chặn trước
khi ghi nên tệp không bị hỏng. Làm lại không dùng escape — đúng thứ tôi đã có ghi nhớ về heredoc.

### 4.3 Tôi viết một chỗ mong manh

`"_ct_uq" in dir()` để lấy `roster_version`. Hoạt động nhưng khó đọc và dễ vỡ. Sửa thành biến khai
trước guard.

### 4.4 Một cảnh báo giả do chính lệnh kiểm của tôi

Lệnh kiểm in `?` cho `cost_source` và `request_fingerprint` vì số lần xuất hiện khác **kỳ vọng tôi
đoán trong lệnh kiểm** — không phải yêu cầu nào cả. 2 lần mỗi cái là đúng.

---

## 5. Điều phiên CỐ Ý không làm

| việc | không làm vì |
|---|---|
| **Deploy** | §AB-J cấm phá epoch. MN đã chạy. Mã xong sớm không phải lý do để phá epoch |
| Override lineage · family lineage · retrain atomic | §AB-U: *"Nếu P0 chưa đóng: không mở việc nghiên cứu khác"*. P0 chưa deploy ⇒ chưa đóng |
| Pure-context | §AB-Q: chỉ activate **sau** `ROSTER_SYSTEM_WIDE_LIVE_PROOF_OK`. Zero token spent |
| Gọi provider tay để tạo bằng chứng | §AB-K cấm. Receipt MN là **tự nhiên**, thu từ lượt 05:00 sáng nay |

---

## 6. Điều quan trọng nhất cho người đọc sau

**Bypass là thật, và đo được.** Trong 30 ngày, model ngoài roster có mặt trong bundle: `gemini-2.5-pro`
@MN **29/30 ngày**, @MT 28, @MB 27; `deepseek-reasoner` @MB 27/@MT 26/@MN 24; `glm-5.1`@MN 24;
`claude-sonnet-4-6`@MT 23/@MB 17.

**Nhưng phải đọc đúng:** phần lớn số đó là lượt gọi của **scheduler TRƯỚC §AA**, không phải riêng
Combo. So bundle 13/09 (trước §AA) với 14/09 (sau): MN từ có `gemini-2.5-pro` → **0 model ngoài
roster**. Tức cổng scheduler của §AA **đã đóng được đường chính trên thực tế**.

Cái còn hở là **cấu trúc**: pool riêng của Combo vẫn chứa 4 model không được phép, và Combo chọn
top-N độc lập. Hôm nay nó không dùng tới — **nhưng "hôm nay không dùng" không phải là "không thể
dùng"**. Đó chính xác là điều §AB nói và tôi đã bỏ qua ở §AA khi coi "đếm riêng" là đủ.

**Và một điểm mở tôi KHÔNG đoán:** receipt MN cho thấy `claude-opus-4-6` gọi **2 lượt**. Trace không
ghi `caller`/`execution_class`/`fingerprint` nên **không quy được** lượt thêm cho scheduler hay
Combo. Ghi đúng nhãn `LUOT_THEM_CHUA_QUY_DUOC_NGUON`. Sau khi deploy §AB, mọi lượt sẽ mang đủ ba
trường đó và câu hỏi này tự trả lời.
