class UtilityError(Exception):
    """Base exception for python-utils-61."""

class ConfigurationError(UtilityError):
    """Raised when configuration constraints are violated."""

class ProcessingError(UtilityError):
    """Raised when data pipeline operations fail."""

class Registry:
    """Dynamic exception catalog using registry pattern."""
    _registry = {}

    @classmethod
    def register(cls, name: str, base=UtilityError):
        def decorator(klass):
            cls._registry[name] = klass
            return klass
        return decorator

    @classmethod
    def raise_by_name(cls, name: str, *args):
        exc_class = cls._registry.get(name, UtilityError)
        raise exc_class(*args)

@Registry.register("validation")
class ValidationError(UtilityError):
    def __init__(self, field, reason):
        super().__init__(f"Field {field} invalid: {reason}")

def ensure(condition: bool, error_type: str, *args):
    if not condition:
        Registry.raise_by_name(error_type, *args)