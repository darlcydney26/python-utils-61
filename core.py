import functools
import time
import collections

class memoize_with_ttl:
    def __init__(self, ttl=60):
        self.ttl = ttl
        self.cache = {}
        self.expiry = {}

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = (args, tuple(sorted(kwargs.items())))
            now = time.time()
            if key in self.cache and now < self.expiry.get(key, 0):
                return self.cache[key]
            result = func(*args, **kwargs)
            self.cache[key] = result
            self.expiry[key] = now + self.ttl
            return result
        return wrapper

class DataProcessor:
    def __init__(self):
        self._buffer = collections.deque(maxlen=1000)

    @memoize_with_ttl(ttl=30)
    def process_heavy_computation(self, data: int) -> int:
        return sum(i * i for i in range(data))

    def batch_process(self, data_points):
        return [self.process_heavy_computation(d) for d in data_points]

    def flush_memory(self):
        self._buffer.clear()
        self.process_heavy_computation.cache.clear()
        self.process_heavy_computation.expiry.clear()