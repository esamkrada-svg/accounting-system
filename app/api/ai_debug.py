from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from sqlalchemy.orm import Session

from app.database.db import SessionLocal
from ai_agent.agent import DebugAgent
from app.api.auth import get_current_user

router = APIRouter(prefix="/api/ai-debug", tags=["AI Debug"])


# =========================
# DB Dependency (مستقبلي)
# =========================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# =========================
# Request Schema
# =========================
class DebugRequest(BaseModel):
    target_file: str
    error_log: Optional[str] = None


class DebugResponse(BaseModel):
    prompt: str


# =========================
# AI Debug Endpoint
# =========================
@router.post("/analyze", response_model=DebugResponse)
def analyze_code(
    data: DebugRequest,
    token: str,
    db: Session = Depends(get_db),
):
    """
    🧠 Debug Assistant (READ-ONLY)
    - يتحقق من المستخدم
    - يبني Prompt فقط
    """

    # ✅ تحقق أمني
    get_current_user(token)

    # 🧠 تشغيل المساعد
    try:
        agent = DebugAgent(data.target_file)
        prompt = agent.run(error_log=data.error_log)
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"AI Debug Agent failed: {str(e)}"
        )

    return {"prompt": prompt}
