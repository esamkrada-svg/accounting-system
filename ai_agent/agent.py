from pathlib import Path
from typing import Optional, Dict

PROJECT_ROOT = Path(__file__).resolve().parents[1]

CONTEXT_FILES = [
    "AI_DEBUG_RULES.md",
    "AI_REVIEW_GUIDE.md",
    "SYSTEM_MAP.md",
    "ACCOUNTING_RULES.md",
]


def read_file(path: Path) -> str:
    if not path.exists():
        return f"[FILE NOT FOUND]: {path}"
    return path.read_text(encoding="utf-8")


def load_context() -> Dict[str, str]:
    """
    تحميل ملفات السياق المعرفي للنظام (READ-ONLY)
    """
    context = {}
    for file_name in CONTEXT_FILES:
        file_path = PROJECT_ROOT / file_name
        context[file_name] = read_file(file_path)
    return context


def load_code(target: Optional[str]) -> str:
    """
    تحميل كود الهدف (ملف واحد فقط)
    """
    if not target:
        return "[NO TARGET FILE PROVIDED]"

    code_path = PROJECT_ROOT / target
    return read_file(code_path)


def analyze(
    problem: str,
    target_file: Optional[str] = None,
    extra_notes: Optional[str] = None
) -> Dict[str, str]:
    """
    🧠 التحليل الأساسي للمساعد البرمجي
    - لا يعدل الكود
    - لا يكتب ملفات
    - يعيد تحليل + اقتراحات فقط
    """

    context = load_context()
    code = load_code(target_file)

    analysis = {
        "problem": problem,
        "target_file": target_file or "N/A",
        "extra_notes": extra_notes or "",
        "context_files_loaded": list(context.keys()),
        "code_preview": code[:800],
    }

    suggestions = (
        "🔍 Suggested next steps:\n"
        "- Review business rules related to the problem\n"
        "- Verify database state and constraints\n"
        "- Check posting logic and filtering (posted=True)\n"
        "- Run isolated test on the affected module\n"
    )

    return {
        "analysis": str(analysis),
        "suggestions": suggestions
    }
