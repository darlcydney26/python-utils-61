import functools
import time
import itertools

def retry_with_backoff(retries=3, delay=1):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(retries):
                try:
                    return func(*args, **kwargs)
                except Exception:
                    if attempt == retries - 1: raise
                    time.sleep(delay * (2 ** attempt))
        return wrapper
    return decorator

def chunker(iterable, size):
    it = iter(iterable)
    return iter(lambda: tuple(itertools.islice(it, size)), ())

def flatten(nested_iterable):
    for item in nested_iterable:
        if isinstance(item, (list, tuple, set)):
            yield from flatten(item)
        else:
            yield item

def compose(*functions):
    def inner(arg):
        return functools.reduce(lambda acc, f: f(acc), functions, arg)
    return inner

def memoize_with_expiry(timeout=60):
    cache = {}
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args):
            now = time.time()
            if args in cache and (now - cache[args]['time'] < timeout):
                return cache[args]['value']
            result = func(*args)
            cache[args] = {'value': result, 'time': now}
            return result
        return wrapper
    return decorator