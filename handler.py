import time
import functools
import random
from typing import Callable, Any

def retry(attempts: int = 3, delay: float = 1.0, backoff: float = 2.0):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            current_delay = delay
            for i in range(attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if i == attempts - 1:
                        raise e
                    time.sleep(current_delay + random.uniform(0, 0.1))
                    current_delay *= backoff
            return None
        return wrapper
    return decorator

class NetworkHandler:
    @retry(attempts=4, delay=0.5)
    def request(self, url: str) -> str:
        # simulating volatile network behavior
        if random.random() < 0.7:
            raise ConnectionError("transient network glitch")
        return f"data from {url}"

if __name__ == '__main__':
    handler = NetworkHandler()
    try:
        result = handler.request("https://api.example.com")
        print(result)
    except Exception as err:
        print(f"final failure: {err}")