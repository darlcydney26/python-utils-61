class DataProcessingError(Exception):
    """Base exception for data flow issues."""

class TransformationError(DataProcessingError):
    """Raised when data shape mismatch occurs."""

class SchemaViolationError(DataProcessingError):
    """Raised when data fails strict validation."""

def graceful_fail(func):
    """Decorator for trapping errors with custom labels."""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            raise DataProcessingError(f"Failure in {func.__name__}: {str(e)}") from e
    return wrapper

class ErrorAggregator:
    """Registry for silent failure collection."""
    def __init__(self):
        self.errors = []

    def capture(self, error: Exception):
        self.errors.append({
            "type": type(error).__name__,
            "msg": str(error),
            "context": "data-pipeline-runtime"
        })

    def has_errors(self) -> bool:
        return len(self.errors) > 0

    def report(self):
        return self.errors