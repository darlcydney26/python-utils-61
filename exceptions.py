import sys
import traceback
from typing import Any, Dict, Optional, Type


class EnhancedUtilError(Exception):
    """A base exception that captures context and formats traceback cleanly."""

    def __init__(
        self, message: str, context: Optional[Dict[str, Any]] = None
    ) -> None:
        super().__init__(message)
        self.message: str = message
        self.context: Dict[str, Any] = context or {}
        self._exc_info = sys.exc_info()

    def __str__(self) -> str:
        context_str = (
            f" | Context: {self.context}" if self.context else ""
        )
        return f"{self.message}{context_str}"

    def detailed_report(self) -> str:
        """Generates a detailed report of the exception, including captured traceback."""
        report = [f"[{self.__class__.__name__}]: {self.message}"]
        if self.context:
            report.append("Context Metadata:")
            for k, v in self.context.items():
                report.append(f"  - {k}: {v}")
        if self._exc_info and self._exc_info[1]:
            tb = "".join(traceback.format_exception(*self._exc_info))
            report.append("Caused by Underlying Exception:")
            report.append(tb)
        return "\n".join(report)


class ConfigurationError(EnhancedUtilError):
    """Raised when a system-wide configuration is invalid or missing."""


class ProcessingError(EnhancedUtilError):
    """Raised when an operation within the processor fails."""


class ValidationFailed(EnhancedUtilError):
    """Raised when validators find malformed or inappropriate data."""


def raise_with_context(
    exc_type: Type[EnhancedUtilError], message: str, **context: Any
) -> None:
    """Helper function to raise an exception with inline keyword context."""
    raise exc_type(message, context=context)
