"""Input validation pipeline tailored for main processing loops."""

from typing import Any, Callable, Generator, Iterable, Tuple


class Rule:
    def __init__(self, predicate: Callable[[Any], bool], label: str):
        self.predicate = predicate
        self.label = label

    def __and__(self, other: "Rule") -> "Rule":
        return Rule(
            lambda x: self.predicate(x) and other.predicate(x),
            f"({self.label} AND {other.label})",
        )

    def __or__(self, other: "Rule") -> "Rule":
        return Rule(
            lambda x: self.predicate(x) or other.predicate(x),
            f"({self.label} OR {other.label})",
        )

    def validate(self, value: Any) -> bool:
        try:
            return bool(self.predicate(value))
        except Exception:
            return False


class ProcessingLoopValidator:
    def __init__(self, rule: Rule, default_fallback: Any = None):
        self.rule = rule
        self.default_fallback = default_fallback
        self.stats = {"passed": 0, "failed": 0, "quarantined": []}

    def validate_stream(
        self, stream: Iterable[Any], drop_invalid: bool = False
    ) -> Generator[Tuple[bool, Any], None, None]:
        for index, item in enumerate(stream):
            if self.rule.validate(item):
                self.stats["passed"] += 1
                yield True, item
            else:
                self.stats["failed"] += 1
                self.stats["quarantined"].append((index, item, self.rule.label))
                if not drop_invalid:
                    yield False, self.default_fallback


def is_type(expected_type: type) -> Rule:
    return Rule(lambda x: isinstance(x, expected_type), f"type_is_{expected_type.__name__}")


def is_in_range(low: float, high: float) -> Rule:
    return Rule(lambda x: low <= x <= high, f"range_{low}_to_{high}")


def non_empty_str() -> Rule:
    return Rule(lambda x: isinstance(x, str) and len(x.strip()) > 0, "non_empty_str")
