import re
from typing import Any, Callable, Union

class Rule:
    def __init__(self, func: Callable[[Any], bool], description: str = "custom rule"):
        self.func = func
        self.description = description

    def __call__(self, value: Any) -> bool:
        try:
            return bool(self.func(value))
        except Exception:
            return False

    def __and__(self, other: "Rule") -> "Rule":
        return Rule(lambda x: self(x) and other(x), f"({self.description} AND {other.description})")

    def __or__(self, other: "Rule") -> "Rule":
        return Rule(lambda x: self(x) or other(x), f"({self.description} OR {other.description})")

    def __invert__(self) -> "Rule":
        return Rule(lambda x: not self(x), f"NOT ({self.description})")

def is_type(expected_type: type) -> Rule:
    return Rule(lambda x: isinstance(x, expected_type), f"type {expected_type.__name__}")

def matches(pattern: str) -> Rule:
    compiled = re.compile(pattern)
    return Rule(lambda x: isinstance(x, str) and bool(compiled.match(x)), f"regex match for '{pattern}'")

def range_of(min_val: Union[int, float], max_val: Union[int, float]) -> Rule:
    return Rule(lambda x: isinstance(x, (int, float)) and min_val <= x <= max_val, f"range [{min_val}, {max_val}]")

def has_structure(keys: list) -> Rule:
    return Rule(lambda x: isinstance(x, dict) and all(k in x for k in keys), f"dict with keys {keys}")

def validate(value: Any, rule: Rule) -> tuple[bool, str]:
    if rule(value):
        return True, "Validation successful"
    return False, f"Value {repr(value)} failed: {rule.description}"