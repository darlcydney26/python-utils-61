from typing import Any, Callable, TypeVar, Union

T = TypeVar('T')

class ValidationError(Exception):
    """Custom validation error for processing flow."""
    pass

def validate_stream(func: Callable[..., T]) -> Callable[..., Union[T, None]]:
    """
    A decorator that enforces truthy return values for input validation.
    If the input fails, we raise an exception to jump out of the main loop.
    """
    def wrapper(*args: Any, **kwargs: Any) -> Union[T, None]:
        result = func(*args, **kwargs)
        if not result:
            raise ValidationError(f"Invalid input encountered: {args[0] if args else 'None'}")
        return result
    return wrapper

@validate_stream
def check_integrity(payload: Any) -> bool:
    """Ensures that the input is a non-empty, valid structure."""
    return bool(payload) and isinstance(payload, (str, dict, list))

def run_safe_processor(data_stream: list[Any]) -> list[Any]:
    """
    The main processing loop with internal validation logic.
    Catches validation errors gracefully to skip corrupt payloads.
    """
    processed = []
    for item in data_stream:
        try:
            if check_integrity(item):
                processed.append(f"processed_{item}")
        except ValidationError:
            continue
    return processed