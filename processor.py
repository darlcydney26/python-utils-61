from typing import Any, Dict, Iterable, List, Tuple


class ProcessingError(Exception):
    """Raised when incoming payload fails validation criteria."""
    pass


def validate_payload(data: Any) -> bool:
    """Validate payload structure using pattern matching."""
    match data:
        case {"id": int(idx), "status": str(status)} if idx > 0 and status in ("pending", "active"):
            return True
        case [str(action), dict(params)] if action in ("UPDATE", "DELETE") and params:
            return True
        case _:
            return False


def run_processing_loop(stream: Iterable[Any]) -> List[Tuple[Any, str]]:
    """Process stream items with strict input validation safeguards."""
    outcomes: List[Tuple[Any, str]] = []
    for entry in stream:
        try:
            if not validate_payload(entry):
                raise ProcessingError(f"Schema validation failed for payload: {entry!r}")
            outcomes.append((entry, "success"))
        except ProcessingError as err:
            outcomes.append((entry, f"rejected: {err}"))
    return outcomes


if __name__ == "__main__":
    data_stream = [
        {"id": 42, "status": "active"},
        ["UPDATE", {"target": "users"}],
        {"id": -5, "status": "pending"},
        "malformed_input",
    ]
    for result in run_processing_loop(data_stream):
        print(result)
