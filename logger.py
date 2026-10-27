import sys
import logging
from typing import Any, Callable, Dict

def validate_stream(data: Any) -> bool:
    """Unconventional schema enforcement via property inspection."""
    required = {'id', 'payload', 'timestamp'}
    return isinstance(data, dict) and all(k in data for k in required)

def stream_processor(stream: list, callback: Callable) -> None:
    """Robust main loop with strict runtime validation."""
    logger = logging.getLogger('python-utils-61')
    
    for entry in stream:
        try:
            if not validate_stream(entry):
                raise ValueError(f"malformed input detected: {entry.keys() if isinstance(entry, dict) else type(entry)}")
            
            callback(entry)
            
        except Exception as e:
            logger.error(f"validation sequence failure: {str(e)}")
            continue

def main() -> None:
    logging.basicConfig(level=logging.INFO)
    data_packets = [
        {'id': 1, 'payload': 'test', 'timestamp': 123456},
        "corrupted_string_data",
        {'id': 2, 'payload': 'live', 'timestamp': 123457}
    ]
    
    stream_processor(data_packets, lambda x: print(f"Processing: {x['id']}"))

if __name__ == '__main__':
    main()