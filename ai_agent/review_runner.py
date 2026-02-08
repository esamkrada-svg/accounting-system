"""
review_runner.py
----------------
يشغّل مراجعة ذكية للكود بدون أي تعديل تلقائي.
يعتمد على:
- context_loader
- prompt_builder
"""

from ai_agent.context_loader import load_context, load_code
from ai_agent.prompt_builder import build_debug_prompt


def run_review(
    target_code_path: str,
    error_log: str | None = None
) -> str:
    """
    يشغّل مراجعة ذكية على ملف محدد.
    لا يعدل الكود — فقط يولّد Prompt جاهز للإرسال إلى LLM.
    """

    print("🧠 AI Review Runner")
    print("=" * 40)

    # 1) تحميل السياق
    context = load_context()

    # 2) تحميل الكود الهدف
    code = load_code(target_code_path)

    # 3) بناء البرومبت
    prompt = build_debug_prompt(
        context=context,
        code=code,
        error_log=error_log
    )

    print("✅ Review prompt generated successfully.")
    return prompt


# تشغيل يدوي (اختياري – للاختبار فقط)
if __name__ == "__main__":
    prompt = run_review(
        target_code_path="app/main.py",
        error_log=None
    )

    print("\n" + "=" * 40)
    print("📤 PROMPT PREVIEW (first 1500 chars)")
    print("=" * 40)
    print(prompt[:1500])
