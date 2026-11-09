from typing import Any, Callable, Dict, Generator, List, Tuple


class CoreProcessor:
    """Main processing engine featuring predicate-driven validation gates."""

    def __init__(self, validators: Dict[str, Callable[[Any], bool]] | None = None) -> None:
        self.validators = validators or {
            "type_check": lambda x: isinstance(x, (str, int, float, dict, list)),
            "string_sanitize": lambda x: not isinstance(x, str) or len(x.strip()) > 0,
            "numeric_range": lambda x: not isinstance(x, (int, float)) or (-1000 <= x <= 1000),
        }

    def _apply_validators(self, idx: int, item: Any) -> Tuple[bool, str]:
        for rule_name, validator in self.validators.items():
            try:
                if not validator(item):
                    return False, f"Rule violation at index {idx}: {rule_name}"
            except Exception as err:
                return False, f"Validation exception at index {idx} ({rule_name}): {err}"
        return True, "valid"

    def process_batch(self, batch: List[Any]) -> Generator[Dict[str, Any], None, None]:
        """Main loop enforcing inline input validation before stream consumption."""
        for idx, item in enumerate(batch):
            valid, reason = self._apply_validators(idx, item)
            if not valid:
                yield {"index": idx, "status": "rejected", "reason": reason, "result": None}
                continue

            processed = item.upper() if isinstance(item, str) else item
            yield {
                "index": idx,
                "status": "success",
                "reason": "valid",
                "result": processed,
            }


if __name__ == "__main__":
    sample_data = ["hello", "", 42, 99999, {"key": "val"}, None]
    engine = CoreProcessor()
    results = list(engine.process_batch(sample_data))
    print(f"Processed {len(results)} items through loop.")