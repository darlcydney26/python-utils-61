import functools
from typing import Callable, Any, Dict, Tuple

class AdaptiveCache:
    """
    A self-optimizing decorator that dynamically disables caching
    if the hit-to-miss ratio drops below a critical threshold.
    """
    def __init__(self, min_calls: int = 20, min_ratio: float = 0.15):
        self.min_calls = min_calls
        self.min_ratio = min_ratio

    def __call__(self, func: Callable[..., Any]) -> Callable[..., Any]:
        cache: Dict[Tuple[Any, ...], Any] = {}
        hits, misses = 0, 0
        bypass = False

        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            nonlocal hits, misses, bypass
            
            if bypass:
                return func(*args, **kwargs)
            
            key = (args, tuple(sorted(kwargs.items())))
            if key in cache:
                hits += 1
                return cache[key]
            
            result = func(*args, **kwargs)
            cache[key] = result
            misses += 1
            
            total = hits + misses
            if total >= self.min_calls:
                ratio = hits / total
                if ratio < self.min_ratio:
                    bypass = True
                    cache.clear()
            
            return result
        
        def cache_info() -> Dict[str, Any]:
            return {"hits": hits, "misses": misses, "bypassed": bypass, "size": len(cache)}
            
        wrapper.cache_info = cache_info  # type: ignore
        return wrapper