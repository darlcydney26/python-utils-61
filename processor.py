import functools
import itertools
from typing import Callable, Iterable, Any, TypeVar

T = TypeVar('T')
R = TypeVar('R')

class Pipeline:
    """A lightweight functional pipeline wrapper for chaining operations."""
    def __init__(self, data: Iterable[Any]):
        self._data = data

    def pipe(self, func: Callable[[Iterable[Any]], Iterable[Any]]) -> 'Pipeline':
        return Pipeline(func(self._data))

    def map(self, func: Callable[[Any], Any]) -> 'Pipeline':
        return Pipeline(map(func, self._data))

    def filter(self, predicate: Callable[[Any], bool]) -> 'Pipeline':
        return Pipeline(filter(predicate, self._data))

    def collect(self) -> list:
        return list(self._data)


def chunk_stream(iterable: Iterable[T], size: int) -> Iterable[tuple[T, ...]]:
    """Yield successive n-sized chunks from an iterable."""
    it = iter(iterable)
    while chunk := tuple(itertools.islice(it, size)):
        yield chunk


def auto_retry_batch(batch_func: Callable[[list[T]], R], retries: int = 3) -> Callable[[list[T]], R]:
    """Decorator to retry failing batch processing operations."""
    @functools.wraps(batch_func)
    def wrapper(items: list[T]) -> R:
        last_err = None
        for _ in range(retries):
            try:
                return batch_func(items)
            except Exception as e:
                last_err = e
        raise RuntimeError(f"Batch processing failed after {retries} attempts") from last_err
    return wrapper


def deep_flatten(nested_iterable: Iterable[Any]) -> Iterable[Any]:
    """Recursively flatten arbitrarily nested iterables excluding strings."""
    for item in nested_iterable:
        if isinstance(item, Iterable) and not isinstance(item, (str, bytes)):
            yield from deep_flatten(item)
        else:
            yield item
