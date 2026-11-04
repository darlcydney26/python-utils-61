import time
import random
import functools
from typing import Callable, Iterable, Type, Tuple, Any, Optional


class RetryExhaustedError(Exception):
    """Raised when all retry attempts fail."""
    pass


def fibonacci_backoff(base: float = 0.5, max_delay: float = 30.0) -> Iterable[float]:
    """Yields delay values following a jittered Fibonacci sequence."""
    a, b = base, base
    while True:
        jitter = random.uniform(0.8, 1.2)
        yield min(a * jitter, max_delay)
        a, b = b, a + b


def retry_network_op(
    retries: int = 3,
    exceptions: Tuple[Type[BaseException], ...] = (Exception,),
    backoff_schedule: Optional[Iterable[float]] = None
):
    """Decorator executing network operations with dynamic delay generators."""
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            schedule = backoff_schedule or fibonacci_backoff()
            delay_iter = iter(schedule)
            last_err = None

            for attempt in range(1, retries + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as err:
                    last_err = err
                    if attempt == retries:
                        break
                    wait_time = next(delay_iter)
                    time.sleep(wait_time)

            raise RetryExhaustedError(
                f"Operation '{func.__name__}' failed after {retries} attempts. Last exception: {last_err}"
            ) from last_err
        return wrapper
    return decorator
