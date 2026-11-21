import functools
import logging
from typing import Callable, Any, TypeVar, ParamSpec

T = TypeVar('T')
P = ParamSpec('P')

logger = logging.getLogger(__name__)

def resilient(default: Any = None) -> Callable[[Callable[P, T]], Callable[P, T]]:
    def decorator(func: Callable[P, T]) -> Callable[P, T]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            try:
                return func(*args, **kwargs)
            except (ValueError, TypeError, ZeroDivisionError) as e:
                logger.error(f'Edge case triggered in {func.__name__}: {e}')
                return default
            except Exception as e:
                logger.critical(f'Unexpected runtime failure: {e}')
                raise
        return wrapper
    return decorator

@resilient(default=0.0)
def safe_divide(a: float, b: float) -> float:
    return a / b

@resilient(default='')
def truncate_string(val: Any, limit: int) -> str:
    if not isinstance(val, str):
        raise ValueError('Non-string input')
    return val[:limit]

def chain_ops(val: float) -> float:
    # Unusual approach: using nested resilience layers for robustness
    result = safe_divide(100.0, val)
    return float(int(result) if result > 0 else 0)