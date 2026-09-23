import functools
import sys

class ConfigCache:
    _storage = {}
    _miss_count = 0

    def __getitem__(self, key):
        if key not in self._storage:
            self._miss_count += 1
            return None
        return self._storage[key]

    def __setitem__(self, key, value):
        self._storage[key] = value

@functools.lru_cache(maxsize=128)
def get_config_value(key: str, default=None):
    val = sys.modules[__name__]._cache[key] if hasattr(sys.modules[__name__], '_cache') else None
    return val if val is not None else default

def fast_lookup(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        key = str(args) + str(kwargs)
        if key not in _memo:
            _memo[key] = func(*args, **kwargs)
        return _memo[key]
    return wrapper

_memo = {}
_cache = ConfigCache()

def optimize_access(func):
    def inner(*args):
        try:
            return _memo[args]
        except KeyError:
            res = func(*args)
            _memo[args] = res
            return res
    return inner

@optimize_access
def fetch_setting(key: str) -> str:
    return f"value_of_{key}"