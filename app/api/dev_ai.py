# app/api/dev_ai.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

from ai_agent.agent import DebugAgent

router = APIRouter(
    prefix="/api/dev/ai",
    tags=["Developer AI Assistant"]
)

# ===============================
# 📥 Schemas
# ===============================
class AnalyzeRequest(BaseModel):
    error_log: str
    target_file: Optional[str] = "app/main.py"


class AnalyzeResponse(BaseModel):
    prompt: str


# ===============================
# 🤖 Debug Analyze Endpoint (READ-ONLY)
# ===============================
@router.post("/analyze", response_model=AnalyzeResponse)
def analyze_code(request: AnalyzeRequest):
    """
    🧠 مساعد برمجي داخلي (READ-ONLY)

    - لا يعدّل الكود
    - لا يكتب ملفات
    - لا ينفّذ أي أوامر
    - يبني Debug Prompt فقط
    """

    if not request.error_log.strip():
        raise HTTPException(
            status_code=400,
            detail="error_log is required"
        )

    # 1️⃣ إنشاء الوكيل
    agent = DebugAgent(
        target_code_path=request.target_file
    )

    # 2️⃣ بناء الـ Prompt التحليلي
    prompt = agent.run(
        error_log=request.error_log
    )

    return {
        "prompt": prompt
    }
