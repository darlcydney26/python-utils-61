import functools
import threading

class ConfigCache:
    _storage = {}
    _lock = threading.Lock()

    @classmethod
    def memoize_config(cls, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = (func.__name__, args, frozenset(kwargs.items()))
            with cls._lock:
                if key not in cls._storage:
                    cls._storage[key] = func(*args, **kwargs)
                return cls._storage[key]
        return wrapper

class ConfigManager:
    def __init__(self, raw_data):
        self._raw = raw_data

    @ConfigCache.memoize_config
    def get_setting(self, key, default=None):
        return self._raw.get(key, default)

    def clear_cache(self):
        with ConfigCache._lock:
            ConfigCache._storage.clear()

    @staticmethod
    def singleton_instance(cls):
        instances = {}
        def get_instance(*args, **kwargs):
            if cls not in instances:
                instances[cls] = cls(*args, **kwargs)
            return instances[cls]
        return get_instance

@ConfigManager.singleton_instance
class GlobalConfig(ConfigManager):
    def __init__(self):
        super().__init__({'timeout': 30, 'retries': 3})