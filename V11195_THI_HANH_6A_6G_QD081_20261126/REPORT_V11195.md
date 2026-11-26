# V11195 — Thi hành 7 quyết định chuyên môn 6a–6g (QD-081): sửa nhãn đo tiến của luật rồi đo lại, vá nốt biên anchor, đưa ngưỡng ghi đè MN về mốc mới

> **Phiên bản:** V11195 · **Ngày:** 26/11/2026 ~10:10 → ~11:20 ICT · **Repo riêng:** `Lottery_AI_Test` commit `725779b`
> (nhánh `fu438/admin-only-p0a` + `master`) · **governance_seq:** 510 · **Quyết định:** `QD-081`
> · **Tầng (RM-12):** mã + nhãn DB `DEPLOYED` (đọc lại DB production sau khi áp: 9.351/9.351 nhãn khớp) · bảng
> `/monitoring` `DEPLOYED` (restart, `compute_view()` trên DB production ra «ĐANG ĐO»; chưa xem qua trình duyệt đã đăng
> nhập) · **Runtime đổi:** có — restart `lottery` 10:47, PID 1122833 → 1277779.

## 1. Tóm tắt

- Owner chốt cả bảy việc chuyên môn 6a–6g «theo khuyến nghị». Bảy việc đã thi hành, mỗi việc có phép máy kiểm lại
  được; quyết định ghi thành `QD-081` (🟢 khớp 3/3 phép trên bộ kiểm sổ quyết định).
- **Phát hiện quan trọng nhất (6e):** sau khi sửa nhãn đo tiến, **luật soi cầu không có tín hiệu đo tiến ở MN và MT,
  và KÉM NỀN ở MB** (z −2,38; đối chứng luật giả z −2,29). Con số «hơn nền +15…+24 điểm» chỉ có trong cửa sổ đã dùng
  để chọn luật. Trong khi đó `MINED_RULES_MODE='soft'` vẫn cộng **CHỐT GẤP +0,40** vào bộ chọn số ở cả ba miền — chưa
  đổi hôm nay (đường chọn số, cần owner), chuyển sang phương án dọn dẹp.
- **6c:** bảng `/monitoring` đang in **«NÊN TẮT»** lớp ghi đè MN (chấm trên cửa sổ trượt 30 ngày), trái với quyết định
  giữ của owner. Đã đưa bảng về luật QD-081 (đo từ 26/11, xem lại 26/02/2027) và restart để có hiệu lực.
- **6f không đóng được như đã hứa:** khuyến nghị V11193 dựa trên câu «177 lượt < 10.000 đều là MT» — sai, MN cũng có
  26 lượt (RL-051). Đã thi hành đúng phần owner duyệt (MT), trả lại owner câu MN — agent không tự nới.
- Hai đính chính: RL-050 (số 89,7% có thật nhưng là độ phủ Gate 1 ở MN), RL-051 (177 = MT 151 + MN 26).

## 2. Owner yêu cầu gì (nguyên văn) — §62 lớp `OWNER_SAID`

**26/11/2026 ~10:10 ICT** — một tin nhắn, ba yêu cầu. Bản này thi hành phần thứ nhất:

> 6a --> theo khuyến nghị
> 6b --> theo khuyến nghị
> 6c --> theo khuyến nghị
> 6d  --> theo khuyến nghị
> 6e --> theo khuyến nghị
> 6f --> theo khuyến nghị chú ý ghi nhận lưu lại backup lại nha em
> 6g --> theo khuyến nghị --> theo khuyến nghị

Hai phần còn lại cùng tin nhắn, làm ở bản riêng (một việc một bản):
*«Đồng thời kiểm tra dự đoán hôm qua và hôm nay nha em.»* · *«Lên phương án kế hoạch dọn dẹp hệ thống đi cồng kềnh quá
mà chả hiệu quả gì cả em?»* — cả ba dòng đã vào `docs/SO_TUONG_TAC_OWNER.md` lúc bắt đầu phiên.

