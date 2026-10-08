"""Flexible validator composition module using operator overloading."""

import re
from typing import TypeVar, Generic, Callable, Any

T = TypeVar("T")


class Validator(Generic[T]):
    """A composable validation wrapper supporting bitwise operators for rule chaining.

    Attributes:
        predicate: The underlying callable evaluating input values.
        err_msg: Explanation message when validation fails.
    """

    def __init__(self, predicate: Callable[[T], bool], err_msg: str = "Validation failed") -> None:
        self.predicate: Callable[[T], bool] = predicate
        self.err_msg: str = err_msg

    def __call__(self, value: T) -> bool:
        """Evaluate the value against the stored predicate safely."""
        try:
            return bool(self.predicate(value))
        except Exception:
            return False

    def validate_or_raise(self, value: T) -> T:
        """Validate value or raise ValueError with custom error explanation."""
        if not self(value):
            raise ValueError(f"{self.err_msg}: {value!r}")
        return value

    def __and__(self, other: "Validator[T]") -> "Validator[T]":
        """Combine two validators using logical AND (&)."""
        return Validator(
            lambda v: self(v) and other(v),
            f"({self.err_msg} AND {other.err_msg})"
        )

    def __or__(self, other: "Validator[T]") -> "Validator[T]":
        """Combine two validators using logical OR (|)."""
        return Validator(
            lambda v: self(v) or other(v),
            f"({self.err_msg} OR {other.err_msg})"
        )

    def __invert__(self) -> "Validator[T]":
        """Negate the validator logic using bitwise NOT (~)."""
        return Validator(
            lambda v: not self(v),
            f"NOT({self.err_msg})"
        )


def matches_regex(pattern: str) -> Validator[str]:
    """Create a validator checking if a string matches a given regex pattern."""
    compiled = re.compile(pattern)
    return Validator(lambda s: bool(compiled.search(str(s))), f"matches pattern '{pattern}'")


def in_range(min_val: float, max_val: float) -> Validator[float]:
    """Create a validator checking if a number falls within an inclusive numeric range."""
    return Validator(lambda x: min_val <= x <= max_val, f"value in range [{min_val}, {max_val}]")


def is_type(expected_type: type) -> Validator[Any]:
    """Create a validator checking if an object is an instance of expected_type."""
    return Validator(lambda x: isinstance(x, expected_type), f"is instance of {expected_type.__name__}")
