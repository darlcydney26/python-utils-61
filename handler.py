import functools
import time
import logging
from typing import Callable, Any, Dict

def memoize_with_expiry(ttl: int = 60):
    def decorator(func: Callable):
        cache: Dict[tuple, tuple] = {}
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = (args, tuple(sorted(kwargs.items())))
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

def retry_operation(attempts: int = 3, delay: float = 0.1):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_ex = None
            for _ in range(attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_ex = e
                    time.sleep(delay)
            raise last_ex
        return wrapper
    return decorator

def pipe(data: Any, *funcs: Callable):
    return functools.reduce(lambda v, f: f(v), funcs, data)

class DataPipeline:
    def __init__(self, initial_data: Any):
        self.data = initial_data
    
    def process(self, *funcs: Callable):
        self.data = pipe(self.data, *funcs)
        return self

    def get(self):
        return self.data