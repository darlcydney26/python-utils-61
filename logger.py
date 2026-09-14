import logging
from logging.handlers import RotatingFileHandler
import sys

def setup_logger(name='app_logger', log_file='app.log', level=logging.INFO):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    file_handler = RotatingFileHandler(
        log_file, maxBytes=1048576, backupCount=5
    )
    file_handler.setFormatter(formatter)
    
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)
    
    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)
    
    return logger

class LogContextManager:
    def __init__(self, logger):
        self.logger = logger
    def __enter__(self):
        self.logger.info('Entering execution context')
        return self.logger
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.logger.error(f'Exiting with error: {exc_val}')
        else:
            self.logger.info('Exiting execution context successfully')