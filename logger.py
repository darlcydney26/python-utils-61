import sys
import time
from datetime import datetime

class SmartLogger:
    def __init__(self, prefix='[APP]'):
        self.prefix = prefix
        self.stream = sys.stdout

    def __call__(self, message: str, level: str = 'INFO'):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        formatted = f"{timestamp} {self.prefix} {level:^7} | {message}"
        self.stream.write(formatted + '\n')
        self.stream.flush()

    def verbose(self, data: dict):
        for key, value in data.items():
            self(f"{key} -> {value}", 'DEBUG')

    @staticmethod
    def quick_profile(func):
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            result = func(*args, **kwargs)
            duration = time.perf_counter() - start
            print(f"[PERF] {func.__name__} took {duration:.4f}s")
            return result
        return wrapper

log = SmartLogger()