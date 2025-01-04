import random
import string
from uuid import UUID


def generate_random_string(length: int, letters: bool = True, digits: bool = True, punctuation: bool = False, lowercase: bool = False, uppercase: bool = False):
    choices = ''
    if letters:
        choices += string.ascii_letters
    if digits:
        choices += string.digits
    if punctuation:
        choices += string.punctuation

    s = ''.join(random.choices(choices, k=length))

    if lowercase:
        return s.lower()
    elif uppercase:
        return s.upper()
    else:
        return s


def sanitize_json(data: dict):
    for key, value in data.items():
        if isinstance(value, UUID):
            data[key] = str(value)
        if isinstance(value, dict):
            data[key] = sanitize_json(value)

    return data
