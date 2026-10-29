"""Functional pipeline utilities for chaining data transformations."""

from functools import reduce
from typing import Any, Callable, Generic, TypeVar

T = TypeVar("T")
R = TypeVar("R")


class Pipe(Generic[T]):
    """A creative wrapper allowing infix pipelines using the '>>' operator.

    Example:
        >>> Pipe([1, 2, 3]) >> (lambda x: [i * 2 for i in x]) >> sum
        12
    """

    __slots__ = ("_value",)

    def __init__(self, value: T) -> None:
        """Initialize the pipeline container with an initial value."""
        self._value: T = value

    def __rshift__(self, func: Callable[[T], R]) -> "Pipe[R]":
        """Pass the current pipeline value into the provided function."""
        return Pipe[R](func(self._value))

    def unwrap(self) -> T:
        """Extract and return the underlying transformed value."""
        return self._value

    def __repr__(self) -> str:
        return f"Pipe({self._value!r})"


def compose(*funcs: Callable[[Any], Any]) -> Callable[[Any], Any]:
    """Compose multiple functions right-to-left into a single function.

    Args:
        *funcs: Functions to compose together.

    Returns:
        A new function representing the composed operations.
    """
    return reduce(lambda f, g: lambda x: f(g(x)), funcs, lambda x: x)


def tap(action: Callable[[T], None]) -> Callable[[T], T]:
    """Create a side-effect function that inspects a value and returns it.

    Args:
        action: A callable invoked with the current item for side effects.

    Returns:
        A function that executes the action and returns the input unaltered.
    """
    def _inspector(val: T) -> T:
        action(val)
        return val
    return _inspector
