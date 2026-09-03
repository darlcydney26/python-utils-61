from typing import Any, Callable, TypeVar, Optional, Dict

T = TypeVar('T')

class DataPipe:
    """A minimalist pipeline for data transformation."""

    def __init__(self, initial_data: Any) -> None:
        self._data: Any = initial_data

    def pipe(self, func: Callable[[Any], T]) -> 'DataPipe':
        """Applies a transformation function to current state."""
        self._data = func(self._data)
        return self

    def extract(self) -> Any:
        """Returns the processed data result."""
        return self._data

def batch_process(items: list[Any], transform: Callable[[Any], T]) -> list[T]:
    """Functional batch processor for iterative sequences."""
    return [transform(i) for i in items]

class ConfigRegistry:
    """A dictionary-like registry with lazy access."""

    def __init__(self) -> None:
        self._storage: Dict[str, Any] = {}

    def register(self, key: str, value: Any) -> None:
        """Persists a new configuration entry."""
        self._storage[key] = value

    def get(self, key: str, default: Optional[Any] = None) -> Any:
        """Retrieves value or returns fallback constant."""
        return self._storage.get(key, default)
