import functools
import time
import collections

class MemoizedProcessor:
    def __init__(self, limit=1024):
        self.cache = collections.OrderedDict()
        self.limit = limit

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = (args, frozenset(kwargs.items()))
            if key in self.cache:
                self.cache.move_to_end(key)
                return self.cache[key]
            
            result = func(*args, **kwargs)
            self.cache[key] = result
            self.cache.move_to_end(key)
            
            if len(self.cache) > self.limit:
                self.cache.popitem(last=False)
            return result
        return wrapper

class CoreHandler:
    """Optimized handler using LRU caching strategy."""
    @MemoizedProcessor(limit=512)
    def compute_heavy_task(self, data_point: int) -> int:
        # Simulate intensive computation
        time.sleep(0.01)
        return data_point ** 2 + (data_point % 7)

    def batch_process(self, data_list: list) -> list:
        return [self.compute_heavy_task(x) for x in data_list]

if __name__ == '__main__':
    handler = CoreHandler()
    results = handler.batch_process([1, 2, 3, 1, 2])
    print(f"Processed results: {results}")