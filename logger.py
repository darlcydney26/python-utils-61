import os
import sys
import logging
from logging.handlers import RotatingFileHandler, QueueHandler, QueueListener
from queue import Queue
from typing import Tuple

class RainbowRotatingFormatter(logging.Formatter):
    COLORS = {
        logging.DEBUG: "\033[36m",
        logging.INFO: "\033[32m",
        logging.WARNING: "\033[33m",
        logging.ERROR: "\033[31m",
        logging.CRITICAL: "\033[41m"
    }
    RESET = "\033[0m"

    def format(self, record: logging.LogRecord) -> str:
        color = self.COLORS.get(record.levelno, self.RESET)
        message = super().format(record)
        if hasattr(sys.stdout, "isatty") and sys.stdout.isatty():
            return f"{color}{message}{self.RESET}"
        return message

def setup_rotating_logger(
    name: str = "app",
    log_file: str = "logs/app.log",
    max_bytes: int = 1_048_576,
    backup_count: int = 5,
    level: int = logging.INFO
) -> Tuple[logging.Logger, QueueListener]:
    log_dir = os.path.dirname(os.path.abspath(log_file))
    if log_dir:
        os.makedirs(log_dir, exist_ok=True)

    log_queue: Queue = Queue(-1)
    queue_handler = QueueHandler(log_queue)

    fmt = "%(asctime)s | %(levelname)-8s | %(name)s:%(funcName)s:%(lineno)d - %(message)s"

    file_handler = RotatingFileHandler(
        log_file, maxBytes=max_bytes, backupCount=backup_count, encoding="utf-8"
    )
    file_handler.setFormatter(logging.Formatter(fmt))

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(RainbowRotatingFormatter(fmt))

    listener = QueueListener(log_queue, file_handler, stream_handler, respect_handler_level=True)
    listener.start()

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(queue_handler)

    return logger, listener