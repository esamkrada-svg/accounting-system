# app/api/dev_ai_chat.py

from fastapi import APIRouter
from pydantic import BaseModel
from app.core.dev_context import set_last_advice, get_dev_context

router = APIRouter(
    prefix="/api/dev/ai",
    tags=["AI Dev Assistant"]
)


class ChatRequest(BaseModel):
    message: str


@router.post("/chat")
def chat_with_ai(request: ChatRequest):
    """
    دردشة تطوير ذكية (Read-only)
    """
    message = request.message.strip()

    if not message:
        return {
            "status": "error",
            "message": "الرسالة فارغة"
        }

    # هنا لاحقًا سيتم ربط LLM
    response = {
        "reply": (
            "📌 ملاحظة مبدئية:\n"
            "أنا مساعد تطوير للنظام المحاسبي.\n"
            "سأعطيك نصائح أو توجيه معماري بدون تعديل كود.\n\n"
            f"🧠 سؤالك:\n{message}\n\n"
            "✅ المرحلة الحالية: Chat Engine جاهز."
        )
    }

    set_last_advice(response)

    return {
        "status": "ok",
        "response": response,
        "context": get_dev_context()
    }
