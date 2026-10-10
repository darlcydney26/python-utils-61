import sys
from typing import Any, Dict, Optional


class ContextAwareException(Exception):
    """Dynamic base exception capturing contextual state and diagnostic metadata."""

    def __init__(self, message: str, payload: Optional[Any] = None, **kwargs: Any) -> None:
        self.message = message
        self.payload = payload
        self.context: Dict[str, Any] = kwargs
        self._frame_info = self._capture_caller_frame()
        super().__init__(self._format_message())

    def _capture_caller_frame(self) -> Dict[str, Any]:
        frame = sys._getframe(2) if hasattr(sys, "_getframe") else None
        if not frame:
            return {}
        return {
            "function": frame.f_code.co_name,
            "line": frame.f_lineno,
            "locals_snapshot": {k: repr(v)[:40] for k, v in list(frame.f_locals.items())[:5]},
        }

    def _format_message(self) -> str:
        parts = [self.message]
        if self.payload is not None:
            parts.append(f"Payload={repr(self.payload)[:80]}")
        if self.context:
            ctx_str = ", ".join(f"{k}={v!r}" for k, v in self.context.items())
            parts.append(f"Context=[{ctx_str}]")
        if self._frame_info:
            parts.append(f"Scope={self._frame_info.get('function')}:{self._frame_info.get('line')}")
        return " | ".join(parts)

    def enriched_dict(self) -> Dict[str, Any]:
        return {
            "error_type": self.__class__.__name__,
            "message": self.message,
            "payload": self.payload,
            "context": self.context,
            "caller_frame": self._frame_info,
        }


class ValidationError(ContextAwareException):
    """Raised when incoming data violates structural invariants."""


class TransformationError(ContextAwareException):
    """Raised when data pipeline mutation or serialization fails."""


class PipelineBreakageError(ContextAwareException):
    """Fatal error indicating unrecoverable sequence processing failures."""
