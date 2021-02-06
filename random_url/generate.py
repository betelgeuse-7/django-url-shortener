import string
import random


def generate_random_url(times):
    chars = string.ascii_letters

    output = ''

    for i in range(times):
        output += random.choice(chars)

    return output
