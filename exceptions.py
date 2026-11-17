import sys
import functools
import traceback

class UtilityError(Exception):
    """Base exception for python-utils-61."""
    pass

def graceful_recovery(fallback_value=None):
    """Decorator for suppressing exceptions with optional fallback."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                sys.stderr.write(f"[!] Caught {type(e).__name__} in {func.__name__}: {e}\n")
                return fallback_value
        return wrapper
    return decorator

def error_chaining(message):
    """Custom error raiser for strict control flow."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                raise UtilityError(f"{message}: {str(e)}") from e
        return wrapper
    return decorator

class EdgeCaseHandler:
    def __init__(self, critical=False):
        self.critical = critical

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            if self.critical:
                traceback.print_exception(exc_type, exc_val, exc_tb)
                sys.exit(1)
            return True
        return False