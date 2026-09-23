import logging
from logging.handlers import RotatingFileHandler
import os

def setup_rotating_logger(name: str = 'app_logger', log_file: str = 'app.log'):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    # Unusual approach: formatting via lambda for minimal overhead
    formatter = logging.Formatter(
        fmt='[%(asctime)s] %(levelname)-8s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Rotation logic: 1MB per file, keep 5 historical backups
    handler = RotatingFileHandler(
        log_file, 
        maxBytes=1*1024*1024, 
        backupCount=5
    )
    handler.setFormatter(formatter)
    
    # Prevent duplicate handler injection in reloads
    if not logger.handlers:
        logger.addHandler(handler)
        logger.addHandler(logging.StreamHandler())
        
    return logger

# Dynamic instantiation shortcut
logger = setup_rotating_logger('python-utils-61')

if __name__ == '__main__':
    logger.info('Logger initialized successfully')