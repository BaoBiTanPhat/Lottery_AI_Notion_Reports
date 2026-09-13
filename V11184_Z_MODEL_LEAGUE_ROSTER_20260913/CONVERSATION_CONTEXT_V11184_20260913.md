# CONVERSATION CONTEXT — V11184 · phiên §Z, 13/09/2026 20:44 → 22:xx ICT

> Nguyên văn lời Owner · Agent IDE đã làm gì · **vấp ở đâu**. Viết cho người đọc sau (đặc biệt
> TanPhatAI) để **không phải đoán** vì sao phiên đi theo hướng đã đi.

---

## 1. Owner nói gì — nguyên văn

Prompt **§Z** nhận **13/09/2026 20:44 ICT**. Mười khoá mới, nguyên văn:

> 1. `QD-079 C1+C2+C3 = OWNER_APPROVED.`
> 2. `WEEKLY_MODEL_LEAGUE = OWNER_APPROVED.`
> 3. `INITIAL_LLM_ROSTER_COMPRESSION = OWNER_APPROVED.`
> 4. Mỗi miền tối đa: 3 direct-token LLM chính; 1 direct-token LLM challenger.
> 5. Lần đầu được phép tinh gọn roster về giới hạn trên **sau khi hoàn tất replay và rollback proof**.
> 6. Sau lần tinh gọn đầu tiên: tối đa 1 promotion/demotion trên mỗi miền mỗi tuần; lỗi auth,
>    billing, circuit-open hoặc model unavailable được cách ly ngay và **không tính vào giới hạn
>    thay đổi hiệu năng**.
> 7. Không thay công thức TOTAL.
> 8. Không reset các trọng số hiện tại về mặc định.
> 9. **Không coi CORE là "đã chứng minh lift"**; CORE chỉ có nghĩa là lựa chọn tốt nhất hiện có theo
>    bằng chứng current-regime, reliability, independence và cost.
> 10. Không cần quay lại hỏi Owner hằng tuần nếu thay đổi nằm đúng toàn bộ giới hạn đã phê duyệt.

Và mục tiêu, nguyên văn:

> *"Chấm dứt tình trạng dùng 8 LLM token cho mỗi miền nhưng không có bảng xếp hạng hiện hành, không
> biết model nào cứu/phá TOTAL và không có cơ chế loại bỏ."*
>
> *"Không được kết thúc bằng 'cần đo thêm' nếu không kèm: dữ liệu còn thiếu chính xác; người/tiến
> trình chịu trách nhiệm; hạn cuối; terminal bắt buộc khi tới hạn."*
>
> *"Không dừng ở monitoring-only. Không yêu cầu Owner quyết định lại những nội dung đã được phê
> duyệt trong §Z. Ngoài phạm vi phê duyệt, giữ nguyên production và nêu đúng blocker."*

**Không có yêu cầu rời nào giữa phiên.**

---

## 2. Agent IDE đã làm gì — theo thứ tự thật

1. Truy `_v11183_cong_optimizer.py` trên **mọi ref** → có ở `fu438/admin-only-p0a` và
   `origin/fu438/...` @ `1f0df1e`, **không** có trên `master` @ `c3d24bc`. Nguyên nhân: master lùi
   đúng 2 commit, và 2 commit đó chính là V11183. **Không phải mất tệp.** FF master, push.
2. Dựng `_v11184_pre_z_manifest.py`, chụp preflight §Z-B1.
3. Phóng workflow 16 agent (8 chiều × điều tra + phản biện). Song song tự đo trên DB VPS.
4. Triển khai `QD-079 C1+C2+C3` → deploy → restart (PID `3870722→62494`).
5. Dựng khoá an toàn retrain, nối vào `_retrain()`, chụp checkpoint thật.
6. Dựng cách ly provider, nối vào `_invoke_model_api`, deploy → restart (PID `62494→85063`), gieo
   cách ly từ thông điệp lỗi thật trong DB.
7. Dựng leaderboard — **cổng tái lập trượt hai lần**, đào ba vòng mới ra công thức đúng.
8. Tính quyết định tinh gọn roster, replay, **quyết định KHÔNG lật** vì blocker chính xác.
9. Đưa hai tệp canonical VPS-only vào repo, chạy cổng nhiễm bẩn thật.

