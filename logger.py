import logging
from logging.handlers import RotatingFileHandler
import os

def get_logger(name='app_logger', log_file='app.log', max_bytes=1048576, backup_count=3):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    if not logger.handlers:
        formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
        
        file_handler = RotatingFileHandler(
            log_file, 
            maxBytes=max_bytes, 
            backupCount=backup_count
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
    return logger

class LoggerProxy:
    def __init__(self, name):
        self.logger = get_logger(name)
    
    def __getattr__(self, name):
        return getattr(self.logger, name)

# usage: log = LoggerProxy('main_module')
# log.info('operation started')