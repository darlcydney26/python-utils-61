import functools
import time

class memoize_with_ttl:
    def __init__(self, ttl_seconds=60):
        self.cache = {}
        self.ttl = ttl_seconds

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = (args, frozenset(kwargs.items()))
            now = time.monotonic()
            if key in self.cache:
                result, timestamp = self.cache[key]
                if now - timestamp < self.ttl:
                    return result
            result = func(*args, **kwargs)
            self.cache[key] = (result, now)
            return result
        return wrapper

def bulk_process(items, func, chunk_size=100):
    for i in range(0, len(items), chunk_size):
        yield from map(func, items[i:i + chunk_size])

def lazy_lookup(generator_factory):
    memo = {}
    def fetch(key):
        if key not in memo:
            memo.update(dict(generator_factory()))
        return memo.get(key)
    return fetch