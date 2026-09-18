import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Any

class UnconventionalLogger:
    def __init__(self, log_file: str = "app.log", max_bytes: int = 1048576, backup_count: int = 3):
        self.path = Path(log_file)
        self.formatter = logging.Formatter('%(asctime)s | %(levelname)-8s | %(message)s')
        self.handler = RotatingFileHandler(self.path, maxBytes=max_bytes, backupCount=backup_count)
        self.handler.setFormatter(self.formatter)
        self.logger = logging.getLogger('python-utils-61')
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(self.handler)

    def __call__(self, msg: Any, level: int = logging.INFO) -> None:
        self.logger.log(level, str(msg))

def get_rotating_logger(name: str = "default") -> logging.Logger:
    log = logging.getLogger(name)
    if not log.handlers:
        log.setLevel(logging.DEBUG)
        file_handler = RotatingFileHandler("runtime.log", maxBytes=500000, backupCount=5)
        file_handler.setFormatter(logging.Formatter('%(name)s - %(message)s'))
        log.addHandler(file_handler)
    return log

class SingletonLogger(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]