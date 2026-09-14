# NOTION_SYNC_DELTA_PACKET — V11188 · §AC EOD forensic 14/09 · 15/09/2026

> **Agent IDE KHÔNG ghi Notion** (§57.1) và **không tuyên bố Notion đã sync**. TanPhatAI chỉ sync
> **sau khi** code / private / public / runtime đã khớp.

---

## A. HAI NGÀY, HAI EPOCH — ĐỪNG GỘP

| | |
|---|---|
| **14/09** | chạy **trọn ngày V11185**. Mọi số dự đoán của ngày này thuộc về V11185 |
| **15/09** | ngày đầu tiên dưới **V11186/§AB** (deploy 14/09 20:05, tức **sau** mọi lượt sinh output 14/09) |

⇒ **`§AB_RUNTIME_14SEP = NOT_APPLICABLE_DEPLOYED_AFTER_EOD`.** Cấm dùng kết quả 14/09 để nói §AB
tốt lên hay xấu đi.

---

## B. KẾT QUẢ NGÀY 14/09 — con số để ghi

```
EOD_20260914_RESULT_DATA = COMPLETE_VALID      (MN 3/3 đài · MT 2/2 · MB 1/1)
OFFICIAL_BT_20260914     = MN_LOSE · MT_WIN · MB_LOSE                    → 1/3
OFFICIAL_LO2_20260914    = MN_PARTIAL · MT_WIN · MB_PARTIAL              → 4/6 số trúng
OFFICIAL_LO3_20260914    = MN_LOSE · MT_LOSE · MB_LOSE                   → 0/3
LIVE_SCORING_DEFECT      = KHÔNG CÓ  (stored khớp tính lại 100%, cả 15 trường bundle + 36/36 dòng model)
```

Nền ngẫu nhiên **chính xác từng miền**: MN **0,4200** · MT **0,3100** · MB **0,2600** ⇒ kỳ vọng
**0,99 trúng / 3 miền**. Thực tế **1/3**.

🛑 **n = 1 ngày.** Độ lệch chuẩn một phép Bernoulli tại nền là 0,49 / 0,46 / 0,44 — **lớn hơn mọi
lệch quan sát**. `RM-04`: **chưa được phép kết luận** gì về chất lượng hệ.

---

## C. NGUYÊN NHÂN THUA — RANKER, KHÔNG PHẢI GENERATOR

```
TOTAL_ROOT_CAUSE = MN_RANKER_MISS · MT_OFFICIAL_WIN · MB_RANKER_MISS
```

Pool ứng viên đông cứng của **cả ba miền đều CHỨA** đuôi trúng. `GENERATOR_MISS` bị **loại có bằng
chứng**.

| miền | cơ chế |
|---|---|
| MN | đuôi trúng `14` có 3 phiếu nhưng **cả ba đều ở top2** (`pw=0,80`). **24 = 0,1362 vs 14 = 0,1350 — biên 0,0012** |
| MB | đuôi trúng `31` là **số thứ hai của chính model đã đặt số thua `16` lên đầu** |
| MT | `ranked[0]=20` trúng — WIN |

**Bốn lớp override KHÔNG lớp nào nổ** ngày 14/09 (0 dòng `🎯`, `xien2[0]==bach_thu` cả ba miền).
⇒ `OVERRIDE_HURT` và `OVERRIDE_HELPED` **đều bị loại**.

**Phản tưởng đã bác cách sửa dễ nhất:** bỏ chiết khấu vị trí (`pw` top2 = 1,0) thì MN **vẫn miss**
và MB **vẫn miss**.

---

## D. LƯỢT COMBO NGOÀI ROSTER — hai vế phải đi cùng nhau

```
ROGUE_COMBO_CALL_OUTPUT_IMPACT = NO_OUTPUT_IMPACT_AS_RUN
                               + OUTPUT_CONTAMINATION_PATH_CONFIRMED
```

- `gemini-2.5-pro` @MB 17:33, **26.784 token**, trả `["16","46"]` — **0/2 trúng**.
- Bỏ hẳn phiếu `combo-super`: `16` **vẫn #1** (0,0846 vs `31` chỉ 0,0415) ⇒ **không phải nguyên
  nhân MB thua**, nó góp 10,5% điểm của `16`.
- **Nhưng** lượt đó là **pha AI của chính `combo-super`**, và `combo-super` là **một trong ba
  voter** của số top-1. Đường lan vào bundle official **là có thật**.

**Cấm** ghi gọn thành "không ảnh hưởng" mà bỏ vế thứ hai.

---

## E. 🔴 HAI PHÁT HIỆN MỚI PHẢI VÀO SỔ CƠ CHẾ

### E.1 `EXPECTED_MODEL_COUNT` lệch roster ⇒ mọi bundle bị xếp INCOMPLETE

`EXPECTED_MODEL_COUNT = len(get_output_eligible_ids())` = **15**, danh sách đó **vẫn còn**
`gemini-2.5-pro`, `deepseek-reasoner`, `gpt-5.4` — model **ngoài mọi roster hoặc đang bị cách ly**.

