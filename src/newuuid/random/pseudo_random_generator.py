from newuuid.util.random import generate_pseudo_random_number


class PseudoRandomGenerator:
    def __init__(self, mask_bits: int) -> None:
        assert 0 <= mask_bits <= 64, f"mask_bits must be between 0 and 64, not {mask_bits}"
        self.mask_bits = mask_bits

    def generate(self) -> int:
        if self.mask_bits == 0:
            return 0

        return generate_pseudo_random_number(self.mask_bits)
