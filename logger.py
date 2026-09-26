import logging
from logging.handlers import RotatingFileHandler
import os

def get_logger(name, log_path='app.log', max_size=1048576, backups=3):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    if not logger.handlers:
        formatter = logging.Formatter(
            '%(asctime)s | %(name)s | %(levelname)s | %(message)s'
        )
        
        handler = RotatingFileHandler(
            log_path, 
            maxBytes=max_size, 
            backupCount=backups
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        console = logging.StreamHandler()
        console.setFormatter(formatter)
        logger.addHandler(console)
        
    return logger

class LogContext:
    def __init__(self, logger):
        self.logger = logger
    def __enter__(self):
        self.logger.info('operation start')
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.logger.error(f'operation failed: {exc_val}')
        else:
            self.logger.info('operation complete')

if __name__ == '__main__':
    log = get_logger('core')
    with LogContext(log):
        log.debug('testing rotation logic')