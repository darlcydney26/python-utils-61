import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
import sys

class CreativeLogger:
    def __init__(self, name='app_logger', log_file='app.log'):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        log_path = Path(log_file)
        log_path.touch(exist_ok=True)
        
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(filename)s:%(lineno)d | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        file_handler = RotatingFileHandler(
            log_path,
            maxBytes=1024 * 1024 * 5,
            backupCount=3,
            encoding='utf-8'
        )
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

    def get_logger(self):
        return self.logger

def setup_logging(name='python-utils-61'):
    return CreativeLogger(name=name).get_logger()