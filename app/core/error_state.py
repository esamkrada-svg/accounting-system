# app/core/error_state.py

from typing import Optional, Dict
import threading

_lock = threading.Lock()
_last_error: Optional[Dict] = None


def set_last_error(error: Dict):
    global _last_error
    with _lock:
        _last_error = error


def get_last_error() -> Optional[Dict]:
    with _lock:
        return _last_error
