# -*- coding: utf-8 -*-
"""V11193 — ghi tài liệu: đánh giá dự đoán 25/11 + OpenRouter chặn gọi model từ VPS (FU-460).

Bốn mặt §63 qua `_v11062_nang_version.ghi()`; sổ theo dõi qua `_doc_prepend.prepend()`.
Lời owner 21:35 đã vào `docs/SO_TUONG_TAC_OWNER.md` trong phiên (append trước khi làm).
Chạy MỘT lần:  python web/backend/_v11193_ghi_tai_lieu.py
"""
from __future__ import annotations

import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))

from _doc_prepend import prepend  # noqa: E402
from _v11062_nang_version import ghi  # noqa: E402

V = "V11193"
NGAY = "2026-11-25"
OWNER = ("*\"phần của anh nhiều vài rút gọn quá chỉ có khuyên của em ko chưa đủ em cần trình bày rõ hơn đi , "
         "kiểm tra đánh giá việc dự đoán hôm nay sao rồi em\"*")

BANG_NGAY = """| miền | /du-doan bạch thủ | /du-doan lô 2 số | /choi (số · khuyến nghị) | model trúng bạch thủ / kỳ vọng ngẫu nhiên |
|---|---|---|---|---|
| MN | `12` trúng 1 nháy · **+2,20tr** | `12 85` trúng cả hai · **+4,40tr** | `12` · CÂN NHẮC · đánh đủ +2,20tr | 6/10 · 4,5 |
| MT | `27` trúng · **+3,10tr** | `27 93` trúng một · **+1,30tr** | `14 27` · CÂN NHẮC · đánh đủ +1,30tr | 7/12 (2 rỗng) · 3,6 |
| MB | `12` trượt · **−1,35tr** | `12 49` trượt cả hai · **−2,70tr** | `12` · CHƠI · −1,35tr | 4/12 (2 rỗng) · 2,9 |
| **cộng** | **+3,95tr** | **+3,00tr** | đánh đủ +2,15tr | |"""

BANG_30 = """| cách chơi (27/10 → 25/11, gộp 3 miền) | lời/lỗ thật | kỳ vọng nếu chọn ngẫu nhiên | z |
|---|---|---|---|
| /du-doan bạch thủ | −23,3tr | −3,8tr | −0,65 |
| /du-doan lô 2 số | −27,0tr | −7,6tr | −0,46 |
| /choi đánh đủ mọi ngày | −37,4tr | −5,2tr | −0,92 |
| /choi theo khuyến nghị ⚠ ghi SAU giờ xổ | +1,2tr | −3,7tr | +0,18 |"""

