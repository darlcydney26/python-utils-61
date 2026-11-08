import functools
from typing import Any, Callable, Dict, Union

class DataPipe:
    """An unconventional pipeline for chaining data transformations."""
    def __init__(self, value: Any):
        self.value = value

    def __or__(self, func: Callable) -> 'DataPipe':
        return DataPipe(func(self.value))

    def __repr__(self):
        return f"DataPipe({self.value})"

def transform_dict(data: Dict[str, Any], key_map: Dict[str, str]) -> Dict[str, Any]:
    """Maps dict keys using a provided translation schema."""
    return {key_map.get(k, k): v for k, v in data.items()}

def sanitize_input(val: Union[str, int]) -> str:
    """Force cast to lowercase string and strip whitespace."""
    return str(val).lower().strip()

def batch_process(items: list, transformer: Callable) -> list:
    """Functional processing wrapper for iterables."""
    return list(map(transformer, items))

def registry_factory():
    """Closure-based state storage for handling data."""
    storage = {}
    def register(key: str, val: Any):
        storage[key] = val
    def get_all():
        return storage
    return register, get_all