from datetime import datetime, timedelta
from typing import Any, Dict, Literal, Optional
from uuid import UUID

from newuuid.clock.uuid_clock import UUIDClock
from newuuid.random.pseudo_random_generator import PseudoRandomGenerator
from newuuid.sequence.sequencer import Sequencer
from newuuid.uuidgenerator.uuid_generator import ClockBasedUUIDGenerator

Precision = Literal["milli", "micro", "nano"]


class UUID7Generator(ClockBasedUUIDGenerator):
    """UUIDv7 generator class.

    UUIDv7 is a 128-bit UUID that is based on Epoch time and is sortable.

    There are three variations of UUIDv7 depending on the granularity of the epoch time.

    * Millisecond variation

        0                   1                   2                   3
        0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
       +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
       |                            unixts                             |
       +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
       |unixts |         msec          |  ver  |          seq          |
       +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
       |var|                         rand                              |
       +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
       |                             rand                              |
       +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

    * Microsecond variation

        0                   1                   2                   3
        0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
       +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
       |                            unixts                             |
       +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
       |unixts |         usec          |  ver  |         usec          |
       +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
       |var|             seq           |            rand               |
       +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
       |                             rand                              |
       +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

    * Nanosecond variation

        0                   1                   2                   3
        0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
       +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
       |                            unixts                             |
       +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
       |unixts |         nsec          |  ver  |         nsec          |
       +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
       |var|             nsec          |      seq      |     rand      |
       +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
       |                             rand                              |
       +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

    """

    def __init__(
        self,
        precision: Precision,
        raise_exception_on_backward: bool = False,
        clock: Optional[UUIDClock] = None,
        last_uuid: Optional[UUID] = None,
        sequencer: Optional[Sequencer] = None,
        pseudo_random_generator: Optional[PseudoRandomGenerator] = None,
    ) -> None:
        super().__init__(raise_exception_on_backward, clock, last_uuid)

        self.precision: Precision = precision

        if precision == "milli":
            self.seq_bits = 12
            self.random_bits = 52
        elif precision == "micro":
            self.seq_bits = 14
            self.random_bits = 48
        else:
            self.seq_bits = 8
            self.random_bits = 40

        self._sequencer = sequencer or Sequencer(self.seq_bits)
        self._pseudo_random_generator = pseudo_random_generator or PseudoRandomGenerator(
            self.random_bits
        )

    def timestamp(self, clock: UUIDClock) -> int:
        if self.precision == "milli":
            return clock.epoch_36_bits_seconds_with_12_bits_milli_seconds()
        elif self.precision == "micro":
            return clock.epoch_36_bits_seconds_with_24_bits_micro_seconds()
        elif self.precision == "nano":
            return clock.epoch_36_bits_seconds_with_38_bits_nano_seconds()
        else:
            raise ValueError(f"Invalid precision: {self.precision}")

    @property
    def clock_bits(self) -> int:
        if self.precision == "milli":
            return 48
        elif self.precision == "micro":
            return 60
        elif self.precision == "nano":
            return 74
        else:
            raise ValueError(f"Invalid precision: {self.precision}")

    @property
    def least_seconds(self) -> float:
        if self.precision == "milli":
            return 0.001
        elif self.precision == "micro":
            return 0.000_001
        elif self.precision == "nano":
            return 0.000_000_001
        else:
            raise ValueError(f"Invalid precision: {self.precision}")

    def generate_impl(
        self,
        timestamp: int,
    ) -> UUID:

        precision = self.precision

        var = 0b10
        ver = 0b0111

        seq = self._sequencer.next_sequence(timestamp)

        rand = self._pseudo_random_generator.generate()

        if precision == "milli":
            # 36 bits
            unixts = (timestamp >> 12) & 0x000F_FFFF_FFFF

            # 12 bits
            msec = timestamp & 0x0FFF

            uuid_int = (
                (unixts << 92) | (msec << 80) | (ver << 76) | (seq << 64) | (var << 62) | rand
            )
        elif precision == "micro":
            # 36 bits
            unixts = (timestamp >> 24) & 0x000F_FFFF_FFFF

            # 12 bits
            usec_a = (timestamp >> 12) & 0x0FFF

            # 12 bits
            usec_b = timestamp & 0x0FFF

            uuid_int = (
                (unixts << 92)
                | (usec_a << 80)
                | (ver << 76)
                | (usec_b << 64)
                | (var << 62)
                | (seq << 48)
                | rand
            )
        else:
            # 36 bits
            unixts = (timestamp >> 38) & 0x000F_FFFF_FFFF

            # 12 bits
            nsec_a = (timestamp >> 26) & 0x0FFF

            # 12 bits
            nsec_b = (timestamp >> 14) & 0x0FFF

            # 14 bits
            nsec_c = timestamp & 0x3FFF

            uuid_int = (
                (unixts << 92)
                | (nsec_a << 80)
                | (ver << 76)
                | (nsec_b << 64)
                | (var << 62)
                | (nsec_c << 48)
                | (seq << 40)
                | rand
            )

        return UUID(int=uuid_int)

    @classmethod
    def parse(cls, uuid: UUID, precision: Precision, **kwargs: Any) -> Dict[str, Any]:
        unixts = (uuid.int >> 92) & 0x000F_FFFF_FFFF
        if precision == "milli":
            msec = (uuid.int >> 80) & 0x0FFF
            version = (uuid.int >> 76) & 0x000F
            seq = (uuid.int >> 64) & 0x0FFF
            variant = (uuid.int >> 62) & 0x0003
            rand = uuid.int & 0x3FFF_FFFF_FFFF_FFFF

            time = datetime.fromtimestamp(unixts) + timedelta(milliseconds=msec)
            return {
                "unixts": unixts,
                "msec": msec,
                "ver": str(version),
                "seq": seq,
                "variant": variant,
                "rand": rand,
                "time": time,
            }
        elif precision == "micro":
            usec_a = (uuid.int >> 80) & 0x0FFF
            version = (uuid.int >> 76) & 0x000F
            usec_b = (uuid.int >> 64) & 0x0FFF
            variant = (uuid.int >> 62) & 0x0003
            seq = (uuid.int >> 48) & 0x3FFF
            rand = uuid.int & 0xFFFF_FFFF_FFFF

            usec = (usec_a << 12) | usec_b
            time = datetime.fromtimestamp(unixts) + timedelta(microseconds=usec)
            return {
                "unixts": unixts,
                "usec_a": usec_a,
                "ver": str(version),
                "usec_b": usec_b,
                "variant": variant,
                "rand": rand,
                "time": time,
            }
        else:
            nsec_a = (uuid.int >> 80) & 0x0FFF
            version = (uuid.int >> 76) & 0x000F
            nsec_b = (uuid.int >> 64) & 0x0FFF
            variant = (uuid.int >> 62) & 0x0003
            nsec_c = (uuid.int >> 48) & 0x3FFF
            seq = (uuid.int >> 40) & 0x00FF
            rand = uuid.int & 0x00FF_FFFF_FFFF

            nsec = (nsec_a << 26) | (nsec_b << 14) | nsec_c
            time = datetime.fromtimestamp(unixts) + timedelta(microseconds=nsec // 1000)
            return {
                "unixts": unixts,
                "nsec_a": nsec_a,
                "ver": str(version),
                "nsec_b": nsec_b,
                "variant": variant,
                "nsec_c": nsec_c,
                "seq": f"{seq}({hex(seq)})",
                "rand": rand,
                "time": time,
                "nsec": nsec,
            }


_uuid7_generator_milli = UUID7Generator("milli")
_uuid7_generator_micro = UUID7Generator("micro")
_uuid7_generator_nano = UUID7Generator("nano")


def uuid7(precision: Precision = "micro") -> UUID:
    if precision == "milli":
        return _uuid7_generator_milli.generate()
    elif precision == "micro":
        return _uuid7_generator_micro.generate()
    else:
        return _uuid7_generator_nano.generate()
