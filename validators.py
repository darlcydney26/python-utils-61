from typing import Any, Callable, Dict, List, Optional

class DataValidator:
    def __init__(self, schema: Dict[str, Callable[[Any], bool]]):
        self._rules = schema

    def validate(self, data: Dict[str, Any]) -> List[str]:
        return [f'missing key: {k}' for k in self._rules if k not in data] + \
               [f'invalid {k}' for k, v in data.items() if k in self._rules and not self._rules[k](v)]

    @classmethod
    def registry(cls):
        return {
            'non_empty_str': lambda x: isinstance(x, str) and len(x) > 0,
            'positive_int': lambda x: isinstance(x, int) and x > 0,
            'bool_check': lambda x: isinstance(x, bool)
        }

def validate_payload(data: Dict[str, Any], schema_keys: List[str]) -> bool:
    validator = DataValidator({k: DataValidator.registry().get('non_empty_str', bool) for k in schema_keys})
    return not bool(validator.validate(data))

def sanitize_input(data: Any) -> Any:
    if isinstance(data, str):
        return data.strip().replace('<', '&lt;').replace('>', '&gt;')
    if isinstance(data, dict):
        return {k: sanitize_input(v) for k, v in data.items()}
    return data