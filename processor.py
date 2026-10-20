import sys

def validate_stream(data):
    if not isinstance(data, dict) or 'id' not in data:
        raise ValueError('malformed input packet detected')
    return True

def process_payload(payload):
    return f'processed:{payload.get("id")}'

def run_processor(stream):
    for item in stream:
        try:
            if validate_stream(item):
                result = process_payload(item)
                sys.stdout.write(f'{result}\n')
        except (ValueError, TypeError) as e:
            sys.stderr.write(f'skip: {e}\n')
            continue

if __name__ == '__main__':
    mock_data = [{'id': 1}, 'bad_data', {'id': 2}]
    run_processor(mock_data)