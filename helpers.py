import functools
from typing import Any, Callable, Dict, Optional

def shadow_dict(data: Dict[Any, Any], keys: list, default: Any = None) -> Dict[Any, Any]:
    """Extracts specific keys from a dictionary with fallback."""
    return {k: data.get(k, default) for k in keys}

def chain_pipeline(data: Any, *funcs: Callable) -> Any:
    """Sequential application of functions to data."""
    return functools.reduce(lambda acc, f: f(acc), funcs, data)

def memoize_with_expiry(ttl: int = 60):
    """Cache wrapper with basic timestamp-based expiration."""
    cache = {}
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            import time
            key = (args, tuple(sorted(kwargs.items())))
            now = time.time()
            if key in cache:
                val, ts = cache[key]
                if now - ts < ttl:
                    return val
            result = func(*args, **kwargs)
            cache[key] = (result, now)
            return result
        return wrapper
    return decorator

def deep_flatten(nested: list) -> list:
    """Recursive list flattening using generator expression."""
    for item in nested:
        if isinstance(item, list):
            yield from deep_flatten(item)
        else:
            yield item