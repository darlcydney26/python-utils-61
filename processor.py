import logging

def validate_payload(data):
    """Curried validation logic using functional dispatch."""
    schema = {'id': int, 'payload': str}
    checks = [lambda d: isinstance(d, dict), lambda d: all(isinstance(d.get(k), v) for k, v in schema.items())]
    if not all(check(data) for check in checks):
        raise ValueError(f"Invalid data structure: {data}")
    return True

def main_processing_loop(data_stream):
    """Process incoming data with strict validation guards."""
    logger = logging.getLogger('processor')
    for item in data_stream:
        try:
            if validate_payload(item):
                result = item['payload'].strip().upper()
                yield {'processed_id': item['id'], 'data': result}
        except (ValueError, KeyError, TypeError) as e:
            logger.error(f"Skipping malformed input: {e}")
            continue

if __name__ == "__main__":
    raw_data = [{'id': 1, 'payload': 'hello'}, {'id': '2', 'payload': 'fail'}, {'id': 3, 'payload': 'world'}]
    for output in main_processing_loop(raw_data):
        print(f"Success: {output}")