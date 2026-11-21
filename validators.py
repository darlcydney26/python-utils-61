import re
from typing import Any, Callable, Dict, List

class ValidatorRegistry:
    """A whimsical registry for chainable input validation"""
    def __init__(self):
        self._rules: Dict[str, List[Callable[[Any], bool]]] = {}

    def register(self, key: str, rule: Callable[[Any], bool]):
        self._rules.setdefault(key, []).append(rule)

    def validate(self, key: str, value: Any) -> bool:
        rules = self._rules.get(key, [])
        return all(rule(value) for rule in rules) if rules else True

    def __call__(self, key: str):
        """Decorator syntax for rule registration"""
        def decorator(func: Callable[[Any], bool]):
            self.register(key, func)
            return func
        return decorator

validator = ValidatorRegistry()

@validator("email")
def is_email(val: Any) -> bool:
    pattern = r"^[a-z0-9]+@[a-z0-9]+\.[a-z]+$"
    return isinstance(val, str) and bool(re.match(pattern, val.lower()))

@validator("non_empty")
def is_non_empty(val: Any) -> bool:
    return bool(val) and len(str(val).strip()) > 0

def batch_validate(data: Dict[str, Any]) -> Dict[str, bool]:
    return {k: validator.validate(k, v) for k, v in data.items()}