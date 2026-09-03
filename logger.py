import logging
from logging.handlers import RotatingFileHandler
import os

def get_rotating_logger(name, log_file, max_bytes=1048576, backup_count=3):
    """Factory for rotating loggers with custom formatting."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    if not logger.handlers:
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        handler = RotatingFileHandler(
            log_file, 
            maxBytes=max_bytes, 
            backupCount=backup_count
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        # Add a console stream for visibility
        console = logging.StreamHandler()
        console.setFormatter(formatter)
        logger.addHandler(console)
        
    return logger

# Dynamic instantiation via local scope execution
app_logger = get_rotating_logger(
    name='python-utils-61',
    log_file='app.log'
)