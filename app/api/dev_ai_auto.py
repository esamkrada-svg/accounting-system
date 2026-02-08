# app/api/dev_ai_auto.py

from fastapi import APIRouter, HTTPException
from app.core.error_state import get_last_error
from ai_agent.agent import AIAgent
from ai_agent.context_loader import load_system_context
from ai_agent.prompt_builder import build_debug_prompt

router = APIRouter(
    prefix="/api/dev/ai",
    tags=["Developer AI Assistant"]
)

@router.post("/analyze-last-error")
def analyze_last_error():
    error = get_last_error()

    if not error:
        raise HTTPException(
            status_code=404,
            detail="لا يوجد خطأ لتحليله"
        )

    system_context = load_system_context()

    prompt = build_debug_prompt(
        system_context=system_context,
        problem=error.get("error_log", ""),
        file=error.get("file", ""),
        extra_notes=f"Path: {error.get('path')}"
    )

    agent = AIAgent()
    result = agent.run(prompt)

    return {
        "status": "analyzed",
        "analysis": result.get("analysis", ""),
        "suggestions": result.get("suggestions", "")
    }
