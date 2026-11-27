# V11202 — Bảo mật máy chủ: hai việc owner duyệt đã làm xong và kiểm hai chiều

> **Phiên bản:** V11202 · **Ngày:** 27/11/2026 ~14:55 → 15:25 ICT · **Repo riêng:** commit `e4f98f4` · **governance_seq:** 517
> · **Quyết định:** QD-083 · **Theo dõi:** FU-463 · **Tầng (RM-12):** `RUNTIME_PROVEN` (kiểm trên máy chủ thật)
> · **Service `lottery`:** không restart, mã ứng dụng không đổi.

Theo luật của kho công khai, chi tiết bảo mật máy chủ **chỉ ghi ở kho riêng** (`CHANGELOG.md § V11202`, `FU-463`). Báo cáo này ghi
việc gì đã làm, kiểm ra sao, còn treo gì — không ghi cấu hình.

## 1. Tóm tắt

- Owner duyệt hai việc bảo mật máy chủ; cả hai đã làm xong, mỗi việc có hẹn tự gỡ về trong lúc đổi, kiểm hai chiều rồi mới huỷ hẹn.
- Một bản chụp tệp hệ thống được gỡ khỏi chỉ mục git của kho riêng (tệp vẫn còn trên đĩa).
- Hai việc owner giao «kiểm» đã kiểm xong; ba đề xuất xử lý chờ owner duyệt rõ.
- Một việc owner tự làm (agent cố ý không giữ thông tin đăng nhập).

## 2. Owner yêu cầu gì (nguyên văn)

**27/11 ~14:50** — phần không thuộc bảo mật, nguyên văn:
*«B. Ba câu cũ đang treo ==> cái này em cần kiểm tra tra soát đối chiếu chứ em · C đồng ý theo khuyến nghị nha em. · ==> tất cả kiểm
tra đối chiếu , đối soát , xử lý bài bản chuẩn chỉnh dùm anh nha em. Tinh gọn chính xác ổn định»*

Phần A1–A4 (bảo mật máy chủ): **lược khỏi bản công khai**; nguyên văn ở kho riêng `docs/SO_TUONG_TAC_OWNER.md` dòng 27/11 ~14:50 và
`docs/OWNER_DECISION_LEDGER.json` QD-083.

## 3. Đào bới / phát hiện

- Kiểm cấu hình và nhật ký đăng nhập máy chủ; kiểm khoá đang được phép đăng nhập và khoá nào thật sự được dùng (4 tuần nhật ký).
- Quét các bản sao tệp bí mật trên máy chủ (chỉ đọc quyền tệp và băm, không in giá trị) — có bản sao cần thu gọn.
- Kiểm dịch vụ không thuộc dự án và mức sử dụng thật — có dịch vụ không ai dùng.
- Phát hiện một ràng buộc phải giữ: đường gia hạn chứng chỉ HTTPS của trang chính đi qua một dịch vụ tưởng là thừa.
- Quét kho riêng tìm tệp nhạy cảm: 155 tệp của một bản chụp hệ thống; 10 tệp khác khớp mẫu tìm kiếm nhưng chỉ là chuỗi mẫu trong công cụ
  kiểm (đã phân loại theo RM-09, không phải dữ liệu bí mật).

## 4. Hướng xử lý và vì sao chọn

Làm đúng phần owner duyệt «làm»; phần owner duyệt «kiểm» thì chỉ kiểm và trình đề xuất. Mỗi thay đổi trên máy chủ có sao lưu, có hẹn
tự gỡ về nếu agent mất đường vào, và chỉ huỷ hẹn sau khi kiểm cả chiều «chặn» lẫn chiều «vẫn vào được».

## 5. Đã làm gì

1. Hai thay đổi cấu hình máy chủ owner duyệt — xong, kiểm hai chiều.
2. Gỡ 155 tệp bản chụp hệ thống khỏi chỉ mục git kho riêng + `.gitignore`.
3. Cổng mới `web/backend/_v11202_kiem_baomat.py` (ba phép) + thử chặn 5 ca.
4. Bốn mặt (seq 517), QD-083, FU-463, sổ tương tác owner. Commit `e4f98f4`.

## 6. Cổng kiểm

| cổng | kết quả |
|---|---|
| `_v11202_kiem_baomat.py` | `BAOMAT_V11202=DAT` |
| `_v11202_kiem_baomat.py --thu-chan` (RM-15) | 5/5 ca đúng: sạch ⇒ ĐẠT; 4 vi phạm giả ⇒ TRƯỢT |
| `_v11062_nang_version.py --kiem` | ĐẠT |
| `_v10920_decision_ledger.py` | QD-083 🟢 1/1 · 0 TRÔI |
| `_v10921_report_gate.py` ② `V11202` | xem `CONVERSATION_CONTEXT` §4 |

## 7. Vướng vấp

- Một phép thử của chính agent làm công cụ phía máy dev tự xoá bớt dữ liệu nhận diện máy chủ ⇒ báo hỏng giả; tìm ra nguyên nhân và kiểm
  lại đúng cách.
- Bộ phân quyền của Claude Code từ chối chạy gộp ba việc xử lý vì owner mới duyệt «kiểm» cho phần đó — đúng; đã chuyển thành đề xuất
  chờ owner.

## 8. Gỡ về

Lệnh gỡ về từng việc ghi ở kho riêng (QD-083 `go_ve`). Tài liệu: `git revert e4f98f4`.

## 9. Theo dõi tiếp

| mã | việc | ai chặn | hạn |
|---|---|---|---|
| FU-463 | một việc owner tự làm + ba đề xuất chờ owner duyệt rõ | owner | 29/11 |
| FU-462 | Đợt 1 dọn dẹp (owner đã duyệt) — thi hành ngoài khung 15:30–18:15 | agent | 28/11 |
| FU-345 · FU-459 · FU-451(b) | owner giao agent tự tra soát đối chiếu | agent | 03/12 |

## 10. Ba lớp nguồn (§62)

| lớp | nội dung | bằng chứng |
|---|---|---|
| `OWNER_SAID` | duyệt hai việc bảo mật, giao kiểm hai việc, giao tra soát câu B, duyệt Đợt 1 | kho riêng `docs/SO_TUONG_TAC_OWNER.md` 27/11 ~14:50 |
| `CODE_DID` | hai thay đổi cấu hình máy chủ có hiệu lực; 155 tệp ra khỏi git | `_v11202_kiem_baomat.py` = DAT |
| `DOC_SAID` | phương án 26/11 ghi bốn câu bảo mật «chờ owner» | `docs/KE_HOACH_DON_DEP_20261126.md` mục A5 |

**Lệch:** một con số trong phương án 26/11 (mục bảo mật) không ghi đường dẫn và gọi sai loại tệp; kiểm lại ra số đúng lớn hơn. Đã ghi
đúng ở kho riêng.

**TanPhatAI cần làm:** cập nhật FU-463 (chờ owner: một việc owner tự làm + duyệt ba đề xuất) và QD-083; chi tiết đọc ở kho riêng. Code
đi trước tài liệu: không — thay đổi máy chủ và tài liệu cùng bản V11202.
