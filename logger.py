import logging
from logging.handlers import RotatingFileHandler
import sys

def get_rotating_logger(name, log_file='app.log', max_bytes=1048576, backups=5):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    formatter = logging.Formatter(
        '%(asctime)s [%(levelname)s] %(name)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Console output for visibility
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Rotating file storage
    file_handler = RotatingFileHandler(
        log_file, 
        maxBytes=max_bytes, 
        backupCount=backups
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    return logger

# Dynamic instance for internal usage
if __name__ == '__main__':
    log = get_rotating_logger('python-utils-61')
    log.info('logger initialization sequence complete')