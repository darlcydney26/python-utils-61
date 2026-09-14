import functools
import time
from typing import Any, Callable

def compose(*functions: Callable) -> Callable:
    """Right-to-left function composition."""
    return functools.reduce(lambda f, g: lambda x: f(g(x)), functions, lambda x: x)

def memoize_timed(seconds: int) -> Callable:
    """Decorator with TTL-based expiration."""
    def decorator(func: Callable) -> Callable:
        cache = {}
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = (args, frozenset(kwargs.items()))
            now = time.time()
            if key in cache:
                result, timestamp = cache[key]
                if now - timestamp < seconds:
                    return result
            result = func(*args, **kwargs)
            cache[key] = (result, now)
            return result
        return wrapper
    return decorator

def deep_flatten(items: list) -> list:
    """Recursive flattening via generator yield."""
    def _flat(obj):
        for i in obj:
            if isinstance(i, (list, tuple)):
                yield from _flat(i)
            else:
                yield i
    return list(_flat(items))

def chunker(iterable: Any, size: int):
    """Iterator segmenting for memory efficiency."""
    for i in range(0, len(iterable), size):
        yield iterable[i:i + size]