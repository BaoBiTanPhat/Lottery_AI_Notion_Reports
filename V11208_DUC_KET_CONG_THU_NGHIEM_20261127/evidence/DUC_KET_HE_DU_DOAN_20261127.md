# ĐÚC KẾT — Hệ dự đoán Lottery_AI_Test, 01/08 → 27/11/2026

> Owner yêu cầu 27/11 (QD-084 khoản 2). Một trang. Mọi con số tái lập được bằng script đã commit: `web/backend/_v11206_mn_dao_sau.py
> <ngày> <miền>` · `_v11207_thiet_cai_san.py` · `_v11204_d30_phan_quyet.py` (chạy trên VPS, chỉ đọc).

## 1. Kết luận

**Sau bốn tháng đo ở cả ba miền, bạch thủ và lô 2 số của `/du-doan` không phân biệt được với chọn ngẫu nhiên** — xét **cả bốn cửa sổ**
(A 01/08→13/09 · B 14/09→27/11 · C 30 ngày · D gộp; xem bảng cửa sổ ở `CHANGELOG.md § V11206`), trong 24 ô (3 miền × 2 sản phẩm × 4 cửa
sổ) chỉ **hai ô** vượt |z| 2 — MN lô 2 số cửa sổ D (+2,01) và MB bạch thủ cửa sổ B (+2,03) — và **cả hai không lặp lại**: MN lô 2 số ở
MT +0,02 · MB +0,35; MB bạch thủ 30 ngày gần nhất −0,06. Với 24 ô, một hai ô quanh ±2 là mức nhiễu kỳ vọng; dấu đổi theo cửa sổ. Không đội hình model,
không cách bầu, không lane nào đã thử vượt được ngẫu nhiên một cách đo được. Lô có **thiệt cài sẵn 2,0%** do tỉ lệ trả thưởng — không có
lợi thế lớn hơn mức đó thì đánh lâu là lỗ dần.

| miền (01/08 → 25–27/11) | bạch thủ trúng / ngẫu nhiên | z | lô 2 số ≥1 trúng / ngẫu nhiên | z | lời/lỗ BT · lô |
|---|---|---|---|---|---|
| MN · 118 ngày | 46,6% / 43,1% | +0,78 | 76,3% / 67,7% | +2,01 | −15,4tr · +8,4tr |
| MT · 117 | 31,6% / 35,3% | −0,84 | 58,1% / 58,0% | +0,02 | −40,0tr · −26,1tr |
| MB · 117 | 29,9% / 23,7% | +1,57 | 43,6% / 42,0% | +0,35 | +28,2tr · −2,3tr |
| **gộp** | | **≈ +0,8** | | **≈ +1,3** | **≈ −27tr · −20tr** |

Kết luận này **không mới**: V10945 (01/08) đã đo «15/15 tổ hợp (3 miền × 5 kiểu đánh) không phân biệt được với ngẫu nhiên». Sau đó hệ
vẫn mở thêm hàng chục thử nghiệm.

## 2. Đã thử gì — ra sao

| thứ đã thử | kết quả | nguồn |
|---|---|---|
| đội hình lớn: 27 model AI, ~56 lượt gọi/ngày (01/08–13/09) | không model nào hơn ngẫu nhiên | V11206 |
| roster gọn 4 AI/miền, ~12 lượt/ngày (từ 14/09) | chất lượng không đổi — cắt một nửa LLM không phát hiện khác biệt (p = 1,0) | `_v11185` · V11206 |
| từng model, gộp 3 miền | cao nhất Opus z +2,33 · thấp nhất xgboost −1,67 — 13 phép so cần \|z\| ≈ 2,9 ⇒ không model nào kết luận được | V11207 |
| cách bầu: trọng số · chỉ ML · chỉ AI · combo-super · khử bầy đàn (D-30) | không cách nào hơn | V11206 · V11204 |
| luật đào được (mining) | luật thật không hơn luật giả (FU-338 · FU-340) | V11195 |
| trọng số vs luật thô | −2,80 điểm, z −1,72 (FU-400) | V11190 |
| prompt ba tầng · anti-trap · gỡ gan/nóng/lạnh | không đạt / không đo được (FU-398 · 397 · 284) | V11197 · V11190 |
| lane nghiệm thu · G2-MB · ML×luật×bộ lọc · gan hội tụ | không đạt / không có tín hiệu (FU-264 · 367 · 317 · 394) | V11197 · V11204 |

## 3. Vì sao bốn tháng không ra gì khác «ngẫu nhiên»

1. **Đối tượng:** nếu kết quả xổ là ngẫu nhiên công bằng, quá khứ không chứa quy luật để học — mọi số đo đều khớp với điều này.
2. **Cỡ mẫu** (n cần, đo cho thước bạch thủ vs nền — không phải tuyên bố hiệu quả): thấy +5 điểm ở bạch thủ cần **~590–775 ngày cho mỗi miền**; các phép đo dựng 14–60 ngày ⇒ về cấu trúc không thể kết luận.
3. **Nhìn nhiều lần:** mỗi lần đọc ~24 phép (3 miền × 2 sản phẩm × 4 cửa sổ) ⇒ vài \|z\| ≈ 2 là nhiễu; mỗi «điểm sáng» lại đẻ thêm thử nghiệm.

## 4. Lỗi phương pháp đã mắc — không lặp lại

| lỗi | ví dụ thật |
|---|---|
| dựng thử nghiệm trước khi tính n cần | cửa sổ 14–60 ngày cho câu hỏi cần ~600+ ngày |
| tin điểm sáng một nơi, không kiểm ở nơi khác | MN lô 2 số z +2,01 ⇒ MT +0,02 · MB +0,35 |
| thêm model/lane vì «có thể giúp» | 27 model AI, không model nào để lại giá trị đo được |
| tính sai phép kinh tế cơ bản | «thiệt cài sẵn 10%/14%» ⇒ thật 2,0% (RL-053) |
| đổi ngưỡng sau khi thấy số · đo trên nguồn sai | FU-427 · RM-13 (đo nhầm nguồn ba lần trong ngày 07/08) |

## 5. Từ nay (QD-084)

- **Đóng băng** đường dự đoán: luôn ra số, ghi thẳng «chưa có lợi thế đo được so với ngẫu nhiên» (giao diện: demo cho owner trước).
- **Không thêm, không cắt model** theo chênh lệch chưa đủ mức; chỉ dọn cờ chết (chạy khô: phiếu y hệt).
- **Thử nghiệm mới** chỉ qua cổng `web/backend/_v11208_cong_thu_nghiem.py` + `docs/DANG_KY_THU_NGHIEM.json`: khai giả thuyết · nền · MDE ·
  ngưỡng · ngày đọc **trước** ngày đầu; cổng tự tính n cần; **> 120 ngày ⇒ chặn** trừ khi owner duyệt. Nối cả hai cổng commit.
- Muốn câu trả lời dứt điểm: **một** phép thử gộp 3 miền đăng ký trước, ~240 ngày cho +5 điểm bạch thủ (n cần đo cho thước, cổng tự tính; FU-464 hướng 2 — owner chưa chọn).
