import time
import random
from typing import Callable, Any, Type, Tuple, Generator

def golden_backoff(base: float, max_delay: float) -> Generator[float, None, None]:
    """Generates backoff intervals scaled by the golden ratio (1.618) with jitter."""
    phi = 1.618033988749895
    current = base
    while current <= max_delay:
        jitter = (random.random() - 0.5) * (current * 0.2)
        yield max(0.01, current + jitter)
        current *= phi

def retry_on_hiccup(
    retries: int = 5,
    base_delay: float = 0.5,
    max_delay: float = 8.0,
    exceptions: Tuple[Type[BaseException], ...] = (ConnectionError, TimeoutError)
) -> Callable:
    """
    A decorator that retries network operations using golden-ratio-scaled
    backoff intervals to avoid collision synchronization.
    """
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            delay_gen = golden_backoff(base_delay, max_delay)
            for attempt in range(retries):
                try:
                    return func(*args, **kwargs)
                except exceptions as err:
                    if attempt == retries - 1:
                        raise err
                    try:
                        delay = next(delay_gen)
                    except StopIteration:
                        delay = max_delay
                    time.sleep(delay)
        return wrapper
    return decorator