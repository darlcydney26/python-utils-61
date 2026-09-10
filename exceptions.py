import sys
import time
import json
from typing import Any, Dict, Optional, Type


class UtilBaseException(Exception):
    """Base exception class with dynamic context enrichment and payload chaining."""

    def __init__(self, message: str, payload: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.message = message
        self.timestamp = time.time()
        self.payload = payload or {}
        self.frame_info = self._capture_frame()

    def _capture_frame(self) -> Dict[str, Any]:
        frame = sys._getframe(2) if hasattr(sys, "_getframe") else None
        if not frame:
            return {}
        return {
            "function": frame.f_code.co_name,
            "filename": frame.f_code.co_filename,
            "line": frame.f_lineno,
        }

    def __add__(self, extra: Dict[str, Any]) -> "UtilBaseException":
        """Allows extending payload context using the addition operator."""
        if isinstance(extra, dict):
            self.payload.update(extra)
            return self
        return NotImplemented

    def to_dict(self) -> Dict[str, Any]:
        return {
            "error_type": self.__class__.__name__,
            "message": self.message,
            "timestamp": self.timestamp,
            "origin": self.frame_info,
            "payload": self.payload,
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2)

    def __str__(self) -> str:
        func_name = self.frame_info.get("function", "unknown")
        line_no = self.frame_info.get("line", "?")
        return f"{self.__class__.__name__}[{func_name}:{line_no}]: {self.message} | Payload: {self.payload}"


class ProcessingError(UtilBaseException):
    """Raised when data processing fails."""


class ValidationError(UtilBaseException):
    """Raised when data validation fails."""


class ConfigurationError(UtilBaseException):
    """Raised when configuration is invalid."""


def wrap_exception(target_type: Type[UtilBaseException]):
    """Decorator converting native exceptions into enriched utility exceptions."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as exc:
                if isinstance(exc, UtilBaseException):
                    raise
                err = target_type(str(exc))
                err += {"original_type": exc.__class__.__name__}
                raise err from exc
        return wrapper
    return decorator
