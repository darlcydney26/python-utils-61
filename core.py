import time
import functools
import random
from typing import Callable, Any

def retry_operation(max_attempts: int = 3, base_delay: float = 1.0):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            last_exception = None
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_attempts - 1:
                        sleep_time = base_delay * (2 ** attempt) + random.uniform(0, 0.1)
                        time.sleep(sleep_time)
            raise last_exception
        return wrapper
    return decorator

class NetworkClient:
    def __init__(self, endpoint: str):
        self.endpoint = endpoint

    @retry_operation(max_attempts=3, base_delay=0.5)
    def fetch_data(self):
        # Simulate potential network flakiness
        if random.random() < 0.7:
            raise ConnectionError('Temporary connection drop')
        return {'status': 'success', 'data': 'payload'}