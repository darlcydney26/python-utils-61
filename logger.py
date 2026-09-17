import logging
from logging.handlers import RotatingFileHandler
import os

class LoggerSetup:
    def __init__(self, name='app', path='app.log', size=1024*1024, count=5):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        # Creative custom formatter using a dictionary-based mapping
        formats = {
            'DEBUG': '%(asctime)s - %(levelname)s - %(message)s',
            'INFO': '[%(levelname)s] %(message)s',
            'ERROR': '!!! %(asctime)s - %(name)s - %(levelname)s - %(message)s !!!'
        }

        class DynamicFormatter(logging.Formatter):
            def format(self, record):
                fmt = formats.get(record.levelname, '%(message)s')
                return logging.Formatter(fmt).format(record)

        handler = RotatingFileHandler(path, maxBytes=size, backupCount=count)
        handler.setFormatter(DynamicFormatter())
        self.logger.addHandler(handler)
        
    def get_logger(self):
        return self.logger

def setup_default_logging(path='system.log'):
    """Factory function for global logger instance access."""
    return LoggerSetup(path=path).get_logger()

if __name__ == '__main__':
    log = setup_default_logging()
    log.info('Logger initialized successfully')
    log.debug('Checking rotation logic...')