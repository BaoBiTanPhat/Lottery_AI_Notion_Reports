import sys, json, socket, httpx
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, "/root/Lottery_AI_Test/web/backend")
import os; os.chdir("/root/Lottery_AI_Test/web/backend")
import scheduler as S
key = S._get_api_key_for_model("gpt-oss-120b") or ""
h = {"Authorization": "Bearer " + key, "Content-Type": "application/json"}
out = {"dns_openrouter.ai": sorted({a[4][0] for a in socket.getaddrinfo("openrouter.ai", 443)})}
for ten, req in (("GET_/models", lambda: httpx.get("https://openrouter.ai/api/v1/models?limit=1", headers=h, timeout=30)),
                 ("POST_chat", lambda: httpx.post("https://openrouter.ai/api/v1/chat/completions", headers=h, timeout=30,
                      json={"model": "openai/gpt-oss-120b", "max_tokens": 8, "messages": [{"role": "user", "content": "ok"}]}))):
    r = req()
    out[ten] = {"http": r.status_code, "server": r.headers.get("server"), "cf-ray": r.headers.get("cf-ray"),
                "via": r.headers.get("via"), "than": r.text[:120] if r.status_code != 200 else "ok"}
print(json.dumps(out, ensure_ascii=False, indent=1))
