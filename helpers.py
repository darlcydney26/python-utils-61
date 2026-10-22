import functools
import itertools
import time
from typing import Any, Callable, Iterable, TypeVar

T = TypeVar('T')

def compose(*functions: Callable) -> Callable:
    """Functional pipe for data processing pipelines."""
    return functools.reduce(lambda f, g: lambda x: g(f(x)), functions)

def chunk_stream(data: Iterable[T], size: int) -> Iterable[list[T]]:
    """Iterator for batch processing of large collections."""
    it = iter(data)
    return iter(lambda: list(itertools.islice(it, size)), [])

def retry_with_backoff(retries: int = 3, backoff: float = 0.1):
    """Decorator for transient failure recovery patterns."""
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_ex = None
            for i in range(retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_ex = e
                    time.sleep(backoff * (2 ** i))
            raise last_ex
        return wrapper
    return decorator

def flatten(nested_list: list) -> list:
    """Recursive reduction of multi-dimensional structure."""
    result = []
    for item in nested_list:
        if isinstance(item, list):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result