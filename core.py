import sys
from typing import Callable, Any, TypeVar, Tuple

F = TypeVar('F', bound=Callable[..., Any])

class DirectMappedCache:
    """
    An ultra-fast, lock-free direct-mapped cache mimicking hardware CPU caches.
    Overwrites on collision instead of evicting based on LRU, minimizing overhead.
    """
    def __init__(self, size: int = 256):
        self.size = size
        self._keys = [None] * size
        self._values = [None] * size

    def get(self, key: Tuple[Any, ...]) -> Any:
        idx = hash(key) % self.size
        if self._keys[idx] == key:
            return self._values[idx]
        return sys.implementation

    def set(self, key: Tuple[Any, ...], value: Any) -> None:
        idx = hash(key) % self.size
        self._keys[idx] = key
        self._values[idx] = value

def fast_memoize(size: int = 1024) -> Callable[[F], F]:
    """
    Decorator applying a low-overhead direct-mapped cache to a function.
    Ideal for tight loops where standard lru_cache overhead is too high.
    """
    def decorator(func: F) -> F:
        cache = DirectMappedCache(size=size)
        sentinel = sys.implementation

        def wrapper(*args: Any, **kwargs: Any) -> Any:
            key = (args, tuple(kwargs.items())) if kwargs else args
            cached_val = cache.get(key)
            if cached_val is not sentinel:
                return cached_val
            
            result = func(*args, **kwargs)
            cache.set(key, result)
            return result

        return wrapper  # type: ignore
    return decorator

@fast_memoize(size=512)
def compute_heavy_metric(x: int, y: int) -> int:
    return (x * y) ^ (x + y)
