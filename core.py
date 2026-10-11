import functools
from typing import Any, Callable, Dict, List, TypeVar

T = TypeVar('T')
U = TypeVar('U')

class Pipe:
    """Fluent data processing pipeline using bitwise right-shift operator."""
    def __init__(self, value: Any) -> None:
        self.value = value

    def __rshift__(self, func: Callable[[Any], Any]) -> 'Pipe':
        if callable(func):
            return Pipe(func(self.value))
        return self

    def unwrap(self) -> Any:
        return self.value

    def __repr__(self) -> str:
        return f"Pipe({self.value!r})"

def deep_get(data: Dict[str, Any], path: str, default: Any = None) -> Any:
    """Retrieve nested value using dot-separated path."""
    keys = path.split('.')
    curr: Any = data
    for k in keys:
        if isinstance(curr, dict) and k in curr:
            curr = curr[k]
        else:
            return default
    return curr

def chunkify(items: List[T], size: int) -> List[List[T]]:
    """Split a sequence into fixed-size chunks."""
    if size <= 0:
        raise ValueError("Chunk size must be greater than zero")
    return [items[i:i + size] for i in range(0, len(items), size)]

def safe_cast(val: Any, target_type: type, default: Any = None) -> Any:
    """Attempt type conversion with fallback default."""
    try:
        return target_type(val)
    except (ValueError, TypeError):
        return default
