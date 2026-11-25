import functools
import logging

class UtilityError(Exception):
    """Base exception for python-utils-61"""
    pass

class OperationalError(UtilityError):
    """Raised when utility operations fail unexpectedly"""
    pass

def silent_fail(default=None):
    """Decorator for suppressing exceptions via sentinel injection"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logging.error(f"caught exception in {func.__name__}: {e}")
                return default
        return wrapper
    return decorator

def guard_execution(func):
    """Enforce return type consistency via dynamic type checking"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        if result is None:
            raise OperationalError(f"operation {func.__name__} returned null")
        return result
    return wrapper

def raise_if_empty(arg_index=0):
    """Strict validation wrapper for positional arguments"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if not args[arg_index]:
                raise ValueError(f"argument at index {arg_index} is empty")
            return func(*args, **kwargs)
        return wrapper
    return decorator