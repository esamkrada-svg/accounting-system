# app/core/dev_context.py

from typing import Optional, Dict
from datetime import datetime

# ذاكرة المساعد البرمجي (In-Memory)
_DEV_CONTEXT: Dict[str, Optional[dict]] = {
    "last_error": None,
    "last_analysis": None,
    "last_advice": None,
    "updated_at": None,
}


def set_last_error(error: dict):
    _DEV_CONTEXT["last_error"] = error
    _DEV_CONTEXT["updated_at"] = datetime.utcnow().isoformat()


def set_last_analysis(analysis: dict):
    _DEV_CONTEXT["last_analysis"] = analysis
    _DEV_CONTEXT["updated_at"] = datetime.utcnow().isoformat()


def set_last_advice(advice: dict):
    _DEV_CONTEXT["last_advice"] = advice
    _DEV_CONTEXT["updated_at"] = datetime.utcnow().isoformat()


def get_dev_context() -> dict:
    return _DEV_CONTEXT
