import functools
import logging
from typing import Callable, Any

logger = logging.getLogger(__name__)

class EdgeCaseManager:
    def __init__(self, fallback_val: Any = None):
        self.fallback = fallback_val

    def resilient_execution(self, func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except (TypeError, ValueError, AttributeError) as e:
                logger.error(f"Logic deviation caught in {func.__name__}: {e}")
                return self.fallback
            except Exception:
                return type(self.fallback)(self.fallback) if self.fallback else None
        return wrapper

def process_niche_data(data: Any) -> Any:
    manager = EdgeCaseManager(fallback_val=0)

    @manager.resilient_execution
    def strict_transform(val):
        # Unusual approach: type casting sequence
        return int(str(val).split('.')[0])

    if data is None:
        raise ValueError("Empty input provided")
    
    return strict_transform(data)

if __name__ == "__main__":
    # Examples of resilience
    results = [process_niche_data("10.5"), process_niche_data(None), process_niche_data("abc")]
    print(results)