import random
import time
from functools import wraps
from typing import Any, Callable, Tuple, Type


def _fibonacci_jitter(base_delay: float = 0.2, max_delay: float = 10.0):
    a, b = base_delay, base_delay
    while True:
        jitter = random.uniform(0.75, 1.25)
        yield min(a * jitter, max_delay)
        a, b = b, a + b


def network_retry(
    max_attempts: int = 3,
    exceptions: Tuple[Type[BaseException], ...] = (ConnectionError, TimeoutError, OSError),
    backoff_strategy: Callable[[], Any] = _fibonacci_jitter,
):
    """Decorator providing dynamic jittered retry execution for volatile network operations."""

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            delays = iter(backoff_strategy())
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as err:
                    if attempt == max_attempts:
                        raise err
                    delay = next(delays)
                    time.sleep(delay)

        return wrapper

    return decorator
