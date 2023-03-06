import os
import time
from typing import Optional
from uuid import UUID


def generate_pseudo_random_number(bits: int):
    bytes = (bits + 7) // 8
    random_int = int.from_bytes(os.urandom(bytes), byteorder="big")

    mask = (2**bits) - 1
    while random_int > mask:
        random_int = int.from_bytes(os.urandom(bytes), byteorder="big")

    return random_int


class Sequencer:
    def __init__(
        self,
        bits: int = 26,
    ) -> None:
        # 26 bits
        self.last_timestamp: Optional[int] = None
        self.counter = generate_pseudo_random_number(26)

    def next_sequence(self, timestamp: int) -> int:
        if self.last_timestamp is not None and timestamp <= self.last_timestamp:  # type: ignore
            new_counter_raw = self.counter + 1
        else:
            new_counter_raw = generate_pseudo_random_number(26)
        self.counter = new_counter_raw & 0x03FF_FFFF
        self.last_timestamp = timestamp
        return self.counter


class UUID7Generator:
    def __init__(
        self,
    ) -> None:
        self._sequenecer = Sequencer(26)
        self._last_uuid: Optional[UUID] = None

    def generate(self, unix_ts_ms: Optional[int] = None) -> UUID:
        # 48 bits
        unix_ts_ms = unix_ts_ms or (time.time_ns() // 10**6) & 0xFFFF_FFFF_FFFF

        # 26 bits
        seq = self._sequenecer.next_sequence(unix_ts_ms)

        # 48 bits
        node = generate_pseudo_random_number(48)

        # 4 bits
        ver = 7

        # 12 bits
        rand_a = (seq >> 14) & 0x0FFF

        # 62 bits
        rand_b = ((seq & 0x3FFF) << 48) | node

        # 2 bits
        var = 0b10

        uuid_int = (unix_ts_ms << 80) | (ver << 76) | (rand_a << 64) | (var << 62) | rand_b
        uuid = UUID(int=uuid_int)

        if self._last_uuid is not None and uuid <= self._last_uuid:
            return self.generate(unix_ts_ms + 1)

        self._last_uuid = uuid
        return uuid
