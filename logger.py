import os
import sys
import logging
from logging.handlers import RotatingFileHandler
from typing import Optional, Union, PathLike

class DynamicRotatingLogger:
    """A fluent, self-configuring rotating logger with dual-stream formatting."""
    
    def __init__(self, name: str = "app", log_dir: Union[str, PathLike] = "logs"):
        self.name = name
        self.log_dir = os.path.abspath(str(log_dir))
        os.makedirs(self.log_dir, exist_ok=True)
        self._logger = logging.getLogger(self.name)
        self._logger.setLevel(logging.DEBUG)
        self._logger.propagate = False
        
    def configure(
        self,
        filename: str = "app.log",
        max_bytes: int = 1_048_576,
        backup_count: int = 5,
        level: int = logging.INFO,
        fmt: Optional[str] = None
    ) -> logging.Logger:
        if self._logger.handlers:
            self._logger.handlers.clear()

        filepath = os.path.join(self.log_dir, filename)
        handler = RotatingFileHandler(
            filepath, maxBytes=max_bytes, backupCount=backup_count, encoding="utf-8"
        )
        
        default_fmt = "[%(asctime)s] [%(levelname)s] [%(name)s:%(threadName)s] - %(message)s"
        formatter = logging.Formatter(fmt or default_fmt, datefmt="%Y-%m-%d %H:%M:%S")
        handler.setFormatter(formatter)
        handler.setLevel(level)

        console = logging.StreamHandler(sys.stdout)
        console.setFormatter(formatter)
        console.setLevel(level)

        self._logger.addHandler(handler)
        self._logger.addHandler(console)
        self._logger.debug(f"Logger initialized at {filepath}")
        return self._logger

def setup_rotating_logger(
    name: str = "main",
    log_file: str = "output.log",
    max_mb: float = 2.0,
    backups: int = 3
) -> logging.Logger:
    bytes_limit = int(max_mb * 1024 * 1024)
    builder = DynamicRotatingLogger(name=name)
    return builder.configure(filename=log_file, max_bytes=bytes_limit, backup_count=backups)
