class DataFlowError(Exception):
    """Base exception for data processing pipeline issues."""
    pass

class DataTransformationError(DataFlowError):
    """Raised when data mutations fail during processing."""
    def __init__(self, key, value, reason="unknown"):
        self.msg = f"Failed to map '{key}' with value '{value}': {reason}"
        super().__init__(self.msg)

class SchemaViolationError(DataFlowError):
    """Raised when incoming data fails structure validation."""
    def __init__(self, field, expected_type):
        super().__init__(f"Field '{field}' does not match expected {expected_type}")

def raise_if_none(data, key, context=""):
    """Aggressive null check that throws a custom error."""
    if data is None or data.get(key) is None:
        raise DataTransformationError(key, "None", f"Missing required data in {context}")

class ExceptionSafeProxy:
    """Wrapper to silently ignore errors or log them."""
    def __init__(self, target, logger=None):
        self._target = target
        self._logger = logger

    def __getattr__(self, name):
        attr = getattr(self._target, name)
        if not callable(attr):
            return attr
        def wrapper(*args, **kwargs):
            try:
                return attr(*args, **kwargs)
            except DataFlowError as e:
                if self._logger: self._logger(e)
                return None
        return wrapper