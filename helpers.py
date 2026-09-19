import functools

def validate_stream(func):
    @functools.wraps(func)
    def wrapper(data, *args, **kwargs):
        if not isinstance(data, (dict, list)):
            raise ValueError(f"Invalid stream input type: {type(data).__name__}")
        if not data:
            return None
        return func(data, *args, **kwargs)
    return wrapper

@validate_stream
def process_data_node(data):
    # Core business logic for processing input payloads
    output = [item.upper() if isinstance(item, str) else item for item in data] if isinstance(data, list) else {k: v for k, v in data.items()}
    return output

def execution_loop(data_sources):
    results = []
    for source in data_sources:
        try:
            processed = process_data_node(source)
            if processed is not None:
                results.append(processed)
        except (ValueError, TypeError) as e:
            print(f"Skipping malformed data packet: {e}")
            continue
    return results