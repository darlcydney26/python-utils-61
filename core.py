import functools
import itertools
import operator

def deep_get(data, keys, default=None):
    """Access nested dictionaries using a dot-notation string."""
    return functools.reduce(lambda d, k: d.get(k, {}) if isinstance(d, dict) else default, keys.split('.'), data) or default

def chunker(iterable, size):
    """Yield successive chunks from an iterable."""
    it = iter(iterable)
    return iter(lambda: list(itertools.islice(it, size)), [])

def compose(*functions):
    """Functional composition of arbitrary callables."""
    return functools.reduce(lambda f, g: lambda x: f(g(x)), functions, lambda x: x)

def memoize_method(func):
    """Method-specific caching using instance dict."""
    cache_name = f'_{func.__name__}_cache'
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        if not hasattr(self, cache_name):
            setattr(self, cache_name, {})
        cache = getattr(self, cache_name)
        key = (args, tuple(sorted(kwargs.items())))
        if key not in cache:
            cache[key] = func(self, *args, **kwargs)
        return cache[key]
    return wrapper

def flatten(nested):
    """Recursively collapse nested iterables."""
    for item in nested:
        if isinstance(item, (list, tuple)):
            yield from flatten(item)
        else:
            yield item