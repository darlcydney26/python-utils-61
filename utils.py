import collections
import functools
import itertools

def batcher(iterable, size):
    it = iter(iterable)
    while True:
        chunk = tuple(itertools.islice(it, size))
        if not chunk: break
        yield chunk

def memoize_with_expiry(seconds):
    def decorator(func):
        cache = {}
        @functools.wraps(func)
        def wrapper(*args):
            now = __import__('time').time()
            if args in cache:
                result, timestamp = cache[args]
                if now - timestamp < seconds:
                    return result
            result = func(*args)
            cache[args] = (result, now)
            return result
        return wrapper
    return decorator

def deep_flatten(items):
    for x in items:
        if isinstance(x, collections.abc.Iterable) and not isinstance(x, (str, bytes)):
            yield from deep_flatten(x)
        else:
            yield x

def compose(*functions):
    def compose2(f, g):
        return lambda x: f(g(x))
    return functools.reduce(compose2, functions, lambda x: x)

def pluck(data, key, default=None):
    return [d.get(key, default) if isinstance(d, dict) else getattr(d, key, default) for d in data]