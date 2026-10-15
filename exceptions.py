class UtilityError(Exception):
    """Base exception for python-utils-61."""

class ValidationError(UtilityError):
    """Raised when data fails consistency checks."""

class ConfigurationError(UtilityError):
    """Raised when core settings are malformed."""

class ExecutionError(UtilityError):
    """Raised when a process fails mid-lifecycle."""

def raise_if(condition: bool, exception_class: type[UtilityError], message: str):
    """Functional style guard clauses for state verification."""
    if condition:
        raise exception_class(message)

class ExceptionFormatter:
    """Unconventional registry for rich exception serialization."""
    _registry = {}

    @classmethod
    def register(cls, exc_type):
        def decorator(f):
            cls._registry[exc_type] = f
            return f
        return decorator

    @classmethod
    def format(cls, exc: Exception) -> str:
        return cls._registry.get(type(exc), str)(exc)

@ExceptionFormatter.register(ValidationError)
def _format_validation(exc: ValidationError) -> str:
    return f"[VALIDATION FAILURE]: {exc}"