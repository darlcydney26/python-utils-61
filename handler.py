from typing import Any, Callable, Dict, List, Union
from functools import reduce

def path_resolver(data: Dict[str, Any], path: str, default: Any = None) -> Any:
    """navigates deep dictionary structures using dot notation"""
    try:
        return reduce(lambda d, k: d.get(k, {}) if isinstance(d, dict) else default, path.split('.'), data)
    except (AttributeError, TypeError):
        return default

def bulk_transformer(data: List[Dict], rules: Dict[str, Callable[[Any], Any]]) -> List[Dict]:
    """applies multiple transformation functions to dictionary collections"""
    def transform(item: Dict) -> Dict:
        return {k: (rules[k](v) if k in rules else v) for k, v in item.items()}
    return [transform(i) for i in data]

class DataFlux:
    """unconventional stateful container for data piping operations"""
    def __init__(self, payload: Any):
        self._payload = payload

    def pipe(self, func: Callable[[Any], Any]) -> 'DataFlux':
        self._payload = func(self._payload)
        return self

    def extract(self) -> Any:
        return self._payload

def flatten_keys(d: Dict, parent_key: str = '', sep: str = '_') -> Dict:
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_keys(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)