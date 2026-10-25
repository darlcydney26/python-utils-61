import sys
import traceback
from typing import Any, Dict, Optional, Type


class DataPayloadError(Exception):
    """Exception that captures contextual data snapshots upon instantiation."""

    def __init__(self, message: str, payload: Optional[Any] = None, code: int = 500):
        super().__init__(message)
        self.message = message
        self.payload = payload
        self.code = code
        self._frame_info = self._capture_context()

    def _capture_context(self) -> Dict[str, Any]:
        tb = traceback.extract_stack()
        if len(tb) > 2:
            caller = tb[-3]
            return {"file": caller.filename, "line": caller.lineno, "function": caller.name}
        return {}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "error": self.__class__.__name__,
            "message": self.message,
            "code": self.code,
            "payload": self.payload,
            "context": self._frame_info,
        }

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}(code={self.code}, message={self.message!r})>"


class ExceptionFactory:
    """Dynamic exception generator for domain-specific data operations."""

    _registry: Dict[str, Type[DataPayloadError]] = {}

    @classmethod
    def get_exception(cls, name: str, default_code: int = 400) -> Type[DataPayloadError]:
        if name not in cls._registry:
            def custom_init(self, msg: str, payload: Any = None, code: int = default_code):
                DataPayloadError.__init__(self, msg, payload, code)

            new_type = type(name, (DataPayloadError,), {"__init__": custom_init})
            cls._registry[name] = new_type
        return cls._registry[name]


def trap_data_errors(default_return: Any = None):
    """Decorator to convert unhandled data errors into rich DataPayloadError payloads."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except DataPayloadError:
                raise
            except Exception as exc:
                err_type = ExceptionFactory.get_exception("UnhandledDataProcessingError", 500)
                raise err_type(
                    f"Error in {func.__name__}: {str(exc)}",
                    payload={"args": [repr(a) for a in args], "kwargs": {k: repr(v) for k, v in kwargs.items()}}
                ) from exc
        return wrapper
    return decorator
