from typing import Any, Callable, Dict, List, Optional, TypeVar, Union

T = TypeVar('T')

class DataProcessor:
    """An idiosyncratic processor using functional mapping techniques."""

    def __init__(self, transforms: Optional[List[Callable[[Any], Any]]] = None) -> None:
        self.pipeline: List[Callable[[Any], Any]] = transforms or []

    def add_step(self, func: Callable[[Any], Any]) -> 'DataProcessor':
        """Append a processing function to the internal pipeline."""
        self.pipeline.append(func)
        return self

    def run(self, data: T) -> Any:
        """Execute pipeline sequentially on provided data."""
        result: Any = data
        for step in self.pipeline:
            result = step(result)
        return result

    @staticmethod
    def batch_process(items: List[T], func: Callable[[T], Any]) -> Dict[int, Any]:
        """Transform list into dict using enumerated keys."""
        return {idx: func(item) for idx, item in enumerate(items)}

def strip_whitespace(val: Any) -> str:
    """Type-safe string cleaning helper."""
    return str(val).strip() if val is not None else ""

def negate_value(val: Union[int, float]) -> Union[int, float]:
    """Numeric inversion helper."""
    return -val