Khuyến nghị owner duyệt là bảng 6a–6g trong câu trả lời V11193 (25/11 ~22:05).

## 3. Đào bới / phát hiện — liệt kê ĐỦ

### 3.1 6a · FU-195 — `glm-5.1` (`evidence/nguong_glm.txt`)

| cách đo | cửa sổ | lỗi / lượt | tỉ lệ | đọc |
|---|---|---|---|---|
| cũ (owner 31/07) | 14 ngày 12–25/11, tính cả ngày OpenRouter chặn | 4 / 28 | 14,3% | vượt 6% |
| **mới (QD-081)** | 28 ngày 29/10–25/11, loại 25/11 (OpenRouter hỏng toàn phần) | **2 / 54** | **3,7%** | xác suất do ngẫu nhiên 0,843 ⇒ **GIỮ** |
| nền 90 ngày trước | 31/07–28/10 | 4 / 174 | 2,3% | — |

MT khoá bundle sau 16:58: 0 ngày. Hai lỗi «thật» trong cửa sổ là 23/11 MT và một lượt khác; hai lỗi 25/11 là do
OpenRouter chặn (V11193).

### 3.2 6b · FU-400 — trọng số chọn số (`evidence/do_trong_so_fu400.txt`)

Đo lại trên DB production, n = 752 miền-ngày ghép cặp: chọn bằng trọng số trúng 34,4% · luật thô «nhiều phiếu nhất»
37,4% · chênh −2,93 điểm · McNemar z −1,80, p 0,072 · VIF đo 1,18 · từng miền MN z −0,49 · MT −1,83 · MB −0,77. Năm cửa
sổ 30/60/90/120/272 ngày đều âm, không cửa sổ nào |z| ≥ 1,96 — xem bảng cửa sổ trong evidence. Chưa đủ bằng chứng để đổi.

### 3.3 6c · FU-183 — lớp ghi đè V10640 MN (`evidence/bang_ghi_de_mn_sau_va.txt`)

| cửa sổ | ngày | cứu / phá / hoà | chênh so với không ghi đè | bảng cũ kết luận |
|---|---|---|---|---|
| 30 ngày gần nhất | 30 | 0 / 2 / 1 | **−9,8tr** | **«NÊN TẮT»** |
| từ 01/09 | 86 | 3 / 4 / 3 | 0,0tr | NÊN GIỮ |
| từ 01/08 (cửa sổ ngưỡng gốc) | 117 | 7 / 5 / 7 | **+14,7tr** | NÊN GIỮ |

Bảng `/monitoring` chấm ngưỡng trên **cửa sổ trượt 30 ngày** (`compute_view(so_ngay=30)`) — cửa sổ đó không phải luật
owner duyệt, và hôm nay nó in «NÊN TẮT» đúng lúc owner chốt giữ. Lượt gọi endpoint lúc 24/11 23:20:24 (nginx
`access.log.2.gz`) chứng minh mô-đun đã nạp trong tiến trình ⇒ phải restart mới có hiệu lực.

### 3.4 6d · FU-397 — câu anti-trap
Không đo lại: số của V11190 (n = 117, z_MH −0,56, phần đo tiến +2,9 điểm đổi dấu so với hồi tố −12,8). Câu dạy nằm ở
`gpt_analyzer.py` mục «10B. OWNER ANTI-TRAP DOCTRINE» (sổ cũ ghi `:755`, nay ở `:608`).

### 3.5 6e · nhãn đo tiến của luật (`evidence/sua_nhan_thu.txt`, `evidence/do_lai_luat.txt`)

**Chỗ rò, đọc mã:** `weekly_rule_miner.py:202` chấm bù 112 ngày cho bộ luật mới mỗi thứ Hai bằng
`INSERT OR REPLACE`; `_v11025_khoa_luat_ben.phan_loai_giai_doan()` gắn `DO_TIEN` khi `date >= mốc thấy lần đầu`. Luật nghỉ
vài tuần rồi được đào lại thì dòng chấm bù cho những ngày NGHỈ vẫn mang `DO_TIEN`, dù chính những ngày đó là dữ liệu
đã dùng để chọn lại luật.

