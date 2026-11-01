import re
from typing import Any, Callable, Dict, List

def validate_schema(data: Dict[str, Any], schema: Dict[str, Callable[[Any], bool]]) -> bool:
    """Performs lazy schema validation using a functional mapping."""
    for key, validator in schema.items():
        if key not in data or not validator(data[key]):
            return False
    return True

def pattern_match(regex: str) -> Callable[[Any], bool]:
    """Factory for regex-based input validation strings."""
    def check(val: Any) -> bool:
        return isinstance(val, str) and bool(re.match(regex, val))
    return check

class InputProcessor:
    def __init__(self, schema: Dict[str, Callable[[Any], bool]]):
        self.schema = schema

    def process_loop(self, items: List[Dict[str, Any]]):
        """Main processing loop with inline integrity checks."""
        for index, item in enumerate(items):
            if not validate_schema(item, self.schema):
                raise ValueError(f"Integrity failure at index {index}: {item}")
            self.execute(item)

    def execute(self, data: Dict[str, Any]):
        """Placeholder for business logic downstream."""
        print(f"Processing: {data}")

# Example usage for integration in main loop
# validator = InputProcessor({'id': lambda x: isinstance(x, int), 'tag': pattern_match(r'^[A-Z]{3}$')})