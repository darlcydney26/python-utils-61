from typing import Any, Callable, List, Tuple, Union
import functools


class Pipe:
    """A pipeline utility wrapping data for chained function execution via bitwise operators."""

    def __init__(self, value: Any) -> None:
        self.value = value

    def __rshift__(self, func: Callable[..., Any]) -> "Pipe":
        """Overloads >> operator to pass current value into a single-arg function."""
        return Pipe(func(self.value))

    def __or__(self, target: Union[Callable[..., Any], Tuple[Callable[..., Any], Any]]) -> "Pipe":
        """Overloads | operator to allow functions with positional arguments."""
        if isinstance(target, tuple):
            func, *args = target
            return Pipe(func(self.value, *args))
        return Pipe(target(self.value))

    def unwrap(self) -> Any:
        """Extract the inner transformed value."""
        return self.value


def safe_get(data: Any, path: str, default: Any = None) -> Any:
    """Safely query nested dictionaries or lists using dot notation (e.g. 'users.0.name')."""
    try:
        for key in path.split("."):
            if isinstance(data, list) and key.isdigit():
                data = data[int(key)]
            elif isinstance(data, dict):
                data = data[key]
            elif hasattr(data, key):
                data = getattr(data, key)
            else:
                return default
        return data
    except (IndexError, KeyError, TypeError, AttributeError):
        return default


def auto_batch(size: int) -> Callable:
    """Decorator that splits iterable inputs into fixed chunks before batch processing."""
    def decorator(func: Callable[[List[Any]], Any]) -> Callable:
        @functools.wraps(func)
        def wrapper(iterable: Any, *args: Any, **kwargs: Any) -> List[Any]:
            items = list(iterable)
            chunks = [items[i : i + size] for i in range(0, len(items), size)]
            return [func(chunk, *args, **kwargs) for chunk in chunks]
        return wrapper
    return decorator