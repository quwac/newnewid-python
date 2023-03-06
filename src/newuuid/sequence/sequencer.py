from typing import Optional

from newuuid.util.random import generate_pseudo_random_number


class Sequencer:
    def __init__(
        self,
        mask_bits: int,
        initial_last_timestamp: Optional[int] = None,
        initial_counter: Optional[int] = None,
    ) -> None:
        assert 0 <= mask_bits <= 64, f"mask_bits must be between 0 and 64, not {mask_bits}"
        self.mask_bits = mask_bits
        self.mask: int = (1 << mask_bits) - 1
        self.last_timestamp: Optional[int] = initial_last_timestamp
        if initial_counter is None:
            self.counter = self._new_counter()
        else:
            self.counter = initial_counter

    def _new_counter(self) -> int:
        return generate_pseudo_random_number(self.mask_bits - 1)

    def next_sequence(self, timestamp: int) -> int:
        if self.mask_bits == 0:
            return 0

        if self.last_timestamp is not None and timestamp <= self.last_timestamp:
            new_counter_raw = self.counter + 1
        else:
            new_counter_raw = self._new_counter()
        self.counter = new_counter_raw & self.mask
        self.last_timestamp = timestamp
        return self.counter
