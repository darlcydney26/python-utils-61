import collections
import functools
import itertools

def compose(*functions):
    """functional piping mechanism for data streams"""
    return functools.reduce(lambda f, g: lambda x: g(f(x)), functions)

class Registry(collections.UserDict):
    """dynamic decorator-based component registration system"""
    def register(self, key):
        def wrapper(func):
            self[key] = func
            return func
        return wrapper

    def execute(self, key, *args, **kwargs):
        return self.get(key)(*args, **kwargs)

def flatten(iterable):
    """recursive transformation of nested iterables"""
    for item in iterable:
        if isinstance(item, (list, tuple)):
            yield from flatten(item)
        else:
            yield item

def memoize_with_ttl(ttl=60):
    """cache implementation with expiration logic"""
    def decorator(func):
        cache = {}
        @functools.wraps(func)
        def wrapper(*args):
            import time
            now = time.time()
            if args in cache and now - cache[args][1] < ttl:
                return cache[args][0]
            result = func(*args)
            cache[args] = (result, now)
            return result
        return wrapper
    return decorator

registry = Registry()