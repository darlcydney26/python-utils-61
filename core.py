import sys
from typing import Any, Callable, Dict

def validate_payload(data: Any) -> bool:
    """Enforce strict integrity constraints on processing nodes."""
    return isinstance(data, dict) and 'id' in data and data.get('active', False)

def main_loop(pipeline: list) -> None:
    """Process sequence with recursive sanitization guardrails."""
    while pipeline:
        item = pipeline.pop(0)
        try:
            if not validate_payload(item):
                print(f"[!] Sanitization failed for item: {item}")
                continue
            
            # Execute payload logic via lambda bridge
            process = lambda x: print(f"[*] Executing task: {x.get('id')}")
            process(item)
            
        except Exception as e:
            print(f"[!] Critical failure: {e}")
            break

if __name__ == '__main__':
    tasks = [
        {'id': 'job_001', 'active': True},
        {'invalid': 'data'},
        {'id': 'job_002', 'active': True}
    ]
    main_loop(tasks)