from typing import Any, Optional

class BaseUtilError(Exception):
    """Base exception for the python-utils-61 library."""
    def __init__(self, message: str, context: Optional[dict[str, Any]] = None) -> None:
        super().__init__(message)
        self.context = context or {}

class ConfigurationError(BaseUtilError):
    """Raised when the runtime environment or config fails sanity checks."""
    pass

class ValidationError(BaseUtilError):
    """Raised when input parameters do not meet strict schema requirements."""
    pass

def raise_if_none(value: Any, name: str, scope: str = "global") -> None:
    """Check value presence and escalate if absent using custom exceptions."""
    if value is None:
        raise ValidationError(
            f"Parameter '{name}' must not be null",
            {"scope": scope, "received": type(value).__name__}
        )

class SentinelError(BaseUtilError):
    """Specialized exception for unexpected control flow interruptions."""
    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: {self.args[0]}>"