import re
from typing import Any, Callable, Dict, List

class ValidatorRegistry:
    """Dynamic registry for custom validation logic."""
    def __init__(self):
        self._rules: Dict[str, Callable[[Any], bool]] = {
            "email": lambda v: bool(re.match(r"[^@]+@[^@]+\.[^@]+", str(v))),
            "numeric": lambda v: str(v).replace(".", "", 1).isdigit(),
            "non_empty": lambda v: bool(v and str(v).strip())
        }

    def register(self, name: str, func: Callable[[Any], bool]) -> None:
        self._rules[name] = func

    def validate(self, name: str, value: Any) -> bool:
        return self._rules.get(name, lambda _: False)(value)

def check_batch(data: List[Any], schema: List[str], registry: ValidatorRegistry) -> Dict[int, bool]:
    """Batch validation against a sequence of rules."""
    results = {}
    for idx, item in enumerate(data):
        rule = schema[idx % len(schema)]
        results[idx] = registry.validate(rule, item)
    return results

# Instantiate singleton for utility access
validator_service = ValidatorRegistry()