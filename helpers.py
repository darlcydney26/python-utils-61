import collections.abc
import functools
from typing import Any, Callable, TypeVar

T = TypeVar('T')

def deep_flatten(items: Any) -> list:
    flat = []
    for item in items:
        if isinstance(item, (list, tuple, set)):
            flat.extend(deep_flatten(item))
        else:
            flat.append(item)
    return flat

def memoize_with_expiry(ttl: int) -> Callable:
    def decorator(func: Callable) -> Callable:
        cache = {}
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            key = (args, tuple(sorted(kwargs.items())))
            import time
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

def compose(*functions: Callable) -> Callable:
    return functools.reduce(lambda f, g: lambda x: f(g(x)), functions, lambda x: x)

def pluck(data: list[dict], key: str) -> list[Any]:
    return [item.get(key) for item in data if isinstance(item, dict) and key in item]