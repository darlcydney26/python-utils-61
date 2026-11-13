import functools
import logging
from typing import Callable, Any, Dict

logger = logging.getLogger(__name__)

class Registry:
    _storage: Dict[str, Any] = {}

    @classmethod
    def register(cls, name: str):
        def decorator(func: Callable):
            cls._storage[name] = func
            return func
        return decorator

    @classmethod
    def invoke(cls, name: str, *args, **kwargs):
        if name not in cls._storage:
            raise ValueError(f"No function registered as {name}")
        return cls._storage[name](*args, **kwargs)

def memoize_with_logging(func: Callable):
    cache = {}

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        key = (args, frozenset(kwargs.items()))
        if key not in cache:
            logger.debug(f"Computing result for {func.__name__}")
            cache[key] = func(*args, **kwargs)
        return cache[key]
    return wrapper

def batch_process(items: list, chunk_size: int = 10):
    for i in range(0, len(items), chunk_size):
        yield items[i:i + chunk_size]

def smart_deep_get(data: dict, path: str, default: Any = None):
    keys = path.split('.')
    for key in keys:
        if not isinstance(data, dict) or key not in data:
            return default
        data = data[key]
    return data