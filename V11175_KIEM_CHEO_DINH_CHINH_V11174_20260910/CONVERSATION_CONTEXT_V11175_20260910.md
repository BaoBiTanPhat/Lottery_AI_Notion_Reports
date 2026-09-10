# CONVERSATION CONTEXT — V11175 · 10/09/2026

> Nguyên văn lời owner · agent làm gì · vấp ở đâu (§57.2). Giờ **Việt Nam (UTC+07:00)**.
> `CURRENT_ACTOR = CLAUDE_CODE` · **Prompt 43 R1 giữ `PARTIAL` — không mở Prompt 44.**
> **Kết thúc: SC-12 vẫn `DEPLOYED_PENDING_SCHEDULED_PROOF` · Pure Context vẫn `PURE_CONTEXT_PARTIAL`**
> **`PRODUCTION_MUTATIONS = 0` · `DB MUTATIONS = 0` · `DEPLOY/RESTART = 0`**

---

## 1 · Owner nói gì — NGUYÊN VĂN

| giờ ICT | NGUYÊN VĂN | loại | agent đã làm gì | trạng thái |
|---|---|---|---|---|
| **~10:05** | *«đã báo cáo đầy đủ chưa em?»* | `HỎI` | **Không trả lời bằng trí nhớ.** Chạy 12 tác nhân kiểm chéo độc lập (6 góc × 1 lớp phản biện) → **CHƯA ĐẦY ĐỦ** → tự kiểm lại 2 lỗi P0 → sửa 12 mục tại chỗ gốc → 1 mục chặn ở owner | `ĐÃ_LÀM` |

---

## 2 · Điều đáng nói nhất — một câu hỏi bốn chữ lôi ra hai lỗi P0

Owner chỉ hỏi *«đã báo cáo đầy đủ chưa em?»*. Em **định** trả lời «rồi» — vì em nhớ là đã push đủ
hai kho, cổng đã đạt, bốn mặt đã ghi. **Tất cả những điều đó đều đúng.**

Nhưng em cho chạy lớp kiểm chéo trước khi trả lời, và nó tìm ra hai chỗ **em nhớ là đã làm, mà
thực tế không phải**:

**① Tệp bằng chứng «58/58» là tệp sai.** Em nhớ đã chạy 58/58 nên gắn `v11174_vah12_kq.json` vào
`evidence/` — **mà không mở nó ra đọc**. Nội dung thật:

```json
{ "dat": false, "ICT": "2026-09-10T01:56:48+07:00",
  "preimage": { "database.py": "758cf2cf…", "main.py": "d59a6ae9…" } }
```

`dat: false`, **không chứa số test nào**, và hai hash đó là **hash POST**. Nó là lượt chạy **sau
khi đã cài** — fail-closed đúng luật — và nó **ghi đè** artifact 58/58 thật, vì `--out` mặc định
trỏ cùng một đường dẫn.

**② Digest `396c7559…` không tái lập được.** Em nhớ đã tính nó nên chép lại con số vào báo cáo,
CHANGELOG, SSOT, CONTEXT, và đặt nó làm **điều kiện chặn** nâng `SC12_RUNTIME_PROVEN`. Thử **sáu**
công thức trên chính DB production: **không cái nào ra `396c7559…`**.

---

## 3 · Điều đáng nói thứ hai — lỗi nặng hơn không phải chuyện tái lập

Khi đi tìm công thức đúng, em phát hiện một điều tệ hơn: **tiêu chí đó sai từ lúc viết ra**.

`final_bundles` **tăng tự nhiên mỗi ngày**. Đo lúc 10:37 hôm nay:

```
final_bundles = 583 dòng          (V11174 công bố 582)
dòng mới: id=860 · 2026-09-10 · MN · ACTIVE · created_at 05:26:43
```

