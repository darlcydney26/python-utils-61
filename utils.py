import functools
from typing import Any, Callable, Dict, Union

def deep_transform(data: Any, func: Callable[[Any], Any]) -> Any:
    """Recursively apply a transformation function to all values in nested structures."""
    if isinstance(data, dict):
        return {k: deep_transform(v, func) for k, v in data.items()}
    elif isinstance(data, list):
        return [deep_transform(i, func) for i in data]
    return func(data)

def memoize_data(expiry: int = 3600) -> Callable:
    """Unconventional time-based cache for expensive data processing ops."""
    import time
    cache: Dict[str, tuple] = {}

    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = str(args) + str(kwargs)
            now = time.time()
            if key in cache:
                val, timestamp = cache[key]
                if now - timestamp < expiry:
                    return val
            result = func(*args, **kwargs)
            cache[key] = (result, now)
            return result
        return wrapper
    return decorator

def coalesce(*args: Any) -> Any:
    """Return the first non-None value from the provided arguments."""
    return next((arg for arg in args if arg is not None), None)

class DataSentinel:
    """A unique object instance for signaling data absence."""
    def __repr__(self) -> str:
        return "<Sentinel>"

SENTINEL = DataSentinel()