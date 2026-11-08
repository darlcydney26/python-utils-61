import functools
from typing import Any, Callable, TypeVar, Dict

T = TypeVar('T')

class DataMunger:
    """An unconventional approach to recursive data manipulation."""
    def __init__(self, data: Any):
        self._data = data

    def morph(self, func: Callable[[Any], Any]) -> 'DataMunger':
        if isinstance(self._data, dict):
            self._data = {k: self._walk(v, func) for k, v in self._data.items()}
        elif isinstance(self._data, list):
            self._data = [self._walk(v, func) for v in self._data]
        else:
            self._data = func(self._data)
        return self

    def _walk(self, val: Any, func: Callable) -> Any:
        if isinstance(val, dict):
            return {k: self._walk(v, func) for k, v in val.items()}
        if isinstance(val, list):
            return [self._walk(v, func) for v in val]
        return func(val)

    def reveal(self) -> Any:
        return self._data

def flexible_processor(transform_map: Dict[type, Callable]) -> Callable:
    """Higher-order function for type-specific data transformation."""
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            if type(result) in transform_map:
                return transform_map[type(result)](result)
            return result
        return wrapper
    return decorator