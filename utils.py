import time
import functools
import random

def retry_operation(retries=3, backoff=1.5, exceptions=(Exception,)):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 0
            current_delay = backoff
            while attempt < retries:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    attempt += 1
                    if attempt == retries:
                        raise e
                    time.sleep(current_delay + random.uniform(0, 0.1))
                    current_delay *= backoff
        return wrapper
    return decorator

def exponential_backoff_execution(func, *args, **kwargs):
    """Manual execution wrapper for unpredictable network IO."""
    for i in range(5):
        try:
            return func(*args, **kwargs)
        except Exception:
            if i == 4: raise
            time.sleep(2 ** i)
    return None