"""
API 调用封装（示例）
用法：
  from api_client_example import call_deepseek
  response = call_deepseek(messages)

配置项从同一目录下的 keys_example.py 读取。
复制 keys_example.py 为 keys.py 并填入真实密钥后即可使用。
"""

import requests

# ⚠ 首次使用：复制 keys_example.py 为 keys.py，填入真实密钥
try:
    from keys import (
        API_SOURCE, OPENCODE_API_KEY, DEEPSEEK_API_KEY,
        THINKING_ENABLED, REASONING_EFFORT,
    )
except ImportError:
    from keys_example import (
        API_SOURCE, OPENCODE_API_KEY, DEEPSEEK_API_KEY,
        THINKING_ENABLED, REASONING_EFFORT,
    )

OPENCODE_BASE_URL = "https://opencode.ai/zen/v1"
DEEPSEEK_BASE_URL = "https://api.deepseek.com/v1"

if API_SOURCE == "opencode":
    BASE_URL = OPENCODE_BASE_URL
    API_KEY = OPENCODE_API_KEY
    MODEL = "deepseek-v4-flash-free"
elif API_SOURCE == "deepseek":
    BASE_URL = DEEPSEEK_BASE_URL
    API_KEY = DEEPSEEK_API_KEY
    MODEL = "deepseek-v4-flash"
else:
    raise ValueError(f"未知 API_SOURCE: {API_SOURCE}，可选: opencode / deepseek")


def call_deepseek(messages, temperature=0.7, max_tokens=2048):
    """调用 API 并返回回复文本"""
    if not API_KEY or "你的" in API_KEY:
        raise ValueError("API_KEY 为空或仍为占位符，请复制 keys_example.py 为 keys.py 并填入真实密钥")

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": MODEL,
        "messages": messages,
        "max_tokens": max_tokens,
    }

    if THINKING_ENABLED == "enabled":
        payload["reasoning_effort"] = REASONING_EFFORT
        payload["thinking"] = {"type": "enabled"}
    else:
        payload["temperature"] = temperature

    resp = requests.post(f"{BASE_URL}/chat/completions", headers=headers,
                         json=payload, timeout=120)
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"]
