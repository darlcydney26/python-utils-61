import time
import random

MAX_RETRY_ATTEMPTS = 5
BASE_DELAY_SECONDS = 0.5
BACKOFF_MULTIPLIER = 2
MAX_DELAY_SECONDS = 30
JITTER_FACTOR = 0.2

def fibonacci_delays(max_attempts, base_delay, max_delay):
    delays = []
    a, b = base_delay, base_delay
    for _ in range(max_attempts):
        delay = min(a, max_delay)
        delays.append(delay)
        a, b = b, a + b
    return delays

def apply_fibonacci_retry(func):
    def wrapper(*args, **kwargs):
        delays = fibonacci_delays(MAX_RETRY_ATTEMPTS, BASE_DELAY_SECONDS, MAX_DELAY_SECONDS)
        last_exception = None
        for attempt in range(MAX_RETRY_ATTEMPTS):
            try:
                result = func(*args, **kwargs)
                return result
            except (ConnectionError, TimeoutError) as e:
                last_exception = e
                if attempt == MAX_RETRY_ATTEMPTS - 1:
                    break
                delay = delays[attempt]
                jitter = delay * JITTER_FACTOR * random.random()
                sleep_time = delay + jitter
                time.sleep(sleep_time)
            except Exception as e:
                raise
        raise last_exception
    return wrapper

def example_network_call(url, fail_until=3):
    if not hasattr(example_network_call, 'calls'):
        example_network_call.calls = 0
    example_network_call.calls += 1
    if example_network_call.calls < fail_until:
        raise ConnectionError(f"Failed to connect to {url} on attempt {example_network_call.calls}")
    return f"Success from {url} after {example_network_call.calls} attempts"

@apply_fibonacci_retry
def retryable_network_call(url):
    return example_network_call(url)

def test_retry_logic():
    example_network_call.calls = 0
    try:
        result = retryable_network_call("https://example.com")
        return result
    except Exception as e:
        return str(e)

def retry_with_custom_handler(operation, max_attempts=MAX_RETRY_ATTEMPTS, delay_gen=None):
    if delay_gen is None:
        delay_gen = fibonacci_delays(max_attempts, BASE_DELAY_SECONDS, MAX_DELAY_SECONDS)
    for attempt, delay in enumerate(delay_gen):
        try:
            return operation()
        except Exception as exc:
            if attempt >= max_attempts - 1:
                raise
            errors = getattr(retry_with_custom_handler, 'errors', [])
            errors.append((attempt, str(exc), delay))
            retry_with_custom_handler.errors = errors
            time.sleep(delay)
    return None

RETRYABLE_ERRORS = (ConnectionError, TimeoutError, OSError)
DEFAULT_TIMEOUT = 10