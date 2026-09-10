# V11175 — KIỂM CHÉO ĐỘC LẬP V11174 · ĐÍNH CHÍNH

> `SOURCE_TIMESTAMP` **2026-09-10 10:05 → 11:10 ICT** · `PROJECT/SCOPE` **Lottery_AI_Test**
> `AUTHORITY` owner hỏi *«đã báo cáo đầy đủ chưa em?»* — 10/09/2026 ~10:05 ICT
> `PRODUCTION_MUTATIONS` **0** · `DB MUTATIONS` **0** · `DEPLOY/RESTART` **0**
> `SUPERSEDES` — · `SUA CHO GOC CUA` **V11174** (không thay thế, chỉ đính chính tại chỗ)
> `SC-12` vẫn **`DEPLOYED_PENDING_SCHEDULED_PROOF`** · Pure Context vẫn **`PURE_CONTEXT_PARTIAL`**

---

## 1 · TÓM TẮT — EXECUTIVE VERDICT

Owner hỏi một câu ngắn: *«đã báo cáo đầy đủ chưa em?»*. Em **không trả lời bằng trí nhớ** mà cho
chạy **12 tác nhân độc lập** (6 góc kiểm × 1 lớp phản biện mỗi góc, 1,48 triệu token), mỗi góc
tự chạy lệnh và mặc định **nghi ngờ** kết luận của góc trước.

# CÂU TRẢ LỜI: **CHƯA ĐẦY ĐỦ**

**37 phát hiện → 29 được phản biện xác nhận · 8 bị bác hoặc hoá ra đã làm rồi.**
Trong đó **2 mức P0 nói thẳng rằng báo cáo V11174 có số không có bằng chứng chống lưng**.
**Em tự kiểm lại cả hai — cả hai đều ĐÚNG.**

**Đã sửa xong trong bản này: 12 mục.** **Còn 1 mục CHẶN Ở OWNER** (mục 9.3).
**Production không đụng một byte.**

---

## 2 · OWNER YÊU CẦU GÌ — NGUYÊN VĂN + GIỜ

| giờ ICT | NGUYÊN VĂN | loại | agent đã làm gì | trạng thái |
|---|---|---|---|---|
| **10/09 ~10:05** | *«đã báo cáo đầy đủ chưa em?»* | `HỎI` | Không trả lời bằng trí nhớ. Chạy 12 tác nhân kiểm chéo độc lập → **CHƯA ĐẦY ĐỦ**, 29 phát hiện xác nhận → sửa 12 mục, 1 mục chặn ở owner | `ĐÃ_LÀM` |

Ràng buộc §R còn hiệu lực và **đã được tôn trọng trong phiên này**:
`FINAL_BUNDLES_ZERO_WRITE` · *«Không tự tạo FU hoặc Plan mới»* (chính vì câu này mà mục 9.3 phải
chờ owner) · *«Không tạo Prompt 44»* · *«Không trộn ERP»*.

---

## 3 · ĐÀO BỚI / PHÁT HIỆN

### 3.1 · Cách kiểm — vì sao tin được kết quả

6 góc chạy song song, **mỗi góc bị một góc phản biện riêng soi lại**, và góc phản biện được lệnh
*«mặc định nghi ngờ, phải tự chạy lệnh, không được xác nhận chỉ vì nghe hợp lý»*. Kết quả:
**8/37 phát hiện bị chính lớp phản biện bác bỏ** — trong đó có hai cáo buộc khá nặng
(*«cổng báo cáo tự ghi tệp»*, *«artifact chỉ còn một bản sống»*) hoá ra sai.
Lớp phản biện cũng **đính chính ngược lại góc kiểm** ở hai chỗ, ví dụ chỉ ra rằng câu
*«Không mở FU mới»* là **chữ của chính agent**, không phải lời owner.

### 3.2 · 🔴 P0-1 — tệp bằng chứng «58/58» là tệp SAI

`evidence/v11174_vah12_kq.json` mà V11174 gắn nhãn *«kết quả test installer · 58/58»* thực tế ghi:

