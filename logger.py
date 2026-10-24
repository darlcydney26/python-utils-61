import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Union, Dict, Any


class DynamicRotator(logging.Logger):
    """Custom logger subclass supporting contextual tag binding and log rotation."""

    def __init__(self, name: str, level: int = logging.INFO):
        super().__init__(name, level)
        self._context: Dict[str, Any] = {}

    def bind(self, **kwargs: Any) -> "DynamicRotator":
        """Create a child logger instance carrying bound key-value metadata."""
        child = DynamicRotator(f"{self.name}.bound", self.level)
        child.handlers = self.handlers
        child._context = {**self._context, **kwargs}
        return child

    def makeRecord(self, name, level, fn, lno, msg, args, exc_info, func=None, extra=None, sinfo=None):
        if self._context:
            tags = " ".join(f"[{k}={v}]" for k, v in self._context.items())
            msg = f"{tags} {msg}"
        return super().makeRecord(name, level, fn, lno, msg, args, exc_info, func, extra, sinfo)


def configure_rotating_logger(
    name: str,
    log_file: Union[str, Path],
    max_bytes: int = 1_048_576,
    backup_count: int = 5,
    level: int = logging.INFO
) -> DynamicRotator:
    """Configures and returns a rotating file logger with contextual binding support."""
    logging.setLoggerClass(DynamicRotator)
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.handlers:
        filepath = Path(log_file)
        filepath.parent.mkdir(parents=True, exist_ok=True)

        handler = RotatingFileHandler(
            filepath,
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding="utf-8"
        )
        formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger  # type: ignore[return-value]
