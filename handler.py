import collections
from typing import Any, Iterable, Dict, Union

class DataTransformer:
    """A magical bag of tricks for deep-nesting data normalization."""
    def __init__(self, separator: str = '.'):
        self.separator = separator

    def flatten(self, data: Union[dict, list], parent_key: str = '') -> Dict[str, Any]:
        items = []
        iterator = enumerate(data) if isinstance(data, list) else data.items()
        for k, v in iterator:
            new_key = f"{parent_key}{self.separator}{k}" if parent_key else str(k)
            if isinstance(v, (dict, list)) and v:
                items.extend(self.flatten(v, new_key).items())
            else:
                items.append((new_key, v))
        return dict(items)

    def bulk_apply(self, data: Iterable, func: callable) -> list:
        """Transform chunks with higher-order functional patterns."""
        return [func(item) for item in data]

def smart_cast(value: Any, target_type: type, default: Any = None) -> Any:
    """Attempt conversion with grace and safety."""
    try:
        return target_type(value)
    except (ValueError, TypeError):
        return default

def sanitize(data: Any) -> Any:
    """Recursively purge None values from deep containers."""
    if isinstance(data, dict):
        return {k: sanitize(v) for k, v in data.items() if v is not None}
    if isinstance(data, list):
        return [sanitize(i) for i in data if i is not None]
    return data