import sys
import traceback
import logging
from typing import Any, Optional

class RobustLogger:
    def __init__(self, name: str = 'py-utils-61'):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)

    def execute_with_fallback(self, func: callable, fallback: Any, *args: Any, **kwargs: Any) -> Any:
        try:
            return func(*args, **kwargs)
        except (KeyboardInterrupt, SystemExit) as e:
            raise e
        except Exception as err:
            self._log_catastrophic_failure(err)
            return fallback

    def _log_catastrophic_failure(self, err: Exception) -> None:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        formatted_tb = traceback.format_exception(exc_type, exc_value, exc_traceback)
        
        payload = {
            "error": str(err),
            "context": formatted_tb[-1].strip(),
            "trace": "".join(formatted_tb[:-1])
        }
        
        sys.stderr.write(f"[CRITICAL] {payload['error']} | {payload['context']}\n")
        self.logger.error(f"Deep failure trace: {payload['trace']}")

def safe_log(message: str, level: int = logging.INFO) -> None:
    try:
        if not isinstance(message, str):
            raise ValueError("Log input must be string")
        logging.log(level, message)
    except Exception:
        logging.critical("Recursive failure in logging pipeline")