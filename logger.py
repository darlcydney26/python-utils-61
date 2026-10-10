import logging
from logging.handlers import RotatingFileHandler
import os

def get_logger(name='python-utils-61', log_file='app.log', level=logging.INFO):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    if not logger.handlers:
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
        # Creative rotating handler with capacity check
        handler = RotatingFileHandler(
            log_file, 
            maxBytes=1024 * 1024 * 5, 
            backupCount=3
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        # Console stream as secondary output
        console = logging.StreamHandler()
        console.setFormatter(formatter)
        logger.addHandler(console)
    
    return logger

# Instantiate singleton logger
logger = get_logger()