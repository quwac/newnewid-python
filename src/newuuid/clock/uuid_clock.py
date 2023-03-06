import time
from datetime import datetime
from typing import Tuple


class UUIDClock:
    GREGORIAN_OFFSET = 0x1B2_1DD_213_814_000

    def time_ns(self) -> int:
        return time.time_ns()

    # ----------------------------
    # epoch_*_seconds
    # ----------------------------

    def epoch_seconds(self) -> int:
        return self.time_ns() // 1_000_000_000

    def epoch_milli_seconds(self) -> int:
        return self.time_ns() // 1_000_000

    def epoch_100_nano_seconds(self) -> int:
        return self.time_ns() // 100

    # ----------------------------
    # gregorian
    # ----------------------------

    def gregorian_100_nano_seconds(self) -> int:
        return self.time_ns() // 100 + self.GREGORIAN_OFFSET

    # ----------------------------
    # epoch_seconds_with_*_seconds_fraction
    # ----------------------------

    def epoch_36_bits_seconds_with_12_bits_milli_seconds(self) -> int:
        seconds, milli_part = divmod(self.time_ns() // 1_000_000, 1_000)
        return ((seconds & 0x000F_FFFF_FFFF) << 12) | milli_part

    def epoch_36_bits_seconds_with_24_bits_micro_seconds(self) -> int:
        seconds, micro_part = divmod(self.time_ns() // 1_000, 1_000_000)
        return ((seconds & 0x000F_FFFF_FFFF) << 24) | micro_part

    def epoch_36_bits_seconds_with_38_bits_nano_seconds(self) -> int:
        seconds, nano_part = divmod(self.time_ns(), 1_000_000_000)
        return ((seconds & 0x000F_FFFF_FFFF) << 38) | nano_part

    # ----------------------------
    # converter
    # ----------------------------

    @classmethod
    def to_datetime_from_epoch_seconds(cls, epoch_seconds: int) -> datetime:
        return datetime.fromtimestamp(epoch_seconds)

    @classmethod
    def to_datetime_from_epoch_milli_seconds(cls, epoch_milli_seconds: int) -> datetime:
        return datetime.fromtimestamp(epoch_milli_seconds / 1_000)

    @classmethod
    def to_datetime_from_epoch_micro_seconds(cls, epoch_micro_seconds: int) -> datetime:
        return datetime.fromtimestamp(epoch_micro_seconds / 1_000_000)

    @classmethod
    def to_datetime_from_epoch_100_nano_seconds(
        cls, epoch_100_nano_seconds: int
    ) -> Tuple[datetime, int]:
        return (
            datetime.fromtimestamp(epoch_100_nano_seconds / 10_000_000_000),
            epoch_100_nano_seconds % 10_000_000_000,
        )

    @classmethod
    def to_datetime_from_gregorian_100_nano_seconds(
        cls, gregorian_100_nano_seconds: int
    ) -> Tuple[datetime, int]:
        epoch_100_nano_seconds = gregorian_100_nano_seconds - cls.GREGORIAN_OFFSET
        return (
            datetime.fromtimestamp(epoch_100_nano_seconds / 10_000_000_000),
            epoch_100_nano_seconds % 10_000_000_000,
        )

    @classmethod
    def to_datetime_from_epoch_nano_seconds(cls, epoch_nano_seconds: int) -> Tuple[datetime, int]:
        return (
            datetime.fromtimestamp(epoch_nano_seconds / 10_000_000_000),
            epoch_nano_seconds % 1_000_000_000,
        )
