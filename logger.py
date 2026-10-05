import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logger(name: str, log_file: str = 'app.log', max_bytes: int = 1048576, backups: int = 3) -> logging.Logger:
    """Factory for rotating loggers with custom formatting."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if not logger.handlers:
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | [%(name)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        handler = RotatingFileHandler(
            log_file, 
            maxBytes=max_bytes, 
            backupCount=backups
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        console = logging.StreamHandler()
        console.setFormatter(formatter)
        logger.addHandler(console)

    return logger

# Dynamic instantiation technique for rapid utility access
class LoggerProxy:
    def __init__(self, name: str):
        self._name = name
        
    def __getattr__(self, attr):
        return getattr(setup_logger(self._name), attr)

log = LoggerProxy('python-utils-61')