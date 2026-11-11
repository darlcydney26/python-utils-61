import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional, Union


class RingBufferFormatter(logging.Formatter):
    """Custom formatter that appends an incremental sequence identifier to log entries."""

    def __init__(self, fmt: Optional[str] = None, datefmt: Optional[str] = None):
        fmt = fmt or "[%(asctime)s] [#%(seq)05d] %(levelname)s: %(message)s"
        super().__init__(fmt=fmt, datefmt=datefmt)
        self._seq = 0

    def format(self, record: logging.LogRecord) -> str:
        self._seq += 1
        setattr(record, "seq", self._seq)
        return super().format(record)


def setup_rotating_logger(
    name: str = "app_logger",
    log_file: Union[str, Path] = "logs/app.log",
    max_bytes: int = 1_048_576,
    backup_count: int = 5,
    level: int = logging.INFO,
    enable_console: bool = True,
) -> logging.Logger:
    """Configures a logger with custom sequence formatting and rotating file storage."""
    target_path = Path(log_file)
    target_path.parent.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.handlers.clear()

    formatter = RingBufferFormatter()

    file_handler = RotatingFileHandler(
        filename=target_path,
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(level)
    logger.addHandler(file_handler)

    if enable_console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        console_handler.setLevel(level)
        logger.addHandler(console_handler)

    return logger
