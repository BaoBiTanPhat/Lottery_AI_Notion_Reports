# CONVERSATION CONTEXT — V11182 · 11–12/09/2026 · Prompt 43 R1 §X

> Nguyên văn lời Owner + agent làm gì + vấp ở đâu.

---

## Owner nói gì — nguyên văn, theo giờ

**11/09/2026 ~23:44 ICT** — prompt §X:

> *"Cấm: WAIT_DATA chung chung; tiếp tục family đã chết chỉ để có thêm dòng; gọi 19 model
> mỗi ngày để chứng minh hạ tầng của một family vô tín hiệu."*

> *"F4_DIGIT_ALGEBRA: phép đo trước sai G2; chưa được đánh giá hợp lệ; trạng thái đúng phải
> là MEASUREMENT_INVALID_NOT_EVALUATED; không được gọi F4_NO_SIGNAL khi chưa đo lại đúng."*

> *"Không có lần chạy thứ hai bằng cách đổi ngưỡng. Chỉ được chạy lại nếu chứng minh code
> defect làm kết quả trước vô hiệu."*

> *"Nếu deterministic F5 chưa pass: không gọi LM/LLM; không tiêu provider; không dựng
> prompt giả."*

> *"Không dùng 32 nhãn lo3 lịch sử sai."*

> *"Không reset, checkout, clean, stash hoặc ghi đè công việc không thuộc phiên."*

> *"Mọi đo lường phải kết thúc bằng REPAIR, RETIRE, HISTORICAL_GATE_PASS, hoặc
> BLOCKED_WITH_EXACT_REASONS."*

---

## Agent làm gì

**23:55–23:58** — preflight: chụp Git hai kho, service, crontab nguyên văn + SHA, tiến trình,
schema, row counts, digest lịch sử. Sinh `PRE_X_MANIFEST.json` **trước mọi mutation**.

**23:58–00:00** — tắt 4 dòng cron của family đã chết (comment-out). Kiểm an toàn: dòng đang
chạy giảm **đúng bằng** số dòng tắt (97→93), đọc lại crontab thật để xác nhận.

**00:00–00:10** — §X6 thước đo chính xác · §X2 circuit/retry · §X3 validator · §X4 canonical
lineage. Deploy, kiểm từng phần bằng dữ liệu thật.

**00:05** — F4: sinh prereg có hash, đo **đúng một lần**, 117.270 cell, BH-FDR giữ **0**,
holdout **không mở**.

**00:09–00:12** — F5: dựng pooled logistic ranker, 12 feature, blocked split, Poisson-binomial
chính xác. Trượt cả ba miền về phía **ÂM**. Thêm nhánh đối chứng baseline tần suất.

**00:15–00:25** — bộ thử §X11 (50 phép), chạy lại toàn bộ 4 bộ cũ, sửa 2 phép hồi quy.

**00:30–00:45** — ma trận official §X5 + ma trận 19 model §X7 + chấm lại 32 nhãn `lo3`.

**00:45–01:00** — zero-write, sửa README/READ_THIS_FIRST, sổ rút lại, quyết định, báo cáo.

---

## Vấp ở đâu — liệt kê đủ, không giấu

### 1 · `RM-10` — đoán tên API circuit breaker
Viết adapter với `_circuit_state` / `_CIRCUIT` — **cả hai không tồn tại**. Hậu quả: `doc_circuit`
trả `UNKNOWN` cho **cả 4 model** thử, tức adapter **mù hoàn toàn**; và vì `UNKNOWN` bị xử như
`OPEN` nên nó sẽ **chặn mọi lời gọi provider**, tức tự khoá cả hệ. Đọc `grep` trên mã nguồn ra
tên thật: `_OPENROUTER_CIRCUIT_BREAKER` (dict) và `_openrouter_circuit_check()`.

Hai sự thật chỉ lộ ra khi đọc mã, cả hai đổi cách dùng:
- Circuit **chỉ** áp cho tuyến **OpenRouter**. Model đi anthropic/google/openai/deepseek
  **không có** circuit ⇒ trạng thái đúng là `NO_CIRCUIT_FOR_ROUTE`, gọi được bình thường.
- Circuit là bộ nhớ **trong tiến trình** ⇒ challenger khởi động luôn sạch; nó chỉ mở **trong**
  lượt chạy. Giá trị của §X2 vì thế là chặn các model **sau** và chặn retry vô ích.

Ngoài ra: `_openrouter_circuit_check()` **xoá** entry hết hạn (có tác dụng phụ). Đọc **thẳng
dict** mới là thuần đọc, đúng §X12 — đã kiểm bằng test: entry vẫn còn sau khi đọc.

