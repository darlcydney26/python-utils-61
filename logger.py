import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logger(name='app_logger', log_file='app.log', level=logging.INFO):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    if not logger.handlers:
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
        # Custom approach: using a lambda for lazy rotation logic
        file_handler = RotatingFileHandler(
            log_file, 
            maxBytes=1024 * 1024 * 5, 
            backupCount=3
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
    return logger

class LoggerMeta(type):
    def __call__(cls, *args, **kwargs):
        instance = super().__call__(*args, **kwargs)
        instance.log = setup_logger(cls.__name__)
        return instance

# Usage pattern: class MyService(metaclass=LoggerMeta)
# This injects a logger into any class instance automatically