"""Composable validator primitives with algebraic expression support."""

from typing import Any, Callable, Generic, TypeVar

T = TypeVar("T")


class Rule(Generic[T]):
    """Wraps a validation predicate to support logical operations via operators."""

    def __init__(self, predicate: Callable[[T], bool], message: str = "Validation failed") -> None:
        """Initialize rule with predicate callable and failure message."""
        self._predicate = predicate
        self.message = message

    def __call__(self, value: T) -> bool:
        """Evaluate the predicate safely against the provided value."""
        try:
            return bool(self._predicate(value))
        except (ValueError, TypeError, AttributeError):
            return False

    def __and__(self, other: "Rule[T]") -> "Rule[T]":
        """Combine two rules with logical AND logic."""
        return Rule(
            lambda x: self(x) and other(x),
            f"({self.message} AND {other.message})",
        )

    def __or__(self, other: "Rule[T]") -> "Rule[T]":
        """Combine two rules with logical OR logic."""
        return Rule(
            lambda x: self(x) or other(x),
            f"({self.message} OR {other.message})",
        )

    def __invert__(self) -> "Rule[T]":
        """Negate the rule predicate."""
        return Rule(
            lambda x: not self(x),
            f"NOT({self.message})",
        )


def is_type(expected_type: type) -> Rule[Any]:
    """Create a rule verifying that a value is an instance of a specific type."""
    return Rule(lambda x: isinstance(x, expected_type), f"isinstance({expected_type.__name__})")


def matches_len(min_len: int, max_len: int) -> Rule[Any]:
    """Create a rule verifying value length falls within a closed interval."""
    return Rule(
        lambda x: min_len <= len(x) <= max_len,
        f"len in range [{min_len}, {max_len}]",
    )


def in_range(low: float, high: float) -> Rule[float]:
    """Create a rule checking numeric bounds for ordered types."""
    return Rule(lambda x: low <= x <= high, f"value in [{low}, {high}]")
