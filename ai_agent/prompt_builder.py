def build_debug_prompt(context: dict, code: str, error_log: str | None = None) -> str:
    parts = []
    parts.append("أنت وكيل تصحيح أخطاء (Debug Assistant) لمشروع Python / FastAPI.")
    parts.append("التزم بالقواعد التالية:\n" + context.get("AI_DEBUG_RULES.md", ""))

    parts.append("\nسياق النظام:\n" + context.get("SYSTEM_MAP.md", ""))
    parts.append("\nقواعد محاسبية:\n" + context.get("ACCOUNTING_RULES.md", ""))

    if error_log:
        parts.append("\nسجل الخطأ:\n" + error_log)

    parts.append("\nالكود الهدف:\n" + code)

    parts.append(
        "\nالمطلوب:\n"
        "1) اشرح سبب المشكلة بالعربية.\n"
        "2) اقترح إصلاحًا واحدًا فقط.\n"
        "3) اذكر لماذا الإصلاح آمن.\n"
        "4) لا تقترح إعادة هيكلة كبيرة.\n"
    )
    return "\n".join(parts)
