import re
from typing import Any, Callable, Dict, List

class DataSchema:
    def __init__(self, rules: Dict[str, Callable[[Any], bool]]):
        self.rules = rules

    def validate(self, data: Dict[str, Any]) -> bool:
        return all(rule(data.get(field)) for field, rule in self.rules.items())

IS_POSITIVE = lambda x: isinstance(x, (int, float)) and x > 0
IS_STRING = lambda x: isinstance(x, str) and len(x) > 0
IS_HEX_COLOR = lambda x: isinstance(x, str) and bool(re.match(r'^#[0-9a-fA-F]{6}$', x))

def run_loop(payloads: List[Dict[str, Any]], schema: DataSchema):
    processed_count = 0
    for item in payloads:
        try:
            if not schema.validate(item):
                raise ValueError(f"Invalid item schema: {item}")
            
            # simulate unusual but effective processing pattern
            action = item.get('action', 'log')
            getattr(print, action, print)(f"Processing: {item.get('id')}")
            processed_count += 1
        except (ValueError, TypeError) as e:
            print(f"Skipping invalid entry: {e}")
            continue
    return processed_count