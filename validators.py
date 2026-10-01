from typing import Any, Callable, Generator, Dict, Union, List

def validate_structure(data: Any, schema: Any, path: str = "$") -> Generator[str, None, None]:
    """
    Recursively validates data against a structural schema, yielding mismatch messages.
    Supports exact values, types, callable predicates, and nested list/dict models.
    """
    if isinstance(schema, dict):
        if not isinstance(data, dict):
            yield f"{path}: expected dict, got {type(data).__name__}"
            return
        for key, rule in schema.items():
            if key not in data:
                yield f"{path}.{key}: missing required key"
            else:
                yield from validate_structure(data[key], rule, f"{path}.{key}")
    elif isinstance(schema, list):
        if not isinstance(data, (list, tuple)):
            yield f"{path}: expected list-like, got {type(data).__name__}"
            return
        if len(schema) == 1:
            rule = schema[0]
            for idx, item in enumerate(data):
                yield from validate_structure(item, rule, f"{path}[{idx}]")
        else:
            for idx, rule in enumerate(schema):
                if idx >= len(data):
                    yield f"{path}[{idx}]: missing positional item"
                else:
                    yield from validate_structure(data[idx], rule, f"{path}[{idx}]")
    else:
        is_valid = False
        if isinstance(schema, type):
            is_valid = isinstance(data, schema)
        elif callable(schema):
            try:
                is_valid = bool(schema(data))
            except Exception:
                is_valid = False
        else:
            is_valid = (data == schema)

        if not is_valid:
            name = schema.__name__ if hasattr(schema, "__name__") else str(schema)
            yield f"{path}: failed validation against {name} (value: {repr(data)})"

def audit_payload(payload: Any, schema: Any) -> dict:
    """
    Performs audit on payload, returning status and list of structural infractions.
    """
    errors = list(validate_structure(payload, schema))
    return {
        "valid": len(errors) == 0,
        "errors": errors
    }