# CONVERSATION CONTEXT — V11180 · 11/09/2026 · Prompt 43 R1 §W (W0–W7)

> Một trong ba bản cùng ngày. Ngữ cảnh đầy đủ ở
> [`CONVERSATION_CONTEXT_V11181_20260911.md`](../V11181_W_FAILCLOSED_NATURAL_LANE_20260911/CONVERSATION_CONTEXT_V11181_20260911.md).

---

## Owner nói gì — nguyên văn, theo giờ

**~13:27 ICT** — prompt §W:

> *"W0 — QUYẾT ĐỊNH 13:30 NGAY LẬP TỨC, FAIL-CLOSED… Không được trì hoãn câu trả lời GO/NO-GO
> để viết báo cáo dài."*

> *"W1 — `exact_tails` KHÔNG đồng nghĩa action-eligible… Không bao giờ gán
> `diagnostic_label=ACTIONABLE` chỉ vì `model_decision=RANKED`."*

> *"W2 — Loại bỏ điều kiện pre-draw `st_src == ACTUAL_FOR_DATE` vì trước giờ xổ target chưa thể
> có actual result đầy đủ."*

> *"W4 — Không group bằng `model_id` prefix… Không dùng `COUNT(*)>0` để kết luận upstream hoàn
> tất… `NON_TTY_sh` không đủ để kết luận `CRON_NATURAL`."*

> *"W7 — Không group BASE và DELTA thành một Top-K chưa từng tồn tại."*

> *"Không nới thống kê hoặc action gate để tạo giả ứng viên đủ điều kiện."*

---

## Agent làm gì

**13:27–13:35** — kiểm gói freeze `12:32:54` theo **từng** tiêu chí §W0.A bằng lệnh. Ra
**7/16 trường thiếu/bẩn**. Xuất quyết định W0 **ngay**, không viết báo cáo dài trước như Owner
yêu cầu.

**13:35–14:35** — 68 phút sửa 10 lỗi: 35 khối vá vào module chính qua ba đợt, viết
`_v11180_lich_dai.py` / `_v11180_migrate_w.py` / `_v11180_thu_w.py`, viết lại
`_v11178_freeze.py` và `_v11178_lane.sh`, migration, deploy, ba bộ test, đóng hai gói freeze
hợp lệ lúc `14:32:47` và `14:32:57`.

---

## Vấp ở đâu

### 1 · `RM-10` — đoán tên, hai lần, cổng bắt cả hai
- `getattr(gpt_analyzer, "OPENROUTER_MODELS", [])` — tên **không tồn tại** trong module đó; mặc
  định `[]` khiến nó **trượt im lặng**, tức bản đồ tuyến provider sẽ sai mà không ai biết. Tên
  thật đọc bằng grep: `gpt_analyzer.OPENROUTER_MODELS_SET` (dòng 125) và
  `model_registry.OPENROUTER_MODELS` (dòng 1051). Cổng `_v11020_cong_doan_ten` chặn commit.
- Cột `final_bundles.final_numbers_json` — **không tồn tại**, script EOD sập ngay. Tên cột thật
  đọc bằng `PRAGMA table_info`.

### 2 · `RM-09` — đếm chuỗi thô, hai lần
Hai phép test `W5-15`/`W5-16b` quét `EXEC_LIVE` và `would_save` trên **cả tệp**. Hai chuỗi đó
còn trong **docstring mô tả lỗi cũ** — `§60.3` bảo **GIỮ** chú thích làm bằng chứng đã làm. Sửa:
thêm `ma_thuan()` / `ma_thuan_sh()` bỏ docstring và chú thích trước khi quét.

### 3 · Heredoc nuốt `\n` — lần thứ ba trong ngày
Làm hỏng `_v11180_thu_w.py` (`return "` không đóng chuỗi). Từ đó chuyển hẳn sang Write tool.

### 4 · Fixture sai ba lần, cổng đúng cả ba
- 40 ngày → chỉ 5 ngày cùng thứ, dưới `MIN_MAU_LICH_SU=8` ⇒ cổng lịch đài **từ chối**.
- Fixture dùng đài giả (`TP.HCM`/`Da Nang`/`Ha Noi`) không khớp lịch canonical.
- Mỗi đài 4 số, dưới `TOI_THIEU_SO_MOI_DAI=10` ⇒ upstream báo `PARTIAL`.

Cả ba lần đều là **code đúng, fixture sai**. Nới fixture, **không** nới ngưỡng.

### 5 · `worktree_clean` không bao giờ đạt
`docs/_I2_DA_CHAY.json` do **chính hook cổng commit** ghi ra **trong lúc** commit ⇒ commit xong
là bẩn lại, commit thêm cũng không thoát vòng. Chọn khai báo `worktree_exclusions` tường minh
kèm hash thay vì nới định nghĩa "sạch" — để việc loại trừ **không** thành lỗ hổng im lặng.

### 6 · Hook chặn cả lệnh, kể cả phần vá
Hai lần một lệnh Bash gộp `python … && git commit` bị hook chặn ⇒ **phần vá cũng không chạy**,
nhưng thông điệp commit đã mô tả nó như đã làm. Phát hiện khi kiểm lại tệp; ghi đính chính
`V11179c` thay vì sửa im lặng.

---

## Code đi trước tài liệu

Có. `_v11180_lich_dai.py` · `_v11180_migrate_w.py` · `_v11180_thu_w.py` · `_v11178_freeze.py`
viết lại, cùng 35 khối vá cho `_v11178_context_only_v11.py`, `_v11178_ranker.py`,
`_v11178_eod.py`, `_v11178_lane.sh`. Ghi nhận vào `docs/SO_TUONG_TAC_OWNER.md` **trong cùng
phiên**, kèm nguyên văn và giờ.
