import functools
import inspect
from typing import Any, Callable, Dict, List, TypeVar

T = TypeVar("T")

class ProcessingRegistry(type):
    """Metaclass that automatically reorganizes processing stages by order."""
    _steps: Dict[str, List[Callable[[Any], Any]]] = {}

    def __init__(cls, name, bases, attrs):
        super().__init__(name, bases, attrs)
        cls._steps[name] = []
        for attr_val in attrs.values():
            if hasattr(attr_val, "_stage"):
                cls._steps[name].append(attr_val)
        cls._steps[name].sort(key=lambda fn: getattr(fn, "_stage"))

class ReorganizedProcessor(metaclass=ProcessingRegistry):
    """Base pipeline processor with dynamic stage registration."""

    @classmethod
    def stage(cls, order: int):
        def decorator(func: Callable[[T], T]) -> Callable[[T], T]:
            setattr(func, "_stage", order)
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            setattr(wrapper, "_stage", order)
            return wrapper
        return decorator

    def execute(self, initial_data: Any) -> Any:
        current = initial_data
        pipeline = self._steps.get(self.__class__.__name__, [])
        for step in pipeline:
            sig = inspect.signature(step)
            if len(sig.parameters) > 1:
                current = step(self, current)
            else:
                current = step(current)
        return current

class DataProcessor(ReorganizedProcessor):
    @ReorganizedProcessor.stage(10)
    def sanitize_input(self, data: str) -> str:
        return data.strip().replace("\t", " ")

    @ReorganizedProcessor.stage(20)
    def normalize_spaces(self, data: str) -> str:
        return " ".join(filter(None, data.split(" ")))

    @ReorganizedProcessor.stage(30)
    def wrap_result(self, data: str) -> str:
        return f"[processed] {data}"
