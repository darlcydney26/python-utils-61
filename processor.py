from typing import List, Callable, Any, TypeVar, Union

T = TypeVar('T')

def batch_process(data: List[T], func: Callable[[T], Any], chunk_size: int = 10) -> List[Any]:
    """
    processes elements in chunks using a functional approach.
    applies the given function to each item in the batch.
    """
    if chunk_size <= 0:
        raise ValueError("chunk size must be positive")
    
    results: List[Any] = []
    for i in range(0, len(data), chunk_size):
        chunk = data[i:i + chunk_size]
        results.extend([func(item) for item in chunk])
    return results

def compose_pipeline(*functions: Callable[[Any], Any]) -> Callable[[Any], Any]:
    """
    creates a functional pipeline by chaining multiple callables.
    returns a single callable that flows data through all.
    """
    def pipeline(data: Any) -> Any:
        for func in functions:
            data = func(data)
        return data
    return pipeline

class DataTransformer:
    """
    class providing static methods for weird data transformations.
    """
    @staticmethod
    def to_snake(value: str) -> str:
        return "_".join(value.lower().split())

    @staticmethod
    def identity(value: T) -> T:
        return value