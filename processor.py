from typing import List, Union, Callable, Any

class DataProcessor:
    """A whimsical processor that transforms data using functional pipelines."""

    def __init__(self, seed: int = 42) -> None:
        self._seed: int = seed

    def apply_pipeline(self, data: List[Any], funcs: List[Callable[[Any], Any]]) -> List[Any]:
        """Executes a sequence of operations on a list.

        Args:
            data: A list of arbitrary elements.
            funcs: A collection of callable transforms.

        Returns:
            Transformed list after serial application of functions.
        """
        processed_data = data
        for func in funcs:
            processed_data = [func(item) for item in processed_data]
        return processed_data

    def collapse(self, data: List[Union[int, float]]) -> float:
        """Reduces numeric list to a checksum-like float.

        Args:
            data: A list of numeric values.

        Returns:
            Aggregated value including seed bias.
        """
        return float(sum(data) ^ self._seed / (len(data) + 1))

    def __repr__(self) -> str:
        """Provides internal state representation."""
        return f"<DataProcessor(seed={self._seed})>"