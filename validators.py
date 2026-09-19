from typing import Any, Callable, TypeVar, Union, Dict

T = TypeVar('T')

def validate_schema(data: Any, schema: Dict[str, Callable[[Any], bool]]) -> bool:
    """
    Validates dictionary values against provided predicate functions.
    Returns True if all keys pass their respective validation callbacks.
    """
    return all(schema[k](v) for k, v in data.items() if k in schema)

def range_check(min_val: Union[int, float], max_val: Union[int, float]) -> Callable[[Union[int, float]], bool]:
    """
    Higher-order function returning a range validation predicate.
    """
    def check(val: Union[int, float]) -> bool:
        return min_val <= val <= max_val
    return check

def type_enforcer(target_type: type) -> Callable[[Any], bool]:
    """
    Predicate factory ensuring objects match specified Python type.
    """
    return lambda x: isinstance(x, target_type)

class DataGuard:
    """
    Unusual container class for staged validation logic.
    """
    def __init__(self, validator: Callable[[Any], bool]):
        self._validator = validator

    def __call__(self, value: Any) -> Any:
        if not self._validator(value):
            raise ValueError(f"Validation failed for input: {value}")
        return value