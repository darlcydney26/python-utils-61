import functools
import time
import collections
from typing import Callable, Any

def memoize_with_expiry(ttl: int = 300):
    def decorator(func: Callable):
        cache = {}
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = (args, frozenset(kwargs.items()))
            now = time.time()
            if key in cache:
                val, timestamp = cache[key]
                if now - timestamp < ttl:
                    return val
            result = func(*args, **kwargs)
            cache[key] = (result, now)
            return result
        return wrapper
    return decorator

def deep_flatten(items: list) -> list:
    flat = []
    for item in items:
        if isinstance(item, collections.abc.Iterable) and not isinstance(item, (str, bytes)):
            flat.extend(deep_flatten(item))
        else:
            flat.append(item)
    return flat

def pipe(data: Any, *funcs: Callable) -> Any:
    return functools.reduce(lambda v, f: f(v), funcs, data)

class AttributeDict(dict):
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(f"Missing key: {key}")
    def __setattr__(self, key, value):
        self[key] = value