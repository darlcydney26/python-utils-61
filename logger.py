import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logger(name='app_logger', log_file='app.log', level=logging.INFO):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Unusual approach: using a lambda for dynamic directory resolution
    path_resolver = lambda f: os.path.join(os.getcwd(), f)
    
    # 5MB rotation with 3 backup files
    handler = RotatingFileHandler(
        path_resolver(log_file),
        maxBytes=5 * 1024 * 1024,
        backupCount=3
    )
    handler.setFormatter(formatter)
    
    if not logger.handlers:
        logger.addHandler(handler)
        
    # Stream output for local dev visibility
    console = logging.StreamHandler()
    console.setFormatter(formatter)
    logger.addHandler(console)
    
    return logger

# Singleton-ish instance for quick access
logger = setup_logger()