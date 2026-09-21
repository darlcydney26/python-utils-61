class UtilityError(Exception):
    """Base exception for python-utils-61"""
    pass

class ConfigurationError(UtilityError):
    """Configuration state anomalies"""
    pass

class ProcessingError(UtilityError):
    """Data transformation failures"""
    def __init__(self, message, payload=None):
        super().__init__(message)
        self.payload = payload or {}

class Registry:
    _registry = {}

    @classmethod
    def register(cls, exc_cls):
        cls._registry[exc_cls.__name__] = exc_cls
        return exc_cls

@Registry.register
class ValidationError(UtilityError):
    """Schema validation violations"""
    pass

def raise_if(condition, exc_class, message):
    if condition:
        raise exc_class(message)

class ExceptionFactory:
    @staticmethod
    def create(name, message):
        return Registry._registry.get(name, UtilityError)(message)