```json
{ "phien_ban": "V11174-VAh12-ZEROWRITE", "dat": false,
  "ICT": "2026-09-10T01:56:48+07:00",
  "preimage": { "database.py": "758cf2cf…", "main.py": "d59a6ae9…" } }
```

**`dat: false`, và không chứa số test nào.** Hai hash trong trường `preimage` chính là **hash
POST** — tức đây là lượt chạy **sau khi đã cài**, `--test` fail-closed đúng luật. Lượt 58/58 thật
chạy **trước** đó và **bị chính lượt 01:56 ghi đè**, vì `--out` mặc định trỏ cùng một đường dẫn.

### 3.3 · ✅ 58/58 ĐÃ TÁI LẬP — con số đúng, tệp mới là cái sai

Dựng cây cô lập `/tmp/v11174_repro` từ hai bản sao lưu:

```
sha256 main.py.pre_v11174      → 4ed5fd7ebaee8d23…83781cf   ✅ ĐÚNG PREIMAGE
sha256 database.py.pre_v11174  → fd3d2349ab917c6f…566eb16   ✅ ĐÚNG PREIMAGE
```

> Đây đồng thời là **bằng chứng độc lập rằng đường gỡ về của V11174 là THẬT** — hai bản sao lưu
> khôi phục ra **đúng** preimage đã công bố.

Chạy `--test` với DB mở `mode=ro`:

```
TONG: 58/58 DAT          ← 58 dòng "DAT", 0 dòng "HONG"
artifact: dat: true, preimage 4ed5fd7e… / fd3d2349…
```

Production **không đổi một byte** sau khi tái lập (`d59a6ae9…` / `758cf2cf…`).
Chứng cứ: `evidence/v11174_vah12_test_stdout.txt` · `evidence/v11174_vah12_kq_TAILAP.json`.

### 3.4 · 🔴 P0-2 — digest `396c7559…` không tái lập được, VÀ tiêu chí đó SAI TỪ THIẾT KẾ

Thử **sáu** công thức trên chính DB production (`mode=ro`): `SELECT *` sắp theo cột 1 / theo `id` /
theo `date,region`, và ba biến thể cột rút gọn. **Không công thức nào ra `396c7559…`.**

**Nhưng phần nặng hơn không phải chuyện tái lập.** `final_bundles` **tăng tự nhiên mỗi ngày**.
Đo lúc 10:37 hôm nay:

```
final_bundles = 583 dòng   (V11174 công bố 582)
dòng mới: id=860 · 2026-09-10 · MN · ACTIVE · created_at 05:26:43
```

⇒ Nếu tối nay em cứ theo tiêu chí *«digest toàn bảng không đổi»*, nó sẽ báo **drift giả** ngay
trên chính bản deploy này. **Tiêu chí ấy sai từ lúc viết ra**, không phải sai vì hôm nay.

**Tiêu chí đúng — phạm vi khoá theo ngày, kèm đúng lệnh sinh ra nó:**

```python
cur.execute("SELECT * FROM final_bundles WHERE date<='2026-09-09' ORDER BY 1")
m = hashlib.sha256()
for r in cur.fetchall(): m.update(repr(r).encode())
# 582 dòng → 0c5f84f8de9bbada94abe2b665dc53c5ab4044f07e64f2ebe796efff6278ffb2
```

Dòng có `date ≥ 2026-09-10` là **tăng trưởng hợp lệ**, không phải drift.

### 3.5 · 🔴 VA-2′ mới NỬA CHỪNG — `A58_VIOLATION_HALF_DONE`

```
du-doan.html:1354       if (!filteredModels.length && sourcePreds.wr_gate_filtered)
                            filteredModels = sourcePreds.wr_gate_filtered;
du-doan.html:1438-1439  … cùng mẫu cho qualityFilteredModels
du-doan.html:1443-1444  … in thẳng tên model từ wr_gate_filtered
```

