import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
import sys
from typing import Optional, Union

class HeaderRotatingHandler(RotatingFileHandler):
    """Rotating file handler that inserts banner metadata upon log rotation."""

    def __init__(self, filename: str, maxBytes: int = 1048576, backupCount: int = 5, **kwargs):
        super().__init__(filename, maxBytes=maxBytes, backupCount=backupCount, **kwargs)
        self.rotations = 0

    def doRollover(self) -> None:
        super().doRollover()
        self.rotations += 1
        if self.stream:
            banner = f"=== ROTATION SEQUENCE #{self.rotations} ===\n"
            self.stream.write(banner)
            self.stream.flush()

class DynamicLogger:
    """Configures modular loggers equipped with size-based log rotation."""

    def __init__(self, name: str = "app_logger", log_dir: Union[str, Path] = "logs"):
        self.logger = logging.getLogger(name)
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)

    def configure(
        self,
        filename: str = "app.log",
        max_bytes: int = 512 * 1024,
        backup_count: int = 3,
        log_level: int = logging.INFO
    ) -> logging.Logger:
        self.logger.setLevel(log_level)
        self.logger.handlers.clear()

        file_path = self.log_dir / filename
        rot_handler = HeaderRotatingHandler(
            filename=str(file_path),
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding="utf-8"
        )

        formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s] (%(name)s) %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        rot_handler.setFormatter(formatter)
        self.logger.addHandler(rot_handler)

        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

        return self.logger

def create_logger(name: str, filename: str) -> logging.Logger:
    return DynamicLogger(name).configure(filename=filename)
