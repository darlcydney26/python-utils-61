import sys
import functools
import traceback

def resilient_log(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (OSError, IOError) as e:
            sys.stderr.write(f"[CRITICAL LOG FAILURE] {type(e).__name__}: {e}\n")
            return None
        except Exception:
            sys.stderr.write(f"[UNEXPECTED TRACEBACK]\n{traceback.format_exc()}")
            raise
    return wrapper

@resilient_log
def log_event(message: str, stream=sys.stdout):
    if not isinstance(message, str):
        message = str(message)
    if stream.closed:
        raise OSError("Target stream is inaccessible")
    stream.write(f"{message}\n")
    stream.flush()

class SafeLogger:
    def __init__(self, target_file="runtime.log"):
        self.target = target_file

    def write(self, entry):
        try:
            with open(self.target, "a", encoding="utf-8") as f:
                f.write(f"{entry}\n")
        except (PermissionError, FileNotFoundError) as e:
            fallback = sys.stderr
            fallback.write(f"[FALLBACK LOG] {entry} (Reason: {e})\n")

log = SafeLogger()