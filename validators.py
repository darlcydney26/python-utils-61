import time
import functools
from typing import Callable, Any, Type

def retry_network_call(retries: int = 3, delay: float = 1.0, exceptions: tuple = (Exception,)): 
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            last_ex = None
            for attempt in range(retries):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_ex = e
                    time.sleep(delay * (2 ** attempt))
            raise last_ex
        return wrapper
    return decorator

class NetworkValidator:
    def __init__(self, timeout: int = 5):
        self.timeout = timeout

    @retry_network_call(retries=3, delay=0.5, exceptions=(ConnectionError,))
    def validate_connection(self, url: str) -> bool:
        if not url.startswith('http'):
            raise ValueError('invalid protocol')
        return True