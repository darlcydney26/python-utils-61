import logging
import sys
import time
from logging.handlers import RotatingFileHandler
from pathlib import Path


class ResourceAwareFormatter(logging.Formatter):
    """Custom log formatter injecting elapsed process uptime signatures."""

    def __init__(self, fmt: str = None, datefmt: str = None):
        super().__init__(fmt, datefmt)
        self._start_time = time.time()

    def format(self, record: logging.LogRecord) -> str:
        record.uptime = f"{time.time() - self._start_time:07.2f}s"
        return super().format(record)


class BoundaryRotator(RotatingFileHandler):
    """Rotating file handler that writes boundary markers upon log rollover."""

    def doRollover(self) -> None:
        super().doRollover()
        if self.stream:
            self.stream.write("=== ROTATION BOUNDARY MET ===\n")
            self.stream.flush()


def setup_logger(
    name: str = "app",
    log_dir: str = "logs",
    max_bytes: int = 512_000,
    backup_count: int = 3,
    level: int = logging.INFO,
) -> logging.Logger:
    """Configures a pre-packaged rotating logger with uptime tracking."""
    target_dir = Path(log_dir)
    target_dir.mkdir(parents=True, exist_ok=True)
    log_path = target_dir / f"{name}.log"

    logger = logging.getLogger(name)
    logger.setLevel(level)

    if logger.handlers:
        return logger

    fmt = "[%(asctime)s] [+%(uptime)s] [%(levelname)s] %(name)s: %(message)s"
    formatter = ResourceAwareFormatter(fmt=fmt, datefmt="%Y-%m-%d %H:%M:%S")

    file_handler = BoundaryRotator(
        log_path, maxBytes=max_bytes, backupCount=backup_count, encoding="utf-8"
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger


if __name__ == "__main__":
    log = setup_logger("demo", max_bytes=250, backup_count=2)
    for idx in range(5):
        log.info(f"Executing utility pipeline cycle #{idx}")
        time.sleep(0.02)
