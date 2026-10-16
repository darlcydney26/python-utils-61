import functools
import itertools
import time
from typing import Callable, Any, Iterable, List

def compose(*functions: Callable) -> Callable:
    """Functional pipeline builder for nested calls."""
    return functools.reduce(lambda f, g: lambda x: f(g(x)), functions, lambda x: x)

def chunks(data: Iterable, size: int) -> Iterable:
    """Generator for splitting iterables into slices."""
    it = iter(data)
    for item in iter(lambda: tuple(itertools.islice(it, size)), ()): 
        yield item

def throttle(seconds: int = 1) -> Callable:
    """Decorator for execution frequency limitation."""
    def decorator(func: Callable) -> Callable:
        last_called = [0.0]
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            elapsed = time.time() - last_called[0]
            if elapsed < seconds:
                time.sleep(seconds - elapsed)
            result = func(*args, **kwargs)
            last_called[0] = time.time()
            return result
        return wrapper
    return decorator

def deep_flatten(nested: Iterable) -> List[Any]:
    """Recursive list flattening via generator yields."""
    result = []
    for item in nested:
        if isinstance(item, (list, tuple)):
            result.extend(deep_flatten(item))
        else:
            result.append(item)
    return result

def memoize_dynamic(func: Callable) -> Callable:
    """Unusual memoization using a function attribute cache."""
    func.cache = {}
    @functools.wraps(func)
    def wrapper(*args):
        if args not in func.cache:
            func.cache[args] = func(*args)
        return func.cache[args]
    return wrapper