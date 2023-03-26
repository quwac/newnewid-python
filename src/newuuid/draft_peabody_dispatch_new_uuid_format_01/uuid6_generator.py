from typing import Any, Dict, Optional
from uuid import UUID

from newuuid.clock.uuid_clock import UUIDClock
from newuuid.random.pseudo_random_generator import PseudoRandomGenerator
from newuuid.sequence.sequencer import Sequencer
from newuuid.uuidgenerator.uuid_generator import ClockBasedUUIDGenerator


class UUID6Generator(ClockBasedUUIDGenerator):
    def __init__(
        self,
        raise_exception_on_backward: bool = False,
        clock: Optional[UUIDClock] = None,
        last_uuid: Optional[UUID] = None,
        sequencer: Optional[Sequencer] = None,
        pseudo_random_generator: Optional[PseudoRandomGenerator] = None,
    ) -> None:
        super().__init__(raise_exception_on_backward, clock, last_uuid)
        self._sequencer = sequencer or Sequencer(14)
        self._pseudo_random_generator = pseudo_random_generator or PseudoRandomGenerator(48)

    def timestamp(self, clock: UUIDClock) -> int:
        return clock.gregorian_100_nano_seconds()

    @property
    def clock_bits(self) -> int:
        return 60

    @property
    def least_seconds(self) -> float:
        return 0.000_000_1

    def generate_impl(self, timestamp: int) -> UUID:
        # timestamp is 60 bits

        # upper 48 bits
        time_high_and_time_mid = (timestamp >> 12) & 0xFFFF_FFFF_FFFF

        # 4 bits
        ver = 6

        # lower 12 bits
        time_low = timestamp & 0x0FFF

        # 2 bits
        var = 0b10

        # 14 bits
        clock_seq = self._sequencer.next_sequence(timestamp)

        # 48 bits
        node = self._pseudo_random_generator.generate()

        return UUID(
            int=(time_high_and_time_mid << 80)
            | (ver << 76)
            | (time_low << 64)
            | (var << 62)
            | (clock_seq << 48)
            | node
        )

    @classmethod
    def parse(cls, uuid: UUID, **kwargs: Any) -> Dict[str, Any]:
        # 32 bits
        time_high = (uuid.int >> 96) & 0xFFFF_FFFF

        # 16 bits
        time_mid = (uuid.int >> 80) & 0xFFFF

        # 4 bits
        version = (uuid.int >> 76) & 0xF
        assert version == 6, f"version must be 6, but {version}"

        # 12 bits
        time_low = (uuid.int >> 64) & 0x0FFF

        # 2 bits
        variant = (uuid.int >> 62) & 0x3

        # 14 bits
        clock_seq = (uuid.int >> 48) & 0x3FFF

        # 48 bits
        node = uuid.int & 0xFFFF_FFFF_FFFF

        gregorian_100_nano_seconds = (time_high << 28) | (time_mid << 12) | time_low
        time, epoch_100_nano_fraction = UUIDClock.to_datetime_from_gregorian_100_nano_seconds(
            gregorian_100_nano_seconds
        )
        epoch_nano_fraction = epoch_100_nano_fraction * 100

        return {
            "time_high": time_high,
            "time_mid": time_mid,
            "ver": str(version),
            "time_low": time_low,
            "variant": variant,
            "clock_seq": clock_seq,
            "node": node,
            "gregorian_100_nano_seconds": gregorian_100_nano_seconds,
            "time": time.isoformat(),
            "epoch_nano_fraction": epoch_nano_fraction,
        }


_uuid6_generator = UUID6Generator()


def uuid6() -> UUID:
    return _uuid6_generator.generate()
