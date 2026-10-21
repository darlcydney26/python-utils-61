import time
import functools
import random
from typing import Callable, Any, Type

def retry_network_op(exceptions: tuple[Type[Exception], ...] = (Exception,), 
                     max_retries: int = 3, 
                     backoff_base: float = 1.0):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            last_ex = None
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_ex = e
                    wait = backoff_base * (2 ** attempt) + random.uniform(0, 0.1)
                    time.sleep(wait)
            raise last_ex
        return wrapper
    return decorator

# Usage example for the brave
@retry_network_op(exceptions=(ConnectionError,), max_retries=5)
def fetch_data(url: str):
    import urllib.request
    with urllib.request.urlopen(url) as response:
        return response.read()
