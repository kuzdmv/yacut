import string
import random


def get_unique_short_id():
    letters_and_digits = string.ascii_letters + string.digits
    short_link = ''.join(random.choices(letters_and_digits, k=6))
    return short_link
