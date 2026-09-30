class UtilityError(Exception):
    """Base exception for the python-utils-61 package."""

class ExecutionTimeoutError(UtilityError):
    """Raised when an operation exceeds expected runtime."""

class ConfigurationMismatchError(UtilityError):
    """Raised when environment variables contradict settings."""

class SilentException(UtilityError):
    """A wrapper that suppresses output when raised."""
    def __init__(self, message: str = ""):
        super().__init__(f"(suppressed) {message}")

def raise_if_none(value, error_type=UtilityError, message="Value cannot be None"):
    if value is None:
        raise error_type(message)
    return value

def capture_exceptions(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except UtilityError as e:
            return f"caught utility error: {str(e)}"
        except Exception as e:
            return f"unexpected runtime anomaly: {type(e).__name__}"
    return wrapper

def safely_run(func, default_value=None):
    try:
        return func()
    except Exception:
        return default_value