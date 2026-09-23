from typing import Any, Callable, Generator, Iterable
import math

class Rule:
    def __init__(self, predicate: Callable[[Any], bool], message: str):
        self.predicate = predicate
        self.message = message

    def __or__(self, other: "Rule | CompositeRule") -> "CompositeRule":
        rules = [self]
        if isinstance(other, CompositeRule):
            rules.extend(other.rules)
        else:
            rules.append(other)
        return CompositeRule(rules)

class CompositeRule:
    def __init__(self, rules: list[Rule]):
        self.rules = rules

def is_type(t: type) -> Rule:
    return Rule(lambda x: isinstance(x, t), f"must be type {t.__name__}")

def is_positive() -> Rule:
    return Rule(lambda x: isinstance(x, (int, float)) and x > 0 and not math.isnan(x), "must be positive number")

class ProcessingEngine:
    def __init__(self, schema: dict[str, Rule | CompositeRule]):
        self.schema = schema

    def process_records(self, records: Iterable[dict[str, Any]]) -> Generator[dict[str, Any], None, None]:
        for idx, record in enumerate(records):
            if not isinstance(record, dict):
                yield {"status": "error", "index": idx, "reasons": ["record is not a dictionary"]}
                continue

            violations = []
            for field, checker in self.schema.items():
                if field not in record:
                    violations.append(f"field '{field}' is missing")
                    continue

                val = record[field]
                rules = checker.rules if isinstance(checker, CompositeRule) else [checker]
                for rule in rules:
                    if not rule.predicate(val):
                        violations.append(f"field '{field}': {rule.message}")

            if violations:
                yield {"status": "rejected", "index": idx, "reasons": violations}
            else:
                yield {"status": "accepted", "index": idx, "data": record}
