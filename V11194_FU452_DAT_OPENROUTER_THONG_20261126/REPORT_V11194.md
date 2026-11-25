# V11194 — FU-452 đạt: Claude chạy lại thật ở MN 26/11; OpenRouter tự thông lại, `gpt-oss-120b` có số

> **Phiên bản:** V11194 · **Ngày:** 26/11/2026 05:24 → 05:4x ICT · **Repo riêng:** `Lottery_AI_Test` commit `639560b`
> (nhánh `fu438/admin-only-p0a` + `master`) · **governance_seq:** 509 · **Tầng (RM-12):** `REPORT_PROVEN` (đo, chỉ
> đọc) · **Runtime đổi:** không.

## 1. Tóm tắt

- **`FU-452` đạt.** Lượt MN 26/11 05:16 có `claude-opus-4-6` ra `32` và `claude-sonnet-4-6` ra `85 53`. Đây là lượt MN đầu
  tiên sau khi owner nạp tiền Anthropic và cách ly được nhả (V11191). MT/MB đã đạt từ 25/11 (V11192).
- **OpenRouter tự thông lại.** Lệnh gọi của service lúc 05:15:11 trả **200**, và `gpt-oss-120b` có số ở MN. Lượt thử một
  lần lúc 05:25:46 cũng trả `POST` **200** sau 1,17 s. Hôm qua 21:39 cùng lệnh đó còn trả 400.
- **Owner không còn phải chọn `FU-460`.** Lựa chọn (B) «chờ tự thông» đã tự xảy ra. Quyết định không cách ly ở V11193
  là đúng: bộ ngắt mạch tự mở lại, không ai phải đụng tay. `FU-460` → `WAIT_LIVE` cho tới khi lượt MT/MB chiều nay có
  `glm-5.1` ra số.

## 2. Owner yêu cầu gì (nguyên văn) — §62 lớp `OWNER_SAID`

**Không có lời owner mới trong phiên này.** Phiên là lượt kiểm tự động đã hẹn từ trước, theo hai yêu cầu cũ:

| giờ (ICT) | nguyên văn | việc của phiên này |
|---|---|---|
| 25/11 ~13:12 | *"deepseek và claude athopic anh đã nạp tiền rồi ah em"* | xác nhận Claude chạy lại thật ở MN (`FU-452`) |
| 25/11 ~21:35 | *"phần của anh nhiều vài rút gọn quá chỉ có khuyên của em ko chưa đủ em cần trình bày rõ hơn đi , kiểm tra đánh giá việc dự đoán hôm nay sao rồi em"* | phép đánh giá ngày đã lộ sự cố OpenRouter; agent hứa kiểm OpenRouter mỗi ngày một lượt (`FU-460`) |

Cả hai đã có dòng trong `docs/SO_TUONG_TAC_OWNER.md`. Không thêm dòng mới vì owner chưa nói gì thêm.

## 3. Đào bới / phát hiện — liệt kê ĐỦ

### 3.1 Lượt kiểm hẹn giờ (`evidence/kiem_luot_that_0525.txt`)

`_v11191_kiem_luot_that.py 2026-11-26` chạy lúc 05:24 trên VPS:

- `FU-452` **ĐẠT**: hai dòng Claude ở MN có số.
- Cách ly còn `gpt-5-mini`, `gpt-5.4`, đúng lệnh owner 13/09.
- `FU-451a` (scorecard + stdout) **CHƯA ĐẠT**. Đúng dự kiến: scorecard chạy buổi tối, nên kiểm lại sau 18:45.
- PID service 1122833, không đổi từ 24/11 23:17.

### 3.2 Bốn model AI ở MN (`evidence/dong_ai_26_mn.txt`, `evidence/journal_0515.txt`)

| model | giờ ghi | số | lệnh gọi trong journal |
|---|---|---|---|
| `claude-opus-4-6` | 05:16:04 | `32` | `api.anthropic.com` 200 lúc 05:15:09 |
| `gpt-oss-120b` | 05:16:04 | `02 89` | `openrouter.ai` 200 lúc 05:15:11 |
| `gemini-2.5-flash` | 05:16:04 | `02 89` | `generativelanguage.googleapis.com` 200 lúc 05:15:43 |
| `claude-sonnet-4-6` | 05:16:06 | `85 53` | `api.anthropic.com` 200 lúc 05:16:06 |

