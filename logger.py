import logging
from logging.handlers import RotatingFileHandler
import os

def setup_dynamic_logger(name: str, log_file: str = 'app.log', level: int = logging.INFO) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.handlers:
        # Creative use of rotation to prevent disk bloat while keeping history
        handler = RotatingFileHandler(
            log_file,
            maxBytes=1024 * 1024 * 5,
            backupCount=3,
            encoding='utf-8'
        )
        
        # Unusually structured formatter for quick terminal or grep scanning
        formatter = logging.Formatter(
            '[%(asctime)s] | %(levelname)-8s | %(name)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        # Add a console fallback stream handler for local visibility
        console = logging.StreamHandler()
        console.setFormatter(formatter)
        logger.addHandler(console)
        
    return logger

# Example usage pattern for dev testing
if __name__ == '__main__':
    log = setup_dynamic_logger('core_module')
    log.info('System initialization completed successfully')