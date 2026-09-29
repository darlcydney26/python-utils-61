import functools
import collections
import time

class Memoizer:
    def __init__(self, func):
        self.func = func
        self.cache = {}
        self.expiry = {}
        self.ttl = 300

    def __call__(self, *args, **kwargs):
        key = (args, frozenset(kwargs.items()))
        now = time.time()
        if key in self.cache and (now - self.expiry.get(key, 0)) < self.ttl:
            return self.cache[key]
        result = self.func(*args, **kwargs)
        self.cache[key] = result
        self.expiry[key] = now
        return result

def fast_flatten(nested_iterable):
    """Generates flattened sequence using recursive generator delegation."""
    for item in nested_iterable:
        if isinstance(item, (list, tuple, set)):
            yield from fast_flatten(item)
        else:
            yield item

def throughput_monitor(func):
    """Decorator for tracking execution frequency patterns."""
    stats = collections.Counter()
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        stats[func.__name__] += 1
        return func(*args, **kwargs)
    wrapper.stats = stats
    return wrapper

def batch_process(data, chunk_size=1000):
    """Memory-efficient slicing for large data segments."""
    for i in range(0, len(data), chunk_size):
        yield data[i:i + chunk_size]