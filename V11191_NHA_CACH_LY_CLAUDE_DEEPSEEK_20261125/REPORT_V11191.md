# V11191 — Owner nạp Anthropic + DeepSeek: gọi thử đạt cả 4 model, nhả cách ly; Opus về lại hàng chính 3 miền; DeepSeek vẫn chưa được gọi vì ngoài roster

**Ngày:** 25/11/2026 · **Commit riêng:** `7ff3b31` (`Lottery_AI_Test`, nhánh `fu438/admin-only-p0a` = `master`) ·
**Tầng:** nhả cách ly `DEPLOYED` (trạng thái runtime trên VPS, không sửa mã service, không restart) ·
`RUNTIME_PROVEN` **chờ lượt thật** MT ~16:38 · MB ~17:31 (25/11) · MN 05:15 (26/11) · nối tiếp `V11190`

---

## 1. Tóm tắt

- Owner báo đã nạp tiền **Anthropic** và **DeepSeek**. Đây là trả lời việc 1 trong danh sách chốt sáng nay
  (`FU-452`): chọn **(a) nạp Anthropic**, không chuyển Claude sang OpenRouter.
- **Kiểm trước:** số dư DeepSeek qua cổng tra miễn phí là **19,94 USD** (24/11: −0,05). Anthropic không có cổng tra
  số dư, nên chứng minh bằng một lượt gọi thật.
- **Gọi thử đúng đường production, mỗi model đúng một lượt, không retry:** `claude-opus-4-6`, `claude-sonnet-4-6`,
  `deepseek-reasoner`, `deepseek-v4-pro-real` — **cả 4 đạt** ⇒ nhả cách ly kèm bằng chứng. Hai model OpenAI
  (`gpt-5.4`, `gpt-5-mini`) **giữ cách ly** vì OpenAI chưa nạp.
- **Kết quả:** roster gọi tự về đúng bản owner duyệt (`QD-080`) — Opus ở **hàng chính cả 3 miền**, Sonnet **dự bị
  MN**. MN hết thủng sàn §59: model AI sống **2 → 4**. Không sửa mã, không restart (PID `1122833` giữ nguyên).
- **Phát hiện:** DeepSeek **có tiền nhưng vẫn không được gọi** — roster từ 14/09 không còn DeepSeek ở miền nào, và
  mỗi miền đã đủ trần 4. Đưa DeepSeek vào nghĩa là **thay** một model đang có ⇒ trình owner.

## 2. Owner yêu cầu gì (nguyên văn) — §62 lớp `OWNER_SAID`

| giờ (ICT) | nguyên văn | loại |
|---|---|---|
| 25/11 ~13:12 | *"deepseek và claude athopic anh đã nạp tiền rồi ah em"* | XÁC_NHẬN |

Ngữ cảnh: tin nhắn ngay trước đó của agent (25/11 ~11:58) là danh sách chốt ba phần; việc 1 phía owner là *«Nạp
tiền để Claude chạy lại … (a) nạp tiền tài khoản Anthropic · (b) chuyển Claude sang gọi qua OpenRouter — em khuyên
(a)»*. Trong cùng danh sách agent đã ghi *«OpenAI và DeepSeek không cần nạp: hiện không model nào của hai hãng này
nằm trong danh sách đang được gọi»* — owner vẫn nạp DeepSeek; xem mục 3.4.

Phiên không có yêu cầu trực tiếp nào khác.

## 3. Đào bới / phát hiện — liệt kê ĐỦ

### 3.1 Trạng thái cách ly trước khi làm (`data/provider_quarantine.json` trên VPS, đọc 13:1x)

| model | từ lúc | lỗi nguyên văn (rút gọn) |
|---|---|---|
| `claude-opus-4-6` | 11/11 16:36 | 400 *«Your credit balance is too low to access the Anthropic API»* |
| `claude-sonnet-4-6` | 12/11 05:15 | như trên |
| `deepseek-reasoner` | 13/09 21:29 | 402 *«Insufficient Balance»* |
| `deepseek-v4-pro-real` | 13/09 21:29 | 402 *«Insufficient Balance»* |
| `gpt-5.4` | 13/09 21:29 | 429 *«You have no credits remaining»* |
| `gpt-5-mini` | 13/09 21:29 | 429 *«You have no credits remaining»* |

### 3.2 Đường gọi và khoá thật (RM-13 — chứng minh nguồn là production)

- Khoá production lấy ở `scheduler._get_api_key_for_model` theo thứ tự **DB per-model → env per-model → DB chung →
  env chung** — không phải đọc thẳng `.env`. Bài gọi thử dùng **đúng hàm này**.
