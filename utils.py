import functools
import time
import itertools
from typing import Callable, Any, Iterable

def retry_on_failure(retries: int = 3, delay: float = 1.0):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(retries):
                try:
                    return func(*args, **kwargs)
                except Exception:
                    if attempt == retries - 1: raise
                    time.sleep(delay)
        return wrapper
    return decorator

def chunked_iterable(iterable: Iterable, size: int) -> Iterable:
    it = iter(iterable)
    return iter(lambda: list(itertools.islice(it, size)), [])

def compose(*functions: Callable) -> Callable:
    return functools.reduce(lambda f, g: lambda x: f(g(x)), functions, lambda x: x)

def deep_flatten(items: Iterable) -> Iterable:
    for x in items:
        if isinstance(x, (list, tuple)):
            yield from deep_flatten(x)
        else:
            yield x

def memoize_with_expiry(ttl: int = 60):
    cache = {}
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args):
            now = time.time()
            if args in cache and (now - cache[args][1]) < ttl:
                return cache[args][0]
            result = func(*args)
            cache[args] = (result, now)
            return result
        return wrapper
    return decorator