import random


def generate_random_digit(length: int = 6) -> int:
    return random.randint(
        10**(length - 1),
        10**length - 1
    )
