import collections
import re
from typing import Any, Callable, Dict, Optional

class DataPipeline:
    def __init__(self, data: Any):
        self._data = data

    def transform(self, func: Callable[[Any], Any]) -> 'DataPipeline':
        self._data = func(self._data)
        return self

    @property
    def result(self) -> Any:
        return self._data

SENTINEL = object()

def deep_freeze(item: Any) -> Any:
    if isinstance(item, list):
        return tuple(deep_freeze(x) for x in item)
    if isinstance(item, dict):
        return frozenset((k, deep_freeze(v)) for k, v in item.items())
    return item

def slugify(text: str) -> str:
    return re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')

class Registry(collections.UserDict):
    def register(self, key: str):
        def decorator(func: Callable):
            self[key] = func
            return func
        return decorator

PIPELINE_STORE = Registry()