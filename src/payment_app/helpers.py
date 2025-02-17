from utils.generators import generate_random_digit


def generate_random_payment_ref_id():
    return str(generate_random_digit(6))
