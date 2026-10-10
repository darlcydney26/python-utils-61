# python-utils-61

A comprehensive collection of production-ready Python utility functions designed to streamline daily development tasks. This library bridges common gaps in the standard library by providing robust helpers for data processing, file I/O, and string manipulation.

## Features

*   **Robust File Operations:** Simplifies directory synchronization and recursive file pattern matching with intuitive one-liners.
*   **Data Validation Helpers:** Includes high-performance decorators to enforce schema constraints on dictionaries and JSON payloads.
*   **Concurrency Utilities:** Provides thread-safe decorators and easy-to-implement rate limiting for asynchronous API interactions.
*   **String Normalization:** Advanced tools for slugification, fuzzy matching, and multi-encoding text sanitization.

## Installation

Install the package via pip:

```bash
pip install python-utils-61
```

Or add it to your `requirements.txt`:

```text
python-utils-61>=1.0.0
```

## Basic Usage

Import the desired utilities directly to simplify your boilerplate code:

```python
from pyutils61.file_tools import secure_write
from pyutils61.validation import validate_schema

# Securely write JSON data to a file
data = {"status": "success", "id": 101}
secure_write("config.json", data)

# Enforce a schema on incoming data
schema = {"id": int, "status": str}
if validate_schema(data, schema):
    print("Data structure verified.")
```

## License

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Distributed under the MIT License. See `LICENSE` for more information.

---

*Developed by Developer | Maintained with ❤️ for the Python community.*