import functools
import itertools
import time
from typing import Any, Callable, Iterable, TypeVar

T = TypeVar('T')

def compose(*funcs: Callable) -> Callable:
    """Functional pipeline builder for data processing"""
    return lambda x: functools.reduce(lambda v, f: f(v), funcs, x)

def chunker(iterable: Iterable[T], size: int) -> Iterable[list[T]]:
    """Iterator windowing using zip_longest trickery"""
    args = [iter(iterable)] * size
    return ([e for e in t if e is not None] for t in itertools.zip_longest(*args))

def throttled(interval: float) -> Callable:
    """Decorator for temporal execution gating"""
    def decorator(func: Callable):
        last_called = [0.0]
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            elapsed = time.time() - last_called[0]
            if elapsed < interval:
                time.sleep(interval - elapsed)
            last_called[0] = time.time()
            return func(*args, **kwargs)
        return wrapper
    return decorator

def deep_get(data: dict, path: str, default: Any = None) -> Any:
    """Dot-notation navigation for nested dictionaries"""
    try:
        return functools.reduce(lambda d, k: d.get(k, {}), path.split('.'), data)
    except AttributeError:
        return default

def flatten(nested: list) -> list:
    """Recursive list structural simplification"""
    flat = []
    for item in nested:
        if isinstance(item, list):
            flat.extend(flatten(item))
        else:
            flat.append(item)
    return flat