VA-2′ lọc danh sách thành `[]` → điều kiện `!length` **thành đúng** → **UI lấy đúng danh sách
nhiễm mà VA-2′ vừa bỏ**. Thêm nữa `quality_filtered_model_count` (`main.py:652`, lấy từ
`non_scoreable_count`) **không đi qua** VA-2′ ⇒ có thể ra cảnh **danh sách rỗng nhưng đếm = 2**.

Đúng lối `§60.1` cảnh báo: *«gỡ mệnh lệnh nhưng giữ nhãn thì nhãn tự dạy lại»*.

### 3.6 · Các phát hiện xác nhận còn lại

| mã | mức | phát hiện |
|---|---|---|
| G1-01 · G3-02 · G4-02 | P1 | **`FU-451` là mã ma** — 4 dòng HISTORY viện tới, `FOLLOW_UP_TRACKER` **chưa bao giờ có** (`grep -c` = 0; cao nhất FU-450) |
| G4-03 · G6-02 | P1 | **`PRJ_RETRACTION_SILENT`** — V11174 tự khai chỗ gốc là `FOLLOW_UP_TRACKER:183` nhưng **không sửa dòng đó** |
| G4-04 | P1 | 7 claim bị bác **không vào `SO_RUT_LAI.json`** ⇒ cổng `_v11085` **mù** với chúng |
| G4-01 | P1 | **Bước 8 bỏ hẳn** — khoá owner mới `FINAL_BUNDLES_ZERO_WRITE` không có dòng nào trong `OWNER_DECISION_LEDGER.json` |
| G1-02 · G4-05 | P1 | 4 tệp điều hướng kho công khai **trễ 8 bản** (khai `V11166 · 443 thư mục`; thật: **452 · V11174**) |
| G1-03 | P2 | **361 đường raw** vẫn trỏ chủ cũ `irissnss` sau khi chuyển tổ chức (V11171) |
| G2-01 | P2 | Cổng toàn dải **KHÔNG ĐẠT 39/251** — V11174 **không ghi** kết quả này |
| G5-03 | P1 | `output_counterfactual_rank` bị gọi là **BẢNG** (thật: **CỘT** trong `shadow_model_promotion_scorecard_daily`); số TRƯỚC lấy mốc **06/09** |
| G6-08 | P3 | «13/13 XÁC MINH» mạnh hơn nội dung — cổng 6 mang `INDETERMINATE`, cổng 7 không có artifact công bố · 🟢 **cả hai bảo lưu nay ĐÃ GỠ** (🔴 **ĐÍNH CHÍNH D-8 (`RL-034`)**) |
| G5-06 | P3 | «worktree sạch» — thật ra **208 tệp untracked** (đều trong `backups/`) |
| G4-08 | P2 | Snapshot dùng để **hoàn nguyên dữ liệu** lại **chỉ nằm trên chính VPS phải hoàn nguyên** |
| G6-06 | P2 | CONVERSATION_CONTEXT **bỏ mất vấp đáng giá nhất** — lần thứ **ba** mắc lỗi khung `FU-447` |

### 3.7 · Phát hiện BỊ BÁC — ghi để không ai lặp lại

| mã | cáo buộc | vì sao sai |
|---|---|---|
| G1-04 | *«cổng báo cáo `_v10921` TỰ GHI tệp `_I2_DA_CHAY.json`»* | **REFUTED** — không phải cổng đó ghi |
| G1-05 | *«artifact V11173/V11174 chỉ còn một bản sống»* | **REFUTED** — bản trên VPS còn nguyên |
| G2-03 | *«1 phép RM-01 không kết luận được chưa công bố ở đâu»* | **ALREADY_DONE** — đã công bố ở V11167 |
| G2-04 | *«verdict `PRJ_RETRACTION/WINDOW=SẠCH` rỗng nghĩa»* | **REFUTED** — lúc cổng chạy hai tệp có nội dung thật |
| G3-04 | *«sổ tương tác đổi nhãn cột»* | **REFUTED** |
| G4-09 | *«bước 9 chưa đóng gọn»* | **REFUTED** |
| G6-07 | *«nguyên văn owner chỉ là tiêu đề prompt»* | **REFUTED** |
| G3-03 | *«CHANGELOG không ghi điều kiện nâng tầng»* | **ALREADY_DONE** |

