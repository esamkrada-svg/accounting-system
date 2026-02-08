# app/api/dev_ai_errors.py

from fastapi import APIRouter
from app.core.error_state import get_last_error

router = APIRouter(
    prefix="/api/dev/ai",
    tags=["Developer AI Assistant"]
)


@router.get("/last-error")
def last_error():
    error = get_last_error()

    if not error:
        return {
            "status": "ok",
            "message": "لا يوجد أي خطأ مسجل حاليًا"
        }

    return {
        "status": "error",
        "data": error
    }