| ngày | MN | MT | MB |
|---|---|---|---|
| 03–11/09 | 14–15 | 12–13 | 15 |
| **14/09** | **11** | **11** | **11** |

`classify_bundle_quality(11)` = **`INCOMPLETE`** cả ba miền. Từ 14/09 **mọi bundle đều INCOMPLETE
theo thiết kế**. Hạn xử lý **16/09**.

### E.2 Có lớp hậu-xếp-hạng THỨ NĂM

`main_number_anti_trap` + `near_miss_anti_trap` (`main.py:10441+`) chạy trong **cùng hàm**, **sau**
bốn lớp override. Tài liệu dự án lâu nay chỉ ghi **bốn**.
**Bạch thủ duy nhất thắng trong ngày (MT `20`) bị chính lớp này gắn cờ `FULL_SPENT`.** Hạn **17/09**.

---

## F. TOKEN / COST 14/09

```
TOKEN_14SEP = ACTUAL_CALLS_AND_TOKENS_MEASURED
              14 lượt / 424.615 token   (MN 5/151.015 · MT 4/113.756 · MB 5/159.844)
              main chain 12/366.710 · Combo 2/57.905 · shadow 0 · retry 0 · denied 0
COST_14SEP  = UNKNOWN cho 9 lượt · TÍNH LẠI ĐƯỢC cho 5 lượt OpenRouter
```

**Cấm ghi 0. Cấm dùng lại `−74,7%`** (ước lượng đã rút lại, `RL-047`).

---

## G. TRẠNG THÁI CÁC THAY ĐỔI — ghi đúng tầng

| thay đổi | tầng đúng |
|---|---|
| §AA roster 8→4 | `OPERATIONALLY_STABLE_ONE_DAY` — **không** phải `PREDICTIVELY_BETTER` |
| Shadow pause · quarantine · no-retry | `LIVE_PROVEN_ZERO` (0 lượt cả ba miền) |
| **QD-079 optimizer C1+C2+C3** | 🔴 **`DEPLOYED`, KHÔNG phải `RUNTIME_PROVEN`** — optimizer **chưa chạy lần nào** kể từ khi vá; lượt đầu là **CN 20/09 03:00** |
| §AB (Combo gate · dispatcher · fingerprint · cost) | `DEPLOYED_PENDING_NATURAL_PROOF` |
| Rollback CẤP 1 | `EXISTS_AND_VERIFIED` (sha khớp 5/5) |
| CẤP 2 + expiry | `DEPLOYED_OFF_BY_DEFAULT` |
| TOTAL formula · weights · prompt CORE | `UNCHANGED` |

⚠️ **Đính chính công thức TOTAL:** `partial_bonus_shadow` **CHỈ ghi vào trace, KHÔNG nhân vào
score** (`main.py:10004`). Mô tả cũ có thừa cấu phần này.

---

## H. HẠ TẦNG P0 — `EXACT_BLOCKER` carry-forward

| mục | số thật |
|---|---|
| backup off-machine | lần cuối **17/04 — 150 ngày**. Hai tarball **cùng một ảnh chụp DB** ⇒ **một** điểm khôi phục |
| mất theo **bảng** | **233/257 bảng (90,7%)** không có trong backup = **55,9%** dung lượng DB |
| OOM | **2 sự kiện ngày 05/09** — *không phải 0*; số 0 trước đây là artifact journal xoay vòng |
| SSH brute-force | ~**25.246** lượt `Failed password` |
| mã nguồn | **CÓ** bản sao ngoài máy (GitHub + local) |

**Câu đúng:** *"**DỮ LIỆU** thời gian thực không có bản sao ngoài máy từ 18/04"* — **không** phải
"toàn hệ không có bản sao".

---

## I. ĐIỀU TANPHATAI KHÔNG ĐƯỢC LÀM

- **Không** gán bất kỳ kết quả dự đoán nào của 14/09 cho §AB.
- **Không** ghi nguyên nhân thua là `GENERATOR_MISS` — đã bị loại có bằng chứng.
- **Không** ghi lượt Combo ngoài roster là nguyên nhân MB thua.
- **Không** rút gọn `NO_OUTPUT_IMPACT_AS_RUN` mà bỏ vế `OUTPUT_CONTAMINATION_PATH_CONFIRMED`.
- **Không** nâng `DEPLOYED_PENDING_NATURAL_PROOF` thành `ROSTER_SYSTEM_WIDE_LIVE_PROOF_OK` — chờ
  đủ ba receipt ngày 15/09.
- **Không** ghi QD-079 là đang thi hành / đã chứng minh — tầng đúng là `DEPLOYED`.
- **Không** ghi cost bằng 0; **không** dùng lại `−74,7%`.
- **Không** nâng `PREDICTIVE_LIFT` khỏi `NOT_PROVEN`; giữ `POOL_VERDICT=HOLD` · `SC12=CLOSED`.
- **Không** kết luận gì về chất lượng hệ từ con số bạch thủ 1/3 — n=1 ngày.
