import functools
import logging
from typing import Callable, Any, TypeVar, ParamSpec

P = ParamSpec('P')
R = TypeVar('R')

class ResilienceEnvelope:
    def __init__(self, fallback_value: Any = None, silent: bool = True):
        self.fallback = fallback_value
        self.silent = silent
        self.logger = logging.getLogger('processor')

    def __call__(self, func: Callable[P, R]) -> Callable[P, R]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            try:
                return func(*args, **kwargs)
            except (ValueError, TypeError, ZeroDivisionError) as e:
                if not self.silent:
                    self.logger.error(f"Edge case hit in {func.__name__}: {e}")
                return self.fallback  # type: ignore
            except Exception as e:
                self.logger.critical(f"Uncaught chaos in {func.__name__}: {e}")
                raise
        return wrapper

def safe_divide(a: Any, b: Any) -> float:
    @ResilienceEnvelope(fallback_value=float('inf'))
    def _execute(x: float, y: float) -> float:
        return x / y
    return _execute(float(a), float(b))

def sanitize_list(data: Any) -> list:
    @ResilienceEnvelope(fallback_value=[])
    def _execute(d: list) -> list:
        return [item.strip() for item in d if item]
    return _execute(data)

if __name__ == '__main__':
    print(safe_divide(10, 0))
    print(sanitize_list(None))