import functools
import collections

def memoize_with_ttl(ttl_seconds=300):
    def decorator(func):
        cache = {}
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = (args, tuple(sorted(kwargs.items())))
            now = __import__('time').time()
            if key in cache:
                val, timestamp = cache[key]
                if now - timestamp < ttl_seconds:
                    return val
            result = func(*args, **kwargs)
            cache[key] = (result, now)
            return result
        return wrapper
    return decorator

class BatchProcessor:
    def __init__(self, size=100):
        self.size = size
        self.buffer = collections.deque()

    def process(self, items, callback):
        for item in items:
            self.buffer.append(item)
            if len(self.buffer) >= self.size:
                callback(list(self.buffer))
                self.buffer.clear()
        if self.buffer:
            callback(list(self.buffer))
            self.buffer.clear()

def fast_flatten(nested_list):
    result = []
    stack = [iter(nested_list)]
    while stack:
        try:
            item = next(stack[-1])
            if isinstance(item, (list, tuple)):
                stack.append(iter(item))
            else:
                result.append(item)
        except StopIteration:
            stack.pop()
    return result