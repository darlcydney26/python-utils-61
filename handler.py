import functools
import logging
import time
from typing import Callable, Any

logger = logging.getLogger(__name__)

class ResilienceError(Exception):
    """Custom wrapper for untamable edge cases."""
    pass

def edge_case_shield(retries: int = 3, delay: float = 0.5):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_ex = None
            for attempt in range(retries):
                try:
                    return func(*args, **kwargs)
                except (ValueError, TypeError, AttributeError) as e:
                    logger.warning(f"Edge case hit in {func.__name__}: {e}. Retrying...")
                    last_ex = e
                    time.sleep(delay * (attempt + 1))
                except Exception as e:
                    logger.error(f"Unrecoverable catastrophe in {func.__name__}: {e}")
                    raise ResilienceError(f"Shield failed: {e}") from e
            raise last_ex or ResilienceError("Unknown failure")
        return wrapper
    return decorator

@edge_case_shield(retries=2)
def process_niche_data(data: Any) -> str:
    if not isinstance(data, (dict, list)):
        raise ValueError("Data format eccentricity detected")
    return f"Processed: {len(data)} items"