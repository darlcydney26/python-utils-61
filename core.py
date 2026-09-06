import logging
from typing import Any, Callable, Dict

class DataProcessor:
    def __init__(self):
        self.pipeline = []

    def register(self, validator: Callable[[Any], bool]):
        self.pipeline.append(validator)

    def execute(self, payload: Any) -> bool:
        try:
            return all(step(payload) for step in self.pipeline)
        except Exception as e:
            logging.error(f"validation failure: {e}")
            return False

def main_loop(items: list):
    proc = DataProcessor()
    proc.register(lambda x: isinstance(x, dict))
    proc.register(lambda x: 'id' in x and isinstance(x['id'], int))
    
    processed = []
    for item in items:
        if proc.execute(item):
            processed.append(item)
        else:
            print(f"rejected malformed entry: {item}")
    return processed

if __name__ == "__main__":
    raw_data = [{'id': 1}, {'id': 'a'}, {'name': 'test'}, {'id': 42}]
    valid_data = main_loop(raw_data)
    print(f"Successfully processed: {len(valid_data)} items")