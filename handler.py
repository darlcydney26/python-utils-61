import functools
import time

class MemoizationEngine:
    def __init__(self, capacity=128):
        self.cache = {}
        self.capacity = capacity

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = (args, tuple(sorted(kwargs.items())))
            if key not in self.cache:
                if len(self.cache) >= self.capacity:
                    self.cache.pop(next(iter(self.cache)))
                self.cache[key] = func(*args, **kwargs)
            return self.cache[key]
        return wrapper

@MemoizationEngine(capacity=256)
def fast_compute_heavy_logic(n: int) -> int:
    result = 0
    for i in range(n):
        result += i ** 2
    return result

def execute_task(data_points: list):
    start = time.perf_counter()
    results = [fast_compute_heavy_logic(x) for x in data_points]
    duration = time.perf_counter() - start
    return {'results': results, 'meta': {'latency': duration, 'cached': True}}