Số dòng có số theo ngày: `gpt-oss-120b` 24/11 **3/3** · 25/11 **0/3** · 26/11 **1/1** (mới chạy MN). `glm-5.1` chỉ chạy
MT/MB, nên 26/11 chưa có dòng nào.

### 3.3 `gpt-oss-120b` và Gemini cùng ra `02 89`: trùng số hay chép? (RM-13)

Hai model ra cùng một cặp số, nên agent phải loại khả năng dòng `gpt-oss-120b` được chép từ đường dự phòng Gemini.
Ba bằng chứng cho thấy đây là **hai lượt độc lập**:

- Văn bản phân tích **khác cấu trúc**: `gpt-oss-120b` mở bằng `current_week_context`, Gemini mở bằng `db_tails`.
- **Khác băm**: `158859c9` (12.328 ký tự) và `790a26a9` (9.674 ký tự).
- Lệnh gọi OpenRouter về lúc 05:15:11, **sớm hơn** lệnh gọi Gemini 32 giây. Khi đó chưa có kết quả Gemini để chép.

### 3.4 OpenRouter thông lại lúc nào (`evidence/thu_openrouter_0525.txt`, `evidence/journal_0515.txt`)

- Lượt thử 25/11 21:39: `GET /key` 200 · `POST` tối thiểu **400** «Request path cannot be relayed» sau 0,25 s.
- Lượt thử 26/11 05:25:46: `GET /key` 200 · `POST` tối thiểu **200** sau 1,17 s, phản hồi `chat.completion` thật.
- Từ 25/11 17:33 tới 26/11 05:15:10, service **không gọi OpenRouter lần nào** (đếm journal: 0). Vì vậy thời điểm thông
  lại chỉ khoanh được trong khoảng **25/11 21:39 → 26/11 05:15:11**.
- Không có xác nhận chính thức về nguyên nhân. Agent không suy đoán thêm.

## 4. Hướng xử lý và vì sao chọn

- **Đóng `FU-452` là `CLOSED_PASS`.** Điều kiện đóng ghi sẵn ở V11192 là «MN có Opus + Sonnet ra số». Điều kiện này đạt,
  có lệnh gọi 200 trong journal làm chứng.
- **`FU-460` → `WAIT_LIVE`, chưa đóng.** Mới có một lượt MN, và `glm-5.1` chỉ chạy MT/MB. Đóng ngay là kết luận trên nửa
  bằng chứng (RM-07). Điều kiện đóng: lượt MT ~16:36 và MB ~17:32 ngày 26/11 có `glm-5.1` cùng `gpt-oss-120b` ra số, và
  journal không còn «Request path cannot be relayed». Nếu 400 quay lại thì trả mục về `OWNER_DECISION_NEEDED`, giữ nguyên
  hai lựa chọn của V11193.
- **Không đổi roster, không đưa DeepSeek vào.** Owner chưa chốt, và nay không còn lý do để đổi.

## 5. Đã làm gì

1. Đọc kết quả lượt kiểm hẹn giờ 05:24.
2. Đọc `predictions` ngày 26/11 trên VPS (`mode=ro`). Lần đầu ghi nhầm tên cột `region`; tra `PRAGMA table_info` ra
   `target_region` rồi chạy lại (RM-10).
3. Đọc journal 05:14–05:18 và đếm lệnh gọi OpenRouter từ 25/11 17:33.
4. So văn bản phân tích của bốn model AI ở MN.
5. Gọi thử OpenRouter **một lượt**, không retry, theo đúng thủ tục ghi ở `FU-460`.
6. Sao lưu `backups/*.pre_v11194`. Ghi bốn mặt (seq 509), khối `FU-452` `CLOSED_PASS` và khối `FU-460` `WAIT_LIVE`.
   Commit `639560b`, đẩy lên nhánh và `master`.

## 6. Cổng kiểm

| cổng | kết quả |
|---|---|
| `_v11044_cong_so_hieu.py` | cấp `V11194` (trống) |
| `_v11062_nang_version.py --kiem` | `NANG_VERSION_V11062=ĐẠT` (seq 509) |
| `_v10920_decision_ledger.py` | 0 TRÔI · 2 «không kết luận được» do DB local cũ (RM-01). Không đọc thành TRÔI |
| `_v11027_so_muc_quan_tri.py` | không mục nào biến mất |
| `trang_thai_mo_coi()` | trống; `FU-452` đọc ra `CLOSED_PASS`, `FU-460` đọc ra `WAIT_LIVE` |
| `_v10921_report_gate.py` ① + ② `V11194` | xem `CONVERSATION_CONTEXT` §4 |

