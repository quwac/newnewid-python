import secrets


class PseudoRandomGenerator:
    """Pseudo random generator."""

    def generate(self, bits: int, use: str) -> int:
        """Generate pseudo random bits.

        CSPRNG is used for the generation.

        Args:
            bits (int): Number of bits to generate.
            use (str): Use of the generated bits. This is used for mocking in test classes.

        Returns:
            int: Pseudo random bits.
        """
        return secrets.randbits(bits)
