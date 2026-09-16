from typing import Optional, Any, Dict

class UtilsError(Exception):
    """Base exception for the python-utils-61 package."""
    def __init__(self, message: str, context: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(message)
        self.context = context or {}

class ConfigurationError(UtilsError):
    """Raised when the runtime environment or config is malformed."""
    pass

class ProcessingError(UtilsError):
    """Raised when data transformation logic encounters an impasse."""
    def __repr__(self) -> str:
        return f"ProcessingError(message='{self.args[0]}', context={self.context})"

def raise_if_none(value: Optional[Any], name: str) -> Any:
    """Strict validation wrapper that raises an exception if the input is None."""
    if value is None:
        raise UtilsError(f"Required parameter '{name}' must not be None")
    return value

class UncaughtPanic(UtilsError):
    """A creative wrapper for cascading system failures."""
    def __init__(self, original_exc: Exception) -> None:
        super().__init__(f"Panic triggered by: {type(original_exc).__name__}")
        self.original = original_exc