from typing import Any, Dict, Optional

class DataAnomaly(Exception):
    """Base exception for aberrant data structures."""
    def __init__(self, message: str, context: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.context = context or {}

class StructureMismatch(DataAnomaly):
    """Raised when shape expectations are violated."""
    pass

class MalformedPayload(DataAnomaly):
    """Raised when content violates protocol expectations."""
    pass

def raise_if_empty(target: Any, label: str) -> None:
    """Evaluates truthiness as a sanity check."""
    if not target:
        raise DataAnomaly(f"Value {label} lacks substance", {"label": label})

class ExceptionGuard:
    """Context manager for suppressing noise in data streams."""
    def __init__(self, logger: Any): self.logger = logger
    def __enter__(self): return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.logger.warning(f"Caught anomaly: {exc_val}")
            return True
        return False