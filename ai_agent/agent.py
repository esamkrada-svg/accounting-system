from pathlib import Path
from typing import Optional

from ai_agent.context_loader import load_context, load_code
from ai_agent.prompt_builder import build_debug_prompt


PROJECT_ROOT = Path(__file__).resolve().parents[1]


class DebugAgent:
    """
    🧠 Debug Agent (READ-ONLY)
    - يجمع السياق
    - يبني Prompt
    - لا ينفّذ أي تعديل
    """

    def __init__(self, target_code_path: str):
        self.target_code_path = target_code_path

    def run(self, error_log: Optional[str] = None) -> str:
        """
        تشغيل التحليل وبناء Prompt فقط
        """
        # 1️⃣ تحميل السياق
        context = load_context()

        # 2️⃣ تحميل الكود الهدف
        code = load_code(self.target_code_path)

        # 3️⃣ بناء الـ Prompt
        prompt = build_debug_prompt(
            context=context,
            code=code,
            error_log=error_log
        )

        return prompt


# ===============================
# 🧪 تشغيل يدوي (اختياري)
# ===============================
if __name__ == "__main__":
    agent = DebugAgent("app/main.py")

    prompt = agent.run(
        error_log="Example error: IntegrityError on journal_entries.entry_no"
    )

    print("=" * 80)
    print("🧠 GENERATED DEBUG PROMPT")
    print("=" * 80)
    print(prompt)
