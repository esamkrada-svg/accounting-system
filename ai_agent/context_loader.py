from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DEFAULT_CONTEXT_FILES = [
    "AI_DEBUG_RULES.md",
    "AI_REVIEW_GUIDE.md",
    "SYSTEM_MAP.md",
    "ACCOUNTING_RULES.md",
]


def read_text(path: Path) -> str:
    if not path.exists():
        return f"[FILE NOT FOUND]: {path}"
    return path.read_text(encoding="utf-8")


def load_context(context_files=None) -> dict:
    files = context_files or DEFAULT_CONTEXT_FILES
    context = {}
    for name in files:
        context[name] = read_text(PROJECT_ROOT / name)
    return context


def load_code(relative_path: str) -> str:
    return read_text(PROJECT_ROOT / relative_path)
