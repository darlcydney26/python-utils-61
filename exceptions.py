import sys
import functools
from typing import Callable, Any

class UtilityError(Exception):
    """Base exception for python-utils-61."""
    pass

class EdgeCaseHandler:
    def __init__(self, fallback: Any = None):
        self.fallback = fallback

    def __call__(self, func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                return func(*args, **kwargs)
            except (ValueError, TypeError, ZeroDivisionError, IndexError) as e:
                sys.stderr.write(f"[python-utils-61] Silencing {type(e).__name__}: {e}\n")
                return self.fallback
            except Exception as e:
                raise UtilityError(f"Critical failure in {func.__name__}: {e}") from e
        return wrapper

def resilient(default: Any = None) -> Callable:
    """Decorator for suppressing non-critical runtime exceptions."""
    return EdgeCaseHandler(fallback=default)

@resilient(default=0)
def safe_divide(a: float, b: float) -> float:
    return a / b

@resilient(default=[])
def safe_get_index(data: list, index: int) -> Any:
    return data[index]