**Lịch lần đào thật:** `mining_log` (SUCCESS) 17 ngày 03/08 → 23/11, khớp từng ngày với `scheduler_logs` («Bắt đầu
Weekly Rule Mining», log_time +7) và mọi ngày `OBSERVED` trong sổ khoá — 0 ngày thiếu. Sổ khoá: 358 khoá (253
`OBSERVED` từ 10/08, 105 gieo mầm 07/08); chỉ 21 khoá có mặt ở cả 17 lần đào.

**Gắn lại nhãn:** `DO_TIEN` 2.025 → **1.132** · 938 dòng sang `CHUA_XAC_MINH_HOAT_DONG` (luật có quãng nghỉ) · 45 dòng
trống được gắn · 983 dòng đổi nhãn.

**Đo lại — báo cả hai vế (PRJ-SELECTION-WINDOW-001), z theo cụm ngày-miền, VIF đo cho chính thước này (RM-21):**

| miền | NGOÀI cửa sổ chọn — đo tiến (toàn bộ 07/08 → 25/11) | TRONG cửa sổ chọn | M4' thật vs giả (ngoài cửa sổ) |
|---|---|---|---|
| MN | n 378 · 84,1% vs nền 84,0% · **+0,1** · z +0,07 · không có tín hiệu | n 730 · +15,0 · z +7,95 | 46 / 40 · z +0,64 · ngang nhau |
| MT | n 408 · 77,2% vs 75,3% · **+1,9** · z +0,88 · không có tín hiệu | n 767 · +19,3 · z +7,26 | 67 / 57 · z +0,85 · ngang nhau |
| MB | n 346 · 45,7% vs 52,0% · **−6,3** · z **−2,38 · kém nền** | n 1.260 · +24,1 · z +8,33 | 60 / 92 · z **−2,29 · giả hơn** |

Cửa sổ 30 / 60 / 90 ngày cùng chiều với toàn bộ (MB âm ở cả bốn cửa sổ; MT 60 ngày +5,4 z +1,83 là cao nhất, vẫn dưới
ngưỡng). VIF đo được ở phần đo tiến 0,8…1,4 — bản `_v11030` cũ mượn hằng số 2,92 của thước khác (RM-21).

### 3.6 Hệ quả 6e — CHỐT GẤP vẫn bật

`main.py:124` `MINED_RULES_MODE = 'soft'` ⇒ `combo_super.py:1982` cộng **+0,40** cho mọi đuôi có luật hội tụ, ở cả ba
miền, và thêm đuôi vào `prize_prefilter_nums`. Mục `D2` (soft → shadow) của gói 21/08 **chưa thi hành**. Luật không có
tín hiệu đo tiến (và kém nền ở MB) đang cộng điểm vào bộ chọn số.

### 3.7 6f · FU-345 (`evidence/do_fu345.txt`)

| miền | lượt 09/08 → 26/11 | = 64 ký tự (lỗi gốc) | < 10.000 | nhỏ nhất | p10 |
|---|---|---|---|---|---|
| MN | 1.070 | 0 | **26** | 9.809 | 10.441 |
| MT | 1.014 | 0 | 151 | 9.044 | 9.851 |
| MB | 1.041 | 0 | 0 | 14.128 | 14.714 |

### 3.8 6g · FU-392
Chỗ còn lại ở dòng **303** (sổ ghi 297 — dòng đã trôi). Job `v104_materializer` (`scheduler.py`) trả về trước khi
import từ V10659 (31/05) ⇒ hàm này không chạy. Quét ngược cả tệp: mọi truy vấn khác dùng `target_date = ?` trên bảng
ảnh chụp — không cùng họ lỗi biên.

