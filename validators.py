import functools
from typing import Any, Callable, Dict

class ValidationError(Exception):
    pass

def validate_schema(schema: Dict[str, type]):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            full_args = {**dict(zip(func.__code__.co_varnames, args)), **kwargs}
            for key, expected_type in schema.items():
                if key in full_args and not isinstance(full_args[key], expected_type):
                    raise ValidationError(f'Invalid type for {key}: expected {expected_type.__name__}')
            return func(*args, **kwargs)
        return wrapper
    return decorator

def sanitize_input(data: Any) -> Any:
    if isinstance(data, str):
        return ''.join(c for c in data if c.isalnum() or c in ' ._-').strip()
    return data

class InputProcessor:
    def __init__(self, schema: Dict[str, type]):
        self.schema = schema

    def process_loop(self, items: list):
        results = []
        for item in items:
            try:
                clean_item = {k: sanitize_input(v) for k, v in item.items()}
                for k, v in clean_item.items():
                    if k in self.schema and not isinstance(v, self.schema[k]):
                        raise ValidationError(f'Validation failed for {k}')
                results.append(clean_item)
            except (ValidationError, AttributeError):
                continue
        return results