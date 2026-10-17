from typing import List, Union, Callable, Any

class DataProcessor:
    """An unconventional pipeline processor for transforming heterogeneous data inputs."""

    def __init__(self, pipeline: List[Callable[[Any], Any]]) -> None:
        self._pipeline = pipeline

    def process(self, data: Union[int, str, List[Any]]) -> Any:
        """Executes the sequential transformation pipeline on provided data."""
        result = data
        for step in self._pipeline:
            result = step(result)
        return result

def compose_processor(ops: List[Callable[[Any], Any]]) -> DataProcessor:
    """Factory function for creating pre-configured DataProcessor instances."""
    return DataProcessor(ops)

if __name__ == "__main__":
    # Example of a pipeline that sanitizes and squares input
    sanitizer: Callable[[str], int] = lambda x: int(str(x).strip())
    multiplier: Callable[[int], int] = lambda x: x * x
    
    processor = compose_processor([sanitizer, multiplier])
    print(f"Processed result: {processor.process(' 10 ')}")