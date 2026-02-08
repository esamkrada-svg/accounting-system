# app/core/error_middleware.py
from app.core.error_state import set_last_error
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from app.core.error_store import set_last_error
import traceback


class ErrorCaptureMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            return await call_next(request)
        except Exception as exc:
            trace = traceback.format_exc()
set_last_error({
    "error": str(e),
    "path": str(request.url.path),
    "method": request.method,
})
            set_last_error(
                error_log=str(exc),
                file=trace
            )

            raise  # نعيد الخطأ كما هو (لا نغيّر السلوك)
