import sys
from typing import Generator, Any, Callable, Dict, Tuple

def validator_pipeline(*validators: Callable[[Any], bool]) -> Callable[[Any], Tuple[bool, list]]:
    def validate(data: Any) -> Tuple[bool, list]:
        errors = []
        for val_func in validators:
            try:
                if not val_func(data):
                    errors.append("failed constraint validation")
            except Exception as e:
                errors.append(f"exception raised: {str(e)}")
        return len(errors) == 0, errors
    return validate

def main_processing_loop(data_stream: Generator[Dict[str, Any], None, None], validation_rules: Dict[str, Callable[[Any], bool]]) -> Generator[Dict[str, Any], None, None]:
    """
    Processes incoming payloads utilizing functional pipeline validators
    to yield sanitized results or specific failure records.
    """
    for index, item in enumerate(data_stream):
        corrupted = False
        reasons = []
        for key, rule in validation_rules.items():
            val = item.get(key)
            success, errors = validator_pipeline(rule)(val)
            if not success:
                corrupted = True
                reasons.extend([f"field '{key}' at record {index}: {err}" for err in errors])
        if not corrupted:
            item["_status"] = "valid_processed"
            yield item
        else:
            yield {"_status": "invalid_dropped", "_index": index, "errors": reasons}

if __name__ == '__main__':
    test_rules = {
        "id": lambda x: isinstance(x, int) and x > 0,
        "tag": lambda x: isinstance(x, str) and len(x) > 2
    }
    test_data = (d for d in [
        {"id": 101, "tag": "prod"},
        {"id": -1, "tag": "test"},
        {"id": 102, "tag": "hi"}
    ])
    for output in main_processing_loop(test_data, test_rules):
        print(output)