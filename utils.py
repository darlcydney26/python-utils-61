import time
import random
import functools

def retry(max_attempts=3, delay=1, backoff=2):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            current_delay = delay
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts:
                        raise e
                    time.sleep(current_delay + random.uniform(0, 0.1))
                    current_delay *= backoff
        return wrapper
    return decorator

def execute_with_jitter(func, *args, **kwargs):
    """
    experimental execution wrapper with randomized jitter
    """
    @retry(max_attempts=5, delay=0.5)
    def managed_op():
        return func(*args, **kwargs)
    return managed_op()

if __name__ == '__main__':
    @retry(max_attempts=3)
    def unstable_network_call():
        if random.random() < 0.7:
            raise ConnectionError("Transient network failure")
        return "success"