import logging
from typing import Any, Dict, Callable

def validate_payload(data: Any, schema: Dict[str, type]) -> bool:
    if not isinstance(data, dict): return False
    return all(k in data and isinstance(data[k], v) for k, v in schema.items())

def process_stream(data_source: list, schema: Dict[str, type], processor: Callable):
    logging.basicConfig(level=logging.INFO)
    for entry in data_source:
        try:
            if not validate_payload(entry, schema):
                raise ValueError(f"malformed entry detected: {entry}")
            processor(entry)
        except (ValueError, TypeError) as e:
            logging.error(f"processing skip: {e}")
            continue

if __name__ == '__main__':
    # Example usage: process integer-based data stream
    raw_data = [{'id': 1, 'val': 10}, {'id': 2, 'val': 'invalid'}]
    target_schema = {'id': int, 'val': int}
    
    def logic(item):
        print(f"processing {item['id']}")
        
    process_stream(raw_data, target_schema, logic)