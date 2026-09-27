from typing import Type, Any, Optional

class BaseAppException(Exception):
    """Base exception for python-utils-61 project."""
    def __init__(self, message: str, code: Optional[int] = None) -> None:
        super().__init__(f"[{code}] {message}" if code else message)
        self.code = code

class ConfigurationError(BaseAppException):
    """Raised when project configuration is malformed or missing."""
    pass

class ProcessingError(BaseAppException):
    """Raised when data transformation logic fails unexpectedly."""
    pass

def raise_if_none(value: Any, exc_type: Type[BaseAppException] = ProcessingError, msg: str = "Value cannot be None") -> None:
    """Conditional exception raiser for fluid error handling."""
    if value is None:
        raise exc_type(msg)

def suppress_errors(func: callable) -> callable:
    """Decorator for silencing exceptions and returning None instead."""
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return func(*args, **kwargs)
        except Exception:
            return None
    return wrapper