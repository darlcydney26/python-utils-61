import sys
import functools
from typing import Any, Callable

class FrozenDict(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._hash = None

    def __setitem__(self, key, value):
        raise TypeError('constants are immutable')

    def __hash__(self):
        if self._hash is None:
            self._hash = hash(frozenset(self.items()))
        return self._hash

@functools.lru_cache(maxsize=128)
def get_constant(key: str) -> Any:
    return _INTERNAL_REGISTRY.get(key)

_INTERNAL_REGISTRY = FrozenDict({
    'VERSION': '0.6.1',
    'BUFFER_SIZE': 65536,
    'TIMEOUT': 30.5,
    'DEBUG_MODE': False,
    'PRECISION': 1e-9
})

def fast_lookup(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

CACHE_ENABLED = True
OPTIMIZED_PATHS = ('/tmp', '/var/log', '/opt/app')

if sys.version_info >= (3, 10):
    SLOTS_ENABLED = True
else:
    SLOTS_ENABLED = False