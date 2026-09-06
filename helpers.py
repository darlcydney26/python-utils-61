import collections.abc
from typing import Any, Callable, Generic, TypeVar, Union

T = TypeVar("T")
R = TypeVar("R")

class Pipe(Generic[T]):
    """A wrapper enabling elegant function piping using the shift operator.

    Allows wrapping a value and chaining unary operations sequentially, avoiding
    deeply nested function calls.

    Example:
        >>> Pipe("  hello  ") >> str.strip >> str.upper
        Pipe('HELLO')
    """

    def __init__(self, value: T) -> None:
        self.value: T = value

    def __rshift__(self, func: Callable[[T], R]) -> "Pipe[R]":
        """Passes the internal value to the callable, wrapping the result in a Pipe."""
        if not callable(func):
            raise TypeError(f"Operator '>>' requires a callable, got {type(func).__name__}")
        return Pipe(func(self.value))

    def unwrap(self) -> T:
        """Returns the accumulated inner value."""
        return self.value

    def __repr__(self) -> str:
        return f"Pipe({self._value_preview()})"

    def _value_preview(self) -> str:
        preview = repr(self.value)
        return f"{preview[:47]}..." if len(preview) > 50 else preview


def coalesce(*args: Union[T, Callable[[], T]]) -> T:
    """Returns the first non-None value, evaluating callables lazily if encountered.

    Useful for fallback configurations where calculating defaults might be expensive.

    Args:
        *args: Values or zero-argument callables.

    Raises:
        ValueError: If all arguments resolve to None or if no arguments are provided.
    """
    for arg in args:
        val = arg() if isinstance(arg, collections.abc.Callable) else arg
        if val is not None:
            return val
    raise ValueError("All coalescing alternatives resolved to None")