# python-utils-61

A comprehensive collection of production-ready Python utility functions designed to streamline daily development tasks. This library focuses on performance, type safety, and reducing boilerplate code across your data processing and system automation scripts.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Features

*   **Robust File Handling:** Simplify common IO operations with context-aware helpers for safe file reading, directory synchronization, and automated cleanup.
*   **Data Validation Engine:** High-performance decorators for schema validation and type-checking, ensuring data integrity before processing.
*   **Enhanced Logging Wrapper:** An easy-to-configure logging interface that supports rotating file handlers and structured JSON output for seamless integration with observability stacks.
*   **Concurrency Helpers:** Simplified abstractions for multi-threading and asynchronous task queues, minimizing race conditions in resource-heavy environments.

## Installation

Install the package directly via pip:

```bash
pip install python-utils-61
```

For development installations including test dependencies:

```bash
git clone https://github.com/Developer/python-utils-61.git
cd python-utils-61
pip install -e .
```

## Basic Usage

Quickly incorporate robust logging and data validation into your project:

```python
from python_utils_61.logger import setup_logger
from python_utils_61.validation import validate_schema

# Initialize structured logging
logger = setup_logger("my_app", level="INFO")

# Define a simple validation schema
schema = {"id": int, "name": str}
data = {"id": 1, "name": "Task-01"}

if validate_schema(data, schema):
    logger.info("Data validated successfully.")
else:
    logger.error("Validation failed for input.")
```

## Contributing

Contributions are welcome! Please ensure all new utility modules include comprehensive type hinting and corresponding test cases in the `tests/` directory.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.