- Gọi: `gpt_analyzer._call_anthropic` (qua `ANTHROPIC_MODEL_API_MAP`) và `_call_deepseek` (qua `DEEPSEEK_API_ROUTE`:
  `deepseek-reasoner → deepseek-v4-flash`, `deepseek-v4-pro-real → deepseek-v4-pro`, cả hai thinking) — y như nhánh
  `is_claude` / `is_deepseek` của `_invoke_model_api`.
- Import `scheduler` không tự khởi động lịch (`_scheduler = None` tới khi có lệnh start — kiểm trước khi chạy).

### 3.3 Nhả cách ly có hiệu lực ngay, không cần restart

`_CL.kiem(selected_model)` (`gpt_analyzer.py:6835-6843`) và `_doc_cach_ly()` của roster
(`_v11185_roster_goi_token.py:220, 310, 435`) đều **đọc lại tệp** mỗi lượt gọi. Đã kiểm bằng máy: ngay sau khi nhả,
`get_token_call_roster` trả roster mới (mục 5).

### 3.4 DeepSeek có tiền nhưng KHÔNG được gọi — chạy thẳng cổng uỷ quyền cuối

Lịch sử (`predictions`, đo trên DB VPS): trước 13/09 `deepseek-reasoner` chạy **official** (`ai_chain` 26–62 dòng/tháng
+ `auto_daily` 13–31 dòng/tháng), `deepseek-v4-pro-real` chạy **shadow** (`shadow_auto_eval` 39–91 dòng/tháng). Lượt
cuối 13/09 17:41, đều lỗi 402.

Từ 14/09 roster `QD-080` thu về 4 model/miền và **không giữ DeepSeek**. Cổng `uy_quyen_goi` áp **cùng một roster**
cho mọi lớp thực thi trừ `maintenance`. Chạy thẳng sau khi nhả (`evidence/uy_quyen_sau_nha.txt`):

| model | miền | lớp | kết quả |
|---|---|---|---|
| `claude-opus-4-6` | MN · MT · MB | official | `ALLOW` |
| `claude-opus-4-6` | MT | combo_super | `ALLOW` |
| `claude-sonnet-4-6` | MN | official | `ALLOW` |
| `claude-sonnet-4-6` | MT | official | `DENY_OUTSIDE_ROSTER` (chỉ là dự bị MN) |
| `deepseek-reasoner` | MN / MT | official / combo_super | **`DENY_OUTSIDE_ROSTER`** |
| `deepseek-v4-pro-real` | MT / MB | shadow | **`DENY_OUTSIDE_ROSTER`** |
| `gpt-5.4` | MB | official | `DENY_QUARANTINED` |

⇒ Nạp DeepSeek **chưa có tác dụng** cho tới khi DeepSeek được đưa vào roster.

### 3.5 Lệch tài liệu/mã — `DOC_SAID ≠ CODE_DID` (bắt buộc báo theo §62)

`_v11184_cach_ly_provider.py:20-21` ghi *«Chỉ mở lại bằng BẰNG CHỨNG SỨC KHOẺ, và mở ra hàng CHALLENGER, KHÔNG trả
thẳng về CORE (khoá §Z E5)»*, dòng 160 đặt `e["tra_ve_hang"] = "CHALLENGER"`.

- **CODE_DID:** `grep tra_ve_hang` trên VPS — **không mã nào đọc trường này** ngoài chính mô-đun. Roster đưa model về
  đúng hàng đã duyệt.
- **OWNER_SAID:** nguyên văn `QD-080` mục 6 (owner 13/09 20:44) — *«lỗi auth, billing, circuit-open hoặc model
  unavailable được cách ly ngay và không tính vào giới hạn thay đổi hiệu năng»*. Tìm «E5» trong sổ quyết định, sổ
  tương tác và báo cáo V11184–V11186: **không có nguyên văn owner nào** đòi nhả về hàng dự bị.
- **Kết luận:** câu chú thích là thiết kế của agent V11184, chưa từng được thi hành và không có lời owner đứng sau.
  Hết tiền không phải giáng hạng vì hiệu năng ⇒ Opus về lại hàng chính là đúng `QD-080`. **Không sửa mã** trong phiên.

### 3.6 Lượt production thật đầu tiên sẽ ở đâu

Ngày bình thường 09–10/11 (`evidence/lich_su_deepseek_claude.txt`): Opus + Sonnet MN **05:15** (`auto_daily`), Opus
MT **16:38–16:40** và MB **17:31** (`ai_chain`). Nhả lúc 13:17 ⇒ lượt thật đầu tiên là **MT chiều nay**.

## 4. Hướng xử lý và vì sao chọn

