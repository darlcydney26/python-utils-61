# python-utils-61

A comprehensive collection of lightweight, high-performance Python utility functions designed to streamline repetitive development tasks. This library focuses on clean code principles and zero external dependencies for maximum portability.

## Features

*   **Data Validation**: Robust type-checking and sanitization helpers for nested JSON structures.
*   **File System Wrappers**: Simplified recursive directory walking and batch file renaming utilities.
*   **Performance Decorators**: Built-in memoization and execution time logging to optimize expensive functions.
*   **String Formatting**: Advanced slugifiers and case-conversion tools for cleaner data processing.

## Installation

Install the package directly via pip:

```bash
pip install python-utils-61
```

Or add it to your `requirements.txt`:

```text
python-utils-61>=1.0.0
```

## Basic Usage

Import the modules directly to leverage the utility set:

```python
from pyutils61 import strings, decorators

# Use performance logging on a function
@decorators.time_execution
def process_data(data):
    return strings.to_slug(data)

result = process_data("Hello World!")
print(result) # Output: hello-world
```

## License

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Distributed under the MIT License. See `LICENSE` for more information.