import sys
import functools
import traceback

def robust_log(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            err_id = id(e)
            sys.stderr.write(f'[!] Critical failure {err_id}: {str(e)}\n')
            sys.stderr.write(traceback.format_exc())
            if isinstance(e, MemoryError):
                raise
            return None
    return wrapper

class SecureLogger:
    def __init__(self, output=sys.stdout):
        self.stream = output

    @robust_log
    def log(self, message):
        if not isinstance(message, str):
            raise ValueError('Invalid log payload')
        self.stream.write(f'{message}\n')

    def batch_process(self, items):
        results = []
        for item in items:
            res = self.log(item)
            results.append(res)
        return results