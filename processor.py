"""Stream transformation processor using overloaded pipeline operators."""

from typing import TypeVar, Callable, Iterable, Generator, Generic, Union

T = TypeVar("T")
R = TypeVar("R")
S = TypeVar("S")


class Stage(Generic[T, R]):
    """A single pipeline processing stage wrapping a transformation function."""

    def __init__(self, func: Callable[[T], R]) -> None:
        """Initialize the processing stage with a mapping callable."""
        self._func: Callable[[T], R] = func

    def __call__(self, item: T) -> R:
        """Execute the stage transformation on a single input item."""
        return self._func(item)

    def __rshift__(self, next_stage: Union["Stage[R, S]", Callable[[R], S]]) -> "Stage[T, S]":
        """Compose two stages using the bitwise right-shift operator (>>)."""
        target: Stage[R, S] = next_stage if isinstance(next_stage, Stage) else Stage(next_stage)
        return Stage(lambda item: target(self(item)))


class BatchProcessor(Generic[T, R]):
    """Executes a pipeline stage lazily over an iterable data stream."""

    def __init__(self, pipeline: Stage[T, R]) -> None:
        """Initialize batch processor with a pre-configured pipeline."""
        self.pipeline: Stage[T, R] = pipeline

    def process(self, stream: Iterable[T]) -> Generator[R, None, None]:
        """Process an iterable stream through the pipeline, yielding results.

        Args:
            stream: An iterable sequence of input elements.

        Yields:
            Transformed elements after passing through the pipeline.
        """
        for element in stream:
            yield self.pipeline(element)

    def drain(self, stream: Iterable[T]) -> list[R]:
        """Consume the entire stream immediately and return results as a list."""
        return list(self.process(stream))
