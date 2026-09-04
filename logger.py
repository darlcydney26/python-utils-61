import sys
import logging
from typing import Any, Dict

def validate_payload(data: Any) -> Dict[str, Any]:
    if not isinstance(data, dict):
        raise ValueError(f"Invalid data type: {type(data).__name__}")
    if "id" not in data or not isinstance(data["id"], int):
        raise ValueError("Missing or invalid integer ID")
    return data

class ProcessingLogger:
    def __init__(self):
        self.logger = logging.getLogger("python-utils-61")
        self.logger.setLevel(logging.INFO)
        handler = logging.StreamHandler(sys.stdout)
        self.logger.addHandler(handler)

    def execute_loop(self, queue: list):
        for item in queue:
            try:
                clean_item = validate_payload(item)
                self.logger.info(f"Processed record {clean_item['id']}")
            except (ValueError, TypeError) as e:
                self.logger.error(f"Skipping malformed input: {e}")
            except Exception as e:
                self.logger.critical(f"Unexpected system failure: {e}")

if __name__ == "__main__":
    p = ProcessingLogger()
    p.execute_loop([{"id": 1}, "corrupted", {"id": 2}])