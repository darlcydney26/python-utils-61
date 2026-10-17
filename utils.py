import time
import functools
import random

def resilient(retries=3, backoff=0.5, exceptions=(Exception,)):
    """Decorator implementing exponential backoff with jitter."""
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
                    delay = (backoff * (2 ** (attempt - 1))) + (random.uniform(0, 0.1))
                    time.sleep(delay)
            return None
        return wrapper
    return decorator

class NetworkHandler:
    """Utility class for network operation wrappers."""
    @staticmethod
    def execute(operation, *args, **kwargs):
        decorator = resilient(retries=3, backoff=1.0)
        return decorator(operation)(*args, **kwargs)