Đó là **bundle MN bình thường của hôm nay**. Nghĩa là nếu tối nay em cứ theo tiêu chí *«digest
toàn bảng không đổi»*, nó sẽ báo **DRIFT GIẢ** ngay trên chính bản deploy em vừa làm — và em có
thể đã kết luận sai về một hệ đang chạy đúng.

**Tiêu chí đúng:** dòng `date ≤ 2026-09-09` phải bất biến → `0c5f84f8…` trên 582 dòng.
Dòng `date ≥ 2026-09-10` là **tăng trưởng hợp lệ**.

---

## 4 · Điều đáng nói thứ ba — VA-2′ mới nửa chừng

Em báo VA-2′ như một mảnh **đã đóng**. Đo lại:

```
du-doan.html:1354       if (!filteredModels.length && sourcePreds.wr_gate_filtered)
                            filteredModels = sourcePreds.wr_gate_filtered;
du-doan.html:1438-1444  … cùng mẫu, và in thẳng tên model
```

VA-2′ lọc danh sách thành `[]` → điều kiện `!length` **thành đúng** → **UI lấy đúng danh sách
nhiễm mà VA-2′ vừa bỏ**. Đây đúng lối `§60.1` cảnh báo: *«gỡ mệnh lệnh nhưng giữ nhãn thì nhãn tự
dạy lại»*. Mã vi phạm **`A58_VIOLATION_HALF_DONE`**.

**Em KHÔNG vá ngay** — `du-doan.html` là mặt official đang phục vụ, ngoài phạm vi
`SC-12 = MEASUREMENT_ONLY`, và lúc phát hiện là **10:39, trong giờ chạy**. Ghi thành nợ P1.

---

## 5 · Lớp phản biện bác 8/37 — và đó cũng là kết quả

Góc phản biện được lệnh **mặc định nghi ngờ, phải tự chạy lệnh**. Nó **bác 8 phát hiện**, gồm hai
cáo buộc khá nặng: *«cổng báo cáo tự ghi tệp»* và *«artifact chỉ còn một bản sống»* — cả hai đều
sai. Nó còn **đính chính ngược lại góc kiểm**: chỉ ra câu *«Không mở FU mới»* là **chữ của chính
em**, không phải lời owner *(ràng buộc gốc trong §R thì đúng là lời owner — nên em vẫn không tự
mở FU)*.

Nếu em nhận cả 37 mục là thật, em đã đi sửa những thứ **không hỏng** — và đó cũng là một dạng tô vẽ.

---

## 6 · Vấp ở đâu

| # | vấp | ai bắt |
|---|---|---|
| 1 | 🔴 Gắn một tệp `dat:false` làm bằng chứng `58/58` — **không mở ra đọc trước khi push** | góc 5 + góc 6, độc lập |
| 2 | 🔴 Công bố digest **không tái lập được**, rồi đặt nó làm **điều kiện chặn** | góc 5 |
| 3 | 🔴 Tiêu chí no-drift **sai từ thiết kế** — sẽ báo drift giả tối nay | em, khi kiểm lại P0-2 |
| 4 | 🔴 Viết `PRJ_RETRACTION=SẠCH` trong khi **không sửa chỗ gốc** — cổng báo sạch vì sổ rút lại chưa có mục | góc 4 + 6 |
| 5 | 🔴 Tuyên bố *«KHÔNG CÓ quyết định nào chặn ở owner»* — có đúng một | góc 4 |
| 6 | 🟠 Bỏ **bước 8** (sổ quyết định) và **1/3 bước 7** (`FOLLOW_UP_TRACKER`) | góc 4 |
| 7 | 🟠 Bỏ bước **sinh lại tệp điều hướng** — kho công khai khai sai «latest V11166» suốt **8 bản**, và **361 đường raw** còn trỏ chủ cũ `irissnss` | góc 1 |
| 8 | 🟡 **Lần thứ BA** mắc lỗi khung báo cáo `FU-447` (V11172 báo ra → V11173 mắc → V11174 mắc) — CONTEXT của V11174 **bỏ mất** đúng cái vấp đáng giá nhất này | góc 6 |

