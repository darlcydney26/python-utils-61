from typing import Any, Callable, Union

class DataNavigator:
    """Fluid wrapper for navigating and mutating arbitrary nested structures."""

    def __init__(self, data: Any) -> None:
        self._data = data

    @property
    def value(self) -> Any:
        return self._data

    def __rshift__(self, target: Union[str, Callable[[Any], Any]]) -> "DataNavigator":
        if callable(target):
            return DataNavigator(target(self._data))
        return DataNavigator(self._resolve_path(self._data, str(target)))

    def _resolve_path(self, obj: Any, path: str) -> Any:
        for key in path.split("."):
            if not key or obj is None:
                continue
            if isinstance(obj, dict):
                obj = obj.get(key)
            elif isinstance(obj, (list, tuple)) and key.isdigit():
                idx = int(key)
                obj = obj[idx] if -len(obj) <= idx < len(obj) else None
            else:
                obj = getattr(obj, key, None)
        return obj

    def apply(self, func: Callable[[Any], Any]) -> "DataNavigator":
        return DataNavigator(func(self._data))

    def unwrap(self, fallback: Any = None) -> Any:
        return fallback if self._data is None else self._data


def fluent_query(data: Any, *steps: Union[str, Callable[[Any], Any]], default: Any = None) -> Any:
    """Queries complex data structures using mixed dot-paths and transform functions."""
    nav = DataNavigator(data)
    for step in steps:
        nav = nav >> step
    return nav.unwrap(default)
