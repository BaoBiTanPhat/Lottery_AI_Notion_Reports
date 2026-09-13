# CONVERSATION CONTEXT — V11185 · phiên §AA, 13/09/2026 22:00 → 23:xx ICT

## 1. Owner nói gì — nguyên văn

Prompt **§AA**, tiếp nối sau V11184. Điều quan trọng nhất: **Owner tự soi nguồn và gỡ đúng blocker
mà V11184 đã nêu.**

> *"Không chờ tới 20/09 chỉ để 'truy thêm'. Nguồn mã hiện tại đã cho thấy đủ căn nguyên để sửa:
> `scheduler.py` import `TOKEN_MODELS as AUTO_AI_MODELS`; daily AI chain dùng trực tiếp
> `AUTO_AI_MODELS` ở preflight, parallel pool, main provider loop và diversity pass;
> `get_expected_models(slot, region)` chỉ đang ghi log; MB post-MT rerun chọn từ `AUTO_AI_MODELS`;
> `allowed_regions` hiện đã chặn đường bỏ phiếu nhưng chưa bảo đảm chặn mọi đường gọi API."*

> *"Biến roster từ một danh sách chỉ lọc khi bỏ phiếu thành một chính sách được thi hành ngay
> trước mọi HTTP provider call."*
>
> *"Mục tiêu ưu tiên số một: `UNBOUNDED_SHADOW_PROVIDER_CALLS = 0`."*
>
> *"Không kết thúc bằng monitoring-only. Không gia hạn mơ hồ. Không yêu cầu Owner phê duyệt lại
> roster 8→4 hoặc Weekly Model League."*

Và mốc hoạt động (§AA-I): sẵn sàng trước **03:30 ICT 14/09** thì activate trước **04:00**, dùng
**cùng một roster epoch** cho cả ba miền; cấm MN dùng roster mới mà MT/MB cùng ngày dùng roster cũ.

**Không có yêu cầu rời nào giữa phiên.**

---

## 2. Agent IDE đã làm gì — theo thứ tự thật

1. Preflight: git/router/VPS/PID/crontab/quarantine/trace.
2. Dựng inventory call-site — **khớp chính xác 9 vị trí** Owner chỉ.
3. Dựng `_v11185_roster_goi_token.py` (SSOT chính sách gọi), tự kiểm 32/32.
4. Vá 6 call-site trong `_run_ai_models_predict` + MB rerun.
5. Giới hạn shadow lane về đúng challenger được chỉ định.
6. Chứng minh zero-official-impact rồi tắt 3 dòng cron `_v11059`.
7. Xác định Combo Super **có** gọi thêm provider ⇒ đếm riêng, không đổi semantics.
8. Dựng `_v11185_thu_aa.py` (45/45), chạy toàn bộ regression **377/377**.
9. Restart **22:36 ngày 13/09** — activate xong, trước mốc 03:30 rất xa.

---

## 3. Vấp ở đâu — hai lỗi của chính tôi

### 3.1 Bản vá đầu của tôi làm §AA-E2 VÔ TÁC DỤNG HOÀN TOÀN

Khi vá MB rerun, tôi chèn đoạn chọn theo roster ở trên rồi **giữ khối win-rate cũ "để tham chiếu"**.
Nhưng khối đó vẫn chạy:

```python
selected_models = [m[0] for m in ai_model_wrs[:3]]
```

— tức **ghi đè** lựa chọn roster. Nếu deploy như vậy thì MB rerun vẫn chọn top-3 theo win-rate từ
toàn bộ 8 model, đúng thứ §AA-E2 cấm, và roster ở trên chỉ là trang trí.

**Bắt được nhờ đọc lại mã sau khi vá**, không nhờ cổng nào. Đã xoá hẳn khối đó.

**Bài học: "giữ lại để tham chiếu" trong một hàm đang chạy không phải là trung lập — nó vẫn thực
thi.** Muốn tham chiếu thì để trong git và backup, không để trong luồng.

