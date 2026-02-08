# app/api/dev_ai_context.py

from fastapi import APIRouter
from app.core.dev_context import get_dev_context

router = APIRouter(
    prefix="/api/dev/ai",
    tags=["AI Dev Assistant"]
)


@router.get("/context")
def read_dev_context():
    """
    عرض السياق الحالي للمساعد البرمجي
    """
    return {
        "status": "ok",
        "context": get_dev_context()
    }
