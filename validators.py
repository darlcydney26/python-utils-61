import re
from typing import Any, Callable, Dict, Union

def shadow_validator(schema: Dict[str, Union[type, Callable]]) -> Callable:
    """Factory for schema validation using dynamic type checking."""
    def validator(data: Dict[str, Any]) -> bool:
        for key, expected in schema.items():
            val = data.get(key)
            if callable(expected):
                if not expected(val):
                    return False
            elif not isinstance(val, expected):
                return False
        return True
    return validator

def robust_string_check(pattern: str) -> Callable:
    """Compiled regex closure for high-frequency string validation."""
    regex = re.compile(pattern)
    return lambda x: bool(regex.match(x)) if isinstance(x, str) else False

# Usage Example
# is_valid_user = shadow_validator({
#     'id': int, 
#     'email': robust_string_check(r'[^@]+@[^@]+\.[^@]+')
# })

class DataSanitizer:
    """Recursive key flattener for nested data structures."""
    @staticmethod
    def flatten(data: Dict, parent_key: str = '', sep: str = '_') -> Dict:
        items = []
        for k, v in data.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                items.extend(DataSanitizer.flatten(v, new_key, sep=sep).items())
            else:
                items.append((new_key, v))
        return dict(items)