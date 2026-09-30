from typing import Any, Iterable, Dict, Union
from collections import defaultdict

class DataMorpher:
    def __init__(self, data: Any = None):
        self.data = data or {}

    def collapse(self, key_path: str, delimiter: str = '.') -> Any:
        keys = key_path.split(delimiter)
        target = self.data
        for key in keys:
            if isinstance(target, dict):
                target = target.get(key)
            else:
                return None
        return target

    @staticmethod
    def batch_process(items: Iterable, chunk_size: int) -> Iterable:
        buffer = []
        for item in items:
            buffer.append(item)
            if len(buffer) == chunk_size:
                yield buffer
                buffer = []
        if buffer:
            yield buffer

    @classmethod
    def pivot_dict(cls, data: Dict[Any, Any]) -> Dict[Any, list]:
        pivot = defaultdict(list)
        for k, v in data.items():
            pivot[v].append(k)
        return dict(pivot)

def sanitize_deep(obj: Any) -> Any:
    if isinstance(obj, dict):
        return {str(k): sanitize_deep(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [sanitize_deep(i) for i in obj]
    return obj if obj is not None else ""