---

## 3. Vấp ở đâu — ghi đủ, không giấu

### 3.1 Cổng tái lập TRƯỢT hai lần, và script tự dừng cả hai lần

Tôi viết bộ chấm leaderboard với một **cổng bắt buộc**: hàm tái lập phải dựng lại đúng `bach_thu` từ
`score_breakdown` với tỷ lệ ≥95%, nếu không thì `sys.exit(2)` — không công bố số nào.

- **Lần 1:** 82.0% / 86.3% / 85.1%. Dừng.
- Tôi nêu giả thuyết *"`source_predictions_json` đi lạc khỏi `bach_thu`"* (bundle bị ghi lại, JSON
  cũ). Tương quan ban đầu ủng hộ: nhóm `GHI_MOT_LAN` khớp **86/86 = 100%**, nhóm `DA_GHI_LAI` chỉ
  84.1%.
- **Phép đo tiếp theo BÁC BỎ chính giả thuyết đó:** `bach_thu` **luôn** nằm trong `ranked_numbers`
  (0/81 vắng mặt), ở vị trí 1–8. JSON **không** cũ.
- **Nguyên nhân thật:** bốn tầng ghi đè được Owner duyệt ở `main.py:10255/10276/10296/10316`.
- **Lần 2:** so với `ranked[0]` thay vì `bach_thu` → 96.3%. Vẫn dừng.
- **Nguyên nhân cuối:** `pp1_convergence_dampener` (×0.85) áp **sau** khi cộng components. 18/18 ca
  lệch đều có pp1 event.
- **Lần 3:** công thức đầy đủ → **99.38% ⇒ ĐẠT**.

**Nếu không có cổng đó, tôi đã công bố một leaderboard rescue/break dựng trên hàm khớp 82%.**

### 3.2 Bộ phân loại lỗi của tôi bỏ sót ca thật

Tôi viết danh sách dấu hiệu lỗi deterministic **từ trí nhớ**, có chuỗi `credit_balance_exhausted`.
Đọc `predictions.verdict_reason` ngày 13/09 thì thông điệp thật của `gpt-5.4` là:

```
Error code: 429 - {'error': {'message': 'You have no credits remaining. Add credits ...
```

Không chứa chuỗi tôi đoán. Với mã 429 nó rơi vào `MA_HTTP_TRANSIENT` ⇒ bị xếp nhầm thành **lỗi tạm
thời, gọi lại sau 15 phút**, trong khi thực chất là **hết tiền**. Sửa bằng chuỗi đọc từ DB, và thêm
hai bài thử dùng **nguyên văn** cả hai thông điệp. Gieo cách ly xong còn bắt thêm **hai model tôi
chưa biết** cũng hỏng vì hết tiền: `gpt-5-mini` và `deepseek-v4-pro-real`.

### 3.3 Đoán tên trường hai lần (RM-10)

- `MODEL_REGISTRY` là **list**, tôi viết `.items()` như dict.
- Khoá phân loại direct-token là `class` ∈ `TOKEN`/`NO_TOKEN`, tôi lọc theo `provider`/`route` ⇒ kết
  quả **"0 direct-token LLM"**, một con số vô lý đủ để tôi dừng và đọc cấu trúc thật.

### 3.4 Sai thứ tự gate khi chọn challenger

Bản đầu xếp challenger theo coverage (Gate 4) ⇒ ra `claude-sonnet-4-6` ở cả ba miền, **trùng họ
ANTHROPIC** với một CORE. §Z đặt **Gate 3 (diversity) trước Gate 4**. Sửa xong, MT và MB đạt **4 họ
nguồn phân biệt**.

### 3.5 Bài thử cổng bị mù

Bài *"chỉnh chọn thực sự đổi kết quả"* bản đầu đặt `thắng=36/60`, cho p thô ≈**0.077** — vốn đã
trượt ngưỡng 0.05, nên bài thử **không phân biệt được** "bị chặn vì thiếu chỉnh-chọn" với "bị chặn vì
p thô lớn". Sửa thành `38/60` (p thô **0.02595**, dưới 0.05) thì bài thử mới có nghĩa: `n=69` bị
chặn, `n=1` thì `GHI`.