### 3.2 Bài thử của tôi đếm chuỗi thô (RM-09)

Bài `B9` kiểm `"selected_models = [m[0] for m in ai_model_wrs[:3]]" not in src` và báo **HỎNG** —
trong khi mã đã đúng. Lý do: chuỗi đó còn nằm trong **chú thích của chính tôi** giải thích vì sao
đã xoá. Chú thích mô tả lối sai **không phải** lối sai.

Sửa sang AST (`ast.unparse(ast.parse(src))` bỏ chú thích) → 45/45.

Đây là lỗi tôi vẫn cảnh báo người khác, và vẫn tự mắc.

### 3.3 Một cảnh báo giả

`_v11184_intake_model.py` báo `rc=2` trong lượt chạy regression — thoạt nhìn là hồi quy. Thật ra
tệp **chưa được deploy lên VPS**, `rc=2` là "file not found". Deploy xong: 19/19. Không phải hồi
quy, là khoảng trống triển khai.

---

## 4. Điều phiên CỐ Ý không làm, và vì sao

| việc | không làm vì |
|---|---|
| Pure-context bounded shadow (§AA-O) | Ưu tiên số một của §AA là `UNBOUNDED_SHADOW_PROVIDER_CALLS = 0`. Mở một lane shadow mới **cùng lúc** với việc đóng lane cũ là tự mâu thuẫn. ⇒ `RETIRED_BEFORE_TOKEN_SPEND`, mở lại sau receipt #1 với preregistration đầy đủ |
| Đổi Combo Super | §AA-A cấm đổi Combo semantics khi chưa chứng minh output-equivalent. Combo **có** gọi thêm provider (`combo_super.py:1134`) ⇒ đếm riêng, không giấu |
| Cost observability · override lineage · family lineage · retrain atomic path | Bốn mục này §AA đòi, nhưng ưu tiên cứng của phiên là đóng đường gọi token trước mốc 03:30. Cả bốn ghi thành `EXACT_BLOCKER` **đủ bốn thành phần**: dữ liệu thiếu, người chịu trách nhiệm, hạn 20/09, terminal bắt buộc |
| Hạ tầng P0 (§AA-U) | Đúng lời §AA: *"không dùng hạ tầng làm lý do trì hoãn roster/token fix"* |

---

## 5. Code đi trước tài liệu — `PRJ-INTERACTION-LEDGER-001`

`_v11185_roster_goi_token.py` và `_v11185_thu_aa.py` có trong repo và trên VPS trước khi vào
`CHANGELOG`/`SSOT`. Owner đã cho phép tường minh. Đây là chỗ khai.

---

## 6. Điều quan trọng nhất cho người đọc sau

**Roster trước §AA chỉ là danh sách lọc khi BỎ PHIẾU.** `allowed_regions` chặn được ai được tính
điểm, nhưng `scheduler.py` vẫn gọi API cho cả 8 model vì nó duyệt hằng số tĩnh `AUTO_AI_MODELS`.
Nghĩa là hệ **trả tiền cho 8 model rồi bỏ phiếu của một nửa**.

Sau §AA, quyết định gọi ai nằm ở **đúng một hàm** `get_token_call_roster`, và hàm đó **fail-closed**:
không đọc được chính sách thì **không gọi model nào**, chứ không quay về 8.

**Con số đáng nhớ:** phần tiết kiệm lớn hơn **không** đến từ tinh gọn roster (−19.9%) mà từ **chặn
shadow** (−54.8%) — 60.3% token của hệ vốn chảy vào 11 model không được phép ra output. Ai đặt ưu
tiên ngược lại sẽ tối ưu nhầm chỗ.

Và **ước lượng −74.7% vẫn chỉ là ước lượng**. Số đo thật đến từ natural receipt lượt MN sáng 14/09.
