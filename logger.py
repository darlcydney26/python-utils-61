import logging
from logging.handlers import RotatingFileHandler
import os

def get_rotating_logger(name, log_file='app.log', max_bytes=1048576, backup_count=3):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    if not logger.handlers:
        handler = RotatingFileHandler(
            log_file, 
            maxBytes=max_bytes, 
            backupCount=backup_count
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    
    return logger

if __name__ == '__main__':
    # usage example: 
    # logger = get_rotating_logger('dev_logger')
    # logger.info('System initialization complete')