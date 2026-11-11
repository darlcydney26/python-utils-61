import time
import functools
import random

def retry_network_call(max_retries=3, backoff_factor=0.5):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_retries:
                try:
                    return func(*args, **kwargs)
                except (ConnectionError, TimeoutError) as e:
                    attempts += 1
                    if attempts >= max_retries:
                        raise e
                    sleep_time = backoff_factor * (2 ** (attempts - 1)) + random.uniform(0, 0.1)
                    time.sleep(sleep_time)
        return wrapper
    return decorator

class NetworkProcessor:
    def __init__(self, endpoint):
        self.endpoint = endpoint

    @retry_network_call(max_retries=5)
    def fetch_data(self, key):
        # Simulate unstable network condition
        if random.random() < 0.7:
            raise ConnectionError(f"Failed to reach {self.endpoint}")
        return {"status": "success", "payload": f"data_for_{key}"}

if __name__ == "__main__":
    proc = NetworkProcessor("https://api.example.com")
    result = proc.fetch_data("user_123")
    print(result)