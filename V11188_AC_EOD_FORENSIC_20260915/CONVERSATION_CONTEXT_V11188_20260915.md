# CONVERSATION CONTEXT — V11188 · §AC EOD forensic, 15/09/2026 02:00 → 03:xx ICT

## 1. Owner nói gì — nguyên văn

Prompt **§AC**, mức *"TỔNG LỰC · CỰC GẮT · ĐỌC CODE + DB + TRACE + LOG + GITHUB · KHÔNG ĐOÁN ·
KHÔNG TÔ XANH · KHÔNG DỪNG Ở «THEO DÕI TIẾP»"*.

Điều chi phối toàn phiên là §AC-A:

> *"Cấm trộn hai epoch: 14/09 trọn ngày chạy V11185. 15/09 trọn ngày phải chạy V11186/§AB. Không
> dùng kết quả 14/09 để tuyên bố §AB đã cải thiện hoặc làm xấu dự đoán: §AB chưa tồn tại trong các
> lượt sinh output ngày 14/09."*

Và câu đóng:

> *"KHÔNG ĐƯỢC KẾT THÚC BẰNG: «TIẾP TỤC THEO DÕI». PHẢI TRẢ LỜI DỨT ĐIỂM CHO OWNER."* — kèm mười
> câu hỏi cụ thể.

**Không có yêu cầu rời nào giữa phiên.**

---

## 2. Thứ tự thật của phiên

| giờ VN | việc |
|---|---|
| 02:00 | `date` trên VPS: **02:00:51 ngày 15/09**. MN chạy 05:15 ⇒ còn 3h14m. Xác định hai ngày, hai epoch |
| 02:05 | Đọc schema thật: `lottery_results` có `station`, **không** có `updated_at`; `predictions` có `ai_model` **không** phải `model_name` |
| 02:10 | Trích ground truth từ `prizes_json` — ba miền `COMPLETE_VALID`, chấm lại official khớp 100% |
| 02:12 | **Phóng workflow 7 nhánh forensic**, mỗi nhánh có một agent phản biện chạy lại truy vấn |
| 02:12 | Preflight lượt tự nhiên — **M8/M9 báo CHẶN** |
| 02:14 | Truy ra đó là **false blocker của chính tôi** (bí danh import). Sửa → **15/15 READY** |
| 02:20–02:40 | Ba blocker §AC-O: override lineage 23/23 · family lineage 30/30 · atomic retrain 42/42 |
| 02:26 | Manifest forensic — `FORENSIC_INPUT_EPOCH_OK` |
| 02:45 | Kiểm độc lập: **0 override nào nổ ngày 14/09** |
| 03:00 | Workflow trả về: 14 agent, 0 lỗi, 2,33 triệu token, 491 lượt gọi công cụ |
| 03:05 | Tự xác minh phát hiện `EXPECTED_MODEL_COUNT` — **cả ba bundle bị xếp `INCOMPLETE`** |

---

## 3. Điều quan trọng nhất cho người đọc sau

### 3.1 Thua không phải vì thiếu số — thua vì xếp sai chỗ

Trực giác tự nhiên khi thấy bạch thủ 1/3 là *"model đoán kém"* hoặc *"cắt còn 4 model nên thiếu
nguyên liệu"*. **Cả hai đều sai, và dữ liệu bác cả hai.**

Pool ứng viên đông cứng của **cả ba miền đều chứa** đuôi trúng. MN và MB là `RANKER_MISS`:

- **MN**: đuôi trúng `14` có **ba** phiếu — nhưng **cả ba đều ở vị trí top2** (`pw=0,80`).
  `smart-ml` và `smart-ensemble` cùng ra đúng cặp `["24","14"]` theo đúng thứ tự đó. Ranker chỉ
  tôn trọng thứ tự nội bộ của chính hai model ấy. Kết quả: **24 = 0,1362 vs 14 = 0,1350 — biên
  0,0012**.
- **MB**: đuôi trúng `31` là **số thứ hai của đúng model đã đặt số thua `16` lên đầu**
  (`gemini-2.5-flash` → `["16","31"]`).

