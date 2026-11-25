# -*- coding: utf-8 -*-
"""V11192 — ghi tài liệu: nghiệm thu lượt thật 25/11 (FU-452 MT/MB · FU-451a) + sửa nhãn mồ côi FU-452.

Bốn mặt §63 qua `_v11062_nang_version.ghi()`; sổ theo dõi qua `_doc_prepend.prepend()`.
Không có lời owner mới trong phiên này (dòng 13:37 đã vào sổ ở commit 3cd9943) ⇒ không ghi sổ tương tác.
Chạy MỘT lần:  python web/backend/_v11192_ghi_tai_lieu.py
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

V = "V11192"
NGAY = "2026-11-25"

BANG_CLAUDE = """| giờ tạo (VN) | miền | model | đường | số ra | lỗi |
|---|---|---|---|---|---|
| 16:36 | MT | `claude-opus-4-6` | `ai_chain` | `["98", "24"]` | không |
| 17:31 | MB | `claude-opus-4-6` | `ai_chain` | `["49"]` | không |"""

BANG_MIEN = """| miền | model AI có dòng `predictions` 25/11 | ghi chú |
|---|---|---|
| MN | 2 — `gemini-2.5-flash` · `gpt-oss-120b` | **đúng dự kiến**: lượt MN 05:15 chạy TRƯỚC lúc nhả cách ly (13:17) |
| MT | 4 — `claude-opus-4-6` · `gemini-2.5-flash` · `glm-5.1` · `gpt-oss-120b` | đúng roster `QD-080` |
| MB | 4 — `claude-opus-4-6` · `gemini-2.5-flash` · `glm-5.1` · `gpt-oss-120b` | đúng roster `QD-080` |"""

BANG_451 = """| nguồn | MN | MT | MB |
|---|---|---|---|
| `scheduler_logs` (UTC → +7) | 16:34 `inserted=27` | 17:30 `inserted=27` | 18:32 `inserted=27` |
| journal `lottery` | 16:34:57 | 17:30:23 | 18:32:55 |"""

CHANGELOG = f"""## V11192 — Nghiệm thu lượt thật 25/11: Opus chạy lại ở MT/MB · vá stdout FU-451a đạt · sửa nhãn mồ côi FU-452 (25/11/2026)

Phiên **chỉ đọc** trên VPS — không sửa mã, không deploy, không đụng DB. Bài kiểm hẹn sẵn ở V11191
(`web/backend/_v11191_kiem_luot_that.py 2026-11-25`) chạy lúc **18:45** VN; thoát `0`.

### 1. FU-452 — Claude chạy lại thật sau khi owner nạp tiền

{BANG_CLAUDE}

{BANG_MIEN}

Cách ly còn đúng `gpt-5-mini`, `gpt-5.4` (OpenAI chưa nạp) — **không model Claude nào bị cách ly lại**.

⇒ **`RUNTIME_PROVEN` cho MT và MB.** MN chờ lượt `auto_daily` 05:15 sáng **26/11** (Opus + Sonnet).

Kết quả xổ (`PARTIAL` ở MT, `LOSE` ở MB) **không thuộc phép nghiệm thu** — một ngày một model là
**chưa được phép kết luận** về chất lượng (`RM-04`).

### 2. FU-451a — vá stdout service chết (V11189)

{BANG_451}

`closed file` từ 04:30 VN: **0** trong `scheduler_logs`, **0** trong journal. Journal có lại dòng
`print()` (6.689 dòng từ 04:30). PID `1122833` không đổi.

⇒ **FU-451 phần (a) `RUNTIME_PROVEN`.** Phần (b) — tính bù bảng xét thăng hạng 14/09→24/11 — vẫn chờ owner.

### 3. Tự sửa lỗi của V11191 — FU-452 rơi thành «mồ côi»

V11191 ghi khối FU-452 với `status = DEPLOYED`. Nhãn này **không có** trong `TREO_STATUSES` lẫn
`DONG_STATUSES` của `web/backend/_v10958_fu_reader.py` ⇒ `trang_thai_mo_coi()` xếp FU-452 **mồ côi**,
rơi khỏi mọi bộ đếm việc treo — đúng họ lỗi V10980 / FU-430. Cổng commit chỉ cảnh báo, không chặn, nên lọt.

**Sửa:** khối FU-452 mới trên cùng sổ theo dõi, nhãn `DEPLOYED_PENDING_LIVE_VERIFY` (đã khai, nhóm TREO) —
đúng thực tế: MT/MB đã chạy thật, MN còn chờ. Khối cũ giữ nguyên (sổ chỉ thêm khối mới phía trên).

**Kiểm:** `load_fu_latest()` đọc FU-452 = `DEPLOYED_PENDING_LIVE_VERIFY`; `trang_thai_mo_coi()` không còn FU-452.

### 4. Tầng verdict (RM-12)

FU-451a **`RUNTIME_PROVEN`** · FU-452 **`RUNTIME_PROVEN` MT/MB**, MN chờ 26/11 · phần DeepSeek
`OWNER_DECISION_NEEDED` (19,94 USD còn nguyên, ngoài roster).

