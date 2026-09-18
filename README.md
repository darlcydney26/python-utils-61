# python-utils-61

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

`python-utils-61` is a curated collection of high-performance, lightweight utility functions designed to streamline daily Python development. It eliminates boilerplate code by providing robust, production-ready tools for nested data manipulation, atomic file operations, and runtime execution profiling.

## Features

* **Deep Dictionary Merging:** Recursively combine nested dictionaries without mutating the original inputs.
* **Atomic File Writer:** Write data safely using temporary-file swapping to prevent file corruption during execution failures.
* **Execution Profiler:** Measure and log the execution time of code blocks down to microsecond precision using a clean context manager.

## Installation

Install the package directly from PyPI:

```bash
pip install python-utils-61
```

## Quick Start

Here is a quick look at how easily you can use the deep merging and profiling utilities in your application:

```python
from python_utils_61 import deep_merge, ExecutionTimer

# 1. Safely merge nested configuration dictionaries
default_config = {"app": {"host": "localhost", "ports": [8080], "debug": True}}
user_config = {"app": {"ports": [8080, 443], "debug": False}}

final_config = deep_merge(default_config, user_config)
print(final_config)
# Output: {'app': {'host': 'localhost', 'ports': [8080, 443], 'debug': False}}

# 2. Profile code execution blocks
with ExecutionTimer("Heavy Computation Pipeline"):
    result = sum(i * i for i in range(1_000_000))
# Console Output: [ExecutionTimer] "Heavy Computation Pipeline" completed in 0.0842s
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.