import functools
from typing import Any, Callable, Dict, List


class Pipe:
    """Lightweight wrapper enabling pipeable function execution via bitwise OR (|)."""

    def __init__(self, func: Callable[..., Any]):
        self.func = func
        functools.update_wrapper(self, func)

    def __ror__(self, other: Any) -> Any:
        if isinstance(other, tuple):
            return self.func(*other)
        return self.func(other)

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        return self.func(*args, **kwargs)


@Pipe
def flatten_dict(data: Dict[str, Any], prefix: str = "", sep: str = ".") -> Dict[str, Any]:
    """Recursively flattens a nested dictionary using key separator."""
    items: List[tuple] = []
    for key, value in data.items():
        new_key = f"{prefix}{sep}{key}" if prefix else str(key)
        if isinstance(value, dict):
            items.extend(flatten_dict(value, prefix=new_key, sep=sep).items())
        else:
            items.append((new_key, value))
    return dict(items)


@Pipe
def chunk_iterable(args: tuple) -> List[List[Any]]:
    """Splits an iterable into fixed-size chunks. Expects (iterable, size)."""
    iterable, chunk_size = args
    lst = list(iterable)
    return [lst[i : i + chunk_size] for i in range(0, len(lst), chunk_size)]


def coalesce(*args: Any, default: Any = None) -> Any:
    """Returns the first non-None argument or the specified default."""
    return next((arg for arg in args if arg is not None), default)


def safe_dig(container: Any, *keys: Any, default: Any = None) -> Any:
    """Safely retrieves a value nested deep within structures without exceptions."""
    current = container
    for key in keys:
        try:
            current = current[key]
        except (KeyError, IndexError, TypeError):
            return default
    return current