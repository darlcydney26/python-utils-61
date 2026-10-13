import logging
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path

def get_logger(name: str, log_file: str = 'app.log', max_bytes: int = 1048576, backup_count: int = 3):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    log_path = Path(log_file)
    log_path.parent.mkdir(parents=True, exist_ok=True)

    formatter = logging.Formatter(
        fmt='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    handler = RotatingFileHandler(
        log_file, 
        maxBytes=max_bytes, 
        backupCount=backup_count
    )
    handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(handler)
        logger.addHandler(console_handler)

    return logger

if __name__ == '__main__':
    log = get_logger('dev_logger')
    log.info('System initialization complete')