Và phản tưởng đã bác luôn cách sửa dễ nhất: bỏ chiết khấu vị trí (`pw` top2 = 1,0) thì **MN vẫn
miss** (0,1362 vs 0,1350) và **MB vẫn miss**. Không có nút vặn đơn giản nào lật được ngày 14/09.

### 3.2 Lượt rò không phải thủ phạm — nhưng đường lan là có thật

Dễ nhất là gán MB thua cho lượt `gemini-2.5-pro` ngoài roster. **Sai.** Bỏ hẳn phiếu `combo-super`
thì `16` vẫn đứng #1 (0,0846 so với `31` chỉ 0,0415). Lượt rò góp **10,5%** điểm của số `16`.

Nhưng nó **không mồ côi**: nó là **pha AI của chính `combo-super`**, và `combo-super` là **một
trong ba voter** của số top-1. Đường từ một model ngoài roster vào bundle official **đã mở** —
hôm nay chỉ tình cờ không đổi số. Đó đúng là thứ §AB đóng.

### 3.3 Nén roster sửa một nửa

`EXPECTED_MODEL_COUNT = len(get_output_eligible_ids())` = **15**, và danh sách đó **vẫn còn**
`gemini-2.5-pro`, `deepseek-reasoner`, `gpt-5.4` — model ngoài mọi roster hoặc đang bị cách ly.
Ngày 14/09 cả ba miền `model_count=11` ⇒ `classify_bundle_quality` = **`INCOMPLETE`**.

Trước 12/09, MN và MB thường chạm đúng 15. Từ 14/09, **mọi bundle đều `INCOMPLETE` theo thiết kế**.
Chính sách gọi đã đổi, ngưỡng hoàn chỉnh thì chưa — đúng lỗi §60 *"bỏ nửa chừng"*.

### 3.4 Có lớp thứ NĂM

Tài liệu dự án suốt nhiều phiên nói **bốn** lớp override. Có **năm**:
`main_number_anti_trap` + `near_miss_anti_trap` (`main.py:10441+`), chạy trong **cùng hàm**, **sau**
bốn lớp kia. Và **bạch thủ duy nhất thắng trong ngày (MT `20`) bị chính lớp này gắn cờ
`FULL_SPENT`**.

---

## 4. Vấp ở đâu

### 4.1 Cổng của chính tôi báo nhầm — và nó suýt gây rollback vô cớ

`_v11188_preflight_natural.py` bản đầu có M8/M9 tìm lời gọi mang **đúng tên**
`get_token_call_roster` / `uy_quyen_goi`. Mã thật import dưới **bí danh**:

```python
from _v11185_roster_goi_token import get_token_call_roster as _v11186_gtcr   # combo_super.py:1289
from _v11185_roster_goi_token import uy_quyen_goi as _uqg                     # gpt_analyzer.py:6806
```

Tên trong nút `ast.Call` là **bí danh**, nên phép kiểm luôn trượt và báo *"cổng không tồn tại"* cho
một cổng đang chạy đúng. Nếu tin bản đầu, tôi đã có thể kích hoạt **rollback vô cớ**. Đã sửa: quét
`ImportFrom` lấy `asname` trước, rồi mới tìm `Call` theo tên cục bộ.

**Một cổng báo nhầm nguy hiểm ngang một cổng không tồn tại.**

### 4.2 Bảy nhánh forensic — phản biện bắt lỗi thật ở CẢ BẢY

Mỗi nhánh có một agent riêng được giao việc **cố bác bỏ**, và bắt buộc **chạy lại truy vấn** thay
vì đọc lại lời. Kết quả đáng giá:

| kết luận ban đầu | sự thật sau phản biện |
|---|---|
| "MN chỉ có một dòng WIN 2/2" | **hai** — `claude-opus-4-6` và `lstm` |
| "số 24 gom ba phiếu cùng một họ ⇒ đếm ba lần một nguồn" | **sai** — `smart-ensemble` = Meta + LSTM, không phải xgboost. Khử trùng **cả hai vế** thì 24 = 0,0916 vẫn thắng 36 = 0,0768 |
| "5 dòng bị SKIP, 3 có số trúng" | **10** dòng SKIP, **7** có số trúng |
| "OOM 30 ngày qua = 0 lần" | **2 sự kiện ngày 05/09** — số 0 là artifact journal xoay vòng (journal chỉ giữ từ 10/09 trong khi uptime từ 18/04) |
| "cost 5 lượt OpenRouter không còn khôi phục được" | **khôi phục được** — `cost_est` là hàm tất định của token × đơn giá |
| "Top-N Combo chọn không tìm thấy ở đâu" | nằm ngay trong `predictions.analysis_text`, cột chưa ai đọc |
| "hai tarball backup = hai điểm khôi phục" | **cùng một ảnh chụp DB** (cùng byte, cùng mtime) |

Không có phản biện, ít nhất bốn con số sai đã vào báo cáo công khai.

### 4.3 `grep -c '[COST]'` — lớp ký tự regex, không phải chuỗi

Một agent công bố *"0 dòng `[COST]` trong journal"* bằng `grep -c '[COST]'` **không thoát ngoặc
vuông**. `[COST]` là **lớp ký tự**, khớp bất kỳ ký tự nào trong `C,O,S,T` ⇒ chạy lại ra **1345**.
Lệnh đúng là `grep -cF '[COST]'`. Đúng họ `RM-09`, và nó lọt tới tận khâu công bố.

### 4.4 RM-10 cắn tôi một lần nữa

`get_output_eligible_ids` **không nằm trong** `database.py` — nó được import từ `model_registry`
dưới bí danh `_goe`. Tôi viết `from database import get_output_eligible_ids` và nhận `ImportError`.

### 4.5 Quoting lồng qua `ssh`

Hai lệnh kiểm vỡ vì dấu `'` trong heredoc bị lớp `ssh '...'` bên ngoài nuốt, cho ra
`no such column: ACTIVE`. Phải chuyển sang ghi script ra tệp rồi `scp`.

---

## 5. Điều phiên CỐ Ý không làm

| việc | không làm vì |
|---|---|
| Restart hoặc deploy bất cứ gì | §AC-M cấm tuyệt đối trước lượt MN 05:15 |
| Sửa `EXPECTED_MODEL_COUNT` | Là thay đổi đường official; §AC-M cấm. Đã ghi thành việc treo hạn 16/09 |
| Sửa lớp anti-trap thứ năm | §AC-C: *"không sửa bốn override legacy trong bước đánh giá"*. Ghi thành việc treo hạn 17/09 |
| Nối ba module lineage vào production | §AC-O: code/test offline được, deploy thì không |
| Bù backup off-machine | Thao tác ghi, ngoài phạm vi phiên read-only. Giữ nguyên `EXACT_BLOCKER` |
| Sửa SSH / fail2ban | §AC-R cấm sửa SSH giữa live |
| Gọi provider tay | §AC cấm. Mọi số đều từ lượt tự nhiên đã xảy ra |

---

## 6. Câu phải nhớ khi đọc lại

**Một ngày là một biên nhận mô tả, không phải bằng chứng.** Bạch thủ 1/3 so với kỳ vọng ngẫu nhiên
0,99/3 nghe như "đúng bằng ngẫu nhiên" — nhưng độ lệch chuẩn của **một** phép Bernoulli tại nền là
**0,49 / 0,46 / 0,44**, lớn hơn mọi lệch quan sát được. Theo `RM-04`, con số này **không cho phép
kết luận gì**, theo cả hai chiều: không được nói hệ kém, và cũng không được nói hệ ổn.

Điều **được phép** kết luận từ ngày 14/09 là những thứ **cơ chế**, không phải thống kê: ranker xếp
sai chỗ ở hai miền; ngưỡng hoàn chỉnh lệch roster; có lớp thứ năm; và đường lan từ model ngoài
roster vào bundle official là có thật.
