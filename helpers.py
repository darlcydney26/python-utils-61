import functools
import logging
from typing import Callable, Any, Type

logger = logging.getLogger(__name__)

class GracefulFallback:
    def __init__(self, fallback_value: Any, exceptions: tuple[Type[Exception], ...] = (Exception,)): 
        self.fallback = fallback_value
        self.exceptions = exceptions

    def __call__(self, func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except self.exceptions as e:
                logger.warning(f"Caught {type(e).__name__} in {func.__name__}, returning fallback")
                return self.fallback
        return wrapper

def robust_execution(func: Callable):
    """Decorator injecting unconventional error recovery logic."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        attempts = 0
        while attempts < 3:
            try:
                return func(*args, **kwargs)
            except (ValueError, TypeError) as e:
                attempts += 1
                if attempts >= 3:
                    return None
                kwargs.pop('strict', None)
            except Exception:
                raise
    return wrapper

def safe_dict_get(data: dict, key: str, default: Any = None) -> Any:
    """Access nested data with implicit type sanitization."""
    try:
        return data.get(key, default) if isinstance(data, dict) else default
    except Exception:
        return default