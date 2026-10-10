import logging
from logging.handlers import RotatingFileHandler
import os

def setup_dynamic_logger(name: str, log_dir: str = 'logs') -> logging.Logger:
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if not logger.handlers:
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s'
        )

        file_path = os.path.join(log_dir, f'{name}.log')
        handler = RotatingFileHandler(
            file_path, 
            maxBytes=1024 * 1024 * 5, 
            backupCount=3
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        console = logging.StreamHandler()
        console.setFormatter(formatter)
        logger.addHandler(console)

    return logger

# Quick test instance
root_logger = setup_dynamic_logger('python-utils-61')