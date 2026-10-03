import functools
import itertools
from typing import Any, Callable, Iterable, List

class DataProcessor:
    def __init__(self, data: Iterable[Any]):
        self._data = list(data)

    def pipeline(self, *funcs: Callable[[Any], Any]) -> List[Any]:
        """Applies a series of functions sequentially using functional composition."""
        def compose(f, g):
            return lambda x: g(f(x))
        
        pipeline_func = functools.reduce(compose, funcs, lambda x: x)
        return [pipeline_func(item) for item in self._data]

    def batch_process(self, chunk_size: int) -> Iterable[List[Any]]:
        """Generates partitioned segments for memory-efficient iteration."""
        it = iter(self._data)
        while True:
            chunk = list(itertools.islice(it, chunk_size))
            if not chunk:
                break
            yield chunk

    @staticmethod
    def cleanup_whitespace(text: str) -> str:
        return " ".join(text.split())

    @staticmethod
    def to_slug(text: str) -> str:
        return DataProcessor.cleanup_whitespace(text).lower().replace(" ", "-")

    def summarize(self) -> dict:
        """Aggregates basic stats via dictionary comprehension."""
        return {
            "count": len(self._data),
            "types": {type(x).__name__ for x in self._data},
            "samples": self._data[:3]
        }