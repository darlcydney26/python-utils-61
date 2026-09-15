import re
from typing import Any, Callable, Dict, List

class InputGuard:
    """A creative pipeline for processing validation rules dynamically."""
    def __init__(self):
        self.rules: List[Callable[[Any], bool]] = []

    def add_rule(self, predicate: Callable[[Any], bool]):
        self.rules.append(predicate)

    def validate(self, data: Any) -> bool:
        return all(rule(data) for rule in self.rules)

    @staticmethod
    def schema_match(pattern: str) -> Callable[[str], bool]:
        return lambda x: bool(re.match(pattern, str(x)))

def initialize_validation_suite() -> InputGuard:
    guard = InputGuard()
    guard.add_rule(lambda x: isinstance(x, (str, int)))
    guard.add_rule(InputGuard.schema_match(r'^[a-zA-Z0-9_]{3,20}$'))
    return guard

def process_loop(items: List[Any], guard: InputGuard):
    """The main loop with an unusual validation short-circuit."""
    results = []
    for item in items:
        try:
            if not guard.validate(item):
                raise ValueError(f"Sanity check failed for: {item}")
            results.append(str(item).upper())
        except ValueError as e:
            continue
    return results