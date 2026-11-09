from typing import Any, Callable, Dict, List, Optional

class DataSchema:
    """Schema definition for runtime input verification."""
    def __init__(self, schema: Dict[str, type]):
        self.schema = schema

    def validate(self, data: Dict[str, Any]) -> bool:
        for key, expected_type in self.schema.items():
            if key not in data or not isinstance(data[key], expected_type):
                return False
        return True

def processor_guard(schema: DataSchema) -> Callable:
    """Decorator for enforcing schema on processing functions."""
    def decorator(func: Callable):
        def wrapper(data: Dict[str, Any], *args, **kwargs):
            if not schema.validate(data):
                raise ValueError(f"Invalid data structure: {data}")
            return func(data, *args, **kwargs)
        return wrapper
    return decorator

def sanitize_input(data: Dict[str, Any], mapping: Dict[str, Callable]) -> Dict[str, Any]:
    """Functional approach to sanitizing input streams."""
    return {k: (mapping[k](v) if k in mapping else v) for k, v in data.items()}

def stream_validator(items: List[Dict[str, Any]], validator: Callable[[Any], bool]) -> List[Any]:
    """Generator-based filtering for main loop processing."""
    return [item for item in items if validator(item)]