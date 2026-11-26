# V11199 — Vá gốc «print của service chết sau 19:20»: v94/v95 thay `sys.stdout` lúc import, cổng V11189 mù `importlib`

> **Phiên bản:** V11199 · **Ngày:** 26/11/2026 ~12:50 → 13:40 ICT · **Repo riêng:** `Lottery_AI_Test` commit `977273b`
> (nhánh `fu438/admin-only-p0a` + `master`) · **governance_seq:** 514 · **Căn cứ:** QD-082 + CLAUDE.md «lỗi rõ ràng có bằng
> chứng: sửa ngay» · **Tầng (RM-12):** `DEPLOYED` (tệp trên VPS 13:30, md5 khớp) — `RUNTIME_PROVEN` chỉ sau lượt kiểm 21:05 ·
> **Runtime đổi:** có (3 mô-đun service nạp lúc 19:18/19:20), **không restart**.

## 1. Tóm tắt

- Mỗi tối từ 19:20, mọi `print` của service chết im lặng tới lần restart sau. Gốc: hai mô-đun đo shadow thay `sys.stdout` lúc
  import, và service nạp chúng bằng `importlib` lúc 19:18 rồi 19:20 — lần thứ hai làm GC đóng buffer chung.
- Dự đoán, kết quả, chấm vẫn chạy đúng; thứ mất là khả năng quan sát buổi tối (chính vì vậy hai sự cố model chết lọt lâu).
- V11192 ghi «FU-451a `RUNTIME_PROVEN`» — **sai** (RL-052): phép kiểm chỉ soi tới 18:45, và cổng V11189 không thấy mô-đun nạp
  bằng `importlib`. Đã vá cả 3 tệp + làm cứng cổng; có hiệu lực từ 19:18 tối nay mà không cần restart.

## 2. Owner yêu cầu gì (nguyên văn) — §62 lớp `OWNER_SAID`

Không có lời mới. Thi hành QD-082 (26/11 ~12:0x): *«tiến hành các đề xuất an toàn trước, tuần tự , cuốn chiếu từ dễ đến khó từ
đơn giản rõ ràng đến phức tạp tra soát, soi xét kỹ lưỡng  v..v...»* — việc này nằm trong Đợt 0 của phương án dọn dẹp.

## 3. Đào bới / phát hiện — liệt kê ĐỦ

- **Đọc mã:** `_materialize_v94_safe_batch.py:52`, `_materialize_v95_data_integrity_audit.py:32` gán
  `sys.stdout = io.TextIOWrapper(sys.stdout.buffer, …)` ở cấp mô-đun (trong `try`). `scheduler.py:8982` và `:9019` nạp bằng
  `importlib.import_module` trong tiến trình service (job 19:18 và 19:20).
- **Đo thật** (`evidence/kiem_stdout_toi.py`): 25/11 19:21–21:00 journal có 71 dòng — **logging 71 · print 0**.
- **Tái hiện** (`evidence/tai_hien_stdout.py`): nạp bản cũ cả hai tệp trong một tiến trình rồi `print` ⇒ `ValueError: I/O
  operation on closed file` (`evidence/tai_hien_ban_cu.txt`); bản mới ⇒ in bình thường (`evidence/tai_hien_ban_moi.txt`).
- **Quét cả họ (RM-07)** (`evidence/tim_stdout.py`, AST): 30 tệp trong `web/backend` có mẫu này; 11 tệp service nạp; chỉ **3**
  gán lúc import (`v94`, `v95`, `_v101_shadow_pilot` — tệp thứ ba nằm dưới `return` của job tắt). 8 tệp còn lại gán trong
  `__main__` hoặc trong hàm.
- **Vì sao cổng mù:** `_v11189_cong_stdout.py` dựng tập mô-đun service nạp bằng regex dòng `import`/`from` — bỏ sót
  `importlib.import_module('…')`.

## 4. Hướng xử lý và vì sao chọn

- Thay phép gán bằng `sys.stdout.reconfigure(encoding="utf-8", errors="replace")` trong `try`: đổi mã hoá tại chỗ, không tạo
  wrapper mới — khi chạy như script vẫn in UTF-8 như cũ. Đây đúng dạng cổng V11189 chấp nhận.
