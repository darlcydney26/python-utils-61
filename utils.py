import time
import functools
import random

def retry_operation(max_attempts=3, backoff=0.5, exceptions=(Exception,)): 
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    attempts += 1
                    if attempts >= max_attempts:
                        raise e
                    sleep_time = backoff * (2 ** (attempts - 1)) + random.uniform(0, 0.1)
                    time.sleep(sleep_time)
        return wrapper
    return decorator

class NetworkCircuit:
    def __init__(self, target_func):
        self.target = target_func

    def __call__(self, *args, **kwargs):
        safe_call = retry_operation(max_attempts=4)(self.target)
        return safe_call(*args, **kwargs)

def fetch_with_backoff(url):
    # Simulate volatile network operation
    if random.random() < 0.7:
        raise ConnectionError("Temporary server glitch")
    return f"Payload from {url}"