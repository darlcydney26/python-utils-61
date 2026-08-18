# python-utils-61

A collection of versatile and reusable utility functions for Python projects. Designed to simplify common programming tasks, `python-utils-61` helps increase developer productivity and code maintainability.

## Features

- **String Manipulation Tools**: Includes functions for advanced string formatting, parsing, and validation.
- **File Handling Functions**: Simplifies file reading, writing, and management, with support for various file formats including CSV and JSON.
- **Data Validation Utilities**: Provides easy-to-use checks for validating user input and ensuring data integrity.
- **Date and Time Helpers**: Offers various functions for parsing, formatting, and manipulating dates and times.

## Installation

To install `python-utils-61`, you can use pip. Open your terminal and run:

```bash
pip install python-utils-61
```

For development purposes, clone the repository to your local machine:

```bash
git clone https://github.com/yourusername/python-utils-61.git
cd python-utils-61
```

Then install the dependencies:

```bash
pip install -r requirements.txt
```

## Basic Usage

Here's a quick example showcasing some of the utility functions:

```python
from utils import StringUtils, FileUtils, Validator

# String manipulation
formatted_string = StringUtils.format_string("Hello, {}!", "World")
print(formatted_string)  # Output: Hello, World!

# File handling
FileUtils.write_json('data.json', {'name': 'Alice', 'age': 30})

# Data validation
if Validator.is_email_valid('test@example.com'):
    print("Email is valid")
else:
    print("Email is invalid")
```

For more detailed documentation, please refer to the [Wiki](https://github.com/yourusername/python-utils-61/wiki) section.

![License](https://img.shields.io/badge/license-MIT-brightgreen)

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.