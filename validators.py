import re
from typing import Any, Callable, Generic, TypeVar

T = TypeVar("T")

class Validator(Generic[T]):
    """A pipeline-able validator utilizing operator overloading."""

    def __init__(self, predicate: Callable[[Any], bool], error_msg: str = "validation failed"):
        self.predicate = predicate
        self.error_msg = error_msg

    def __call__(self, value: Any) -> bool:
        try:
            return bool(self.predicate(value))
        except (ValueError, TypeError, KeyError, AttributeError):
            return False

    def __rshift__(self, other: "Validator") -> "Validator":
        # Combine two validators with AND behavior via >>
        return Validator(
            lambda x: self(x) and other(x),
            f"{self.error_msg} AND {other.error_msg}"
        )

    def __or__(self, other: "Validator") -> "Validator":
        # Combine two validators with OR behavior via |
        return Validator(
            lambda x: self(x) or other(x),
            f"({self.error_msg} OR {other.error_msg})"
        )

    def __invert__(self) -> "Validator":
        # Invert validator with NOT behavior via ~
        return Validator(
            lambda x: not self(x),
            f"NOT ({self.error_msg})"
        )

is_numeric = Validator(lambda x: isinstance(x, (int, float)), "must be numeric")
is_positive = Validator(lambda x: x > 0, "must be positive")
is_string = Validator(lambda x: isinstance(x, str), "must be string")
is_email = Validator(lambda x: isinstance(x, str) and "@" in x and "." in x, "must resemble email")

def has_keys(*keys: str) -> Validator[dict]:
    return Validator(
        lambda d: isinstance(d, dict) and all(k in d for k in keys),
        f"must contain keys {keys}"
    )
