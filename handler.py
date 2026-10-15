import collections
import functools
import itertools

def deep_flatten(items):
    """Flatten nested iterables with recursive yield."""
    for x in items:
        if isinstance(x, (list, tuple, set)):
            yield from deep_flatten(x)
        else:
            yield x

def batch_process(iterable, size):
    """Chunking strategy for memory-efficient iteration."""
    it = iter(iterable)
    return iter(lambda: tuple(itertools.islice(it, size)), ())

def memoize_with_expiry(ttl=60):
    """Caching decorator with basic temporal expiration."""
    def decorator(func):
        cache = {}
        @functools.wraps(func)
        def wrapper(*args):
            import time
            now = time.time()
            if args in cache:
                result, timestamp = cache[args]
                if now - timestamp < ttl:
                    return result
            result = func(*args)
            cache[args] = (result, now)
            return result
        return wrapper
    return decorator

def pluck(data, key, default=None):
    """Dot-notation path extraction for dict hierarchies."""
    return functools.reduce(
        lambda d, k: d.get(k, {}) if isinstance(d, dict) else default,
        key.split('.'),
        data
    ) or default