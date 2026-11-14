import time
import functools
import random

def exponential_backoff(max_retries=3, base_delay=1):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            retries = 0
            while retries < max_retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    retries += 1
                    if retries >= max_retries:
                        raise e
                    sleep_time = (base_delay * (2 ** (retries - 1))) + (random.uniform(0, 1))
                    time.sleep(sleep_time)
            return None
        return wrapper
    return decorator

class NetworkCircuitBreaker:
    def __init__(self, failure_threshold=3, recovery_timeout=30):
        self.threshold = failure_threshold
        self.timeout = recovery_timeout
        self.failures = 0
        self.last_failure_time = 0
        self.state = 'CLOSED'

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if self.state == 'OPEN':
                if time.time() - self.last_failure_time > self.timeout:
                    self.state = 'HALF-OPEN'
                else:
                    raise Exception("circuit breaker is open")
            
            try:
                result = func(*args, **kwargs)
                self.failures = 0
                self.state = 'CLOSED'
                return result
            except Exception as e:
                self.failures += 1
                self.last_failure_time = time.time()
                if self.failures >= self.threshold:
                    self.state = 'OPEN'
                raise e
        return wrapper