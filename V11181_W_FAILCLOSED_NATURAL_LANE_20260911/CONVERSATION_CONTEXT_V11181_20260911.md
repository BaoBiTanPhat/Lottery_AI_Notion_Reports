# CONVERSATION CONTEXT — V11181 · 11/09/2026 · Prompt 43 R1 §W

> Nguyên văn lời Owner + agent làm gì + vấp ở đâu. Không diễn giải lại rồi để trong ngoặc kép.

---

## Owner nói gì — nguyên văn, theo giờ

**~13:27 ICT** — prompt §W. Các câu quyết định hành vi trong phiên:

> *"W0 — QUYẾT ĐỊNH 13:30 NGAY LẬP TỨC, FAIL-CLOSED… Nếu không có packet hợp lệ trước 13:15:
> kết luận ngay `BASE_D1_LIVE=NO_GO_UNFROZEN_PRELIVE_GATE`… Nếu 13:30 đã tự fire trước khi thao
> tác hoàn tất: không sửa hoặc backdate receipt; thu đầy đủ bằng chứng của lần fire; phân loại
> `UNFROZEN_NATURAL_RUN_DIAGNOSTIC_ONLY`; lần chạy đó không đóng natural-proof gate."*

> *"W1 — `exact_tails` KHÔNG đồng nghĩa action-eligible… Không bao giờ gán
> `diagnostic_label=ACTIONABLE` chỉ vì `model_decision=RANKED`."*

> *"W2 — Loại bỏ điều kiện pre-draw `st_src == ACTUAL_FOR_DATE` vì trước giờ xổ target chưa thể
> có actual result đầy đủ."*

> *"W4 — Không group bằng `model_id` prefix… Không dùng `COUNT(*)>0` để kết luận upstream hoàn
> tất… `NON_TTY_sh` không đủ để kết luận `CRON_NATURAL`."*

> *"W7 — Không group BASE và DELTA thành một Top-K chưa từng tồn tại… không gọi
> `would_save`/`would_break`."*

> *"Không nới thống kê hoặc action gate để tạo giả ứng viên đủ điều kiện."*

> *"Mọi phép đo phải kết thúc bằng REPAIR, RETIRE, CONCRETE CHALLENGER hoặc EXACT BLOCKER; cấm
> vòng 'đo tiếp/chờ thêm dữ liệu' chung chung."*

> *"Không hỏi Owner chọn A/B/C. Không tuyên bố 'mọi cổng đạt' nếu thiếu bất kỳ receipt bắt
> buộc nào."*

---

## Agent làm gì

**13:27–13:35** — kiểm gói freeze `12:32:54` theo từng tiêu chí §W0.A bằng lệnh, không bằng trí
nhớ. Ra **7/16 trường thiếu/bẩn**. Xuất quyết định W0 ngay, không viết báo cáo dài trước.

**13:35–14:35** — sửa 10 lỗi P0/P1, viết `_v11180_lich_dai.py`, `_v11180_migrate_w.py`,
`_v11180_thu_w.py`, viết lại `_v11178_freeze.py` và `_v11178_lane.sh`, migration, deploy,
3 bộ test (51 + 16 + 33), đóng hai gói freeze hợp lệ lúc `14:32`.

**16:38 / 17:33** — hai lane delta nổ tự nhiên, chạy xong trước cutoff.

**17:40–17:45** — khảo sát họ challenger kế tiếp, phát hiện sai lầm `RM-18` của chính mình,
đo lại, kết luận `NO_SUCCESSOR_PASSES_PREDEPLOY_GATE`.

**19:05** — EOD tự chạy; tính nền đúng cho bộ-K trước khi đọc bất kỳ con số hit nào.

---

## Vấp ở đâu — liệt kê đủ, không giấu

### 1 · Gói freeze có placeholder và đã được trình như bằng chứng hợp lệ
`"cron_text": sh("ssh_khong_ap_dung")` — chỗ bỏ trống rồi quên. Phiên trước agent đã nói
*"Freeze đã chốt và kiểm xong"*. Đó là sai, và §W0.A liệt kê đúng chuỗi đó là disqualifier.

