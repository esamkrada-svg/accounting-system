from pathlib import Path
from typing import List, Dict, Optional

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DEFAULT_CONTEXT_FILES: List[str] = [
    "AI_DEBUG_RULES.md",
    "AI_REVIEW_GUIDE.md",
    "SYSTEM_MAP.md",
    "ACCOUNTING_RULES.md",
]


def _safe_path(relative_path: str) -> Path:
    """
    ضمان أن المسار داخل المشروع فقط
    """
    full_path = (PROJECT_ROOT / relative_path).resolve()
    if not str(full_path).startswith(str(PROJECT_ROOT)):
        raise ValueError(f"Unsafe path access: {relative_path}")
    return full_path


def read_text(path: Path) -> str:
    if not path.exists():
        return f"[FILE NOT FOUND]: {path}"
    return path.read_text(encoding="utf-8")


def load_context(
    context_files: Optional[List[str]] = None
) -> Dict[str, str]:
    """
    تحميل ملفات السياق المعرفي للنظام (READ-ONLY)
    """
    files = context_files or DEFAULT_CONTEXT_FILES
    context: Dict[str, str] = {}

    for name in files:
        path = _safe_path(name)
        context[name] = read_text(path)

    return context


def load_file(relative_path: str) -> str:
    """
    تحميل أي ملف داخل المشروع بشكل آمن
    """
    path = _safe_path(relative_path)
    return read_text(path)