---

## 4 · HƯỚNG XỬ LÝ VÀ VÌ SAO CHỌN

**Vì sao đính chính TẠI CHỖ GỐC chứ không chỉ viết bản mới:** `PRJ-RETRACTION-001` nói thẳng —
*«sửa ở bản mới rồi im lặng về bản cũ KHÔNG PHẢI rút lại; người đọc bản cũ vẫn đang tin con số
sai»*. V11174 đã push công khai, ai đọc nó cũng đang tin `396c7559…`. Nên em sửa **ngay trong
`REPORT_V11174.md`**, mỗi chỗ gắn nhãn `ĐÍNH CHÍNH D-n`, **không sửa lén**.

**Vì sao mở V11175 riêng thay vì gộp vào V11174:** §63 buộc mỗi version có một dòng `HISTORY`;
gói kiểm chéo này có phép đo mới (tái lập 58/58 trên VPS), có 7 mục `RL` mới và 1 `QD` mới —
đủ là một việc riêng, không phải một lần sửa chính tả.

**Vì sao KHÔNG tự mở `FU-451`:** owner khoá *«Không tự tạo FU hoặc Plan mới»*. Lớp phản biện có
chỉ ra rằng câu *«Không mở FU mới»* trong dòng TanPhatAI là **chữ của agent**, nhưng ràng buộc gốc
trong §R **là lời owner thật**. Em **không tự nới** một ràng buộc để tiện cho mình.

**Vì sao KHÔNG vá `du-doan.html` ngay:** đó là **mặt official đang phục vụ**, ngoài phạm vi
`SC-12 = MEASUREMENT_ONLY`, và lúc phát hiện là **10:39 — trong giờ chạy**. Ghi thành nợ P1, không
lặng lẽ vá.

---

## 5 · ĐÃ LÀM GÌ

| # | việc | trước | sau |
|---|---|---|---|
| 1 | Tái lập 58/58 trên cây cô lập `/tmp` | artifact `dat:false`, không số | `TONG: 58/58 DAT` · stdout + artifact vào `evidence/` |
| 2 | Đổi tên artifact gây hiểu nhầm | `v11174_vah12_kq.json` | `v11174_vah12_kq_SAU_CAI_DAT_dat-false.json` |
| 3 | Rút digest + công bố tiêu chí đúng | `396c7559…` (không tái lập) | `0c5f84f8…` trên **582 dòng `date ≤ 2026-09-09`**, kèm lệnh |
| 4 | `REPORT_V11174.md` | — | **18 khối** sửa, 7 nhãn `ĐÍNH CHÍNH D-1…D-7` |
| 5 | `docs/SO_RUT_LAI.json` | 25 mục | **32 mục** (`RL-026`…`RL-032`, đủ bốn phần bắt buộc) |
| 6 | `docs/FOLLOW_UP_TRACKER.md:181-183` | *«VA-h12, 30/30 test, replay 45 dòng»* | **rút lại tại chỗ gốc**, bảng 3 vế + trạng thái đúng |
| 7 | `docs/OWNER_DECISION_LEDGER.json` | 75 quyết định | **76** — thêm `QD-074` `FINAL_BUNDLES_ZERO_WRITE` |
| 8 | 4 tệp điều hướng kho công khai | `V11166 · 443 thư mục` | **`V11174 · 452`** · `DIEU_HUONG_KHOP_THU_MUC=ĐẠT` |
| 9 | `REPORT_INDEX.md` | 305 đường `irissnss` | **0** · 314 `BaoBiTanPhat` |
| 10 | `00_PUBLIC_RAW_LINKS.md` | 56 đường `irissnss` | **0** · 56 `BaoBiTanPhat`, thử đường thật **http 200** |
| 11 | `evidence/` | 4 tệp | **8 tệp** — thêm stdout, artifact tái lập, artifact V11173, snapshot `day_governance` |
| 12 | Nhãn cổng V11174 | «13/13 XÁC MINH» | **«11 ✅ · 2 ✅ có bảo lưu»** + bảng cổng cấp kho có cả phần **KHÔNG ĐẠT** |

