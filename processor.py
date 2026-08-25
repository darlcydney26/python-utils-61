from functools import lru_cache
from collections import deque

class Processor:
    __slots__ = ['cache', 'max_cache_size', 'window_size']

    def __init__(self, max_cache_size=512, window_size=50):
        self.cache = {}
        self.max_cache_size = max_cache_size
        self.window_size = window_size

    @lru_cache(maxsize=256)
    def _compute(self, x):
        if x < 0:
            x = -x
        return sum(i**2 for i in range(min(x, 100))) + x % 7

    def process_item(self, item):
        if item in self.cache:
            return self.cache[item]
        result = self._compute(item)
        if len(self.cache) >= self.max_cache_size:
            self.cache.pop(next(iter(self.cache)))
        self.cache[item] = result
        return result

    def process_list(self, items):
        if not items:
            return []
        results = [self.process_item(item) for item in items]
        window = deque(maxlen=self.window_size)
        smoothed = []
        for val in results:
            window.append(val)
            if len(window) == self.window_size:
                avg = sum(window) / self.window_size
                smoothed.append(avg)
            else:
                smoothed.append(val)
        return smoothed

    def process_large_data(self, data_stream):
        chunk_size = 1000
        for i in range(0, len(data_stream), chunk_size):
            chunk = data_stream[i:i + chunk_size]
            yield self.process_list(chunk)

def optimize_processing(data):
    proc = Processor()
    return list(proc.process_large_data(data))