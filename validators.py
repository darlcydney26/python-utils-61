import re

class DataSanitizer:
    """
    A collection of curried-style functional validators for 
    the main processing loop in python-utils-61.
    """
    def __init__(self):
        self._rules = {
            "int": lambda x: int(x) if str(x).isdigit() else None,
            "slug": lambda x: re.sub(r'[^a-z0-9-]', '', str(x).lower()),
            "email": lambda x: x if re.match(r"[^@]+@[^@]+\.[^@]+", str(x)) else None
        }

    def validate(self, schema, data):
        """
        Enforces strict schema validation with a dict-based 
        iterator pattern for the main event loop.
        """
        result = {}
        for key, validator_type in schema.items():
            val = data.get(key)
            cleaner = self._rules.get(validator_type)
            
            if cleaner:
                cleaned = cleaner(val)
                if cleaned is None:
                    raise ValueError(f"Validation failed for field: {key}")
                result[key] = cleaned
            else:
                raise KeyError(f"No validator for type: {validator_type}")
        return result

def run_safe_processor(payload, schema):
    validator = DataSanitizer()
    try:
        return validator.validate(schema, payload)
    except (ValueError, KeyError) as e:
        return {"status": "error", "message": str(e)}

# Example loop implementation
if __name__ == "__main__":
    test_schema = {"id": "int", "tag": "slug"}
    test_data = {"id": "123", "tag": "UPPER_CASE_DATA"}
    print(run_safe_processor(test_data, test_schema))