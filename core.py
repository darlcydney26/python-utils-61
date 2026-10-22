import time
import functools
import random

def retry(exceptions, attempts=3, backoff=0.5):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_ex = None
            for i in range(attempts):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_ex = e
                    if i < attempts - 1:
                        sleep_time = backoff * (2 ** i) + (random.random() * 0.1)
                        time.sleep(sleep_time)
            raise last_ex
        return wrapper
    return decorator

class NetworkHandler:
    @staticmethod
    @retry((ConnectionError, TimeoutError), attempts=3)
    def fetch_data(url):
        # Simulated unstable network operation
        if random.random() < 0.7:
            raise ConnectionError(f"Failed to reach {url}")
        return {"status": 200, "data": "success"}

# Example usage:
# handler = NetworkHandler()
# result = handler.fetch_data("https://api.example.com")