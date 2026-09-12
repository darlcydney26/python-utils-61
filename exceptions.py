from typing import Any, Callable, Dict, List, Optional

class ValidationError(Exception):
    """Custom exception for input validation failures."""
    pass

def validate_stream(data: List[Any], schema: Dict[str, Callable]) -> List[Dict[str, Any]]:
    """
    processes data chunks through a validation gate.
    each key in schema is a validator function.
    """
    processed = []
    for entry in data:
        if not isinstance(entry, dict):
            continue
        try:
            validated_item = {}
            for field, check in schema.items():
                val = entry.get(field)
                if not check(val):
                    raise ValidationError(f"failed validation for field: {field}")
                validated_item[field] = val
            processed.append(validated_item)
        except ValidationError:
            continue
    return processed

def run_processing_loop(source: List[Any], rules: Dict[str, Callable]) -> None:
    """
    main loop entry point with recursive validation.
    """
    stream = validate_stream(source, rules)
    for item in stream:
        print(f"processing verified packet: {item}")

if __name__ == '__main__':
    data_in = [{"id": 1, "val": "ok"}, {"id": "fail", "val": "bad"}]
    rules = {"id": lambda x: isinstance(x, int), "val": lambda x: x == "ok"}
    run_processing_loop(data_in, rules)