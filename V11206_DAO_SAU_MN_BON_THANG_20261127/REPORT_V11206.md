# V11206 — Đào sâu dự đoán MN 27/11 + bốn tháng ba miền: chưa có lợi thế đo được so với chọn ngẫu nhiên

> **Phiên bản:** V11206 · **Ngày:** 27/11/2026 ~16:45 → 17:10 ICT · **Repo riêng:** `8581262` · **governance_seq:** 520 · **Theo dõi:** FU-464
> · **Tầng (RM-12):** `RUNTIME_PROVEN` (DB VPS, chỉ đọc) · **Runtime đổi:** không.

## 1. Tóm tắt

- **MN 27/11:** bạch thủ **17 trượt**, lô 2 số **17 · 05 trượt cả hai**, `/choi` 17 trượt. #1 của 0/12 model về.
- **Nguyên nhân:** số 17 thắng phiếu nhờ 6 phiếu — 3 ML gốc cộng **hai model gộp và combo-super vốn cộng lại chính ý kiến ML**
  (bầy đàn). 4 model AI chọn số khác, cũng trượt.
- **Bốn tháng, ba miền:** bạch thủ và lô 2 số **không phân biệt được với chọn ngẫu nhiên** (gộp: z ≈ +0,8 và +1,3). Điểm sáng đơn lẻ
  (MN lô 2 số z +2,01) **không lặp lại** ở MT/MB.
- **Vì sao mấy tháng không trả lời được:** thấy +5 điểm ở bạch thủ cần ~590–775 ngày **cho mỗi miền**.

## 2. Owner yêu cầu gì (nguyên văn)

**27/11 ~16:45:** *«MN nay dự đoán sao em? nguyên nhân , kết quả, hậu quả, kiểm chứng , thực nghiệm moi thứ cần đào sâu kiểm tra dùm anh
chứ chạy không mấy tháng trời đốt rất nhiều token và thời gian rồi em»*

## 3. Đào bới / phát hiện — liệt kê ĐỦ

| phép | kết quả |
|---|---|
| đánh giá ngày (`_v11193_danh_gia_ngay.py`) | MN 3 đài, 37 đuôi về (nền 1 số 37%, 2 số 61%); BT −2,7tr · lô 2 số −5,4tr · `/choi` −2,7tr |
| phiếu công bố | 17: 0,321 (6 phiếu: 3 ML · 2 gộp ML · combo-super) · 05: 0,277 (4 phiếu ML) · 53: 0,140 · 34: 0,125 (AI) — 10 số đầu chỉ 03 về |
| từng model | #1: 0/12 về; #2 về: lstm 03 · combo-super 21 · gpt-oss-120b 65 |
| bốn cửa sổ MN | xem bảng mục 5 và `evidence/mn_dao_sau_20261127.txt` |
| đối chứng ngoài miền | MT, MB chạy y hệt (`evidence/mt_mb_doi_chung.txt`) |
| phản thực | «ML gốc biểu quyết» dưới nền ở cả 3 miền (cửa sổ hiện hành z −0,51 · −1,04 · −0,71); «AI biểu quyết» −0,51 · +0,43 · −0,71 |
| từng model MN 118 ngày | cao nhất claude-opus-4-6 z +2,03 (n 104) · thấp nhất gemini-2.5-flash z −2,02 — với 27 model, ±2 ở hai đầu là mức nhiễu kỳ vọng |
| lượt gọi model AI cho MN | 18,6/ngày (01/08–13/09, 27 model AI) → 3,6/ngày (roster QD-080) → 3,0/ngày (30 ngày) |
| `/choi` | khuyến nghị «NGHỈ» hôm nay ghi 16:40 — sau giờ xổ (FU-455) |

## 4. Hướng xử lý và vì sao chọn

