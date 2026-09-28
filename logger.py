import sys
import functools
import traceback

def resilient_log(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (OSError, IOError) as e:
            sys.stderr.write(f"[CRITICAL LOG FAILURE]: {str(e)}\n")
            return None
        except Exception:
            sys.stderr.write(f"[UNEXPECTED ERROR]: {traceback.format_exc()}")
            return False
    return wrapper

class StreamLogger:
    def __init__(self, stream=sys.stdout):
        self.stream = stream

    @resilient_log
    def log(self, message: str) -> None:
        if not isinstance(message, str):
            raise ValueError("message must be string type")
        self.stream.write(f"{message}\n")
        self.stream.flush()

def safe_logger(message: str):
    logger = StreamLogger()
    result = logger.log(message)
    return result if result is not None else "failed"