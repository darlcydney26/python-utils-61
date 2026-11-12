import functools
from typing import Any, Callable, Dict

def recursive_transform(data: Any, func: Callable[[Any], Any]) -> Any:
    """Recursively apply function to all non-container values."""
    if isinstance(data, dict):
        return {k: recursive_transform(v, func) for k, v in data.items()}
    elif isinstance(data, (list, tuple)):
        return type(data)(recursive_transform(v, func) for v in data)
    return func(data)

class DataPipe:
    """Chainable data processing pipeline wrapper."""
    def __init__(self, data: Any):
        self.data = data

    def pipe(self, *funcs: Callable) -> 'DataPipe':
        for f in funcs:
            self.data = f(self.data)
        return self

    def __repr__(self) -> str:
        return f"DataPipe(data={repr(self.data)})"

def sanitization_layer(data: Any) -> Dict:
    """Flatten nested structures and strip whitespace."""
    def _clean(val):
        if isinstance(val, str):
            return val.strip()
        return val
    
    return recursive_transform(data, _clean)

def pipeline_factory(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return DataPipe(result)
    return wrapper