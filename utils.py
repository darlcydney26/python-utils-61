"""General helper utilities with functional and dynamic capabilities."""

from functools import reduce
from itertools import islice
from typing import Any, Callable, Iterable, Iterator, Optional, Tuple


def dig(target: Any, path: str, default: Any = None, sep: str = ".") -> Any:
    """Traverse nested structures (dicts, lists, objects) using dot paths."""
    curr = target
    for key in path.split(sep):
        if curr is None:
            return default
        if isinstance(curr, dict):
            curr = curr.get(key, default)
        elif isinstance(curr, (list, tuple)) and key.isdigit():
            idx = int(key)
            curr = curr[idx] if 0 <= idx < len(curr) else default
        elif hasattr(curr, key):
            curr = getattr(curr, key, default)
        else:
            return default
    return curr


def chunkify(iterable: Iterable[Any], size: int) -> Iterator[Tuple[Any, ...]]:
    """Yield n-sized chunks lazily using an iterative sentinel pattern."""
    if size < 1:
        raise ValueError("Chunk size must be at least 1")
    iterator = iter(iterable)
    return iter(lambda: tuple(islice(iterator, size)), ())


def flatten(container: Iterable[Any]) -> Iterator[Any]:
    """Recursively flatten arbitrarily nested iterables excluding text/bytes."""
    for item in container:
        if isinstance(item, (list, tuple, set)) and not isinstance(item, (str, bytes)):
            yield from flatten(item)
        else:
            yield item


def coalesce(*args: Any, predicate: Optional[Callable[[Any], bool]] = None) -> Any:
    """Return first argument satisfying predicate (defaults to non-None)."""
    check = predicate or (lambda x: x is not None)
    return next((arg for arg in args if check(arg)), None)


def pipe(value: Any, *funcs: Callable[[Any], Any]) -> Any:
    """Pass an initial value sequentially through transformation pipeline."""
    return reduce(lambda acc, fn: fn(acc), funcs, value)