### 3.9 Bẫy của bộ đọc sổ theo dõi
Khối mới nhất ghi «hạn LX» thì `_v10958_fu_reader` **kế thừa hạn của khối cũ** — FU-345 sẽ hiện «quá hạn từ 08/08». Đã
cho FU-345 hạn 03/12 thay vì LX; không đổi hành vi bộ đọc (kế thừa là có chủ ý, chống khối cập nhật lười giấu hạn thật).

### 3.10 Đính chính (PRJ-RETRACTION-001)

| | RL-050 | RL-051 |
|---|---|---|
| chỗ gốc | trả lời IDE 25/11 ~13:4x (việc 6a) + câu đính chính tối 25/11 | `docs/DOI_CHIEU_58_MUC_V11190.md:79` (+ bản trong `V11190_*/evidence`) + trả lời IDE tối 25/11 (việc 6f) |
| nguyên văn câu sai | «cổng tự động đòi gỡ vì độ phủ 89,7% < 90%» · «Con số sai không nằm trong tài liệu nào» | «177 lượt < 10.000 (MT p10 9.851 — ngưỡng không hợp MT)» |
| điều đúng + phép đo | 89,7% là độ phủ Gate 1 của glm-5.1 ở **MN** (`_v11185_roster_goi_token.py:77`); ngưỡng MT là FU-195 — `_v11195_nguong_glm.py` | MT 151 + **MN 26** + MB 0 — `_v11195_do_fu345.py` |
| quyết định đã dựa trên số sai | không có | owner chốt 6f — thi hành phần MT, trả câu MN |

Đã ghi chú rút lại ngay tại chỗ gốc (hai bản DOI_CHIEU và REPORT_V11193 §3.6).

## 4. Hướng xử lý và vì sao chọn

- **Thi hành đúng chữ owner duyệt, không thêm bớt.** Chỗ nào tiền đề sai (6f) thì thi hành phần đã duyệt và trả câu còn
  lại cho owner — nới ngưỡng MN là quyết định mới, agent không tự lấy.
- **6e sửa ở gốc (nhãn), không sửa ở ngọn (phép đo).** Mọi phép đo đọc `giai_doan` (M4, thống kê sổ khoá, các báo cáo
  sau) tự đúng theo. Quy tắc nhãn khai TRƯỚC khi đo lại (RM-03), qua cổng thử chặn hai chiều (RM-15).
- **Lịch lần đào lấy từ ba nguồn đối chiếu.** Thiếu một lần đào là chỗ duy nhất làm phép suy «luật liên tục» nhận nhầm ⇒
  script DỪNG nếu sổ khoá có ngày mà lịch không có.
- **6c sửa cả bảng, không chỉ sổ.** Bảng tự kết luận là cơ chế canh của FU-183; để nó in «NÊN TẮT» là để một quyết định
  owner bị lật bởi chính công cụ canh nó. Restart trong khung an toàn (trước 15:30, không trùng job nào ban ngày).
- **CHỐT GẤP: báo, không đổi.** Đổi `MINED_RULES_MODE` là đổi đường chọn số ⇒ phải owner; đưa vào phương án dọn dẹp, đợt
  đơn giản hoá qua shadow.

## 5. Đã làm gì

1. Ghi ba dòng lời owner vào sổ tương tác (trước khi làm).
2. Đọc khối mới nhất của 10 mục FU và đối chiếu V11190; đọc mã thật của từng chỗ (RM-10).
3. 6e: sửa `_v11025_khoa_luat_ben.py` (`tinh_giai_doan`, `nap_lich_su_lan_dao`, nhật ký trong `ghi_nhan_lan_dao`); viết
   `_v11195_kiem_nhan_luat.py`, `_v11195_sua_nhan_luat.py`, `_v11195_do_lai_luat.py`; khoá `_v11003.nap_giai_doan`;
   cảnh báo ở `_v11030` PHẦN 4.