Dùng **một thước cho mọi phép**: nền đúng ngày từng sản phẩm (RM-18), chỉ bản ghi tạo trước hạn output cuối (PRJ-SELECTION-WINDOW lọc 1),
z trên tổng Bernoulli, n cần cho +5 điểm. Một điểm sáng chỉ được tin khi **lặp lại ngoài nơi nó được nhìn thấy** — nên chạy lại y hệt cho
MT và MB thay vì đào thêm trong MN. Không viết chữ «thắng» ở đâu (RM-03: các cửa sổ này không đăng ký trước).

## 5. Đã làm gì

| miền (01/08 → 25–27/11) | bạch thủ trúng / nền | z | lời/lỗ | lô 2 số ≥1 trúng / nền | z | lời/lỗ |
|---|---|---|---|---|---|---|
| MN (118 ngày) | 46,6% / 43,1% | +0,78 | −15,4tr | 76,3% / 67,7% | +2,01 | +8,4tr |
| MT (117) | 31,6% / 35,3% | −0,84 | −40,0tr | 58,1% / 58,0% | +0,02 | −26,1tr |
| MB (117) | 29,9% / 23,7% | +1,57 | +28,2tr | 43,6% / 42,0% | +0,35 | −2,3tr |
| **gộp** (trúng 127 vs 119,9 · lô 209 vs 196,9) | | **≈ +0,8** | **≈ −27tr** | | **≈ +1,3** | **≈ −20tr** |

Script tái lập commit kèm: `web/backend/_v11206_mn_dao_sau.py <ngày> [MN|MT|MB]`. Mở FU-464 để owner chọn hướng dùng hệ dự đoán.

## 6. Cổng kiểm

| cổng | kết quả |
|---|---|
| hai đường đo độc lập cho MN 27/11 (`_v11193` và `_v11206`) | khớp: 37 đuôi, 17 và 05 trượt |
| chạy lại MN tới 25/11 sau khi thêm tham số miền | 117 ngày: BT z +0,85, lô z +2,14 — cùng chiều bản 118 ngày |
| `_v11062_nang_version.py --kiem` | ĐẠT |
| `_v10921_report_gate.py` ② `V11206` | xem `CONVERSATION_CONTEXT` §4 |

## 7. Vướng vấp

- Bảng từng model của `_v11193` ra rỗng cho 27/11 — tự tính lại từ `predictions` (12 dòng đủ).
- Số gộp lần đầu chép +0,9 / +1,4; tính lại tay từ ba dòng ra +0,8 / +1,3 — sửa trước khi ghi.

## 8. Gỡ về

Chỉ đọc, không đổi runtime. Tài liệu: `git revert 8581262`.

## 9. Theo dõi tiếp — liệt kê ĐỦ

| mã | việc | ai | hạn |
|---|---|---|---|
| FU-464 | chọn hướng: (1) giữ làm tham khảo, ghi thẳng «chưa có lợi thế» · (2) MỘT phép thử đăng ký trước, gộp 3 miền · (3) bớt lượt gọi AI theo §59 | owner | 03/12 |
| FU-455 | khoá khuyến nghị `/choi` lúc chốt | agent | 28/11 |

## 10. Ba lớp nguồn (§62)

| lớp | nội dung | bằng chứng |
|---|---|---|
| `OWNER_SAID` | hỏi MN hôm nay và mấy tháng chạy có đáng không | kho riêng `docs/SO_TUONG_TAC_OWNER.md` 27/11 ~16:45 |
| `CODE_DID` | bốn tháng không phân biệt được với ngẫu nhiên; bầy đàn trong phiếu | `evidence/` |
| `DOC_SAID` | các phép đo 14–60 ngày dựng từ tháng 7 hứa «đọc kết quả» sau vài tuần | sổ theo dõi các FU đo lường |

**Lệch:** `DOC_SAID` ≠ `CODE_DID` — cỡ mẫu cần (~590–775 ngày/miền) lớn hơn mọi cửa sổ đã đặt hàng chục lần; đó là lý do các phép đo
kết thúc ở «chưa được phép kết luận».

**TanPhatAI cần làm:** ghi FU-464 (chờ owner) và câu trạng thái «chưa có lợi thế đo được» vào hiểu biết chung. Code đi trước tài liệu: không.
