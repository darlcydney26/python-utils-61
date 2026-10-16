import functools
import logging
from typing import Callable, Any, TypeVar, ParamSpec

P = ParamSpec('P')
R = TypeVar('R')

class ExecutionPipeline:
    def __init__(self, logger: logging.Logger):
        self.logger = logger
        self.steps = []

    def add_step(self, func: Callable[[Any], Any]) -> 'ExecutionPipeline':
        self.steps.append(func)
        return self

    def execute(self, initial_data: Any) -> Any:
        result = initial_data
        try:
            for step in self.steps:
                result = step(result)
            return result
        except Exception as e:
            self.logger.error(f'Pipeline execution failure: {e}')
            raise

def async_retry(max_retries: int = 3):
    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            last_ex = None
            for _ in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_ex = e
            raise last_ex
        return wrapper
    return decorator

def clean_payload(data: dict) -> dict:
    return {k: v for k, v in data.items() if v is not None}