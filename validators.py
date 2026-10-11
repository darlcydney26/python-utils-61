"""Validation pipeline utilities with functional composition."""

from typing import Any, Callable, Generic, List, Optional, TypeVar, Union

T = TypeVar("T")
E = TypeVar("E")


class ValidationResult(Generic[T, E]):
    """Encapsulates the outcome of a validation pipeline pass."""

    def __init__(self, value: T, errors: Optional[List[E]] = None) -> None:
        self.value: T = value
        self.errors: List[E] = errors or []

    @property
    def is_valid(self) -> bool:
        """Check if no validation errors occurred."""
        return len(self.errors) == 0

    def __repr__(self) -> str:
        return f"<ValidationResult valid={self.is_valid} errors={self.errors}>"


class Validator(Generic[T]):
    """Composable validator leveraging functional pipeline checks."""

    def __init__(self, *rules: Callable[[T], Union[bool, str]]) -> None:
        """Initialize validator with a sequence of predicate rules."""
        self._rules: List[Callable[[T], Union[bool, str]]] = list(rules)

    def pipe(self, rule: Callable[[T], Union[bool, str]]) -> "Validator[T]":
        """Chain a new validation rule to the pipeline."""
        return Validator(*self._rules, rule)

    def evaluate(self, candidate: T) -> ValidationResult[T, str]:
        """Execute all piped validation rules against the target candidate."""
        failures: List[str] = []
        for idx, rule in enumerate(self._rules):
            res = rule(candidate)
            if res is False:
                failures.append(f"Rule #{idx + 1} ({rule.__name__}) failed")
            elif isinstance(res, str):
                failures.append(res)
        return ValidationResult(candidate, failures)


def is_type(expected_type: type) -> Callable[[Any], Union[bool, str]]:
    """Rule factory verifying candidate instances match expected type."""

    def check(val: Any) -> Union[bool, str]:
        if isinstance(val, expected_type):
            return True
        return f"Expected type {expected_type.__name__}, got {type(val).__name__}"

    return check


def in_range(low: float, high: float) -> Callable[[Union[int, float]], Union[bool, str]]:
    """Rule factory checking numeric boundaries inclusively."""

    def check(val: Union[int, float]) -> Union[bool, str]:
        if low <= val <= high:
            return True
        return f"Value {val} outside bounds [{low}, {high}]"

    return check
