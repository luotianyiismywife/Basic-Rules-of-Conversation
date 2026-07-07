"""
API 配置模板 — 复制为 keys.py 并填入真实密钥
keys.py 已在 .gitignore 中排除，不会上传到仓库。
"""

# ── API 密钥 ──────────────────────────────────────
# 根据 API_SOURCE 选择，只需要填对应的那个

# OpenCode Go 密钥（免费）：https://opencode.ai
OPENCODE_API_KEY = "sk-你的OpenCode密钥"

# DeepSeek 官方密钥（付费）：https://platform.deepseek.com
DEEPSEEK_API_KEY = "sk-你的DeepSeek密钥"


# ── API 源选择 ────────────────────────────────────
# "opencode"  → OpenCode Go 免费接口
#               - 模型: deepseek-v4-flash-free
#               - 不支持思考模式
#               - 适合快速测试
#
# "deepseek"  → DeepSeek 官方 API
#               - 模型: deepseek-v4-flash
#               - 支持思考模式（reasoning_effort）
#               - 需付费
API_SOURCE = "opencode"


# ── 思考配置（仅 DeepSeek 官方支持）────────────────
# OpenCode 模式下此配置无效，强制关闭思考
THINKING_ENABLED = "disabled"   # "enabled" / "disabled"
REASONING_EFFORT = "high"       # "high" / "max"


# ── 角色设定文件 ──────────────────────────────────
# 文件名相对于 角色数据/ 目录
CHARACTER = "你的角色卡.md"  # 角色数据/下任意角色文件