**Không đụng:** mã service · `/du-doan` · writer `final_bundles` · roster · cách ly · DB.
"""

SSOT = """## V11192 (25/11/2026 18:45) — Opus đã chạy thật ở MT/MB; vá stdout FU-451a đạt

**Trạng thái hiện tại:**

- `claude-opus-4-6` ra số thật, không lỗi: MT 16:36 · MB 17:31 (`ai_chain`). MT/MB mỗi miền **4 model AI**
  đúng roster `QD-080`. MN hôm nay còn 2 vì lượt 05:15 chạy trước lúc nhả cách ly — chờ 05:15 ngày **26/11**.
- Cách ly còn `gpt-5.4`, `gpt-5-mini` (OpenAI, ngoài roster).
- Sổ điểm xét thăng hạng (`SHADOW-PROMOTION-SCORECARD`) ghi lại đủ 3 miền từ 25/11 (`inserted=27` mỗi miền);
  service không còn `closed file`; journal có lại `print()`. Khoảng trống 14/09→24/11 chờ owner (FU-451b).
- FU-452 hết «mồ côi» (nhãn V11191 nằm ngoài từ vựng bộ đọc) — nay `DEPLOYED_PENDING_LIVE_VERIFY`.
"""

FU_452 = """### FU-452 · QD2411 · Claude chạy lại sau nạp tiền — MT/MB đạt lượt thật, MN chờ 26/11 · hạn 26/11

| | |
|---|---|
| **issue_id** | `FU-452` · mã đọc `QD2411` |
| **status** | `DEPLOYED_PENDING_LIVE_VERIFY` — MT/MB `RUNTIME_PROVEN` 25/11 · MN chờ 26/11 05:15 · phần DeepSeek chờ owner |
| **cập nhật bởi** | `V11192` (thay nhãn `DEPLOYED` của V11191 — nhãn đó ngoài từ vựng `_v10958_fu_reader` ⇒ mồ côi) |

**Lượt thật 25/11** (`_v11191_kiem_luot_that.py`, VPS 18:45, thoát 0): `claude-opus-4-6` MT 16:36 `["98", "24"]` ·
MB 17:31 `["49"]` — có số, không `PERSISTED_DIAGNOSTIC_EMPTY`. MT/MB đủ 4 model AI. Không Claude nào bị cách ly lại.

**Còn lại để đóng:** lượt MN `auto_daily` 05:15 ngày 26/11 phải có dòng `claude-opus-4-6` **và**
`claude-sonnet-4-6` có số ⇒ MN đủ 4 model AI. Lệnh: `venv/bin/python3 web/backend/_v11191_kiem_luot_that.py 2026-11-26`.

**Còn chờ owner:** DeepSeek (19,94 USD, `DENY_OUTSIDE_ROSTER` mọi lớp). Khuyến nghị: giữ làm dự phòng, thay vào
`gpt-oss-120b`/`glm-5.1` khi số dư OpenRouter (6,29 USD) gần cạn — không đổi roster lúc Opus vừa về.

---

"""

FU_451 = """### FU-451 · SC2511 · Vá stdout service chết — (a) ĐẠT lượt thật 25/11 · (b) chờ owner tính bù · hạn LX

| | |
|---|---|
| **issue_id** | `FU-451` · mã đọc `SC2511` |
| **status** | `OWNER_DECISION_NEEDED` — phần (a) `RUNTIME_PROVEN` 25/11 · còn phần (b) |
| **cập nhật bởi** | `V11192` |

(a) **Đạt.** `scheduler_logs`: `SHADOW-PROMOTION-SCORECARD` MN 16:34 · MT 17:30 · MB 18:32 VN, mỗi miền `inserted=27`.
`closed file` từ 04:30: 0 (cả `scheduler_logs` lẫn journal). Journal có lại `print()` — 6.689 dòng từ 04:30. PID
`1122833` không đổi.

(b) **Chờ owner:** bảng trống 14/09→24/11 (72 ngày) — tính bù measurement-only bằng `backfill()` sẵn có, hay để trống
kèm ghi chú. Khuyến nghị: tính bù. Làn shadow bị chặn có chủ ý từ 14/09 nên phần bù chỉ có dòng OUTPUT.

---

"""


def main() -> int:
    ghi(version=V, ngay=NGAY,
        chu_de="Nghiệm thu lượt thật 25/11: Opus chạy lại MT/MB · vá stdout FU-451a đạt · sửa nhãn mồ côi FU-452",
        khoi_changelog=CHANGELOG, khoi_ssot=SSOT, theo_doi=["FU-451", "FU-452"], runtime_doi=False,
        them={"bang_chung": "artifacts/v11192/kiem_luot_that_1845.txt",
              "journal": "artifacts/v11192/journal_1848.txt"})
    tracker = os.path.join(REPO, "docs", "FOLLOW_UP_TRACKER.md")
    prepend(tracker, FU_451)
    prepend(tracker, FU_452)
    print("  ✓ FOLLOW_UP (FU-452 trên cùng · FU-451)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