### 2 · RM-10 — đoán tên, hai lần
- `getattr(gpt_analyzer, "OPENROUTER_MODELS", [])` — tên **không tồn tại**; mặc định `[]` khiến
  nó **trượt im lặng**. Tên thật `OPENROUTER_MODELS_SET` (dòng 125) và
  `model_registry.OPENROUTER_MODELS` (dòng 1051). Cổng `_v11020_cong_doan_ten` chặn.
- Cột `final_bundles.final_numbers_json` — **không tồn tại**, script sập. Tên cột THẬT đọc
  bằng `PRAGMA table_info(final_bundles)` (đây là **liệt kê schema**, không phải phép đo):

```
bach_thu TEXT · lo2 TEXT · lo3 TEXT · xien2 TEXT · xien3 TEXT
```

### 3 · RM-09 — đếm chuỗi thô, ba lần
- `grep -c "avail >= cut_dt"` trong `kiem_code` của `QD-076`: chuỗi đó còn trong **docstring mô
  tả lỗi cũ** (`§60.3` bảo GIỮ). Sửa: soi thân hàm.
- `'EXEC_LIVE' not in e` và `"would_save" not in e` quét **cả tệp**, kể cả docstring.
  Sửa: thêm `ma_thuan()` / `ma_thuan_sh()` bỏ docstring và chú thích.
- `LIKE '%attempt_id%'` khớp luôn `canonical_attempt_id` ⇒ báo `414/414` sai. Sửa: đọc JSON.

### 4 · RM-18 — suýt công bố hai họ vô tín hiệu (`RL-039`)
Khảo sát `F3_GAP`/`F4_DIGIT` in ra *"43,1% vs nền 16,6%, p=0"*. Không có tín hiệu nào: phép đo
gộp cả 3 đài MN rồi so với nền **một** đài. `3329/7719 = 43,1%` **trùng khít** nền gộp miền
`0,4312` — "tín hiệu" **chính là cái nền**. MB chỉ có một đài nên không lệch, và MB là miền
**duy nhất** không hiện tín hiệu giả — xác nhận chẩn đoán bằng cấu trúc.

Sai lầm bị bắt **bởi con số quá đẹp gây nghi**, không phải bởi một cổng máy nào.

### 5 · Heredoc nuốt `\n` — ba lần trong một phiên
Đúng mục đã ghi nhớ (`no-python-escapes-in-heredoc`). Lần thứ ba làm hỏng
`_v11180_thu_w.py`. Chuyển hẳn sang Write tool và `chr(92)`.

### 6 · Ước giờ thay vì đo
Tưởng 13:10 khi thực tế 12:14 — lệch gần một giờ, suýt làm hỏng kế hoạch freeze.

### 7 · Fixture sai, cổng đúng
Ba lần cổng từ chối vì fixture: 40 ngày → 5 ngày cùng thứ < `MIN_MAU_LICH_SU=8`; đài giả không
khớp lịch canonical; mỗi đài 4 số < `TOI_THIEU_SO_MOI_DAI=10`. **Nới fixture, không nới ngưỡng.**

### 8 · Blocker phát hiện giữa lượt chạy, không sửa vì đã freeze
- Circuit breaker `COST_HIGH` chặn `glm-5.2` và `gpt-5.6-sol-pro` — roster §V9 chưa xét
  trạng thái circuit breaker.
- `phan_loai_loi` xếp `BLOCKED…COST_HIGH` vào `ERROR` nên vẫn retry, chắc chắn vô ích.
- `gpt-oss-120b` trả `RANKED` + `uncertainty=low` + **toàn bộ confidence = 0** — abstain đội lốt
  RANKED, validator chưa bắt.

---

## Code đi trước tài liệu (PRJ-INTERACTION-LEDGER-001)

Có. Bốn tệp mới/viết lại trong phiên: `_v11180_lich_dai.py` · `_v11180_migrate_w.py` ·
`_v11180_thu_w.py` · `_v11178_freeze.py`, cùng bản vá lớn cho `_v11178_context_only_v11.py`,
`_v11178_ranker.py`, `_v11178_eod.py`, `_v11178_lane.sh`. Ghi nhận đã vào
`docs/SO_TUONG_TAC_OWNER.md` mục 11/09 **trong cùng phiên**, kèm nguyên văn và giờ.
