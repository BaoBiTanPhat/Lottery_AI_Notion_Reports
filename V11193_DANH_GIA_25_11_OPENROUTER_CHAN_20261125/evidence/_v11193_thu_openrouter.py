# -*- coding: utf-8 -*-
"""V11193 — gọi thử OpenRouter MỘT lượt, ngoài service, để biết lỗi 400 «Request path cannot be relayed»
nằm ở phía nào. Không retry. Không in khoá (chỉ sha8).

Khoá lấy đúng đường production: `scheduler._get_api_key_for_model` (DB trước, `.env` sau).
Chạy TRÊN VPS trong web/backend:  ../../venv/bin/python3 _v11193_thu_openrouter.py
"""
import hashlib
import json
import sys
import time

sys.stdout.reconfigure(encoding="utf-8")
import httpx  # noqa: E402

import scheduler as S  # noqa: E402  (import không khởi động lịch: _scheduler = None)

URL = "https://openrouter.ai/api/v1/chat/completions"
HEAD = {"Content-Type": "application/json", "HTTP-Referer": "https://xs.io.vn", "X-Title": "Lottery AI"}


def main():
    out = {"luc": time.strftime("%Y-%m-%d %H:%M:%S")}
    key = S._get_api_key_for_model("gpt-oss-120b") or ""
    out["khoa_sha8"] = hashlib.sha256(key.encode()).hexdigest()[:8] if key else None
    h = dict(HEAD, Authorization="Bearer " + key)
    r = httpx.get("https://openrouter.ai/api/v1/key", headers=h, timeout=30)
    out["GET_/key"] = {"http": r.status_code, "than": r.text[:160] if r.status_code != 200 else "ok"}
    if r.status_code == 200:
        d = r.json().get("data", {})
        out["GET_/key"]["limit_remaining"] = d.get("limit_remaining")
        out["GET_/key"]["usage"] = d.get("usage")
    body = {"model": "openai/gpt-oss-120b", "max_tokens": 16,
            "messages": [{"role": "user", "content": "Reply with the single word: ok"}]}
    t = time.time()
    r = httpx.post(URL, json=body, headers=h, timeout=60)
    out["POST_chat_toi_thieu"] = {"http": r.status_code, "giay": round(time.time() - t, 2), "than": r.text[:220]}
    print(json.dumps(out, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