CHANGELOG = f"""## V11193 — Đánh giá dự đoán 25/11; OpenRouter chặn gọi model từ VPS — `gpt-oss-120b`, `glm-5.1` rỗng cả ngày (25/11/2026)

**Owner nguyên văn (25/11 ~21:35 ICT):** {OWNER}

Phiên **chỉ đọc** trên VPS — không sửa mã service, không deploy, không đụng DB, roster hay cách ly.

### 1. Kết quả 25/11 — `web/backend/_v11193_danh_gia_ngay.py 2026-11-25`
Thước tiền của `/choi` (50 điểm/số/đài, giá 18k MN/MT · 27k MB, trả 98k/điểm). Nền ngẫu nhiên đúng ngày (RM-18):
MN 45% · MT 30% · MB 24% cho một số.

{BANG_NGAY}

Bundle `/du-doan` chốt trước giờ xổ (MN 05:17 · MT 16:37 · MB 17:34). Khuyến nghị `/choi` ghi **18:32 — sau giờ xổ cả
ba miền** (`FU-455`) ⇒ không dùng để đánh giá khuyến nghị.

**Bối cảnh 30 ngày** (`_v11190_so_bang_choi_du_doan.py --tu 2026-10-27 --den 2026-11-25`):

{BANG_30}

Mọi cách chơi có khuyến nghị ghi trước giờ xổ đều **trong vùng may rủi** (|z| < 1). Một ngày lời là **chưa được phép kết
luận** (`RM-04`). Ở MN, 10/10 ngày `/choi` ghi «NGHỈ» thì số đều trượt — dấu hiệu khuyến nghị đã thấy kết quả (`FU-455`).

### 2. OpenRouter chặn gọi model từ VPS (`FU-460`)
- `gpt-oss-120b` và `glm-5.1` **rỗng ở cả 5 lượt** 25/11 (MN 05:16 · MT 16:36/16:37 · MB 17:32/17:32) —
  `PERSISTED_DIAGNOSTIC_EMPTY`. 24/11 chạy đủ 5/5; lượt 200 OK cuối: 24/11 17:31.
- Journal: cả 4 kiểu gọi trả **HTTP 400 `Request path cannot be relayed`** ⇒ bộ ngắt mạch mở 10 phút.
- Gọi thử một lượt ngoài service (`_v11193_thu_openrouter.py`, 21:39): `GET /api/v1/key` **200** (khoá hợp lệ) ·
  `POST chat/completions` tối thiểu **400** sau 0,25 s. Phản hồi có `server: cloudflare` + `cf-ray …-HKG` ⇒ **do chính
  OpenRouter trả** qua máy biên Hồng Kông; service không có biến proxy, `/etc/hosts` không trỏ OpenRouter.
- Mã gọi (`gpt_analyzer._call_openrouter`, `httpx.post` tới URL cố định) không đổi từ 14/09. Báo cáo công khai cùng ngày
  25/11 của người dùng khác (Hồng Kông/Trung Quốc từ 08:27 MYT; một dự án Việt Nam) mô tả đúng hiện tượng
  `/key` 200 · chat 400. **Chưa có xác nhận chính thức** về nguyên nhân (vùng/IP hay sự cố).
- Hậu quả: MT và MB còn **2 model AI sống** (Opus, Gemini) — dưới sàn §59 (AI ≥ 3). MN 26/11: Opus, Sonnet, Gemini = 3.
  Đường dự phòng Gemini 503 → OpenRouter (`GOOGLE_OPENROUTER_FALLBACK`) cũng chết theo.
- **Không cách ly:** dòng rỗng KHÔNG tính vào điểm chọn combo-super (`combo_super.py:342-349` loại dòng rỗng); bộ ngắt
  mạch tự mở lại sau 10 phút ⇒ OpenRouter thông là hai model tự chạy lại. Cách ly tay sẽ mất khả năng tự hồi phục.
- Không ai được báo — cùng họ `FU-328` (cổng model rỗng chưa nối).

### 3. Ứng viên thế chỗ — `_v11193_ung_vien_the_cho.py` (60 ngày hoạt động gần nhất, chênh so với nền đúng ngày)
Cả 7 ứng viên (Opus, Sonnet, Gemini Flash/Pro, DeepSeek, gpt-oss-120b, glm-5.1) **không khác nền** ở mọi miền có đủ
mẫu, trừ Opus MB +16,9 ±11,1 điểm (1/20 phép so — có thể do ngẫu nhiên). Chất lượng không tách được ⇒ theo `QD-080`
mục 9 xét độ tin cậy + tính độc lập: `deepseek-reasoner` gọi thẳng DeepSeek (không qua OpenRouter), hãng thứ ba, đã
nạp 19,94 USD, gọi thử đạt 13:17. Trình owner (`FU-460`) — `QD-080` cũ hơn 30 ngày (§56).

### 4. Đính chính lời agent trong phiên (`PRJ-RETRACTION-001`)
Chỗ gốc: trả lời owner 25/11 ~13:4x, danh sách A việc 6a. Câu sai: *«GLM-5.1 (model chính MT): cổng tự động đòi gỡ vì
độ phủ 89,7% < 90%»*. Đúng: ngưỡng `FU-195` là **tỉ lệ lỗi > 6% trong 14 ngày**; đo 11–24/11 **2/28 = 7,1%**
(`docs/DOI_CHIEU_58_MUC_V11190.md:36`). Quyết định dựa trên số sai: chưa có (owner chưa chốt việc 6a).

**Không đụng:** mã service · `/du-doan` · writer `final_bundles` · roster · cách ly · DB.
"""