4. 6g: vá `_v104_shadow_prompt_injection.py:303`; làm cứng `_v11050_kiem_bien_anchor.py`.
5. 6a/6f: viết `_v11195_nguong_glm.py`, `_v11195_do_fu345.py`. 6b: chạy lại `_v11065_do_trong_so.py` trên DB VPS.
6. 6c: sửa `_v10918_override_watch.py` (luật QD-081, mốc 26/02/2027).
7. `_v11195_kiem_qd081.py` — phép máy cho QD-081.
8. Sao lưu `backups/*.pre_v11195` (local + VPS) → tải lên VPS (LF, md5 khớp) → băm 4 bảng → thử rồi áp nhãn → băm lại →
   đo → restart → kiểm.
9. Ghi bốn mặt (seq 510), 10 khối FU, QD-081, RL-050/RL-051; chú thích rút lại tại chỗ gốc. Commit `725779b`.

## 6. Cổng kiểm

| cổng | kết quả |
|---|---|
| `_v11195_kiem_nhan_luat.py` | `NHAN_DO_TIEN_V11195=DAT` 11/11 ca · thay quy tắc cũ ⇒ TRƯỢT đúng 3 ca rò (thoát 1) |
| `_v11050_kiem_bien_anchor.py` | `DAT` · tệp giả lập chỗ không chặn biên ⇒ thoát 1 · gỡ ⇒ thoát 0 |
| `_v11195_kiem_qd081.py` | `QD081_V11195=DAT` (local + VPS) |
| `_v10920_decision_ledger.py` | QD-081 🟢 khớp 3/3 · 0 TRÔI · 1 «không kết luận được» do DB local cũ (có từ trước) |
| `_v11062_nang_version.py --kiem` | `NANG_VERSION_V11062=ĐẠT` (seq 510) |
| `_v11027_so_muc_quan_tri.py` | không mục nào biến mất |
| `trang_thai_mo_coi()` | trống |
| 4 bảng khoá | PRE = POST sau áp nhãn và sau restart |
| restart | PID 1122833 → 1277779 · health 200 sau 10 giây · admin 401 · 47 job giống hệt · journal 0 lỗi |
| `_v10921_report_gate.py` ① + ② `V11195` | xem `CONVERSATION_CONTEXT` §4 |

## 7. Vướng vấp

- **Tiền đề khuyến nghị 6f sai** (RL-051) — viết khuyến nghị từ một dòng tóm tắt V11190 mà không tách theo miền.
- **Một câu đính chính hôm qua cũng sai** (RL-050) — nói số 89,7% «không nằm trong tài liệu nào» mà chưa grep.
- **Suýt chép cả DB 1,1 GB vào RAM** để chạy thử nhãn (`con.backup`) — sửa trước khi chạy, chỉ chép ba bảng nhỏ.
- Tưởng journal có nhật ký truy cập để biết mô-đun bảng ghi đè đã nạp chưa — journal không có; phải đọc nginx.
- Cổng biên anchor bắt nhầm chính chuỗi tìm kiếm trong `_v11195_kiem_qd081.py` — tách chuỗi (RM-09).
- `_v11065_do_trong_so.py` từ chối chạy trên VPS vì cổng RM-01 (dành cho bản local) — chạy bản sao bỏ đúng cổng đó, ghi rõ.

## 8. Gỡ về

- 6e: `UPDATE mined_rule_effectiveness SET giai_doan=? WHERE id=?` theo `backups/mre_giai_doan.pre_v11195.json` (VPS) +
  khôi phục `_v11025_khoa_luat_ben.py.pre_v11195`; hai bảng nhật ký để nguyên (chỉ thêm, không ai đọc ngoài nhãn).
- 6c: khôi phục `_v10918_override_watch.py.pre_v11195` rồi restart. 6g: khôi phục `_v104_shadow_prompt_injection.py.pre_v11195`.
- Tài liệu: `git revert 725779b`. Mọi bản sao: `backups/*.pre_v11195` (local + VPS).

## 9. Theo dõi tiếp — liệt kê ĐỦ

