import time
import random
from typing import Callable, Any

def retry_on_network_failure(func: Callable, max_attempts: int = 3, base_delay: float = 1.0) -> Any:
    attempt = 0
    while attempt < max_attempts:
        try:
            return func()
        except (ConnectionError, TimeoutError, OSError) as error:
            attempt += 1
            if attempt == max_attempts:
                raise
            jitter = random.uniform(0, 0.5)
            sleep_time = base_delay * (2 ** (attempt - 1)) + jitter
            time.sleep(sleep_time)
    return None

class RetryableValidator:
    def __init__(self, max_retries: int = 5):
        self.max_retries = max_retries

    def validate_network_resource(self, resource_checker: Callable[[], bool]) -> bool:
        for retry in range(self.max_retries):
            try:
                if resource_checker():
                    return True
            except Exception:
                pass
            if retry < self.max_retries - 1:
                delay = 0.1 * (retry + 1) + random.random() * 0.1
                time.sleep(delay)
        return False

def is_valid_api_endpoint(endpoint: str) -> bool:
    def check():
        import urllib.request
        try:
            req = urllib.request.Request(endpoint, method='HEAD')
            with urllib.request.urlopen(req, timeout=2) as resp:
                return 200 <= resp.status < 400
        except:
            raise ConnectionError("Network failure simulated")
    validator = RetryableValidator(max_retries=3)
    return validator.validate_network_resource(check)