SSOT = """## V11193 (25/11/2026 21:5x) — OpenRouter chặn gọi model từ VPS; MT/MB còn 2 AI sống

**Trạng thái hiện tại:**

- **OpenRouter trả 400 `Request path cannot be relayed` cho mọi lệnh gọi model từ VPS từ 25/11 05:15** (khoá vẫn hợp
  lệ, `/key` 200). `gpt-oss-120b`, `glm-5.1` rỗng cả ngày 25/11. Model AI sống: MN 26/11 Opus · Sonnet · Gemini (3) ·
  MT Opus · Gemini (2) · MB Opus · Gemini (2) — MT/MB dưới sàn §59. Chờ owner chốt thay tạm bằng `deepseek-reasoner`
  (`FU-460`). Không cách ly — OpenRouter thông là tự chạy lại.
- 25/11: `/du-doan` bạch thủ +3,95tr · lô 2 số +3,00tr (thước `/choi`). 30 ngày gần nhất mọi cách chơi vẫn trong vùng
  may rủi (|z| < 1).
"""

FU_460 = """### FU-460 · QD2611 · OpenRouter chặn gọi model từ VPS — thay tạm `gpt-oss-120b`/`glm-5.1` bằng DeepSeek? · hạn 26/11

| | |
|---|---|
| **issue_id** | `FU-460` · mã đọc `QD2611` |
| **status** | `OWNER_DECISION_NEEDED` |
| **mở bởi** | `V11193` (25/11/2026) |

Từ 25/11 05:15 OpenRouter trả **HTTP 400 `Request path cannot be relayed`** cho mọi lệnh gọi model từ VPS (khoá hợp lệ:
`GET /api/v1/key` 200; phản hồi có `cf-ray …-HKG` ⇒ do OpenRouter trả, không phải proxy/mã mình). `gpt-oss-120b` và
`glm-5.1` rỗng 5/5 lượt 25/11. MT, MB còn 2 model AI sống (dưới sàn §59).

**Owner chọn:**
- **(A) khuyến nghị** — thay TẠM `deepseek-reasoner` (gọi thẳng DeepSeek) vào chỗ model OpenRouter ở hàng chính
  MN/MT/MB cho tới khi OpenRouter thông; thông lại thì trả roster về như cũ. Trước khi bật: gọi thử prompt thật từng miền.
- **(B)** — chờ OpenRouter tự thông, không đổi gì; MT/MB chạy 2 AI chừng nào còn chặn.

**Không cách ly:** dòng rỗng không vào điểm chọn combo-super; bộ ngắt mạch tự mở lại ⇒ tự hồi phục khi OpenRouter thông.
**Kiểm hằng ngày:** `cd web/backend && ../../venv/bin/python3 _v11193_thu_openrouter.py` (một lượt, không retry) —
`POST_chat_toi_thieu.http` = 200 là đã thông.

**Hạn 26/11:** lượt MT 16:38 ngày 26/11 là lượt kế tiếp chạy 2 AI.

---

"""


def main() -> int:
    ghi(version=V, ngay=NGAY,
        chu_de="Đánh giá dự đoán 25/11; OpenRouter chặn gọi model từ VPS — gpt-oss-120b, glm-5.1 rỗng cả ngày",
        khoi_changelog=CHANGELOG, khoi_ssot=SSOT, theo_doi=["FU-460", "FU-455"], runtime_doi=False,
        them={"bang_chung": "artifacts/v11193/"})
    prepend(os.path.join(REPO, "docs", "FOLLOW_UP_TRACKER.md"), FU_460)
    print("  ✓ FOLLOW_UP (FU-460)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
