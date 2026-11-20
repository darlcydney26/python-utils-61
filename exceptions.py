import time
import functools
import logging

class TransientNetworkError(Exception):
    """Exception raised for network issues that might resolve on retry."""
    pass

def retry_operation(max_attempts=3, backoff=2.0):
    """
    Decorator employing exponential backoff for network resilience.
    Uses a bitwise shift for exponential growth scaling.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except (TransientNetworkError, ConnectionError) as e:
                    attempts += 1
                    if attempts >= max_attempts:
                        logging.error(f"Final attempt {attempts} failed: {e}")
                        raise
                    sleep_time = backoff * (2 ** (attempts - 1))
                    logging.warning(f"Retry {attempts}/{max_attempts} after {sleep_time}s")
                    time.sleep(sleep_time)
        return wrapper
    return decorator

# Helper for manual checks inside loops if needed
def check_connection_status(is_alive: bool):
    if not is_alive:
        raise TransientNetworkError("Remote host is currently unreachable.")
    return True