**`PRODUCTION_MUTATIONS = 0` · `DB MUTATIONS = 0` · `DEPLOY/RESTART = 0`.**
Việc duy nhất chạm VPS là **đọc** và một cây tạm trong `/tmp` (DB mở `mode=ro`).

---

## 6 · CỔNG KIỂM

| cổng | kết quả |
|---|---|
| `_v11044_cong_so_hieu.py` | **KHỚP** — V11175 trống, mọi nhãn QD trong báo cáo đều có trong sổ |
| `_v11083_sinh_dieu_huong.py` | **`DIEU_HUONG_KHOP_THU_MUC=ĐẠT`** — 452 thư mục, mới nhất V11174 |
| `_v11062_nang_version.py --kiem` | ĐẠT (seq 489 → **490**) |
| `_v11085_cong_rut_lai.py` | xem mục 7 |
| `_v11088_cong_cua_so_chon.py` · `_v11027_so_muc_quan_tri.py` | SẠCH / ĐẠT |
| `_v10921_report_gate.py V11175` | đủ 9/9 phần |
| `_v10921_report_gate.py` ① toàn dải | 🔴 **KHÔNG ĐẠT — 39/251**, nợ có sẵn của kho, **phiên này không xử** |

**Kiểm chứng độc lập trong phiên:** 12 tác nhân · 494 lần gọi công cụ · 1.484.153 token ·
0 lỗi tác nhân.

---

## 7 · VƯỚNG VẤP — BÀI HỌC

| # | vấp | ai bắt |
|---|---|---|
| 1 | 🔴 **Em gắn một tệp `dat:false` làm bằng chứng cho `58/58`** và không mở nó ra đọc trước khi push | góc kiểm 5 + góc 6, **độc lập với nhau** |
| 2 | 🔴 **Em công bố một digest không tái lập được** rồi đặt nó làm **điều kiện chặn** nâng tầng | góc kiểm 5 |
| 3 | 🔴 **Tiêu chí no-drift của em sai từ thiết kế** — dùng digest toàn bảng cho một bảng tăng mỗi ngày. Tối nay nó sẽ báo drift giả | em tự phát hiện khi kiểm lại P0-2 |
| 4 | 🔴 **Em viết `PRJ_RETRACTION=SẠCH`** trong khi chính báo cáo tự khai chỗ gốc mà **không sửa chỗ gốc** — cổng báo sạch vì sổ rút lại **chưa có** các mục đó | góc kiểm 4 + 6 |
| 5 | 🔴 **Em tuyên bố «KHÔNG CÓ quyết định nào chặn ở owner»** trong khi có đúng một | góc kiểm 4 |
| 6 | 🟠 **Em bỏ bước 8** (ghi quyết định owner) và **1/3 bước 7** (`FOLLOW_UP_TRACKER`) của chuỗi hoàn tất | góc kiểm 4 |
| 7 | 🟠 **Em bỏ hẳn bước sinh lại tệp điều hướng** — để kho công khai khai sai «latest V11166» suốt 8 bản | góc kiểm 1 |

**Bài học chung của cả bảy vấp:** cả bảy đều là **kiểm bằng trí nhớ thay vì bằng lệnh**. Em nhớ
đã chạy 58/58 nên gắn đại một tệp; nhớ đã tính digest nên chép lại con số; nhớ đã «rút lại trong
báo cáo» nên viết là SẠCH. **Không cái nào em mở ra đọc lại.** Đúng cái owner đã dặn từ trước:
*«kiểm bằng lệnh, không bằng trí nhớ»* — và lần này chính câu hỏi của owner mới lôi ra được.

**Điều đáng ghi thứ hai:** một lớp phản biện được lệnh **mặc định nghi ngờ** đã **bác 8/37 phát
hiện**, trong đó có hai cáo buộc nặng. Nếu em nhận hết 37 mục là thật thì em đã đi sửa những thứ
**không hỏng** — và đó cũng là một dạng tô vẽ.

