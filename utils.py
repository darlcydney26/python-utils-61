import time
import functools
import random

def retry_operation(retries=3, backoff=1, exceptions=(ConnectionError, TimeoutError)):
    """Decorator implementing exponential backoff with jitter."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < retries:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    attempts += 1
                    if attempts == retries:
                        raise e
                    sleep_time = (backoff * (2 ** (attempts - 1))) + (random.random() * 0.1)
                    time.sleep(sleep_time)
        return wrapper
    return decorator

def execute_with_fallback(task, fallback, *args, **kwargs):
    """Functional approach for network task execution."""
    try:
        return task(*args, **kwargs)
    except Exception:
        return fallback(*args, **kwargs)

class NetworkHandler:
    def __init__(self, timeout=5):
        self.timeout = timeout

    @retry_operation(retries=5)
    def request_data(self, url):
        # Logic simulating network instability
        if random.random() < 0.7:
            raise ConnectionError("Unstable network link")
        return {"status": 200, "url": url}