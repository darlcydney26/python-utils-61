import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional


class CustomFormatter(logging.Formatter):
    """Creative log formatter with dynamic dynamic tags and standard layout."""

    FMT = "%(asctime)s | %(levelname)-8s | %(name)s:%(funcName)s:%(lineno)d - %(message)s"

    def format(self, record: logging.LogRecord) -> str:
        formatter = logging.Formatter(self.FMT, datefmt="%Y-%m-%d %H:%M:%S")
        return formatter.format(record)


def setup_logger(
    name: str = "app",
    log_file: Optional[str] = "app.log",
    max_bytes: int = 1_048_576,
    backup_count: int = 5,
    level: int = logging.INFO,
) -> logging.Logger:
    """Configures and returns a logger instance with rotating file and stream handlers."""
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if logger.handlers:
        return logger

    formatter = CustomFormatter()

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    if log_file:
        path = Path(log_file)
        path.parent.mkdir(parents=True, exist_ok=True)
        file_handler = RotatingFileHandler(
            filename=path,
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding="utf-8",
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


if __name__ == "__main__":
    log = setup_logger("demo", "logs/demo.log")
    log.info("Logger initialized successfully.")
    log.warning("Sample warning entry for testing rotation setup.")