- Không restart: tiến trình hiện tại (khởi động 10:47) chưa nạp hai tệp; lần nạp đầu là 19:18 ⇒ nạp bản mới. Đặt tệp trước 15:30
  (ngoài khung cấm).
- Làm cứng cổng trước khi coi là xong (RM-15) — cổng mù chính là lý do lỗi sống sót qua V11189.

## 5. Đã làm gì

1. Đọc mã, đo journal 25/11, tái hiện local (bản cũ chết, bản mới sống).
2. Quét AST 11 mô-đun service nạp; vá 3 tệp gán lúc import.
3. Cổng: đọc thêm `importlib.import_module` / `__import__`; thêm 2 ca thử chặn.
4. Sao lưu `backups/*.pre_v11199` (local + VPS) → tải lên VPS 13:30 → md5 khớp → compile OK → cổng trên VPS `DAT`.
5. Hẹn kiểm lượt thật 21:05. Ghi bốn mặt (seq 514), FU-451, RL-052 + chú thích rút lại tại chỗ gốc. Commit `977273b`.

## 6. Cổng kiểm

| cổng | kết quả |
|---|---|
| `_v11189_cong_stdout.py --thu-chan` | 7/7 — ca `importlib` vi phạm ⇒ thoát 1 · bản sạch ⇒ 0 |
| bản CŨ `v94` (git HEAD) + cổng mới | **thoát 1** (bắt được) · bản mới ⇒ 0 |
| cổng trên VPS | `CONG_STDOUT_V11189=DAT` (137 tệp, 0 vi phạm) |
| tái hiện tiến trình | bản cũ `closed file` · bản mới in được |
| PID service | 1277779 trước = sau (không restart) |
| `_v11062_nang_version.py --kiem` · `_v11027_so_muc_quan_tri.py` | `ĐẠT` · không mục nào biến mất |
| `_v10921_report_gate.py` ① + ② `V11199` | xem `CONVERSATION_CONTEXT` §4 |

## 7. Vướng vấp

- Lần quét đầu đếm 30 tệp có mẫu — phải phân loại bằng AST (lúc import hay trong hàm/`__main__`) mới ra đúng 3 tệp (RM-09).

## 8. Gỡ về

Khôi phục `backups/_materialize_v94_safe_batch.py.pre_v11199`, `…v95…`, `_v101_shadow_pilot.py.pre_v11199` (có cả trên VPS) —
có hiệu lực ở lần nạp tiếp theo. Cổng: `git revert 977273b`.

## 9. Theo dõi tiếp — liệt kê ĐỦ

| mã | việc | ai chặn | khi nào |
|---|---|---|---|
| `FU-451` (a) | `/tmp/kiem_stdout_toi.py`: print > 0 trong 19:21–21:00 ngày 26/11 ⇒ đóng (a) | lượt tự nhiên | 26/11 21:05 |
| `FU-451` (b) | tính bù bảng xét thăng hạng 72 ngày | owner | — |
| phương án dọn dẹp | phát hành bản đầy đủ (Đợt 0–3, câu owner 1A–3G) | agent | bản sau |

## 10. Ba lớp nguồn (§62)

| lớp | nội dung | bằng chứng |
|---|---|---|
| `OWNER_SAID` | QD-082 | `docs/SO_TUONG_TAC_OWNER.md` 26/11 ~12:0x |
| `CODE_DID` | 25/11 sau 19:20 print 0 dòng; tái hiện `closed file` | `evidence/` |
| `DOC_SAID` | V11192: «FU-451 phần (a) `RUNTIME_PROVEN`» | `CHANGELOG.md` § V11192 · `REPORT_V11192.md` |

**Lệch:** `DOC_SAID` ≠ `CODE_DID` — đã rút lại (RL-052) tại cả hai chỗ gốc.

**TanPhatAI cần làm:** cập nhật hiểu biết — FU-451a chưa từng đạt cho tới hôm nay (RL-052); bản vá V11199 có hiệu lực từ 19:18
26/11. Theo dõi kết quả kiểm 21:05. **Code đi trước tài liệu:** tệp lên VPS 13:30, tài liệu commit ~13:40 — cùng phiên; căn cứ
`docs/SO_TUONG_TAC_OWNER.md` dòng «26/11 ~12:0x» (QD-082).
