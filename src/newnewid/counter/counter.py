from typing import Optional

from newnewid.random.pseudo_random_generator import PseudoRandomGenerator


class Counter:
    """Timebased counter.

    This class manages a counter.

    The counter is incremented when the same timestamp is given and reset when the timestamp is changed.
    """

    def __init__(
        self,
        counter_bits_length: int,
        max_increment_bits_length: Optional[int],
        pseudo_random_generator: PseudoRandomGenerator,
        initial_timestamp: Optional[int],
        initial_counter: Optional[int],
    ) -> None:
        """Create counter.

        Args:
            counter_bits_length (int): Number of bits of the counter.
            max_increment_bits_length (Optional[int]): Maximum number of bits of the increment. Maximum value is 2^max_increment_bits_length - 1.
            pseudo_random_generator (PseudoRandomGenerator): Pseudo random generator.
            initial_last_timestamp (Optional[int]): Initial timestamp.
            initial_counter (Optional[int]): Initial counter value.
        """
        if counter_bits_length > 0:
            assert (
                max_increment_bits_length is not None
            ), "max_increment_bits_length must be specified"
            assert (
                counter_bits_length >= max_increment_bits_length
            ), f"counter_bits_length must be greater than or equal to max_increment_bits_length, not {counter_bits_length} < {max_increment_bits_length}"
            assert (
                max_increment_bits_length >= 1
            ), f"max_increment_bits_length must be greater than or equal to 1, not {max_increment_bits_length}"

        self.counter_bits_length = counter_bits_length
        self.mask: int = (1 << counter_bits_length) - 1
        self.max_increment_bits_length = max_increment_bits_length
        self._pseudo_random_generator = pseudo_random_generator

        self.last_timestamp = initial_timestamp
        if initial_counter is None:
            if counter_bits_length > 0:
                self.counter = None
            else:
                self.counter = 0
        else:
            self.counter = initial_counter

    def _get_counter_reset_value(self) -> int:
        return self._pseudo_random_generator.generate(self.counter_bits_length - 1, "counter-reset")

    def get_next(self, timestamp: int) -> int:
        """Ge next counter value.

        Args:
            timestamp (int): Current timestamp.

        Returns:
            int: counter value.
        """
        if self.counter_bits_length == 0:
            return 0

        if self.last_timestamp is not None and timestamp <= self.last_timestamp:
            if self.counter is None:
                self.counter = self._get_counter_reset_value()

            if self.max_increment_bits_length == 1:
                increment = 1
            else:
                assert self.max_increment_bits_length is not None
                increment = 0
                while increment <= 0:
                    increment = self._pseudo_random_generator.generate(
                        self.max_increment_bits_length, "counter-increment"
                    )
            new_counter_raw = self.counter + increment
        else:
            new_counter_raw = self._get_counter_reset_value()
        self.counter = new_counter_raw & self.mask
        self.last_timestamp = timestamp
        return self.counter
