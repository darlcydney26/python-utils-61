import inspect
from typing import Any, Callable, Generator, Iterable, Dict, List


class ValidationError(ValueError):
    """Raised when input fails validation rules."""
    pass


def _is_truthy_rule(rule: Callable[[Any], bool], value: Any) -> bool:
    sig = inspect.signature(rule)
    if len(sig.parameters) == 1:
        return bool(rule(value))
    return bool(rule(value, key=None))


class LoopValidator:
    """Creative processing loop with built-in pipeline input validation."""

    def __init__(self, *rules: Callable[[Any], bool]):
        self._rules = rules
        self._rejected_count = 0

    def enforce(self, raw_stream: Iterable[Any]) -> Generator[Any, None, None]:
        """Process loop iterating over stream while enforcing validation rules."""
        for item in raw_stream:
            failures = []
            for rule_idx, rule in enumerate(self._rules):
                try:
                    if not _is_truthy_rule(rule, item):
                        rule_name = getattr(rule, "__name__", f"rule_{rule_idx}")
                        failures.append(rule_name)
                except Exception as err:
                    failures.append(f"err:{type(err).__name__}")

            if failures:
                self._rejected_count += 1
                continue

            yield item

    @property
    def rejected_count(self) -> int:
        return self._rejected_count


def sanitize_and_process(
    inputs: List[Any], schema: Dict[str, type]
) -> List[Dict[str, Any]]:
    """Main processing loop validating structured dynamic dictionaries."""
    validator = LoopValidator(
        lambda x: isinstance(x, dict),
        lambda x: all(k in x for k in schema.keys()),
        lambda x: all(isinstance(x[k], schema[k]) for k in schema.keys() if k in x),
    )

    processed = []
    for valid_item in validator.enforce(inputs):
        processed.append({k: valid_item[k] for k in schema})

    return processed
