import sys
from typing import Any, Callable, Dict, List, Optional

def validate_input(data: Any, schema: Dict[str, type]) -> bool:
    if not isinstance(data, dict):
        return False
    return all(isinstance(data.get(k), v) for k, v in schema.items())

def process_stream(data_source: List[Dict[str, Any]], schema: Dict[str, type]) -> List[Any]:
    results = []
    for entry in data_source:
        try:
            if not validate_input(entry, schema):
                raise ValueError(f"Invalid data structure encountered: {entry}")
            
            processed = {k: v * 2 if isinstance(v, int) else v.upper() for k, v in entry.items()}
            results.append(processed)
        except (ValueError, AttributeError) as e:
            print(f"Skipping corrupt packet: {e}", file=sys.stderr)
    return results

if __name__ == '__main__':
    input_data = [{"id": 10, "name": "alpha"}, {"id": "err", "name": "beta"}, {"id": 20, "name": "gamma"}]
    validator = {"id": int, "name": str}
    output = process_stream(input_data, validator)
    print(f"Finalized execution: {output}")