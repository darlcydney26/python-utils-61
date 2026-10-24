import time
import functools
from typing import Callable, Any, Type

def retry_on_failure(exceptions: tuple[Type[Exception], ...], max_retries: int = 3, delay: float = 1.0):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            last_ex = None
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_ex = e
                    if attempt < max_retries - 1:
                        time.sleep(delay * (2 ** attempt))
            raise last_ex
        return wrapper
    return decorator

def exponential_backoff(func: Callable):
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        retries = 0
        while True:
            try:
                return func(*args, **kwargs)
            except Exception:
                if retries >= 5:
                    raise
                time.sleep(0.1 * (2 ** retries))
                retries += 1
    return wrapper