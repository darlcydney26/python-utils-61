import functools
import sys

class PerformanceCachedException(Exception):
    """Exception with optimized metadata storage using __slots__."""
    __slots__ = ('message', 'payload', '_cached_repr')
    
    def __init__(self, message, payload=None):
        self.message = message
        self.payload = payload
        self._cached_repr = None

    def __repr__(self):
        if self._cached_repr is None:
            self._cached_repr = f"Error({self.message!r}, {self.payload!r})"
        return self._cached_repr

def fast_exception_handler(func):
    """Decorator utilizing memoized error state for rapid access."""
    cache = {}
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        key = (args, tuple(kwargs.items()))
        if key not in cache:
            try:
                cache[key] = func(*args, **kwargs)
            except Exception as e:
                cache[key] = e
                raise e
        val = cache[key]
        if isinstance(val, Exception):
            raise val
        return val
    return wrapper

class ExceptionRegistry:
    """Global registry using dictionary lookups for instant resolution."""
    _registry = {}

    @classmethod
    def register(cls, name, exc_cls):
        cls._registry[name] = exc_cls

    @classmethod
    def get(cls, name):
        return cls._registry.get(name, Exception)

ExceptionRegistry.register("critical", PerformanceCachedException)