### 3.6 Nhãn từ chối sai

Ca "ứng viên và control chấm khác số ngày" bị gán nhãn `NO_WRITE_KHONG_CO_HELDOUT` — sai, vì nó CÓ
held-out. Và bài thử của tôi chỉ kiểm `startswith("NO_WRITE")` nên **ĐẠT trong khi nhãn sai**. Thêm
nhãn `NO_WRITE_KHONG_CUNG_FROZEN_HOLDOUT` và sửa bài thử kiểm **đúng nhãn**.

### 3.7 Heredoc nuốt dấu nháy đơn

`<<PYEOF` không nháy làm shell nuốt `'[]'` trong câu SQL ⇒ lỗi cú pháp SQLite. Phải dùng `<<'PYEOF'`.

---

## 4. Điều Owner yêu cầu mà phiên CỐ Ý chưa làm, và vì sao

| yêu cầu | chưa làm vì |
|---|---|
| Lật roster 8→4 (`INITIAL_LLM_ROSTER_COMPRESSION` đã được duyệt) | Tôi **chứng minh được** `allowed_regions` chặn đường **bỏ phiếu** (`get_output_eligible_ids(region)` tại `main.py:9720`, trong `generate_final_bundle`), nhưng **chưa chứng minh được** nó chặn đường **gọi API**. Nếu chỉ chặn phiếu, lật roster sẽ **đổi output production mà vẫn trả đủ token** — toàn rủi ro, không lợi ích, và `DIRECT_TOKEN_CALL_CAP = MAX_4` sẽ là tuyên bố không kiểm chứng được. Blocker, hạn và terminal bắt buộc ở `REPORT §6.4`. |
| Train vào candidate path (§G mục 3) | `MODEL_DIR` ở cả ba module huấn luyện phục vụ **cả ghi lẫn đọc**, và `_retrain_all.py` là subprocess riêng. Override nửa vời nguy hiểm hơn không override. Tính chất an toàn thật sự — **không bao giờ mất đường về** — đã đạt đủ bằng checkpoint + cổng + tự động gỡ về. |

---

## 5. Code đi trước tài liệu — khai theo `PRJ-INTERACTION-LEDGER-001`

Các tệp sau có trong repo và trên VPS trước khi vào `CHANGELOG`/`SSOT`:
`_v11184_pre_z_manifest.py` · `_v11184_thu_z.py` · `_v11184_retrain_an_toan.py` ·
`_v11184_cach_ly_provider.py` · `_v11184_intake_model.py` · `_canonical_v11165/*`.

Owner đã cho phép tường minh để giữ mạch xử lý nhanh trong IDE. Đây là chỗ khai.

---

## 6. Điều quan trọng nhất cho người đọc sau

**Bạch thủ official không phải top-1 của phiếu model trong 16.8% số ngày.** Bốn tầng ghi đè
(`V10640` MN per-slice · `V10767` MB prev-day ML-plurality · `V10789` MB lane · `V10790` MT lane)
thay `ranked[0]` bằng số khác. Trên những ngày đó, câu hỏi *"model nào cứu/phá TOTAL"* **không có
nghĩa**.

Và `main_selection_reason` bị gán **cứng** ở `main.py:10397` là
`"max_ranked_score_after_gate_and_lane_weight"` **sau** cả bốn nhánh ghi đè — nên bản ghi **nói sai**
điều đã xảy ra ở đúng 16.8% số ngày đó. Bất kỳ ai đọc trường này để chẩn đoán sẽ bị đánh lừa.

**Đừng đọc leaderboard §4 như bảng xếp hạng.** 0/156 ô có ý nghĩa thống kê; một ô 30 ngày trung bình
có 1.7 sự kiện. Nó chứng minh **Gate 2 không dùng được**, chứ không phải model nào hơn model nào.
Đó cũng đúng khoá Owner số 9: *"Không coi CORE là đã chứng minh lift"*.
