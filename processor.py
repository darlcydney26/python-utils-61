import inspect
from typing import Any, Callable, Generator, Generic, Iterable, TypeVar, Union

T = TypeVar("T")
R = TypeVar("R")


class PipeProcessor(Generic[T]):
    """An unconventional stream processor that allows piping with the OR operator.

    Utilizes generator-based pipeline execution and automatic argument unpacking
    via function signature introspection.
    """

    def __init__(self, iterable: Iterable[T]) -> None:
        self.stream: Iterable[T] = iterable

    def __or__(self, func: Callable[..., R]) -> "PipeProcessor[R]":
        """Pipes the current stream elements through the provided function.

        Allows seamless cascading using the bitwise OR operator.
        """
        return PipeProcessor(self._apply(func))

    def _apply(self, func: Callable[..., R]) -> Generator[R, None, None]:
        """Generator applying the callable, automatically unpacking iterables if needed."""
        try:
            sig = inspect.signature(func)
            req_params = sum(
                1
                for p in sig.parameters.values()
                if p.default == inspect.Parameter.empty
                and p.kind
                not in (
                    inspect.Parameter.VAR_POSITIONAL,
                    inspect.Parameter.VAR_KEYWORD,
                )
            )
        except (ValueError, TypeError):
            req_params = 1

        for item in self.stream:
            if req_params > 1 and isinstance(item, (tuple, list)):
                yield func(*item)  # type: ignore
            else:
                yield func(item)

    def consume(self) -> list[T]:
        """Consumes the underlying iterator and returns all elements as a list."""
        return list(self.stream)
