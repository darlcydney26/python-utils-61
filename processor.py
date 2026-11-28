import functools
import time
import collections
from typing import Callable, Any, Dict

def memoize_with_ttl(seconds: int = 300):
    def decorator(func: Callable):
        cache: Dict[tuple, tuple] = {}
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = (args, tuple(sorted(kwargs.items())))
            now = time.time()
            if key in cache and now - cache[key][0] < seconds:
                return cache[key][1]
            result = func(*args, **kwargs)
            cache[key] = (now, result)
            return result
        return wrapper
    return decorator

def deep_flatten(items: list) -> list:
    flat = []
    for item in items:
        if isinstance(item, (list, tuple)):
            flat.extend(deep_flatten(item))
        else:
            flat.append(item)
    return flat

def dict_path_get(data: dict, path: str, default: Any = None):
    keys = path.split('.')
    try:
        return functools.reduce(lambda d, k: d[k], keys, data)
    except (KeyError, TypeError):
        return default

def batch_iterator(iterable: list, size: int):
    for i in range(0, len(iterable), size):
        yield iterable[i:i + size]

class IdentityCounter(collections.Counter):
    def __missing__(self, key):
        return 0