import time
import functools
from typing import Callable, Any, Type

def retry_on_failure(max_attempts: int = 3, delay: float = 1.0, exceptions: tuple = (Exception,)): 
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_error = None
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_error = e
                    if attempt < max_attempts - 1:
                        time.sleep(delay * (2 ** attempt))
            raise last_error
        return wrapper
    return decorator

def validate_network_response(validator_func: Callable[[Any], bool]):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            if not validator_func(result):
                raise ValueError(f"Invalid network response: {result}")
            return result
        return wrapper
    return decorator