| chọn | vì sao |
|---|---|
| Gọi thử **trước**, nhả **sau** | Lệnh owner 13/09: không gọi khi lỗi tiền còn tồn tại; `giai_phong` từ chối nếu thiếu bằng chứng |
| Mỗi model **một lượt**, không retry | Cùng lệnh 13/09; hỏng thì giữ cách ly, không thử lại |
| Đi **đúng đường production** (khoá từ DB, hàm gọi thật) | RM-13/RM-14 — gọi thử bằng khoá `.env` có thể đạt trong khi khoá DB đang dùng vẫn hỏng |
| Không đụng OpenAI | Owner không nạp OpenAI; không model OpenAI nào trong roster |
| Không tự đưa DeepSeek vào roster | Trần 4/miền đã đủ ⇒ phải **thay** một model — là quyết định hiệu năng, chờ owner; và vừa đổi một biến (Opus quay lại) thì không đổi thêm (`QD-018`) |
| Không sửa chú thích §Z E5 | Không ảnh hưởng hành vi; sửa mô-đun đang nạp trong service cần deploy riêng |

## 5. Đã làm gì

**TRƯỚC / SAU / PHIÊN BẢN / KIỂM (§60.4):**

| | TRƯỚC | SAU |
|---|---|---|
| cách ly | 6 model | `gpt-5.4`, `gpt-5-mini` |
| roster MN | chính `gemini-2.5-flash` · `gpt-oss-120b` · dự bị — | chính **`claude-opus-4-6`** · `gemini-2.5-flash` · `gpt-oss-120b` · dự bị **`claude-sonnet-4-6`** |
| roster MT | chính `gemini-2.5-flash` · `glm-5.1` · dự bị `gpt-oss-120b` | chính **`claude-opus-4-6`** · `gemini-2.5-flash` · `glm-5.1` · dự bị `gpt-oss-120b` |
| roster MB | chính `gemini-2.5-flash` · `gpt-oss-120b` · dự bị `glm-5.1` | chính **`claude-opus-4-6`** · `gemini-2.5-flash` · `gpt-oss-120b` · dự bị `glm-5.1` |

**PHIÊN BẢN:** V11191, 25/11/2026 13:17 ICT. **KIỂM:** `_v11191_thu_suc_khoe_provider.py` in roster trước/sau;
`evidence/uy_quyen_sau_nha.txt`.

Gọi thử (`evidence/thu_suc_khoe_nha.json` — không chứa khoá, chỉ `sha256[:8]` của khoá):

| model | đường gọi thật | kết quả | độ trễ | tokens |
|---|---|---|---|---|
| `claude-opus-4-6` | Anthropic trực tiếp | **ĐẠT** — trả `{"ok": 1}` | 2,03 s | 104 |
| `claude-sonnet-4-6` | Anthropic trực tiếp | **ĐẠT** | 1,33 s | 104 |
| `deepseek-reasoner` | DeepSeek → `deepseek-v4-flash` (thinking) | **ĐẠT** | 1,53 s | 142 |
| `deepseek-v4-pro-real` | DeepSeek → `deepseek-v4-pro` (thinking) | **ĐẠT** | 1,47 s | 176 |

Các bước:

1. Sao lưu `data/provider_quarantine.json` → `/root/backups/v11191_pre/` (sha khớp `5b4f0f49…`).
2. Đặt `_v11191_thu_suc_khoe_provider.py` vào `web/backend` trên VPS (công cụ chạy tay, service không nạp).
3. Chạy một lần với `--nha` lúc 13:17 — ngoài khung cấm (05:00–06:30, 15:30–18:15).
4. Tài liệu: `CHANGELOG.md` · `docs/CURRENT_TRUTH_SSOT.md` · `docs/AUTOMATION_STATE.json` (seq **506**) ·
   `docs/AUTOMATION_HISTORY.jsonl` · `docs/FOLLOW_UP_TRACKER.md` (`FU-452`) · `docs/DECISION_LOG.md` ·
   `docs/SO_TUONG_TAC_OWNER.md`.
5. Commit `7ff3b31`, push nhánh + `master`.

**Không đụng:** mã service · `/du-doan` · writer `final_bundles` · roster (`_CHINH_SACH`) · DB · hash 4 bảng khoá
(không ghi gì vào DB).

## 6. Cổng kiểm

| cổng | kết quả |
|---|---|
| `_v11044_cong_so_hieu.py` | V11191 trống trước khi dùng; `SO_HIEU_V11044=KHOP` |
| `_v11062_nang_version.py --kiem` | `NANG_VERSION_V11062=ĐẠT` — bốn mặt đi cùng nhau |
| `_v10920_decision_ledger.py` | 0 `TRÔI`; 1 phép «không kết luận được» do DB local cũ (RM-01) — giữ nguyên từ V11190 |
| hook commit Claude Code (`.claude/hooks/cong_git_commit.py`) | qua — commit `7ff3b31` |
| `giai_phong` | nhận đủ 4 bằng chứng; không lượt nào bị từ chối |
| quét khoá trong `evidence/` | không có chuỗi khoá |
| `_v10921_report_gate.py` ① toàn dải + ② `V11191` | chạy sau khi đẩy báo cáo này — kết quả ghi ở commit dấu vết I2 |

