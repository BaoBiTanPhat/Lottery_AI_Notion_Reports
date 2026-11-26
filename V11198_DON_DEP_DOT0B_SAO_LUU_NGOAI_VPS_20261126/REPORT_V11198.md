# V11198 — Dọn dẹp Đợt 0b: sao lưu dữ liệu production ra ngoài VPS lần đầu sau 76 ngày · khoá bản sao DB để hở · QD-082 ↔ QD-058

> **Phiên bản:** V11198 · **Ngày:** 26/11/2026 12:28 → 12:40 ICT · **Repo riêng:** `Lottery_AI_Test` commit `a634502`
> (nhánh `fu438/admin-only-p0a` + `master`) · **governance_seq:** 513 · **Căn cứ:** `QD-082` · **Tầng (RM-12):**
> `RUNTIME_PROVEN` cho bản sao (băm khớp, manifest `status=ok`) · **Runtime đổi:** không (chỉ đọc DB để sao lưu + `chmod` một
> tệp cũ trong `/tmp`).

## 1. Tóm tắt

- **Dữ liệu production từ 11/09 (76 ngày) chưa có bản sao nào ngoài VPS** — bản ngoài VPS gần nhất là 02/09. Đã sao lưu về máy
  local bằng công cụ sẵn có, có đóng băng + so băm: DB **1.099.997.184 B**, sha256 `c45e2f66…`.
- Một bản DB đầy đủ ngày 11/09 nằm trong `/tmp` với quyền cho mọi tài khoản đọc — đã khoá chỉ root, không xoá.
- Sửa quan hệ quyết định QD-082 ↔ QD-058 (RM-19): QD-082 chỉ thay phần diễn giải «cấm tắt mọi cơ chế» của agent; lời owner
  «đừng đi lùi» giữ nguyên.

## 2. Owner yêu cầu gì (nguyên văn) — §62 lớp `OWNER_SAID`

**26/11/2026 ~12:0x ICT:** *«tiến hành các đề xuất an toàn trước, tuần tự , cuốn chiếu từ dễ đến khó từ đơn giản rõ ràng đến
phức tạp tra soát, soi xét kỹ lưỡng  v..v...»* (QD-082). Không có lời mới trong đợt này.

## 3. Đào bới / phát hiện — liệt kê ĐỦ

- Bước soát thiếu của luồng kiểm kê lập bảng «bản sao gần nhất ở đâu»: trên VPS 3 bản DB đầy đủ (30/05 330,6 MB · 11/09 12:13
  844,8 MB · 11/09 14:09 845,5 MB); ngoài VPS `live_sync` 02/09 ⇒ 76 ngày không có bản sao.
- `/tmp/lottery_ai.db.pre_w`: 845.463.552 B, ngày 11/09, `-rw-r--r--`, nằm trong `/tmp` (`drwxrwxrwt`) ⇒ mọi tài khoản đọc
  được; máy còn chạy các dịch vụ khác ngoài dự án. Không mã/cron nào nhắc tệp. Các bản dưới `/root` được quyền thư mục
  `/root` (`dr-xr-x---`) che. Service `lottery` chạy bằng root ⇒ `chmod 600` không ảnh hưởng gì đang chạy.
- QD-058 (ACTIVE, 10/08) ghi diễn giải «CAM go/tat/cat bat cu co che nao — chi duoc THEM phep do», còn QD-082 ghi `thay_the=[]`
  ⇒ hai quyết định ngược nhau cùng hiệu lực.
- Còn sót: tệp rỗng `/tmp/_live_sync_20260808_183415_lottery_ai.db` (0 byte) của lần đồng bộ hỏng 08/08.

## 4. Hướng xử lý và vì sao chọn

- Sao lưu bằng **công cụ chuẩn của dự án** (`web/_sync_live_forensic_inputs.py`, quy định ở CLAUDE.md «Toàn vẹn dữ liệu sống»):
  đóng băng bằng `sqlite3 .backup` (nhất quán dù production đang ghi), tải về, so băm, xoá bản đóng băng, ghi manifest. Không
  dựng công cụ mới.
- Khoá quyền thay vì xoá: xoá một bản sao là việc của đợt lưu trữ, cần owner chốt «giữ bao nhiêu bản».
- RM-19: tách đúng ba lớp (§62) — lời owner (đừng đi lùi) khác diễn giải của agent (cấm tắt mọi thứ).

