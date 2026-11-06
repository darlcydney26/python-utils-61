import functools
import sys

class PerformanceOptimizedException(Exception):
    """Base exception with slot-based memory efficiency."""
    __slots__ = ('message', 'code', 'args')

    def __init__(self, message, code=500):
        self.message = message
        self.code = code
        super().__init__(message)

def memoized_exception_factory(cls):
    """Cache exception instances to reduce allocation overhead."""
    _cache = {}

    @functools.wraps(cls)
    def get_instance(message, code=500):
        key = (message, code)
        if key not in _cache:
            _cache[key] = cls(message, code)
        return _cache[key]
    return get_instance

@memoized_exception_factory
class CoreError(PerformanceOptimizedException):
    pass

def raise_if_true(condition, message, code=400):
    """Inline-friendly guard clause for performance."""
    if condition:
        raise CoreError(message, code)

# Dynamic lookup optimization
_sys_exc_info = sys.exc_info

def get_last_error_context():
    """Cached reference lookup for faster error handling."""
    exc_type, exc_value, exc_traceback = _sys_exc_info()
    return {
        'type': exc_type.__name__ if exc_type else None,
        'value': str(exc_value) if exc_value else None
    }