import re
from typing import Any, Callable, Dict, List

VALIDATOR_REGISTRY: Dict[str, Callable[[Any], bool]] = {}

def register(name: str) -> Callable:
    def wrapper(func: Callable) -> Callable:
        VALIDATOR_REGISTRY[name] = func
        return func
    return wrapper

@register("email")
def is_valid_email(value: str) -> bool:
    if not isinstance(value, str):
        return False
    regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+".[a-zA-Z0-9-.]+$"
    return bool(re.match(regex, value))

@register("phone")
def is_valid_phone(value: str) -> bool:
    if not isinstance(value, str):
        return False
    regex = r"^\+?1?\d{9,15}$"
    return bool(re.match(regex, value))

@register("username")
def is_valid_username(value: str) -> bool:
    if not isinstance(value, str):
        return False
    regex = r"^[a-zA-Z0-9_]{3,20}$"
    return bool(re.match(regex, value))

@register("password")
def is_valid_password(value: str) -> bool:
    if not isinstance(value, str) or len(value) < 8:
        return False
    has_digit = any(c.isdigit() for c in value)
    has_letter = any(c.isalpha() for c in value)
    has_special = any(not c.isalnum() for c in value)
    return has_digit and has_letter and has_special

def validate_data(data: Dict[str, Any], rules: Dict[str, str]) -> Dict[str, List[str]]:
    errors: Dict[str, List[str]] = {}
    for key, rule in rules.items():
        if key not in data:
            errors[key] = ["Field is required"]
            continue
        validator = VALIDATOR_REGISTRY.get(rule)
        if not validator:
            errors[key] = ["Unknown validation rule"]
            continue
        if not validator(data[key]):
            errors[key] = [f"Invalid {rule}"]
    return errors

def is_valid(data: Dict[str, Any], rules: Dict[str, str]) -> bool:
    error_dict = validate_data(data, rules)
    return len(error_dict) == 0

def batch_validate(items: List[Dict[str, Any]], rules: Dict[str, str]) -> List[bool]:
    return [is_valid(item, rules) for item in items]

def list_validators() -> List[str]:
    return list(VALIDATOR_REGISTRY.keys())

@register("positive_number")
def is_positive_number(value: Any) -> bool:
    try:
        num = float(value)
        return num > 0
    except (ValueError, TypeError):
        return False

@register("non_empty")
def is_non_empty(value: Any) -> bool:
    if isinstance(value, str):
        return len(value.strip()) > 0
    if isinstance(value, (list, dict, set, tuple)):
        return len(value) > 0
    return value is not None