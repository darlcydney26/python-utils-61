from typing import List, Union, Callable, Any

class DataProcessor:
    """Advanced sequence transformation engine with functional piping."""

    def __init__(self, items: List[Any]) -> None:
        self._buffer: List[Any] = items

    def transform(self, pipeline: List[Callable[[Any], Any]]) -> 'DataProcessor':
        """Applies a series of functions to internal data using list comprehension."""
        for step in pipeline:
            self._buffer = [step(item) for item in self._buffer]
        return self

    def filter(self, predicate: Callable[[Any], bool]) -> 'DataProcessor':
        """In-place filtering of elements based on provided boolean condition."""
        self._buffer = [x for x in self._buffer if predicate(x)]
        return self

    def collect(self) -> List[Any]:
        """Final extraction of the processed state."""
        return list(self._buffer)

    @staticmethod
    def compose(func_a: Callable[[Any], Any], func_b: Callable[[Any], Any]) -> Callable[[Any], Any]:
        """Functional composition of two unary operations."""
        return lambda x: func_a(func_b(x))

def process_stream(data: Union[List[int], List[str]]) -> List[Any]:
    """Example workflow for generic input data stream."""
    processor = DataProcessor(data)
    return processor.transform([lambda x: x * 2 if isinstance(x, int) else x.upper()]).collect()