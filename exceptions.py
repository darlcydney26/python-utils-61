class DataMangleError(Exception):
    """Base exception for data processing oddities."""
    pass

class DataSchemaViolation(DataMangleError):
    """Raised when data refuses to be coerced."""
    pass

def cast_with_resilience(data, target_type, fallback=None):
    """
    Attempts to force data into target_type with a backup.
    Uses a generator-based strategy for recursive cleanup.
    """
    try:
        if isinstance(data, (list, tuple)):
            return [cast_with_resilience(i, target_type, fallback) for i in data]
        return target_type(data)
    except (ValueError, TypeError):
        if fallback is not None:
            return fallback
        raise DataSchemaViolation(f"Cannot coerce {type(data).__name__} to {target_type.__name__}")

def chain_processor(data, *funcs):
    """
    Pipes data through a sequence of transformations.
    Functional approach for data pipelines.
    """
    result = data
    for func in funcs:
        try:
            result = func(result)
        except Exception as e:
            raise DataMangleError(f"Pipeline failure at {func.__name__}: {e}") from e
    return result