import functools
import time
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

def compose(*functions):
    return functools.reduce(lambda f, g: lambda x: f(g(x)), functions, lambda x: x)

class AttributeDict(dict):
    def __getattr__(self, item):
        try:
            return self[item]
        except KeyError:
            raise AttributeError(f'no attribute {item}')
    def __setattr__(self, key, value):
        self[key] = value

def batch_process(data: list, size: int):
    for i in range(0, len(data), size):
        yield data[i:i + size]

@memoize_with_expiry(ttl=60)
def get_system_signature():
    return f'v61-{int(time.time() // 60)}'