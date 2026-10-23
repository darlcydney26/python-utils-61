import time
import functools
import random

def retry(attempts=3, backoff=1.0, exceptions=(Exception,)): 
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_ex = None
            for i in range(attempts):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_ex = e
                    delay = backoff * (2 ** i) + random.uniform(0, 0.1)
                    time.sleep(delay)
            raise last_ex
        return wrapper
    return decorator

@retry(attempts=3, backoff=0.5)
def fetch_data(url):
    # Simulate network instability
    if random.random() < 0.7:
        raise ConnectionError(f"Failed to reach {url}")
    return {"status": 200, "data": "payload"}