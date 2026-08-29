import time
from functools import wraps, reduce
from collections import defaultdict

def retry_on_failure(max_retries=3, backoff=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception:
                    if attempt < max_retries - 1:
                        time.sleep(backoff * (attempt + 1))
                    else:
                        raise
            return None
        return wrapper
    return decorator

def flatten(items):
    for item in items:
        if isinstance(item, (list, tuple)):
            yield from flatten(item)
        else:
            yield item

def deep_merge(dict1, dict2):
    result = defaultdict(dict)
    for key in set(dict1) | set(dict2):
        if key in dict1 and key in dict2 and isinstance(dict1[key], dict) and isinstance(dict2[key], dict):
            result[key] = deep_merge(dict1[key], dict2[key])
        else:
            result[key] = dict2.get(key, dict1.get(key))
    return dict(result)

def get_nested(data, keys, default=None):
    try:
        return reduce(lambda d, k: d.get(k) if isinstance(d, dict) else None, keys, data) or default
    except (AttributeError, TypeError):
        return default

def unique_preserve_order(seq):
    return list(dict.fromkeys(seq))

def chunked_sequence(seq, size):
    return [seq[i:i + size] for i in range(0, len(seq), size)]
