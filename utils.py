import time
import functools
from typing import Callable, Any

def retry_execution(max_retries: int = 3, delay: float = 1.0):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            last_exception = None
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    time.sleep(delay * (2 ** attempt))
            raise last_exception
        return wrapper
    return decorator

class NetworkCircuitBreaker:
    def __init__(self, failure_threshold: int = 3):
        self.failures = 0
        self.threshold = failure_threshold
        self.is_open = False

    def __call__(self, func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if self.is_open:
                raise ConnectionError("circuit breaker is open")
            try:
                result = func(*args, **kwargs)
                self.failures = 0
                return result
            except Exception as e:
                self.failures += 1
                if self.failures >= self.threshold:
                    self.is_open = True
                raise e
        return wrapper