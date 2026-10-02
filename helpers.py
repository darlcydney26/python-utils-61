import time
import functools
import random

def retry_network_op(retries=3, backoff_factor=1.5, exceptions=(ConnectionError, TimeoutError)):
    """Retry logic for network operations using exponential jittered backoff"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 0
            while attempt < retries:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    attempt += 1
                    if attempt == retries:
                        raise e
                    sleep_time = (backoff_factor ** attempt) + (random.random() * 0.5)
                    time.sleep(sleep_time)
        return wrapper
    return decorator

class NetworkResilience:
    def __init__(self, limit=5):
        self.limit = limit
    
    def execute(self, task, *args, **kwargs):
        @retry_network_op(retries=self.limit)
        def run():
            return task(*args, **kwargs)
        return run()