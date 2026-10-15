import time
import functools
from typing import Callable, Any, Dict

def time_execution(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start = time.perf_counter()
        result = func(*args, **kwargs)
        print(f"execution time: {time.perf_counter() - start:.6f}s")
        return result
    return wrapper

def dict_deep_merge(base: Dict, update: Dict) -> Dict:
    for k, v in update.items():
        if isinstance(v, dict) and k in base and isinstance(base[k], dict):
            dict_deep_merge(base[k], v)
        else:
            base[k] = v
    return base

def retry_operation(attempts: int = 3, delay: float = 0.5):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_ex = None
            for i in range(attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_ex = e
                    time.sleep(delay * (2 ** i))
            raise last_ex
        return wrapper
    return decorator

def memoize_with_expiry(ttl: int = 300):
    cache = {}
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args):
            now = time.time()
            if args in cache and (now - cache[args]["time"] < ttl):
                return cache[args]["data"]
            res = func(*args)
            cache[args] = {"data": res, "time": now}
            return res
        return wrapper
    return decorator