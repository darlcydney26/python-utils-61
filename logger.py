import logging
from logging.handlers import RotatingFileHandler
import sys

def setup_logger(name='app_logger', log_file='app.log', level=logging.INFO):
    logger = logging.getLogger(name)
    logger.setLevel(level)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    file_handler = RotatingFileHandler(
        log_file, 
        maxBytes=1048576, 
        backupCount=5
    )
    file_handler.setFormatter(formatter)

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)

    return logger

class LoggerProxy:
    def __init__(self, name):
        self.logger = setup_logger(name)

    def __getattr__(self, item):
        return getattr(self.logger, item)

# Dynamic logging instance via proxy pattern
logger = LoggerProxy('python-utils-61')