## 7. Vướng vấp

- **Ghi nhầm tên cột `region`** ở câu truy vấn đầu. Bảng `predictions` dùng `target_region`. Đã tra `PRAGMA` trước khi
  chạy lại, không đoán tên khác.
- **Hai model ra cùng số `02 89`** dễ đọc thành «OpenRouter chưa thông, đường dự phòng chép số Gemini». Agent phải so văn
  bản phân tích và thứ tự lệnh gọi mới loại được giả thuyết đó (§3.3).

## 8. Gỡ về

Phiên không đổi runtime. Gỡ tài liệu: `git revert 639560b`. Bản sao trước khi ghi: `backups/*.pre_v11194`.

## 9. Theo dõi tiếp — liệt kê ĐỦ

| mã | việc | ai chặn | khi nào |
|---|---|---|---|
| `FU-460` | lượt MT/MB 26/11 có `glm-5.1` + `gpt-oss-120b` ra số ⇒ đóng `CLOSED_PASS`; 400 quay lại ⇒ trả owner | lượt tự nhiên | 26/11 ~17:35 |
| `FU-451a` | scorecard + stdout của lượt tối 26/11 | lượt tự nhiên | 26/11 sau 18:45 |
| `FU-455` | lưu khuyến nghị `/choi` trước giờ xổ; rà dòng «theo khuyến nghị» trong các báo cáo cũ | agent | trước 27/11 |
| `FU-328` + cảnh báo số dư | cổng model rỗng; báo khi model rơi, tài khoản cạn **hoặc nhà cung cấp chặn** | agent | trước 27/11 |
| `FU-453` · `FU-451b` · `FU-459` · `FU-270` | các việc chờ owner chốt | owner | — |
| `FU-195` · `FU-400` · `FU-183` · `FU-397` · `FU-456` · `FU-340/338` · `FU-345` · `FU-392` | bảy việc chuyên môn chờ owner chốt | owner | — |
| 8 mục giao diện | owner xem `/monitoring`, `/v82-monitor`, `/du-doan-test` | owner | — |
| `FU-457` · `FU-292` · `FU-318` · `FU-458` · `FU-204` | việc agent tự làm | agent | trước 28/11 |

## 10. Ba lớp nguồn (§62)

| lớp | nội dung | bằng chứng |
|---|---|---|
| `OWNER_SAID` | không có lời mới; hai yêu cầu cũ 25/11 ~13:12 và ~21:35, nguyên văn ở §2 | `docs/SO_TUONG_TAC_OWNER.md` |
| `CODE_DID` | MN 26/11: Opus, Sonnet, Gemini, `gpt-oss-120b` đều có số; OpenRouter 200 ở cả service lẫn lượt thử | `evidence/dong_ai_26_mn.txt`, `evidence/journal_0515.txt`, `evidence/thu_openrouter_0525.txt` |
| `DOC_SAID` | V11193 SSOT: «OpenRouter trả 400 … MT/MB dưới sàn §59»; `FU-460` `OWNER_DECISION_NEEDED` | `docs/CURRENT_TRUTH_SSOT.md` khối V11193, `docs/FOLLOW_UP_TRACKER.md` |

**Lệch `DOC_SAID` ≠ `CODE_DID`:** tài liệu V11193 tả OpenRouter đang chặn, trong khi thực tế sáng 26/11 đã thông. Đã sửa
trong phiên: khối V11194 ở SSOT ghi trạng thái mới và nói rõ nó thay dòng V11193; `FU-460` chuyển `WAIT_LIVE`.

**TanPhatAI cần làm:** cập nhật hiểu biết — OpenRouter **đã thông lại** (200 lúc 26/11 05:15:11), `gpt-oss-120b` có số ở
MN; owner **không còn phải chọn** `FU-460`. Theo dõi `FU-460` `WAIT_LIVE` tới lượt MB ~17:32 ngày 26/11 (`glm-5.1` phải có
số) và `FU-451a` sau 18:45. `FU-452` đã đóng đạt. Không có code đi trước tài liệu trong phiên này.
