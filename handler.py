import functools
import logging
from typing import Callable, Any

class ResilienceOrchestrator:
    def __init__(self, logger: logging.Logger = None):
        self.logger = logger or logging.getLogger(__name__)

    def __call__(self, func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                return func(*args, **kwargs)
            except (TypeError, ValueError, AttributeError) as e:
                self.logger.error(f"schema mismatch or value corruption: {e}")
                return None
            except Exception as e:
                self.logger.critical(f"unhandled cosmic ray incident: {e}")
                raise
        return wrapper

def silent_fallback(default_value: Any) -> Callable:
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                return func(*args, **kwargs)
            except Exception:
                return default_value
        return wrapper
    return decorator

@ResilienceOrchestrator()
def process_payload(data: dict) -> int:
    if not isinstance(data, dict):
        raise TypeError("input must be a dict")
    return int(data['value']) * 2