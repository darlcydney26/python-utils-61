import functools
import time

class memoize_with_ttl:
    def __init__(self, ttl=60):
        self.cache = {}
        self.ttl = ttl
    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = (args, tuple(sorted(kwargs.items())))
            now = time.monotonic()
            if key in self.cache:
                val, timestamp = self.cache[key]
                if now - timestamp < self.ttl:
                    return val
            result = func(*args, **kwargs)
            self.cache[key] = (result, now)
            return result
        return wrapper

def heavy_computation(x, factor=2):
    time.sleep(0.5)
    return x * factor

@memoize_with_ttl(ttl=5)
def optimized_process(data):
    return heavy_computation(data)

def batch_process(items):
    """Vectorized-style application of cached operations."""
    return [optimized_process(i) for i in items]

if __name__ == '__main__':
    # Example usage for performance validation
    start = time.monotonic()
    batch_process([10, 20, 10])
    duration = time.monotonic() - start
    print(f'execution completed in {duration:.4f} seconds')