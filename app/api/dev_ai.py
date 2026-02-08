# app/api/dev_ai.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

from ai_agent.agent import AIAgent
from ai_agent.context_loader import load_system_context
from ai_agent.prompt_builder import build_debug_prompt

router = APIRouter(
    prefix="/api/dev/ai",
    tags=["Developer AI Assistant"]
)

# ===============================
# 📥 Schema
# ===============================
class AnalyzeRequest(BaseModel):
    problem: str
    file: Optional[str] = None
    extra_notes: Optional[str] = None


class AnalyzeResponse(BaseModel):
    analysis: str
    suggestions: str


# ===============================
# 🤖 AI Analyze Endpoint
# ===============================
@router.post("/analyze", response_model=AnalyzeResponse)
def analyze_code(request: AnalyzeRequest):
    """
    🧠 مساعد برمجي داخلي:
    - لا يعدّل الكود
    - لا يكتب ملفات
    - يشرح ويقترح فقط
    """

    if not request.problem.strip():
        raise HTTPException(status_code=400, detail="Problem description is required")

    # 1️⃣ تحميل سياق النظام (MD files)
    context = load_system_context()

    # 2️⃣ بناء الـ Prompt
    prompt = build_debug_prompt(
        system_context=context,
        problem=request.problem,
        file=request.file,
        extra_notes=request.extra_notes
    )

    # 3️⃣ تشغيل المساعد
    agent = AIAgent()
    result = agent.run(prompt)

    return {
        "analysis": result.get("analysis", ""),
        "suggestions": result.get("suggestions", "")
    }
