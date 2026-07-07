"""
对话规则测试运行器（示例版）
- 每个测试用例 = 一次完整独立的对话
- 每个用例生成 .md 记录文件
- 支持命令行指定测试项: python run_tests_example.py TC1 TC3 TC5

使用方式：
  cd 项目根目录
  pip install requests
  python 双人/测试_example/run_tests_example.py TC3 TC4
"""

import sys
import time
from pathlib import Path

# 允许 import 同目录下的模块
sys.path.insert(0, str(Path(__file__).parent))

# 优先使用运行目录（测试/）下的私密 keys.py（含真实密钥）
sys.path.insert(0, str(Path(__file__).parent.parent / "测试"))

from api_client_example import call_deepseek, MODEL
from 测试用例_example import TEST_CASES

# 注：keys.py 从 测试/ 目录导入（含真实密钥），不存在则用 keys_example.py
try:
    import keys as cfg
except ImportError:
    import keys_example as cfg

PROVIDER_LABEL = {"opencode": "OpenCode Go", "deepseek": "DeepSeek 官方"}.get(cfg.API_SOURCE, cfg.API_SOURCE)

BASE_DIR = Path(__file__).parent
RULES_FILE = BASE_DIR.parent / "双人基础规则.md"
CHARACTER_FILE = BASE_DIR / "角色卡-样例.md"
RECORD_DIR = BASE_DIR / "测试记录"


def get_config_name():
    if cfg.THINKING_ENABLED == "disabled":
        return "关闭思考"
    return f"思考-{cfg.REASONING_EFFORT}"


def load_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


SYSTEM_CONTENT = (
    f"## 规则文件\n\n{load_file(RULES_FILE)}\n\n"
    f"## 角色设定\n\n{load_file(CHARACTER_FILE)}"
)


def get_filtered_cases():
    args = sys.argv[1:]
    if not args:
        return TEST_CASES
    wanted = set(args)
    filtered = [tc for tc in TEST_CASES if tc["id"] in wanted]
    skipped = wanted - {tc["id"] for tc in filtered}
    if skipped:
        print(f"⚠ 未找到匹配的测试项: {', '.join(sorted(skipped))}")
    return filtered


def main():
    cases = get_filtered_cases()
    cfg_dir = RECORD_DIR / get_config_name()
    cfg_dir.mkdir(parents=True, exist_ok=True)
    ts = time.strftime("%Y%m%d_%H%M%S")

    for tc in cases:
        tc_id = tc["id"]
        tc_name = tc["name"]

        messages = [{"role": "system", "content": SYSTEM_CONTENT}]
        for role, content in tc["history"]:
            messages.append({"role": role, "content": content})
        if tc["user_input"]:
            messages.append({"role": "user", "content": tc["user_input"]})

        print(f"\n▶ {tc_id}: {tc_name}")

        try:
            start = time.time()
            response = call_deepseek(messages)
            elapsed = time.time() - start
        except Exception as e:
            print(f"  ❌ API 失败: {e}")
            continue

        print(f"  ✅ {elapsed:.1f}s")
        preview = response[:300].replace("\n", "↵")
        print(f"  预览: {preview}")

        safe_name = f"{ts}_{tc_id}.md"
        record_path = cfg_dir / safe_name

        lines = [
            f"# {tc_id}: {tc_name}\n",
            f"时间: {time.strftime('%Y-%m-%d %H:%M:%S')}\n",
            f"耗时: {elapsed:.1f}s\n",
            f"模型: {MODEL}\n",
            f"提供商: {PROVIDER_LABEL}\n\n",
            "## 对话历史\n\n",
        ]
        for msg in messages:
            label = {"system": "【System】", "user": "【User】", "assistant": "【Assistant】"}.get(msg["role"], msg["role"])
            if msg["role"] == "system":
                lines.append(f"### {label}\n\n`（规则文件 + 角色设定，已省略）`\n\n")
            else:
                lines.append(f"### {label}\n\n```\n{msg['content']}\n```\n\n")

        lines.append("---\n\n## AI 回复\n\n```\n")
        lines.append(response)
        lines.append("\n```\n")

        with open(record_path, "w", encoding="utf-8") as f:
            f.writelines(lines)

        time.sleep(0.5)

    print(f"\n{'='*50}")
    print(f"✅ 完成! 共 {len(cases)} 个独立用例")
    print(f"记录目录: {cfg_dir}")


if __name__ == "__main__":
    main()
