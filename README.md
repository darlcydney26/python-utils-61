# python-utils-61

A lightweight collection of robust, production-ready Python utilities designed to streamline common development tasks. This library focuses on performance and type safety to help you write cleaner code with less boilerplate.

## Features

*   **Robust File Operations:** Simplified wrappers for directory traversal, recursive file deletion, and safe file writing.
*   **Performance Decorators:** Built-in tools for easy execution timing and method memoization to optimize expensive computations.
*   **Data Validation:** A set of lightweight helpers to validate environment variables and configuration dictionaries.
*   **Concurrent Execution:** Simplified threading and multiprocessing abstractions for rapid task parallelization.

## Installation

Install the package via pip:

```bash
pip install python-utils-61
```

For development installations, clone the repository and run:

```bash
git clone https://github.com/developer/python-utils-61.git
cd python-utils-61
pip install -e .
```

## Usage

Easily profile your functions using the `@time_execution` decorator to identify bottlenecks in your code:

```python
from pyutils.decorators import time_execution

@time_execution
def process_data(data):
    # Simulate a heavy operation
    return [x**2 for x in data]

result = process_data(range(1000000))
# Output: [INFO] Function 'process_data' took 0.045s to execute
```

## License

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Distributed under the MIT License. See `LICENSE` for more information.