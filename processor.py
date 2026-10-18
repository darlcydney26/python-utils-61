from typing import TypeVar, Callable, Iterable, Generator, Generic, Any
from functools import reduce

T = TypeVar("T")
R = TypeVar("R")


class FunctionalPipeline(Generic[T, R]):
    """A dynamic data transformation pipeline with generator-backed execution.
    
    Allows chaining arbitrary transformation functions and processing iterable
    streams in a memory-efficient, lazily-evaluated sequence.
    """

    def __init__(self, *steps: Callable[[Any], Any]) -> None:
        """Initialize the pipeline with a sequence of callable transformations."""
        self._steps: tuple[Callable[[Any], Any], ...] = steps

    def pipe(self, func: Callable[[R], Any]) -> "FunctionalPipeline[T, Any]":
        """Append a new transformation step onto the existing pipeline chain."""
        return FunctionalPipeline(*self._steps, func)

    def __call__(self, source: Iterable[T]) -> Generator[Any, None, None]:
        """Execute pipeline steps over input iterable and yield transformed results."""
        for item in source:
            yield reduce(lambda val, step: step(val), self._steps, item)

    def execute_batch(self, batch: Iterable[T]) -> list[Any]:
        """Run the full pipeline over an iterable batch and return a materialized list."""
        return list(self(batch))
