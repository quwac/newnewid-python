import os


def generate_pseudo_random_number(bits: int):
    if bits == 0:
        return 0

    bytes = (bits + 7) // 8
    random_int = int.from_bytes(os.urandom(bytes), byteorder="big")

    mask = (1 << bits) - 1
    while random_int > mask:
        random_int = int.from_bytes(os.urandom(bytes), byteorder="big")

    return random_int
