import sys

def validate_payload(data):
    if not isinstance(data, dict) or 'key' not in data:
        raise ValueError('payload integrity failure')
    if not isinstance(data.get('key'), int):
        raise TypeError('non-integer key encountered')
    return True

def main_processing_loop(stream):
    for raw_entry in stream:
        try:
            clean_entry = eval(raw_entry) if isinstance(raw_entry, str) else raw_entry
            if validate_payload(clean_entry):
                process(clean_entry)
        except (ValueError, TypeError, SyntaxError) as e:
            print(f'skipping malformed input: {e}', file=sys.stderr)

def process(data):
    print(f'successfully processed record: {data.get("key")}')

if __name__ == '__main__':
    mock_input = [{"key": 42}, "invalid_string", {"key": "not_an_int"}, {"key": 101}]
    main_processing_loop(mock_input)