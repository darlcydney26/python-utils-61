import logging
from logging.handlers import RotatingFileHandler
import os

class LoggerConfig:
    def __init__(self, name='app_logger', log_file='app.log', max_bytes=1048576, backup_count=3):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        self.formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self._setup_rotation(log_file, max_bytes, backup_count)

    def _setup_rotation(self, log_file, max_bytes, backup_count):
        handler = RotatingFileHandler(
            log_file, 
            maxBytes=max_bytes, 
            backupCount=backup_count
        )
        handler.setFormatter(self.formatter)
        self.logger.addHandler(handler)
        
        console = logging.StreamHandler()
        console.setFormatter(self.formatter)
        self.logger.addHandler(console)

def get_logger(name='python-utils-61'):
    config = LoggerConfig(name=name)
    return config.logger