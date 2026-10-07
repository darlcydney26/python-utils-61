import functools
import logging
import time
from typing import Callable, Any

logger = logging.getLogger('python-utils-61')

class Registry:
    _storage = {}

    @classmethod
    def register(cls, name: str):
        def decorator(func: Callable):
            cls._storage[name] = func
            return func
        return decorator

    @classmethod
    def get(cls, name: str) -> Any:
        return cls._storage.get(name)

def retry_on_failure(attempts: int = 3, delay: float = 1.0):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_ex = None
            for i in range(attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_ex = e
                    time.sleep(delay * (2 ** i))
            logger.error(f'failed after {attempts} attempts')
            raise last_ex
        return wrapper
    return decorator

def clean_dict(data: dict) -> dict:
    return {k: v for k, v in data.items() if v is not None}

@Registry.register('noop')
def noop(*args, **kwargs):
    return None