## 5. Đã làm gì

1. Đọc mã công cụ đồng bộ: nơi đặt bản đóng băng (`/tmp/_live_sync_*`) và việc xoá sau khi tải.
2. Chạy đồng bộ 12:32:48 → 12:34:15; kiểm manifest, kích thước, bản đóng băng đã xoá.
3. Soi quyền 4 bản DB trên VPS + quyền thư mục; `chmod 600` bản trong `/tmp`.
4. Ghi quan hệ thay thế một phần hai chiều vào sổ quyết định.
5. Chạy lại `_v10920_decision_ledger.py` trên dữ liệu mới: 0 TRÔI · 0 «không kết luận được».
6. Ghi bốn mặt (seq 513), FU-462. Commit `a634502`.

## 6. Cổng kiểm

| cổng | kết quả |
|---|---|
| công cụ đồng bộ | `status=ok` · «Local forensic inputs now match VPS copies» · bản đóng băng hôm nay đã xoá |
| kích thước DB | local 1.099.997.184 B = VPS 1.099.997.184 B |
| `_v10920_decision_ledger.py` | 0 TRÔI · 0 «không kết luận được» (trước: 1–2 do DB local cũ) |
| `_v11062_nang_version.py --kiem` | `ĐẠT` (seq 513) |
| `_v11027_so_muc_quan_tri.py` | không mục nào biến mất |
| `trang_thai_mo_coi()` | trống |
| `_v10921_report_gate.py` ① + ② `V11198` | xem `CONVERSATION_CONTEXT` §4 |

## 7. Vướng vấp

- Manifest đồng bộ có trường địa chỉ máy chủ ⇒ bằng chứng công khai là bản **đã ẩn địa chỉ** (`evidence/manifest_live_sync_*_an_ip.json`).

## 8. Gỡ về

- `chmod 644 /tmp/lottery_ai.db.pre_w` (nếu cần trả quyền cũ).
- Bản local cũ trước đồng bộ: `artifacts/live_sync/20261126_123248/before_local/` (local).
- Sổ quyết định: `backups/OWNER_DECISION_LEDGER.json.pre_v11197b`. Tài liệu: `git revert a634502`.

## 9. Theo dõi tiếp — liệt kê ĐỦ

| mã | việc | ai chặn | khi nào |
|---|---|---|---|
| `FU-462` | kiểm 9 lịch Đợt 1 + 2a không chạy; `_v10900` không thêm LỆCH | lượt tự nhiên | 27/11 |
| sao lưu định kỳ | lịch sao lưu ngoài VPS (tần suất, giữ mấy bản) | owner | phương án đầy đủ |
| bản sao DB cũ | 3 bản trên VPS (≈ 2 GB) — giữ hay bỏ | owner | đợt lưu trữ |
| bảo mật máy chủ | một việc cấu hình — chi tiết chỉ ở kho riêng | owner | khi anh đồng ý |
| restart gộp | FU-455 · FU-451 (in chết sau 19:20) · 5 job tắt còn đăng ký | agent | sáng 27/11 |

## 10. Ba lớp nguồn (§62)

| lớp | nội dung | bằng chứng |
|---|---|---|
| `OWNER_SAID` | QD-082; trong QD-058 owner nói «đừng đi lùi», không nói «cấm tắt mọi cơ chế» | `docs/OWNER_DECISION_LEDGER.json` QD-058 `nguyen_van` |
| `CODE_DID` | bản sao local băm khớp; `/tmp/lottery_ai.db.pre_w` `-rw-------` | `evidence/live_sync_output.txt` · `evidence/manifest_*_an_ip.json` |
| `DOC_SAID` | QD-058 `quyet_dinh` ghi «CAM go/tat/cat bat cu co che nao» | sổ quyết định |

**Lệch:** `OWNER_SAID` ≠ `DOC_SAID` ở QD-058 (diễn giải của agent rộng hơn lời owner) — đã ghi thay thế một phần, hai chiều.

**TanPhatAI cần làm:** cập nhật hiểu biết — đã có bản sao production ngoài VPS (26/11 12:34); QD-082 thay một phần QD-058 (phần
diễn giải), QD-058 vẫn ACTIVE. Theo dõi FU-462 (27/11). Không có code đi trước tài liệu trong đợt này.
