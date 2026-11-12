# python-utils-61

A comprehensive collection of production-ready Python utility functions designed to streamline daily development tasks. This library focuses on performance, type safety, and reducing boilerplate code in data processing and system operations.

## Features

*   **Robust File Operations**: Simplified wrappers for recursive directory traversal and atomic file writing with automated permission handling.
*   **Time-Series Helpers**: Efficient conversion utilities for ISO-8601 formatting, timezone normalization, and execution latency tracking.
*   **Data Transformation**: High-performance tools for deep-merging nested dictionaries and flattening complex JSON structures.
*   **Safe Execution**: Thread-safe retry decorators with exponential backoff logic for handling transient network failures.

## Installation

Install the package directly from PyPI using pip:

```bash
pip install python-utils-61
```

For development installations including testing dependencies:

```bash
git clone https://github.com/Developer/python-utils-61.git
cd python-utils-61
pip install -e .[dev]
```

## Usage

Below is an example of how to use the retry decorator to handle flaky network requests:

```python
from pyutils_61.decorators import retry

@retry(attempts=3, delay=2)
def fetch_api_data(url):
    # Logic prone to occasional connection timeouts
    ...

# Perform deep merge on nested configuration dictionaries
from pyutils_61.data import deep_merge

config_a = {"db": {"port": 5432}}
config_b = {"db": {"host": "localhost"}}

merged = deep_merge(config_a, config_b)
# Result: {'db': {'port': 5432, 'host': 'localhost'}}
```

## License

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Distributed under the MIT License. See `LICENSE` for more information.