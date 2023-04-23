from typing import Optional

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
        self.max_value = (1 << mask_bits) - 1
        self._pseudo_random_generator = pseudo_random_generator
        self._last_binary: Optional[int] = None

    def generate(self, monotonic: bool = False) -> int:
        """Generate binary.

        Args:
            monotonic (bool): Whether the binary should be monotonic.

        Returns:
            int: Binary.
        """
        if self.mask_bits == 0:
            return 0

        if monotonic and self._last_binary is not None:
            # Return max_value since monotonicity cannot be guaranteed.
            if self._last_binary == self.max_value:
                return self.max_value
            else:
                binary = self._last_binary
                while binary <= self._last_binary:
                    binary = self._pseudo_random_generator.generate(self.mask_bits, "random-binary")
        else:
            binary = self._pseudo_random_generator.generate(self.mask_bits, "random-binary")

        self._last_binary = binary

        return binary
