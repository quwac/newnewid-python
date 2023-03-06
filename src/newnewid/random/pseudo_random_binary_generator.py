from newnewid.random.pseudo_random_generator import PseudoRandomGenerator


class PseudoRandomBinaryGenerator:
    """Pseudo random binary generator."""

    def __init__(
        self,
        mask_bits: int,
        pseudo_random_generator: PseudoRandomGenerator,
    ) -> None:
        """Create pseudo random binary generator.

        Args:
            mask_bits (int): Number of bits of the mask.
            pseudo_random_generator (PseudoRandomGenerator): Pseudo random generator.
        """
        assert 0 <= mask_bits, f"mask_bits must be greater than or equal to 0, not {mask_bits}"
        self.mask_bits = mask_bits
        self._pseudo_random_generator = pseudo_random_generator

    def generate(self) -> int:
        """Generate binary.

        Returns:
            int: Binary.
        """
        if self.mask_bits == 0:
            return 0

        return self._pseudo_random_generator.generate(self.mask_bits, "random-binary")