---

## 8 · GỠ VỀ

Phiên này **không đụng production**, nên **không có gì để gỡ về ở phía runtime**.
Các tệp tài liệu đều có bản sao lưu trước khi sửa:

```
backups/SO_RUT_LAI.json.pre_v11174b
backups/FOLLOW_UP_TRACKER.md.pre_v11174b
backups/OWNER_DECISION_LEDGER.json.pre_v11174b
backups/00_PUBLIC_RAW_LINKS.md.pre_v11174b
```

Mọi phép ghi JSON đều **kiểm độ dài trước/sau và huỷ nếu tệp ngắn đi** (§63 luật 1).
`REPORT_V11174.md` gỡ về bằng `git checkout db989aa -- V11174_.../REPORT_V11174.md`.

**Trạng thái SC-12 KHÔNG đổi vì phiên này:** vẫn **`DEPLOYED_PENDING_SCHEDULED_PROOF`**.

---

## 9 · THEO DÕI TIẾP

### 9.1 · Việc kế tiếp vẫn là việc cũ — nhưng tiêu chí đã sửa

> Chờ `auto_verify` chạy tự nhiên **16:37–18:34 hôm nay**, rồi thu bằng chứng runtime:
> PID `3870722` gọi hàm đã vá · MT 10/09 nhận `INCLUDE` · **digest phạm vi khoá `0c5f84f8…`
> (582 dòng `date ≤ 2026-09-09`) không đổi** · 4 bảng khoá no-drift.
> Tính đến **10:37 hôm nay**: `day_governance` vẫn **581 dòng**, `classified_at` mới nhất vẫn
> **09/09 18:32:34** ⇒ **`auto_verify` chưa chạy**, trạng thái hiện tại vẫn đúng.

### 9.2 · Nợ MỞ sau phiên này

| mức | nợ |
|---|---|
| 🔴 P1 | **VA-2′ nửa chừng** — `du-doan.html:1354,1438-1444` + `quality_filtered_model_count`. Cần một lượt quét ngược **có phân loại** theo trục WRITER / READER_API / READER_UI (`RL-029`) |
| 🔴 P1 | **Cổng báo cáo toàn dải 39/251 KHÔNG ĐẠT** — 22 bản thiếu hẳn báo cáo, tất cả **≤ V11087B** |
| 🔴 P1 | **R6 · R7 · R8 vẫn `NOT_PERFORMED_THIS_SESSION`** — phiên này **không** đụng tới |
| P1 | **Backfill lịch sử chưa chạy** — **48** dòng MT vẫn `EXCLUDE_PRIMARY` *(số cũ «49» đếm dư 1 — 🔴 **ĐÍNH CHÍNH D-8 (`RL-034`)**)*; 🟢 **`INDETERMINATE` ĐÃ GỠ**: đúng **48 = 45 + 3**, `RL-014` được xác nhận **ĐÚNG** |
| P2 | `--out` của installer **không ghi số test** và **ghi đè** artifact cũ — chính khiếm khuyết đẻ ra P0-1 |
| P2 | Snapshot `daily_eval_log` (1,8 MB) vẫn chỉ trên VPS |
| P2 | Bộ sinh điều hướng **không nằm trong chuỗi hoàn tất 12 bước** ⇒ sẽ lại lạc hậu |
| P2 | Cổng báo cáo **chưa kiểm** mã `FU-xxx` trong báo cáo có tra được trong sổ theo dõi không — nếu có thì `FU-451` đã bị bắt từ V11170 |
| P3 | Lỗi khung báo cáo `FU-447` đã tái phạm **ba lần** ⇒ theo §61 phải **dựng cổng máy**, không được chỉ hứa |

### 9.3 · 🔴 CHẶN Ở OWNER — đúng một việc

