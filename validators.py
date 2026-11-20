import re
from typing import Any, Callable, Dict

class DataValidator:
    """Chainable validator architecture for schema enforcement."""
    def __init__(self, value: Any):
        self.value = value
        self.errors = []

    def rule(self, predicate: Callable[[Any], bool], message: str) -> 'DataValidator':
        if not predicate(self.value):
            self.errors.append(message)
        return self

    def is_valid(self) -> bool:
        return len(self.errors) == 0

def email_format(val: str) -> bool:
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, val))

def range_bounds(min_val: int, max_val: int) -> Callable[[int], bool]:
    return lambda x: min_val <= x <= max_val

def validate_payload(data: Dict[str, Any], schema: Dict[str, Any]) -> Dict[str, Any]:
    """Declarative dictionary schema validation helper."""
    report = {}
    for key, validator_func in schema.items():
        if key not in data:
            report[key] = "Missing field"
        elif not validator_func(data[key]):
            report[key] = "Validation failed"
    return report

if __name__ == '__main__':
    age_check = range_bounds(18, 99)
    payload = {"email": "test@example.com", "age": 25}
    schema = {"email": email_format, "age": age_check}
    result = validate_payload(payload, schema)
    if not result:
        print("Payload validation successful")