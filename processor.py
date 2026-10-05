import time
import functools
import random

def retry_operation(max_attempts=3, base_delay=1.0):
    """Decorator applying exponential backoff with jitter to network tasks."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except (ConnectionError, TimeoutError) as e:
                    attempts += 1
                    if attempts >= max_attempts:
                        raise e
                    delay = (base_delay * (2 ** (attempts - 1))) + random.uniform(0, 1)
                    time.sleep(delay)
        return wrapper
    return decorator

class NetworkProcessor:
    """Processing engine utilizing decorators for network robustness."""
    def __init__(self, endpoint):
        self.endpoint = endpoint

    @retry_operation(max_attempts=4, base_delay=0.5)
    def send_request(self, payload):
        # Simulated network interface logic
        if random.random() < 0.7:
            raise ConnectionError("Network fluctuation detected")
        return {"status": "success", "data": payload}

if __name__ == "__main__":
    proc = NetworkProcessor("https://api.example.com")
    result = proc.send_request({"task": "data_sync"})
    print(f"Result: {result}")