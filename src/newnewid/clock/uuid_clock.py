import time
from datetime import datetime, timedelta
from typing import Tuple


class UUIDClock:
    """Clock for UUID."""

    GREGORIAN_OFFSET = 0x1B2_1DD_213_814_000

    # ----------------------------
    # epoch_*_seconds
    # ----------------------------

    def epoch_seconds(self) -> int:
        """Get time in seconds.

        Returns:
            int: Epoch time in seconds.
        """
        return self.epoch_nano_seconds() // 1_000_000_000

    def epoch_milli_seconds(self) -> int:
        """Get time in milliseconds.

        Returns:
            int: Epoch time in milliseconds.
        """
        return self.epoch_nano_seconds() // 1_000_000

    def epoch_nano_seconds(self) -> int:
        """Get time in nanoseconds.

        Returns:
            int: Epoch time in nanoseconds.
        """
        return time.time_ns()

    def epoch_100_nano_seconds(self) -> int:
        """Get time in 100 nanoseconds.

        Returns:
            int: Epoch time in 100 nanoseconds.
        """
        return self.epoch_nano_seconds() // 100

    # ----------------------------
    # gregorian
    # ----------------------------

    def gregorian_100_nano_seconds(self) -> int:
        """Get time in 100 nanoseconds since Gregorian epoch.

        Returns:
            int: Time in 100 nanoseconds since Gregorian epoch.
        """
        return self.epoch_nano_seconds() // 100 + self.GREGORIAN_OFFSET

    # ----------------------------
    # epoch_36_bits_seconds_with_*_bits_*_seconds
    # ----------------------------

    def epoch_36_bits_seconds_with_12_bits_milli_seconds(self) -> int:
        """Get time in 12 bits milliseconds since epoch.

        Returns:
            int: Time in 12 bits milliseconds since epoch.
        """
        seconds, milli_part = divmod(self.epoch_nano_seconds() // 1_000_000, 1_000)
        return ((seconds & 0x000F_FFFF_FFFF) << 12) | milli_part

    def epoch_36_bits_seconds_with_24_bits_micro_seconds(self) -> int:
        """Get time in 24 bits microseconds since epoch.

        Returns:
            int: Time in 24 bits microseconds since epoch.
        """
        seconds, micro_part = divmod(self.epoch_nano_seconds() // 1_000, 1_000_000)
        return ((seconds & 0x000F_FFFF_FFFF) << 24) | micro_part

    def epoch_36_bits_seconds_with_38_bits_nano_seconds(self) -> int:
        """Get time in 38 bits nanoseconds since epoch.

        Returns:
            int: Time in 38 bits nanoseconds since epoch.
        """
        seconds, nano_part = divmod(self.epoch_nano_seconds(), 1_000_000_000)
        return ((seconds & 0x000F_FFFF_FFFF) << 38) | nano_part

    # ----------------------------
    # converter
    # ----------------------------

    @classmethod
    def to_datetime_from_epoch_seconds(cls, epoch_seconds: int) -> datetime:
        """Convert epoch seconds to datetime.

        Args:
            epoch_seconds (int): Epoch seconds.

        Returns:
            datetime: Datetime.
        """
        return datetime.fromtimestamp(epoch_seconds)

    @classmethod
    def to_datetime_from_epoch_milli_seconds(cls, epoch_milli_seconds: int) -> datetime:
        """Convert epoch milliseconds to datetime.

        Args:
            epoch_milli_seconds (int): Epoch milliseconds.

        Returns:
            datetime: Datetime.
        """
        return datetime.fromtimestamp(epoch_milli_seconds / 1_000)

    @classmethod
    def to_datetime_from_epoch_micro_seconds(cls, epoch_micro_seconds: int) -> datetime:
        """Convert epoch microseconds to datetime.

        Args:
            epoch_micro_seconds (int): Epoch microseconds.

        Returns:
            datetime: Datetime.
        """
        return datetime.fromtimestamp(epoch_micro_seconds / 1_000_000)

    @classmethod
    def to_datetime_from_epoch_100_nano_seconds(
        cls, epoch_100_nano_seconds: int
    ) -> Tuple[datetime, int]:
        """Convert epoch 100 nanoseconds to datetime.

        Args:
            epoch_100_nano_seconds (int): Epoch 100 nanoseconds.

        Returns:
            Tuple[datetime, int]: Datetime and nanoseconds.
        """
        return (
            datetime.fromtimestamp(epoch_100_nano_seconds / 10_000_000_000),
            epoch_100_nano_seconds % 10_000_000_000,
        )

    @classmethod
    def to_datetime_from_gregorian_100_nano_seconds(
        cls, gregorian_100_nano_seconds: int
    ) -> Tuple[datetime, int]:
        """Convert gregorian 100 nanoseconds to datetime.

        Args:
            gregorian_100_nano_seconds (int): Gregorian 100 nanoseconds.

        Returns:
            Tuple[datetime, int]: Datetime and nanoseconds.
        """
        epoch_100_nano_seconds = gregorian_100_nano_seconds - cls.GREGORIAN_OFFSET
        (seconds, fraction_nano) = divmod(epoch_100_nano_seconds * 100, 1_000_000_000)
        (microseconds, fraction_nano) = divmod(fraction_nano, 1000)
        return (
            datetime.fromtimestamp(seconds) + timedelta(microseconds=microseconds),
            fraction_nano,
        )

    @classmethod
    def to_datetime_from_epoch_nano_seconds(cls, epoch_nano_seconds: int) -> Tuple[datetime, int]:
        """Convert epoch nanoseconds to datetime.

        Args:
            epoch_nano_seconds (int): Epoch nanoseconds.

        Returns:
            Tuple[datetime, int]: Datetime and nanoseconds.
        """
        return (
            datetime.fromtimestamp(epoch_nano_seconds / 10_000_000_000),
            epoch_nano_seconds % 1_000_000_000,
        )
