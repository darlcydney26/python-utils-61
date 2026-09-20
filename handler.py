import os
from functools import lru_cache
from typing import Any, Callable, Dict

class DataHandler:
    def __init__(self, storage_path: str = '/tmp/cache'):
        self.storage = storage_path
        self.registry: Dict[str, Callable] = {}

    def register(self, key: str):
        def decorator(func: Callable):
            self.registry[key] = func
            return func
        return decorator

    @lru_cache(maxsize=128)
    def execute(self, key: str, *args: Any, **kwargs: Any) -> Any:
        if key not in self.registry:
            raise ValueError(f'Handler for {key} not registered')
        return self.registry[key](*args, **kwargs)

    def purge_storage(self):
        if os.path.exists(self.storage):
            for file in os.listdir(self.storage):
                os.remove(os.path.join(self.storage, file))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.purge_storage()

def get_handler_instance():
    return DataHandler()