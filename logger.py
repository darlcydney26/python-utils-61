import time
import threading
from collections import deque

class FastLogger:
    def __init__(self, capacity=1024):
        self._buffer = deque(maxlen=capacity)
        self._lock = threading.Lock()
        self._flush_event = threading.Event()
        self._thread = threading.Thread(target=self._worker, daemon=True)
        self._thread.start()

    def log(self, message):
        self._buffer.append(f"{time.time_ns()} | {message}")
        if len(self._buffer) >= self._buffer.maxlen // 2:
            self._flush_event.set()

    def _worker(self):
        while True:
            self._flush_event.wait()
            with self._lock:
                batch = list(self._buffer)
                self._buffer.clear()
            if batch:
                with open('runtime.log', 'a') as f:
                    f.write('\n'.join(batch) + '\n')
            self._flush_event.clear()
            time.sleep(0.1)

logger = FastLogger()