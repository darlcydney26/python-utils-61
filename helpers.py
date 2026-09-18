import functools
import time
import inspect

def functional_pipe(data, *functions):
    return functools.reduce(lambda v, f: f(v), functions, data)

def memoize_with_expiry(ttl=60):
    def decorator(func):
        cache = {}
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = (args, frozenset(kwargs.items()))
            now = time.time()
            if key in cache:
                val, timestamp = cache[key]
                if now - timestamp < ttl:
                    return val
            result = func(*args, **kwargs)
            cache[key] = (result, now)
            return result
        return wrapper
    return decorator

def extract_signature_map(func):
    params = inspect.signature(func).parameters
    return {name: p.annotation for name, p in params.items()}

class Chainable:
    def __init__(self, value):
        self.value = value
    def pipe(self, func):
        return Chainable(func(self.value))
    def unwrap(self):
        return self.value

def flatten_nested_dict(d, parent_key='', sep='_'):
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_nested_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)