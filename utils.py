import functools
import time
import itertools
from typing import Callable, Any, Iterable

def retry_on_failure(retries: int = 3, delay: float = 1.0):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for i in range(retries):
                try:
                    return func(*args, **kwargs)
                except Exception:
                    if i == retries - 1: raise
                    time.sleep(delay)
        return wrapper
    return decorator

def batch_process(iterable: Iterable, size: int):
    it = iter(iterable)
    return iter(lambda: list(itertools.islice(it, size)), [])

def chain_callables(functions: list[Callable]):
    def pipeline(data: Any):
        return functools.reduce(lambda v, f: f(v), functions, data)
    return pipeline

def flip_dict(d: dict):
    return {v: k for k, v in d.items()}