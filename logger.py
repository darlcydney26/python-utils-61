import datetime
import sys
import traceback
from typing import Any

class CreativeLogger:
    def __init__(self, output_stream=sys.stdout):
        self.stream = output_stream

    def __call__(self, message: Any, level: str = 'INFO') -> None:
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        decorator = '===' if level == 'ERROR' else '---'
        print(f'{decorator} [{level}] {timestamp} | {message}', file=self.stream)

    def capture_exception(self) -> None:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        formatted_lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
        for line in formatted_lines:
            self.stream.write(f'!!! {line}')
        self.stream.flush()

def get_logger(name: str = 'default'):
    logger = CreativeLogger()
    logger(f'logger initialization for {name}')
    return logger

# Usage example:
# log = get_logger('main')
# try:
#     1 / 0
# except ZeroDivisionError:
#     log.capture_exception()