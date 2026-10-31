import time
import functools
import random

def retry(max_attempts=3, delay=1.0, backoff=2.0, exceptions=(Exception,)):
    """Exponential backoff decorator for resilient network calls."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            current_delay = delay
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    if attempt == max_attempts - 1:
                        raise e
                    
                    jitter = random.uniform(0, 0.1 * current_delay)
                    time.sleep(current_delay + jitter)
                    current_delay *= backoff
            return None
        return wrapper
    return decorator

def execute_with_fallback(func, fallback_value=None, *args, **kwargs):
    """Functional retry wrapper with static fallback."""
    try:
        return func(*args, **kwargs)
    except Exception:
        return fallback_value

# Usage example for the project:
# @retry(max_attempts=5, exceptions=(ConnectionError, TimeoutError))
# def fetch_data(url):
#     pass