> **`FU-451` là mã ma.** Bốn dòng `AUTOMATION_HISTORY` (V11170 · V11171 · V11173 · V11174) ghi
> `"theo_doi": ["FU-451"]`, nhưng `docs/FOLLOW_UP_TRACKER.md` **chưa bao giờ có mục đó**
> (`grep -c "FU-451"` = **0**; mã cao nhất là **FU-450**; `_v11044` xác nhận FU-451 **còn trống**).
>
> Em **không tự mở** vì owner khoá *«Không tự tạo FU hoặc Plan mới»*, và **không xoá được** bốn
> dòng HISTORY vì §63 luật 3 khoá **chỉ APPEND**. **Owner chọn một:**
>
> **(a)** cho mở `FU-451` theo khung §58 — *«FU-451 · DP1009 · Thu bằng chứng runtime
> `auto_verify` sau deploy SC-12 · hạn 10/09»*; hoặc
> **(b)** bỏ hẳn cách viện mã FU cho việc này, giữ bốn dòng HISTORY như dấu vết và ghi một dòng
> đính chính rằng mã đó **không tương ứng mục treo nào**.

---

## §62 — NGUỒN BA LỚP

### `OWNER_SAID`
> *«đã báo cáo đầy đủ chưa em?»* — 10/09/2026 ~10:05 ICT.
> *(§R, còn hiệu lực)* *«Không tự tạo FU hoặc Plan mới»* · *«`FINAL_BUNDLES_ZERO_WRITE`»*

### `CODE_DID`
- `evidence/v11174_vah12_kq.json` — `"dat": false`, `preimage` = hash **POST** ⇒ artifact sai nhãn.
- `/tmp/v11174_repro` — `sha256` hai bản sao lưu ra **đúng preimage**; `--test` → **`TONG: 58/58 DAT`**.
- `final_bundles` **583 dòng** lúc 10:37; dòng mới `id=860 · 2026-09-10 · MN · 05:26:43`.
- 6 công thức digest — **không cái nào** ra `396c7559…`; công thức khoá ngày ra `0c5f84f8…`.
- `du-doan.html:1354,1438,1439,1443,1444` — 5 điểm đọc **rơi ngược về `wr_gate_filtered`**.
- `main.py:652` — `quality_filtered_model_count` lấy từ `non_scoreable_count`, **không qua** VA-2′.
- `grep -c "FU-451" docs/FOLLOW_UP_TRACKER.md` → **0**; `docs/AUTOMATION_HISTORY.jsonl` → **4**.
- `day_governance` **581 dòng**, `MAX(classified_at)` = `2026-09-09 18:32:34` ⇒ auto_verify chưa chạy.

### `DOC_SAID`
- `REPORT_V11174.md` (bản đầu) — *«13/13 XÁC MINH»* · *«KHÔNG CÓ quyết định nào chặn ở owner»* ·
  *«worktree sạch»* · *«digest `396c7559…`»* — **cả bốn đã đính chính**.
- `docs/FOLLOW_UP_TRACKER.md:183` (bản đầu) — *«VA-h12, 30/30 test, replay đổi đúng 45 dòng»* —
  **đã rút lại tại chỗ gốc**.
- `LATEST_REPORT.json` (bản đầu) — *«latest V11166 · 443 thư mục»* — **đã sinh lại**.

**LỆCH BA LỚP:**
1. `DOC_SAID` ≠ `CODE_DID` ở **bốn** chỗ trên — tất cả đều là **tài liệu nói mạnh hơn mã/dữ liệu**,
   và **tất cả đều do chính agent viết ra ở phiên trước**.
2. `OWNER_SAID` ≠ `DOC_SAID`: owner khoá *«không tự tạo FU»* trong khi tài liệu của agent viện một
   mã FU **không tồn tại** ⇒ đẩy tới mục 9.3.

---

