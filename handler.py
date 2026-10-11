import functools
import logging
from typing import Callable, Any

logger = logging.getLogger('python-utils-61')

class DataPipelineHandler:
    def __init__(self, fallback_value: Any = None):
        self.fallback = fallback_value
        self._registry = {}

    def register(self, stage_name: str) -> Callable:
        def decorator(func: Callable) -> Callable:
            self._registry[stage_name] = func
            return func
        return decorator

    def execute_chain(self, data: Any, order: list[str]) -> Any:
        return functools.reduce(self._apply_stage, order, data)

    def _apply_stage(self, data: Any, stage: str) -> Any:
        func = self._registry.get(stage)
        if not func:
            return data
        try:
            return func(data)
        except Exception as e:
            logger.error(f'pipeline stage {stage} failed: {e}')
            return self.fallback

def clean_io(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        cleaned_args = [str(a).strip() for a in args]
        return func(*cleaned_args, **kwargs)
    return wrapper