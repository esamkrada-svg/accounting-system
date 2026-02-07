import os
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]

CONTEXT_FILES = [
    "AI_DEBUG_RULES.md",
    "AI_REVIEW_GUIDE.md",
    "SYSTEM_MAP.md",
    "ACCOUNTING_RULES.md",
]

CODE_TARGET = "app/main.py"


def read_file(path: Path) -> str:
    if not path.exists():
        return f"[FILE NOT FOUND]: {path}"
    return path.read_text(encoding="utf-8")


def load_context():
    context = {}
    for file_name in CONTEXT_FILES:
        file_path = PROJECT_ROOT / file_name
        context[file_name] = read_file(file_path)
    return context


def load_code():
    code_path = PROJECT_ROOT / CODE_TARGET
    return read_file(code_path)


def run_agent():
    print("🧠 AI Debug Agent v0.1")
    print("=" * 40)

    context = load_context()
    code = load_code()

    print("\n📚 Loaded Context Files:")
    for name in context:
        print(f"- {name}")

    print("\n📄 Target Code:")
    print(f"- {CODE_TARGET}")

    print("\n--- CONTEXT PREVIEW ---")
    for name, content in context.items():
        print(f"\n### {name} ###")
        print(content[:500])  # preview only

    print("\n--- CODE PREVIEW ---")
    print(code[:800])  # preview only

    print("\n✅ Agent loaded context and code successfully.")
    print("🛑 No code was modified. This is a READ-ONLY analysis.")


if __name__ == "__main__":
    run_agent()
