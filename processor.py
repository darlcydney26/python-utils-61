import functools
from typing import Any, Callable, Dict, List, Union


class Pipe:
    """Infix pipe operator wrapper for concise functional data processing."""

    def __init__(self, func: Callable[..., Any]):
        self.func = func
        functools.update_wrapper(self, func)

    def __ror__(self, other: Any) -> Any:
        if isinstance(other, tuple):
            return self.func(*other)
        return self.func(other)

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        return Pipe(lambda x: self.func(x, *args, **kwargs))


@Pipe
def extract_paths(data: Any, delimiter: str = ".") -> Dict[str, Any]:
    """Flattens a deeply nested dictionary into key paths using recursion."""
    out = {}

    def _walk(obj: Any, prefix: str = ""):
        if isinstance(obj, dict) and obj:
            for key, val in obj.items():
                new_prefix = f"{prefix}{delimiter}{key}" if prefix else str(key)
                _walk(val, new_prefix)
        elif isinstance(obj, (list, tuple)) and obj:
            for idx, val in enumerate(obj):
                new_prefix = f"{prefix}[{idx}]"
                _walk(val, new_prefix)
        else:
            out[prefix] = obj

    _walk(data)
    return out


@Pipe
def sanitize_values(data: Any, fallback: Any = None) -> Any:
    """Recursively replaces None or empty strings with a default fallback."""
    if isinstance(data, dict):
        return {k: sanitize_values(v, fallback) for k, v in data.items()}
    elif isinstance(data, list):
        return [sanitize_values(v, fallback) for v in data]
    elif data is None or data == "":
        return fallback
    return data
