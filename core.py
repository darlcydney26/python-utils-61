import collections
import functools
from typing import Any, Callable, Dict, List, Union

def munge(data: Any, path: str, default: Any = None) -> Any:
    """navigates nested structures with dot notation paths"""
    parts = path.split('.')
    for part in parts:
        try:
            if isinstance(data, dict):
                data = data.get(part)
            elif isinstance(data, (list, tuple)):
                data = data[int(part)]
            else:
                return default
        except (KeyError, IndexError, ValueError, TypeError):
            return default
    return data if data is not None else default

def pipeline(data: Any, *funcs: Callable) -> Any:
    """functional composition for data transformation pipelines"""
    return functools.reduce(lambda acc, f: f(acc), funcs, data)

class DataProxy:
    """dynamic attribute access for dictionary objects"""
    def __init__(self, obj: Dict):
        self.__dict__ = obj

    def __repr__(self) -> str:
        return f"DataProxy({self.__dict__})"

def flatten(d: Dict, parent_key: str = '', sep: str = '_') -> Dict:
    """recursive dictionary key flattening"""
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, collections.abc.MutableMapping):
            items.extend(flatten(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)