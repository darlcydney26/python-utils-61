import functools

def validate_inputs(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        for arg in args:
            if arg is None:
                raise ValueError('invalid input: null argument detected')
        return func(*args, **kwargs)
    return wrapper

@validate_inputs
def process_stream(data_packet):
    if not isinstance(data_packet, dict):
        return None
    return {k: v for k, v in data_packet.items() if v is not None}

def main_loop(data_list):
    processed_results = []
    for entry in data_list:
        try:
            result = process_stream(entry)
            if result:
                processed_results.append(result)
        except (ValueError, TypeError) as e:
            print(f'skipping malformed entry: {e}')
            continue
    return processed_results

if __name__ == '__main__':
    sample_data = [{'id': 1, 'val': 'a'}, None, {'id': 2, 'val': 'b'}]
    results = main_loop(sample_data)
    print(f'processed {len(results)} items successfully')