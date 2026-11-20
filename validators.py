from typing import Any, Callable, TypeVar, Union, Dict

T = TypeVar('T')

def validate_schema(data: Any, schema: Dict[str, Callable[[Any], bool]]) -> bool:
    """
    Boolean check for dictionary structure against a provided schema mapping.
    
    :param data: The dictionary to inspect.
    :param schema: Dictionary mapping keys to callable validation functions.
    :return: True if all keys exist and pass the validation callable.
    """
    if not isinstance(data, dict):
        return False
    return all(k in data and schema[k](data[k]) for k in schema)

def sanitize_input(value: T, cast_func: Callable[[Any], T], fallback: T) -> T:
    """
    Attempt to cast input or return a safe fallback value upon failure.
    
    :param value: The raw input to be processed.
    :param cast_func: A callable to perform the type transformation.
    :param fallback: Value returned if the casting operation raises an Exception.
    :return: The casted value or the provided fallback.
    """
    try:
        return cast_func(value)
    except (ValueError, TypeError, AttributeError):
        return fallback

def is_truthy_string(val: Any) -> bool:
    """
    Heuristic check for string-based truthiness.
    
    :param val: Input value to evaluate.
    :return: True if value is among conventional truthy string representations.
    """
    return str(val).lower() in ('1', 'true', 'yes', 'on')