TanPhatAI cần làm: ghi **`V11175`** — `governance_seq 490`, công khai bản này. Ghi **CÂU TRẢ LỜI CHO OWNER LÀ: BÁO CÁO V11174 CHƯA ĐẦY ĐỦ** — 12 tác nhân kiểm chéo độc lập, **37 phát hiện → 29 xác nhận · 8 bị bác**. Ghi **HAI LỖI P0 trong V11174, cả hai agent tự kiểm lại và ĐÚNG**: ① tệp `evidence/v11174_vah12_kq.json` gắn nhãn «58/58» thực tế ghi **`dat: false`** và không chứa số test — nó là lượt chạy 01:56:48 **sau khi đã cài**, đã **ghi đè** artifact 58/58 thật; ② digest **`396c7559…` KHÔNG tái lập được** bằng bất kỳ công thức nào trong sáu công thức đã thử. Ghi **58/58 ĐÃ TÁI LẬP** trên cây cô lập `/tmp/v11174_repro` dựng từ hai bản sao lưu — hash ra **đúng preimage** `4ed5fd7e…`/`fd3d2349…` (đồng thời chứng minh **đường gỡ về là thật**), kết quả **`TONG: 58/58 DAT`**, production không đổi. Ghi **tiêu chí no-drift cũ SAI TỪ THIẾT KẾ**: `final_bundles` tăng tự nhiên mỗi ngày, hôm nay đã **583 dòng** (dòng mới `id=860 · 10/09 · MN · 05:26:43`) ⇒ tiêu chí cũ sẽ báo **drift giả** tối nay; tiêu chí đúng là **`0c5f84f8de9bbada94abe2b665dc53c5ab4044f07e64f2ebe796efff6278ffb2`** trên **582 dòng `date ≤ 2026-09-09`**, kèm đúng lệnh sinh ra nó. Ghi **VA-2′ mới NỬA CHỪNG (`A58_VIOLATION_HALF_DONE`)** — `du-doan.html:1354,1438-1444` rơi ngược về `wr_gate_filtered` thô nên **UI vẫn hiện đúng model bị trần**; nhãn đúng là **`PARTIAL`**, **không phải đã đóng**; **KHÔNG vá trong phiên này** vì đó là mặt official ngoài phạm vi `MEASUREMENT_ONLY`. Ghi **đã sửa TẠI CHỖ GỐC theo `PRJ-RETRACTION-001`**: `REPORT_V11174.md` **18 khối** (`ĐÍNH CHÍNH D-1…D-7`) · `SO_RUT_LAI.json` **25 → 32 mục** (`RL-026`…`RL-032`) · `FOLLOW_UP_TRACKER.md:181-183` rút lại tại chỗ · `OWNER_DECISION_LEDGER.json` **+`QD-074` `FINAL_BUNDLES_ZERO_WRITE`** (bước 8 mà V11174 **bỏ hẳn**) · 4 tệp điều hướng kho công khai từ **«V11166 · 443»** → **«V11174 · 452»** · **361 đường raw** hết trỏ `irissnss` (thử đường thật **http 200**). Ghi **nhãn cổng V11174 hạ từ «13/13» xuống «11 ✅ · 2 ✅ có bảo lưu»**, và **cổng toàn dải 39/251 KHÔNG ĐẠT** nay được ghi thẳng — **nợ có sẵn của kho, phiên này không xử**. Ghi **`PRODUCTION_MUTATIONS = 0 · DB MUTATIONS = 0 · DEPLOY/RESTART = 0`** và **SC-12 vẫn `DEPLOYED_PENDING_SCHEDULED_PROOF`**, Pure Context vẫn **`PURE_CONTEXT_PARTIAL`** — **hai dòng riêng**. Ghi **CHẶN Ở OWNER đúng một việc: `FU-451` là MÃ MA** — 4 dòng HISTORY viện tới, sổ theo dõi `grep -c` = **0**; agent **không tự mở** vì owner khoá *«không tự tạo FU»*, **không xoá được** HISTORY vì §63 chỉ APPEND ⇒ owner chọn **(a)** cho mở theo khung §58 hay **(b)** bỏ hẳn cách viện mã FU. Ghi **bài học chung của cả bảy vấp: kiểm bằng TRÍ NHỚ thay vì bằng LỆNH**. **Không mở Prompt 44. Không mở Plan mới. Không mở FU mới. Không trộn ERP.**
