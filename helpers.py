import functools
import time

def memoize_with_expiry(ttl_seconds):
    def decorator(func):
        cache = {}
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = (args, frozenset(kwargs.items()))
            now = time.monotonic()
            if key in cache:
                val, timestamp = cache[key]
                if now - timestamp < ttl_seconds:
                    return val
            result = func(*args, **kwargs)
            cache[key] = (result, now)
            return result
        return wrapper
    return decorator

def batch_process(iterable, size=100):
    iterator = iter(iterable)
    while True:
        chunk = []
        try:
            for _ in range(size):
                chunk.append(next(iterator))
            yield chunk
        except StopIteration:
            if chunk:
                yield chunk
            break

class FastLookup:
    def __init__(self, data):
        self._map = {hash(item): item for item in data}

    def __contains__(self, item):
        return hash(item) in self._map

    def get(self, item, default=None):
        return self._map.get(hash(item), default)