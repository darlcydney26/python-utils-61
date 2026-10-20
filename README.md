# python-utils-61

A comprehensive collection of performance-oriented Python utility functions designed to streamline daily development tasks. This library focuses on simplifying data manipulation, file system operations, and execution timing for efficient scripting.

## Features

*   **Robust File Operations**: Simplified wrappers for recursive directory traversal and asynchronous logging.
*   **Performance Profiling**: Decorators for measuring function execution time and memory footprint with minimal overhead.
*   **Data Sanitization**: Built-in utilities for cleaning deeply nested dictionaries and parsing inconsistent JSON formats.
*   **Time Utilities**: Precision helpers for timezone-aware date formatting and high-resolution sleep intervals.

## Installation

Install the package via pip:

```bash
pip install python-utils-61
```

Or clone the repository for development:

```bash
git clone https://github.com/Developer/python-utils-61.git
cd python-utils-61
pip install -r requirements.txt
```

## Basic Usage

Import the utility module to access the core functions. Here is an example of using the timer decorator:

```python
from utils.performance import timer

@timer
def process_data(data):
    # Simulate a heavy operation
    return [x * 2 for x in data]

result = process_data(range(1000000))
# Output: Function 'process_data' took 0.045 seconds
```

## Contributing

Contributions are welcome. Please open an issue to discuss proposed changes or submit a pull request for bug fixes. Ensure all new functions include unit tests located in the `/tests` directory.

## License

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Distributed under the MIT License. See `LICENSE` for more information.