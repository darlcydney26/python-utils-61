import time
import functools
from typing import Callable, Any, Type

def retry_network_call(max_retries: int = 3, delay: float = 1.0, backoff: float = 2.0):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            current_delay = delay
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except (ConnectionError, TimeoutError) as e:
                    if attempt == max_retries:
                        raise e
                    time.sleep(current_delay)
                    current_delay *= backoff
            return None
        return wrapper
    return decorator

class NetworkHandler:
    @retry_network_call(max_retries=3)
    def fetch_data(self, endpoint: str) -> str:
        # Simulate flaky network behavior
        import random
        if random.random() < 0.7:
            raise ConnectionError("Unstable network connection")
        return f"Success from {endpoint}"

if __name__ == '__main__':
    handler = NetworkHandler()
    try:
        print(handler.fetch_data("https://api.example.com"))
    except Exception as err:
        print(f"Operation failed after retries: {err}")