# python-utils-61

A comprehensive collection of production-ready Python utility functions designed to streamline daily development tasks. This library focuses on performance, readability, and minimizing boilerplate code for common operations.

## Features

*   **Robust File Handling:** Simplify directory traversal, file system monitoring, and cross-platform path manipulation with a high-level API.
*   **Time & Date Helpers:** Effortless timezone-aware conversions and natural language formatting for human-readable timestamps.
*   **Data Transformation:** Efficient batch processing tools for deep-merging dictionaries and flattening complex nested data structures.
*   **Execution Wrappers:** Lightweight decorators for retry logic, exponential backoff, and execution time profiling of blocking operations.

## Installation

Install the package via pip:

```bash
pip install python-utils-61
```

Or add it to your project using Poetry:

```bash
poetry add python-utils-61
```

## Usage

Easily incorporate modular utilities into your existing codebase. Here is an example of using the retry decorator to handle flaky network requests:

```python
from pyutils_61.decorators import retry

@retry(attempts=3, delay=2)
def fetch_data(url):
    # This will automatically retry on connection failures
    return requests.get(url).json()

# Merging complex dictionaries
from pyutils_61.data import deep_merge

config = deep_merge(base_cfg, user_cfg)
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request for any bug fixes or performance enhancements. For major changes, please open an issue first to discuss the proposed updates.

## License

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Distributed under the MIT License. See `LICENSE` for more information.