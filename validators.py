import re
from typing import Any
def validate_email(email: str) -> bool:
    if not isinstance(email, str) or not email:
        return False
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email) is not None
def validate_phone_number(phone: str) -> bool:
    if not isinstance(phone, str):
        return False
    digits = ''.join(filter(str.isdigit, phone))
    length = len(digits)
    return length == 10 or (length == 11 and digits[0] == '1')
def validate_url(url: str) -> bool:
    if not isinstance(url, str) or not url:
        return False
    pattern = r"^https?://[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(/.*)?$"
    return bool(re.match(pattern, url))
def validate_ipv4(ip: str) -> bool:
    if not isinstance(ip, str):
        return False
    parts = ip.split(".")
    if len(parts) != 4:
        return False
    try:
        return all(0 <= int(p) <= 255 for p in parts)
    except ValueError:
        return False
def validate_positive_number(value: Any) -> bool:
    try:
        return float(value) > 0
    except (ValueError, TypeError):
        return False
def validate_non_empty(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, (str, list, dict, set, tuple)):
        return bool(value)
    return True
def validate_credit_card(card: str) -> bool:
    if not isinstance(card, str):
        return False
    digits = [int(d) for d in card if d.isdigit()]
    if not (13 <= len(digits) <= 19):
        return False
    total = 0
    for i, digit in enumerate(reversed(digits)):
        if i % 2 == 1:
            digit *= 2
            if digit > 9:
                digit -= 9
        total += digit
    return total % 10 == 0
def validate_hex_color(color: str) -> bool:
    if not isinstance(color, str) or not color.startswith("#"):
        return False
    hex_part = color[1:]
    if len(hex_part) not in (3, 6):
        return False
    try:
        int(hex_part, 16)
        return True
    except ValueError:
        return False
def validate_password_strength(password: str) -> bool:
    if not isinstance(password, str) or len(password) < 8:
        return False
    has_upper = sum(1 for c in password if c.isupper()) > 0
    has_lower = sum(1 for c in password if c.islower()) > 0
    has_digit = sum(1 for c in password if c.isdigit()) > 0
    has_special = sum(1 for c in password if not c.isalnum()) > 0
    return sum([has_upper, has_lower, has_digit, has_special]) >= 3