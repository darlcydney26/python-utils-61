"""Dynamic exception hierarchy with contextual payload support."""

from typing import Any, Dict, Optional, Type


class BaseAppError(Exception):
    """Base exception class supporting dynamic context attributes and formatting."""

    def __init__(self, message: str, *, code: Optional[str] = None, **kwargs: Any) -> None:
        super().__init__(message)
        self.message = message
        self.code = code or self.__class__.__name__
        self.payload: Dict[str, Any] = kwargs
        for key, value in kwargs.items():
            if not hasattr(self, key):
                setattr(self, key, value)

    def to_dict(self) -> Dict[str, Any]:
        return {"error": self.code, "message": self.message, "details": self.payload}

    def __repr__(self) -> str:
        ctx = ", ".join(f"{k}={v!r}" for k, v in self.payload.items())
        return f"{self.__class__.__name__}({self.message!r}{', ' + ctx if ctx else ''})"


class ValidationError(BaseAppError):
    """Raised when data validation fails."""


class ProcessingError(BaseAppError):
    """Raised when processing operational pipeline fails."""


class ConfigurationError(BaseAppError):
    """Raised when configuration values are missing or invalid."""


class ExceptionRegistry:
    """Registry mapping error codes to domain exception types."""

    _registry: Dict[str, Type[BaseAppError]] = {
        "ERR_VALIDATION": ValidationError,
        "ERR_PROCESSING": ProcessingError,
        "ERR_CONFIG": ConfigurationError,
    }

    @classmethod
    def register(cls, code: str, exc_cls: Type[BaseAppError]) -> None:
        cls._registry[code] = exc_cls

    @classmethod
    def create(cls, code: str, message: str, **kwargs: Any) -> BaseAppError:
        exc_cls = cls._registry.get(code, BaseAppError)
        return exc_cls(message, code=code, **kwargs)
