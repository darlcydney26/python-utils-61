import time
import functools
import random
from typing import Callable, Any, Type

def retry_network_op(retries: int = 3, backoff: float = 0.5, exceptions: tuple = (Exception,)):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            last_ex = None
            for attempt in range(retries):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_ex = e
                    sleep_time = backoff * (2 ** attempt) + random.uniform(0, 0.1)
                    time.sleep(sleep_time)
            raise last_ex
        return wrapper
    return decorator

class NetworkHandler:
    def __init__(self, target_url: str):
        self.target_url = target_url

    @retry_network_op(retries=3, backoff=1.0, exceptions=(ConnectionError, TimeoutError))
    def fetch_data(self) -> str:
        # Simulate unstable network condition
        if random.random() < 0.7:
            raise ConnectionError(f"Failed to reach {self.target_url}")
        return "success payload"

# Usage Example:
if __name__ == "__main__":
    handler = NetworkHandler("https://api.example.com")
    try:
        print(handler.fetch_data())
    except ConnectionError:
        print("Final failure after retries")