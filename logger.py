import os
import gzip
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Union

def _gzip_namer(name: str) -> str:
    """Appends .gz extension to the rotated log file name."""
    return f"{name}.gz"

def _gzip_rotator(source: str, dest: str) -> None:
    """Compresses the rotated log file using gzip and deletes the original source."""
    if os.path.exists(source):
        with open(source, "rb") as f_in:
            with gzip.open(dest, "wb", compresslevel=9) as f_out:
                f_out.writelines(f_in)
        os.remove(source)

def configure_rotating_logger(
    name: str,
    filepath: Union[str, Path],
    max_bytes: int = 1048576,
    backup_count: int = 5,
    level: int = logging.INFO
) -> logging.Logger:
    """
    Creates and configures a logger that automatically compresses
    rotated log files using gzip on the fly.
    """
    log_path = Path(filepath)
    log_path.parent.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.propagate = False

    if logger.handlers:
        logger.handlers.clear()

    handler = RotatingFileHandler(
        filename=str(log_path),
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding="utf-8"
    )

    handler.namer = _gzip_namer
    handler.rotator = _gzip_rotator

    formatter = logging.Formatter(
        fmt="%(asctime)s [%(levelname)s] %(name)s (%(filename)s:%(lineno)d) - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger