# CONVERSATION CONTEXT — V11189 · Kiểm tổng lực sau 71 ngày đứng, 24/11/2026 22:50 → 23:5x ICT

## 1. Owner nói gì — nguyên văn

| giờ (ICT) | nguyên văn | loại |
|---|---|---|
| 24/11 ~22:50 | *"rất lâu rồi chưa kiểm tra hệ vận hành , hiện anh để khá lâu rồi em tiến hành đo kiểm tổng lực dùm anh , phát hiện gì , xử lý ra sao em?"* | YÊU_CẦU |

Đó là lời duy nhất của owner trong phiên. Owner không có mặt để trả lời câu hỏi giữa phiên — mọi việc
cần owner quyết được **trình**, không tự làm.

## 2. Thứ tự thật của phiên

1. `_v10920_session_start.py` — briefing: 164 mục quá hạn, 26 quyết định tới hạn rà soát, 2 mồ côi.
2. Đọc playbook §2/§3 (10 bộ tự kiểm có sẵn), đọc ghi nhớ: **đo thẳng trên DB VPS**, báo tiến độ từng chặng.
3. **Chặng 1 hạ tầng** — sạch (uptime 220 ngày, PID 169960 từ 14/09, TLS gia hạn 03/10).
4. **Chặng 2 dòng dữ liệu** — 76 ngày không đứt; nhưng số model MN 12 → 10 từ 12–13/11.
5. Truy model rơi ⇒ `provider_quarantine.json` ⇒ **Anthropic hết tiền 11/11**. Làn shadow im từ 14/09 là có chủ ý.
6. **Chặng 3 lịch chạy/học** — retrain 12/12 × 12 tuần; 0 ERROR; phân loại 3 nhóm WARNING ⇒ lộ
   `I/O operation on closed file` 216/216 lượt.
7. Đào `closed file`: mô-đun scorecard không đổi ⇒ tìm thủ phạm ngoài ⇒ journal 0 `print()` / 5 ngày ⇒
   6 mô-đun thay stdout lúc import ⇒ **tái hiện được** bằng import thuần.
8. **Chặng 5 tự kiểm** — consistency 26/26, deadline trễ 0, selfcheck đỏ 16 tuần (ngưỡng lỗi thời).
9. **Chặng 6 kho & sổ** — drift chuẩn hoá ⇒ **git thụt lùi production** ở 2 tệp lõi; sổ quyết định 3 TRÔI
   ⇒ gốc là 2 khối FU in đậm nhãn + HISTORY im.
10. Tra nợ V11188 ⇒ `EXPECTED_MODEL_COUNT=15` ⇒ **216 miền-ngày bị loại khỏi đánh giá**; mệnh đề neo trong
    `QD-074/075` ⇒ trình owner.
11. Vá: bộ vá idempotent 8 tệp (thử trước-hỏng/sau-lành), quét AST cả họ, cổng commit thứ 9 + thử chặn.
12. Kéo vá SC-12 từ VPS về git sau khi chứng minh VPS chỉ thêm.
13. Sửa nhãn `FU-351`/`FU-430`; K1 9/9; mồ côi 0.
14. Hook deploy trả `ask` ⇒ ghi tài liệu bốn mặt **trước** ⇒ `allow`.
15. Deploy lần 1 dừng ở tiền kiểm (lỗi agent, xem mục 4) ⇒ sửa ⇒ deploy lần 2 đạt 11/11.
16. Sổ quyết định còn 1 TRÔI mới: cổng `QD-054` hút `FU-454` ⇒ vá ở gốc + thử chặn 3/3 ⇒ **0 TRÔI**.
17. Commit `4fbe7a6`, push nhánh + fast-forward `master`; báo cáo này.

## 3. Điều quan trọng nhất cho người đọc sau

- **Đầu ra official không hỏng trong 71 ngày.** Những gì hỏng nằm ở tầng **đo lường** (scorecard, đánh giá
  combo-super) và tầng **nguồn lực** (tiền API) — loại hỏng **không gây lỗi**, nên không ai thấy khi không ai nhìn.
- `claude-opus-4-6` không «chết» vì mã — **hết tiền tài khoản Anthropic**. Đừng sửa mã cho nó.
- Bản `database.py`/`daily_evaluation.py` trong git **trước `4fbe7a6`** là bản **thiếu SC-12**. Không deploy bản cũ.
- Cổng `_v10800_timetable_selfcheck` đang đỏ vì ngưỡng cũ — **không có nghĩa** là hệ có 4 sự cố.

## 4. Vấp ở đâu

- **Agent:** script deploy đọc `systemctl show --value` theo vị trí ⇒ dừng ở tiền kiểm. An toàn vì dừng trước
  mọi thao tác ghi; đã kiểm thư mục sao lưu từ xa chưa được tạo.
- **Agent:** phép thử «bản chưa vá» lần đầu nạp nhầm bản đã vá (đường dẫn cứng) — đã bỏ kết quả, sửa, chạy lại.
- **Công cụ cũ:** `_v10848_drift_audit` báo 267 DIFF do CRLF; cổng `QD-054` hút mã FU mới.
- **Quy trình:** selfcheck đỏ 16 tuần mà không ai xử — cổng mất giá trị báo động.

## 5. Điều phiên CỐ Ý không làm

- Không đổi `EXPECTED_MODEL_COUNT` (đụng `QD-074/075`).
- Không nhả cách ly model nào (owner lệnh 13/09: không gọi khi lỗi tiền còn tồn tại).
- Không backfill 72 ngày scorecard (quyết định đo lường — `FU-451b`).
- Không đổi ngưỡng selfcheck / `MB_WATCHDOG` (`FU-454`).
- Không rà 164 mục quá hạn hàng loạt (owner cấm đóng hàng loạt 09/08).
- Không đồng bộ DB 1 GB về local chỉ để gỡ nhãn «không kết luận được» của `QD-056`.

## 6. Câu phải nhớ khi đọc lại

> Hệ chạy đủ không có nghĩa là hệ đang được đo đúng: 72 ngày scorecard hỏng và 216 miền-ngày bị loại khỏi
> đánh giá mà không một dòng ERROR nào.
