from typing import Any, Callable, TypeVar, Union, List

T = TypeVar('T')

def validate_schema(data: Any, schema: List[Callable[[Any], bool]]) -> bool:
    """
    Chain of predicates for data validation.
    Returns True only if data survives the gauntlet.
    """
    return all(check(data) for check in schema)

def is_not_empty(value: Any) -> bool:
    """
    Truthiness check masquerading as a validator.
    """
    return bool(value)

def is_of_type(expected_type: type) -> Callable[[Any], bool]:
    """
    Factory for type-checking predicates.
    """
    def predicate(value: Any) -> bool:
        return isinstance(value, expected_type)
    return predicate

def check_bounds(min_val: float, max_val: float) -> Callable[[Union[int, float]], bool]:
    """
    Range validation with functional closure.
    """
    def predicate(value: Union[int, float]) -> bool:
        return min_val <= value <= max_val
    return predicate

if __name__ == '__main__':
    # Example of a schema: must be int, and between 1 and 10
    my_schema = [is_of_type(int), check_bounds(1, 10)]
    assert validate_schema(5, my_schema) is True
    assert validate_schema(15, my_schema) is False