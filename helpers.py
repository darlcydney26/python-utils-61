import functools
import logging
from typing import Callable, Any

def robust_execution(default_value: Any = None) -> Callable:
    """Decorator that wraps calls in a defensive blanket."""
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except (TypeError, ValueError, AttributeError) as e:
                logging.error(f"caught predictable edge case in {func.__name__}: {e}")
                return default_value
            except Exception as e:
                logging.critical(f"unexpected chaos in {func.__name__}: {e}")
                raise
        return wrapper
    return decorator

def safe_dict_get(data: dict, path: str, default: Any = None) -> Any:
    """Traverse dictionary keys safely using dot notation."""
    if not isinstance(data, dict):
        return default
    keys = path.split('.')
    curr = data
    try:
        for key in keys:
            curr = curr[key]
        return curr if curr is not None else default
    except (KeyError, TypeError):
        return default

@robust_execution(default_value=0)
def perform_division(a: float, b: float) -> float:
    """Edge case division with automatic zero fallback."""
    return a / b