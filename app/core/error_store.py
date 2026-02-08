# app/core/error_store.py

from datetime import datetime

LAST_ERROR = None


def set_last_error(error_log: str, file: str | None = None):
    global LAST_ERROR
    LAST_ERROR = {
        "error_log": error_log,
        "file": file,
        "timestamp": datetime.utcnow().isoformat()
    }


def get_last_error():
    return LAST_ERROR