**Bài học chung của cả tám:** đều là **kiểm bằng trí nhớ thay vì bằng lệnh**. Em nhớ đã chạy nên
gắn đại một tệp; nhớ đã tính nên chép lại con số; nhớ đã «rút lại trong báo cáo» nên viết là SẠCH.
**Không cái nào em mở ra đọc lại.**

---

## 7 · Cho TanPhatAI đọc tiếp

**Đừng đọc V11174 mà bỏ qua V11175.** Bản V11174 đã được sửa **tại chỗ gốc** với bảy nhãn
`ĐÍNH CHÍNH D-1…D-7`, và `CONVERSATION_CONTEXT_V11174` đã gắn banner ở đầu.

**Đừng dùng `396c7559…`.** Nó đã bị rút (`RL-026`). Dùng **`0c5f84f8…`** trên **582 dòng
`date ≤ 2026-09-09`**.

**Đừng đọc VA-2′ là «đã đóng».** Nhãn đúng: **`PARTIAL`** (`RL-029`).

**Đừng đọc «13/13».** Nhãn đúng: **11 ✅ · 2 ✅ có bảo lưu** (`RL-028`).

**Trạng thái KHÔNG đổi:** SC-12 vẫn **`DEPLOYED_PENDING_SCHEDULED_PROOF`** — `day_governance` vẫn
581 dòng, `classified_at` mới nhất vẫn **09/09 18:32:34** lúc 10:37 hôm nay ⇒ `auto_verify` **chưa
chạy**. Pure Context vẫn **`PURE_CONTEXT_PARTIAL`**. **Hai dòng riêng.**

**Một việc chặn ở owner:** `FU-451` là **mã ma** — xem mục 9.3 của `REPORT_V11175.md`.

---

TanPhatAI cần làm: ghi **`V11175`** — công khai bản này cùng `REPORT_V11175.md`. Ghi **câu trả lời cho owner: báo cáo V11174 CHƯA ĐẦY ĐỦ** — 12 tác nhân kiểm chéo, **37 phát hiện → 29 xác nhận · 8 bị bác**. Ghi **hai lỗi P0 đã tự kiểm lại và ĐÚNG**: tệp bằng chứng «58/58» thực tế `dat: false`; digest `396c7559…` **không tái lập được**. Ghi **58/58 ĐÃ TÁI LẬP** (`TONG: 58/58 DAT`) trên cây cô lập dựng từ bản sao lưu — hash ra **đúng preimage**, đồng thời chứng minh **đường gỡ về là thật**. Ghi **tiêu chí no-drift cũ SAI TỪ THIẾT KẾ** — `final_bundles` hôm nay đã **583 dòng**, tiêu chí cũ sẽ báo **drift giả**; tiêu chí đúng **`0c5f84f8…`** trên **582 dòng `date ≤ 2026-09-09`**. Ghi **VA-2′ = `PARTIAL`, không phải đã đóng** (`A58_VIOLATION_HALF_DONE`, `du-doan.html:1354,1438-1444`). Ghi **đã sửa tại chỗ gốc**: `REPORT_V11174.md` 18 khối · `SO_RUT_LAI.json` 25→32 · `FOLLOW_UP_TRACKER:181-183` · `OWNER_DECISION_LEDGER` +`QD-074` · 4 tệp điều hướng V11166→V11174 · 361 đường raw hết trỏ `irissnss`. Ghi **`PRODUCTION_MUTATIONS = 0 · DB MUTATIONS = 0 · DEPLOY/RESTART = 0`**. Ghi **CHẶN Ở OWNER: `FU-451` là mã ma** — owner chọn (a) cho mở theo §58 hay (b) bỏ hẳn cách viện mã FU. Ghi **bài học: kiểm bằng TRÍ NHỚ thay vì bằng LỆNH**. **Không mở Prompt 44. Không mở Plan mới. Không mở FU mới. Không trộn ERP.**
