import functools
import collections
import time

class PerformanceOptimizer:
    def __init__(self, ttl=60, max_size=128):
        self.ttl = ttl
        self.max_size = max_size
        self._cache = collections.OrderedDict()
        self._expiry = {}

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = (args, frozenset(kwargs.items()))
            now = time.monotonic()
            if key in self._cache and now < self._expiry.get(key, 0):
                return self._cache[key]
            
            result = func(*args, **kwargs)
            
            if len(self._cache) >= self.max_size:
                self._cache.popitem(last=False)
            
            self._cache[key] = result
            self._expiry[key] = now + self.ttl
            return result
        return wrapper

cache_manager = PerformanceOptimizer(ttl=300)

@cache_manager
def heavy_computation(data_node, multiplier=1):
    """Simulated expensive calculation node."""
    time.sleep(0.5)
    return sum(map(lambda x: x * multiplier, data_node))

def batch_process(data_stream):
    results = []
    for chunk in data_stream:
        results.append(heavy_computation(tuple(chunk)))
    return results