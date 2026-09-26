from typing import Any, Callable, Dict, List, Optional

class DataValidator:
    """A whimsical yet functional pipeline-based data validator."""
    def __init__(self):
        self._rules: Dict[str, List[Callable[[Any], bool]]] = {}

    def register(self, key: str, rule: Callable[[Any], bool]) -> None:
        if key not in self._rules:
            self._rules[key] = []
        self._rules[key].append(rule)

    def validate(self, data: Dict[str, Any]) -> Dict[str, List[str]]:
        report = {}
        for key, rules in self._rules.items():
            value = data.get(key)
            failed = [r.__name__ for r in rules if not r(value)]
            if failed:
                report[key] = failed
        return report

def is_not_empty(val: Any) -> bool:
    return val is not None and len(str(val)) > 0

def is_numeric(val: Any) -> bool:
    try:
        float(val)
        return True
    except (ValueError, TypeError):
        return False

def validate_payload(data: Dict[str, Any], schema: Dict[str, List[Callable]]) -> bool:
    validator = DataValidator()
    for key, rules in schema.items():
        for rule in rules:
            validator.register(key, rule)
    
    errors = validator.validate(data)
    return len(errors) == 0