### 2 · `RL-041` — hai kết luận sai, cùng một gốc
Chạy đầu của `_v11182_eod_official.py` in ra:

```
CHAM LAI 32 NHAN lo3: WIN trong DB=57 · WIN THAT=0 · WIN SAI=57
3-cang: NOT_SCORABLE_MISSING_PREFIX_LINEAGE
```

Cả hai **sai**, vì agent không đọc cấu trúc thật của cột `lo3`:
- `lo3` là số **ba** chữ số; agent đem so với tập đuôi **hai** chữ số ⇒ không bao giờ khớp.
- Agent kết luận không có lineage 3-càng vì đi tìm **cột tên** `"cang"`/`"prefix"`.

Thật ra **`lo3` CHÍNH LÀ 3-càng**: đo được **588/588** bundle có `len(lo3)=3` và `lo3` **luôn**
kết thúc bằng `bach_thu` ⇒ `lo3 = prefix + lane-specific final BT`.

Sửa thước xong: `WIN thật=25 · WIN sai=32`, toàn bộ tháng 03/2026 — **khớp chính xác V11166**
qua một đường mã hoàn toàn khác.

**Thứ đã tố cáo lỗi là con số `57/57` quá cực đoan**, không phải một cổng máy nào.

### 3 · `RM-09` lần thứ tư trong loạt phiên này
Test `F-pos` quét `"shuffle" not in src5` trên **cả tệp**. Chữ `shuffle` có thật trong `src5` —
nhưng nằm trong chính câu tài liệu `"split": "blocked time split, KHONG shuffle, ..."`, tức
**mô tả việc KHÔNG làm**. Sửa: phân tích AST, soi **danh sách hàm được gọi**, không soi văn bản.

### 4 · Test brittle theo ngày
Hai phép trong `_v11180_thu_w.py` tìm gói freeze của **hôm nay**. Qua nửa đêm + family đã
retire (cron tắt ⇒ không sinh gói mới) ⇒ trượt, và kéo theo **3 phép con bị bỏ qua** vì nằm
trong `if os.path.exists(...)`. Sửa: tìm gói **hợp lệ bất kỳ** trong kho.

### 5 · Một phép test khẳng định hình dạng code CŨ
`W5-16` kiểm `'if mong and aid != mong' in e` — chính dòng mà §X4 vừa siết bỏ. Test phải
cập nhật theo luật mới, không phải giữ luật cũ để test xanh.

### 6 · Crontab SHA có hai giá trị
`crontab -l | sha256sum` (có newline cuối) = `6e2687eb…`; băm chuỗi đã strip = `8b7c84ea…`.
Cả hai đúng trong phương pháp của nó, nhưng trình hai con số cho cùng một thứ là gây nhầm.
Đã thống nhất dùng một cách.

---

## Điều KHÔNG làm, và vì sao

- **Không gọi một lời gọi LM/LLM nào.** F5 chưa pass ⇒ §X10 cấm. Bằng chứng: `v11178_attempts`
  149 → 149, không tăng một dòng.
- **Không chạy lại F4 với ngưỡng khác.** Owner cấm tường minh; và không có code defect nào
  làm kết quả trước vô hiệu.
- **Không xoá** source, bảng `v11178_*`, `shadow_candidates`, freeze packets, lane receipts.
- **Không sửa 157 tệp báo cáo cũ** còn link `irissnss` — đó là **bản ghi lịch sử**. Chỉ sửa
  router gốc (`README.md`, `READ_THIS_FIRST.md`), và ghi rõ quy tắc thay link trong
  `READ_THIS_FIRST.md`.
- **Không ghi DB** để sửa 32 nhãn `lo3` — xác định được đúng 32 dòng bằng phép đọc thuần, nên
  việc ghi trở thành **không cần thiết** chứ không phải bị hoãn.

---

## Code đi trước tài liệu (PRJ-INTERACTION-LEDGER-001)

Có. Bảy tệp mới trong phiên: `_v11182_pre_x_manifest.py` · `_v11182_retire_f1_cron.py` ·
`_v11182_thuoc_do.py` · `_v11182_f4.py` · `_v11182_f5.py` · `_v11182_thu_x.py` ·
`_v11182_eod_official.py`, cùng bản vá cho `_v11178_context_only_v11.py`,
`_v11178_eod.py`, `_v11180_thu_w.py`. Ghi nhận vào `docs/SO_TUONG_TAC_OWNER.md`
**trong cùng phiên**, kèm nguyên văn và giờ.