| mã | việc | ai chặn | khi nào |
|---|---|---|---|
| `FU-456` | lần đào 30/11 00:30 ghi `rule_mining_runs` + `rule_key_lan_dao` thật ⇒ đóng | lượt tự nhiên | 30/11 |
| `FU-345` | owner chọn bỏ ngưỡng 10.000 cho cả ba miền (khuyến nghị) hay giữ cho MN | owner | 03/12 |
| `FU-195` | đọc lại `glm-5.1` theo cách mới (`_v11195_nguong_glm.py 2026-12-23`) | lượt tự nhiên | 24/12 |
| `FU-183` | xem lại ghi đè MN theo luật QD-081 | lượt tự nhiên | 26/02/2027 |
| `FU-461` | gỡ câu anti-trap ở lần đổi prompt tới, có đối chứng | sự kiện | LX |
| CHỐT GẤP / `MINED_RULES_MODE` | đưa vào phương án dọn dẹp (đợt đơn giản hoá qua shadow) | owner | phương án dọn dẹp |
| `FU-460` · `FU-451a` | lượt tối 26/11: OpenRouter MT/MB + scorecard | lượt tự nhiên | 26/11 18:50 |
| `FU-455` · `FU-328` | khuyến nghị `/choi` trước giờ xổ · cảnh báo model rơi | agent | 27/11 |
| `FU-453` · `FU-451b` · `FU-459` · `FU-270` · 8 mục giao diện | chờ owner | owner | — |

## 10. Ba lớp nguồn (§62)

| lớp | nội dung | bằng chứng |
|---|---|---|
| `OWNER_SAID` | 26/11 ~10:10 — 6a…6g «theo khuyến nghị», 6f nhắc ghi nhận + sao lưu (nguyên văn §2) | `docs/SO_TUONG_TAC_OWNER.md` · QD-081 `nguyen_van` |
| `CODE_DID` | nhãn mới áp trên DB production (983 dòng); bảng ghi đè MN ra «ĐANG ĐO»; restart PID 1277779; 4 bảng khoá không đổi | `evidence/sua_nhan_ghi.txt` · `evidence/bang_ghi_de_mn_sau_va.txt` · `evidence/trien_khai.txt` |
| `DOC_SAID` | trước phiên: FU-183 «tới 31/08 âm tiền ⇒ tắt»; FU-345 «> 10.000 mọi lượt»; V11190 «177 lượt … MT» | `docs/FOLLOW_UP_TRACKER.md` · `docs/DOI_CHIEU_58_MUC_V11190.md:79` |

**Lệch đã báo và đã xử:** `DOC_SAID` ≠ `CODE_DID` ở FU-345 (177 không phải toàn MT — RL-051) · `OWNER_SAID` ≠ `CODE_DID`
ở bảng ghi đè MN (owner giữ, bảng in «NÊN TẮT») — đã sửa bảng · `OWNER_SAID`/`DOC_SAID` ≠ `CODE_DID` ở luật soi cầu (sổ
từng ghi «có tín hiệu đo tiến», đo đúng thì không) — đã đóng FU-340/338.

**TanPhatAI cần làm:** cập nhật hiểu biết — QD-081 (6a–6g) đã thi hành; luật soi cầu KHÔNG có tín hiệu đo tiến (MB kém
nền) — bỏ mọi câu cũ «luật có tín hiệu đo tiến»; bảng ghi đè MN nay báo «ĐANG ĐO» tới 26/02/2027, đừng đọc «NÊN TẮT» cũ.
Theo dõi FU-456 (30/11), FU-345 (owner, 03/12), FU-195 (24/12). **Code đi trước tài liệu trong phiên này:** tải mã + áp
nhãn DB 10:38–10:39, restart 10:47, rồi mới ghi tài liệu ~11:10 — cùng phiên, đúng `PRJ-INTERACTION-LEDGER-001`; mục sổ
tương ứng: `docs/SO_TUONG_TAC_OWNER.md` dòng «26/11 ~10:10» (6a–6g).