## 7. Vướng vấp

1. **Giờ sai suýt vào sổ.** Lệnh `TZ=Asia/Ho_Chi_Minh date` trong Git Bash trên Windows **âm thầm trả giờ UTC**
   (06:13 thay vì 13:13). Bắt được vì nó mâu thuẫn với dòng sổ 25/11 ~11:58; đối chiếu bằng `date` không tham số
   và đồng hồ PowerShell. Nhiều khả năng đây là gốc của các mốc giờ lệch 7 tiếng đã phải sửa ở V11190.
2. Truy vấn SQL viết lồng trong `ssh '…'` hỏng vì nháy đơn của `COALESCE(x,'')` — chuyển sang tệp script.
3. Suýt kết luận «nhả là về hàng dự bị» theo chú thích mô-đun — kiểm `grep tra_ve_hang` và nguyên văn owner trước
   (mục 3.5).

## 8. Gỡ về

```bash
ssh root@<VPS> 'cp -p /root/backups/v11191_pre/provider_quarantine.json /root/Lottery_AI_Test/data/provider_quarantine.json'
```

Không cần restart — tệp được đọc lại mỗi lượt gọi. Gỡ về sẽ chặn lại cả 4 model.

## 9. Theo dõi tiếp — liệt kê ĐỦ

| mục | việc | ai chặn | khi nào |
|---|---|---|---|
| `FU-452` | `RUNTIME_PROVEN`: dòng `predictions` của Opus có số, không `PERSISTED_DIAGNOSTIC_EMPTY` | agent kiểm | MT ~16:40 · MB ~17:35 hôm nay |
| `FU-452` | MN có Opus + Sonnet, đủ 4 model AI | agent kiểm | 26/11 sau 05:20 |
| `FU-452` | DeepSeek có đưa vào roster không (phải thay một model; khuyến nghị chưa, xét sau 7 ngày) | **owner** | — |
| `FU-451a` | bảng xét thăng hạng ghi dòng mới cả 3 miền, 0 lỗi «closed file» | agent kiểm | hôm nay sau 18:35 |
| `FU-455` | lưu khuyến nghị `/choi` trước giờ xổ | agent | hạn 27/11 |
| `FU-453` · `FU-451b` · `FU-459` · `FU-270` · `FU-195` · `FU-340/338/456` · `FU-397` · `FU-400` · `FU-183` | 9 việc còn lại của bản trình 24/11 ~23:44 | **owner** | — |
| `FU-457` · `FU-458` · `FU-328` · `FU-292` · `FU-318` · `FU-204` | việc agent tự xử (danh sách B sáng nay) | agent | 27–28/11 |
| — | OpenAI vẫn hết tiền; không model OpenAI nào trong roster ⇒ **không cần nạp** | — | — |

## 10. Ba lớp nguồn (§62)

| lớp | nội dung | bằng chứng |
|---|---|---|
| `OWNER_SAID` | *"deepseek và claude athopic anh đã nạp tiền rồi ah em"* (25/11 ~13:12) | `docs/SO_TUONG_TAC_OWNER.md` dòng 25/11 ~13:12 |
| `CODE_DID` | 4 lượt gọi thật đạt; `giai_phong` nhả 4 model; roster có Opus 3 miền; DeepSeek `DENY_OUTSIDE_ROSTER` | `evidence/thu_suc_khoe_nha.json` · `evidence/uy_quyen_sau_nha.txt` |
| `DOC_SAID` | `FU-452` · `DECISION_LOG` 25/11 ~13:12 · SSOT V11191 | `docs/FOLLOW_UP_TRACKER.md` khối «FU-452 (CẬP NHẬT 25/11 13:17…)» |

**Lệch đã báo:** `DOC_SAID` (`_v11184_cach_ly_provider.py:20-21,160` «nhả về CHALLENGER, khoá §Z E5») ≠ `CODE_DID`
(không mã nào đọc `tra_ve_hang`) — và không có `OWNER_SAID` tương ứng (mục 3.5).

**TanPhatAI cần làm:** cập nhật hiểu biết — Claude (`claude-opus-4-6` hàng chính 3 miền, `claude-sonnet-4-6` dự bị
MN) **chạy lại từ 25/11 13:17**, cách ly chỉ còn `gpt-5.4`/`gpt-5-mini`; **DeepSeek có tiền nhưng ngoài roster nên
không được gọi** (`FU-452`, chờ owner). Không có code đi trước tài liệu trong phiên này — thay đổi là trạng thái
runtime, đã ghi đủ ở `FU-452` và sổ tương tác dòng 25/11 ~13:12. Theo dõi kết quả `RUNTIME_PROVEN` ở báo cáo kế.
