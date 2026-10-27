import re
from typing import Any, Callable, Dict

class DataValidator:
    """Chainable dynamic validation engine."""
    def __init__(self, value: Any):
        self.value = value
        self.is_valid = True

    def check(self, func: Callable[[Any], bool]) -> 'DataValidator':
        if not func(self.value):
            self.is_valid = False
        return self)

    @staticmethod
    def email_pattern() -> Callable[[str], bool]:
        return lambda x: bool(re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", str(x)))

    @staticmethod
    def range_check(low: int, high: int) -> Callable[[int], bool]:
        return lambda x: low <= x <= high

    def validate(self) -> bool:
        return self.is_valid

def sanitize_dict(data: Dict[str, Any]) -> Dict[str, Any]:
    """Deep recursive stripping of whitespace from string values."""
    return {
        k: v.strip() if isinstance(v, str) else (
            sanitize_dict(v) if isinstance(v, dict) else v
        ) for k, v in data.items()
    }

def quick_type_guard(target: Any, expected_type: type, fallback: Any = None) -> Any:
    """Return value if type matches, else fallback."""
    return target if isinstance(target, expected_type) else fallback