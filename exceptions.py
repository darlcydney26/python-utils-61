import inspect
from typing import Any, Callable, Dict, Optional, Type


class EdgeCaseError(Exception):
    """Raised when code encounters structural boundaries or unforeseen edge states."""

    def __init__(
        self,
        message: str,
        original_cause: Optional[BaseException] = None,
        snapshot: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(message)
        self.message = message
        self.original_cause = original_cause
        self.snapshot = snapshot or {}

    def __str__(self) -> str:
        cause_info = f" [Cause: {type(self.original_cause).__name__}({self.original_cause})]" if self.original_cause else ""
        context_info = f" [State: {self.snapshot}]" if self.snapshot else ""
        return f"<EdgeCaseError: {self.message}>{cause_info}{context_info}"


class BoundaryGuard:
    """Context manager and decorator converting primitive runtime exceptions into EdgeCaseError."""

    TRAPPED_EXCEPTIONS: tuple[Type[BaseException], ...] = (
        ZeroDivisionError,
        OverflowError,
        RecursionError,
        IndexError,
        KeyError,
        ValueError,
    )

    def __init__(self, fallback: Any = None, suppress: bool = False):
        self.fallback = fallback
        self.suppress = suppress

    def __enter__(self) -> "BoundaryGuard":
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Any,
    ) -> bool:
        if exc_type is None:
            return True

        if issubclass(exc_type, self.TRAPPED_EXCEPTIONS):
            frame = exc_tb.tb_frame if exc_tb else inspect.currentframe()
            scope_dump = {
                k: repr(v)[:40]
                for k, v in (frame.f_locals.items() if frame else {})
                if not k.startswith("_")
            }
            error = EdgeCaseError(
                f"Edge case intercepted in '{frame.f_code.co_name if frame else 'unknown'}'",
                original_cause=exc_val,
                snapshot=scope_dump,
            )
            if self.suppress:
                return True
            raise error from exc_val
        return False

    def __call__(self, func: Callable) -> Callable:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                with self:
                    return func(*args, **kwargs)
            except EdgeCaseError:
                if self.fallback is not None:
                    return self.fallback
                raise
        return wrapper
