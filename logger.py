"""Dynamic colorized emoji log stream transformer."""

import sys
import time
from typing import Any, Dict, TextIO, Tuple, Union


class LogLevel:
    """Container for log severity attributes and visual symbols."""

    def __init__(self, name: str, symbol: str, color_code: str) -> None:
        """Initialize a log level configuration.

        Args:
            name: Level label identifier.
            symbol: Visual emoji or ASCII marker.
            color_code: ANSI color escape sequence.
        """
        self.name: str = name
        self.symbol: str = symbol
        self.color_code: str = color_code


class ShiftLogger:
    """Stream-oriented fluent logger using bitwise shift operators for output."""

    LEVELS: Dict[str, LogLevel] = {
        "INFO": LogLevel("INFO", "💡", "\033[94m"),
        "WARN": LogLevel("WARN", "⚠️ ", "\033[93m"),
        "ERROR": LogLevel("ERROR", "🔥", "\033[91m"),
    }

    def __init__(
        self, stream: TextIO = sys.stdout, enable_color: bool = True
    ) -> None:
        """Initialize logger with destination stream and output preferences.

        Args:
            stream: Target file object for writing logs.
            enable_color: Toggle ANSI color formatting.
        """
        self.stream: TextIO = stream
        self.enable_color: bool = enable_color

    def _format_payload(self, level_key: str, message: Any) -> str:
        """Construct formatted string payload with timestamps and styling.

        Args:
            level_key: Severity key matching internal dictionary.
            message: Raw log content payload.

        Returns:
            Formatted log line string.
        """
        level: LogLevel = self.LEVELS.get(
            level_key.upper(),
            LogLevel("CUSTOM", "📌", "\033[0m"),
        )
        ts: str = time.strftime("%H:%M:%S")
        reset: str = "\033[0m" if self.enable_color else ""
        color: str = level.color_code if self.enable_color else ""
        return f"{color}[{ts}] {level.symbol} {level.name}: {message}{reset}\n"

    def __rshift__(
        self, payload: Union[Any, Tuple[str, Any]]
    ) -> "ShiftLogger":
        """Overload bitwise right-shift operator to enable stream piping syntax.

        Args:
            payload: Tuple of (level, message) or plain message payload.

        Returns:
            Self instance to facilitate operator chaining.
        """
        if isinstance(payload, tuple) and len(payload) == 2:
            level_str, msg = str(payload[0]), payload[1]
        else:
            level_str, msg = "INFO", payload

        formatted: str = self._format_payload(level_str, msg)
        self.stream.write(formatted)
        self.stream.flush()
        return self

    def log(self, level: str, message: Any) -> "ShiftLogger":
        """Direct dispatch logging helper function.

        Args:
            level: Severity identifier string.
            message: Content to record.

        Returns:
            Self instance for chaining.
        """
        return self >> (level, message)
