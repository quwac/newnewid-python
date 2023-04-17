from dataclasses import dataclass
from datetime import datetime, timezone
from typing import List, Optional

from newnewid.clock.uuid_clock import UUIDClock


@dataclass(frozen=True)
class NanoDateTime:
    datetime: datetime
    nanosecond_fraction: int

    @classmethod
    def from_raw(
        cls,
        year: int,
        month: int,
        day: int,
        hour: int,
        minute: int,
        second: int,
        microsecond: int = 0,
        nanosecond_fraction: int = 0,
        tzinfo: Optional[timezone] = None,
    ) -> "NanoDateTime":
        assert 0 <= microsecond <= 999_999
        assert 0 <= nanosecond_fraction <= 999

        tzinfo = tzinfo or timezone.utc
        dt_epoch_time = datetime(
            year=year,
            month=month,
            day=day,
            hour=hour,
            minute=minute,
            second=second,
            microsecond=microsecond,
            tzinfo=tzinfo,
        )
        return NanoDateTime(dt_epoch_time, nanosecond_fraction)

    @property
    def time_ns(self) -> int:
        return (
            int(self.datetime.timestamp()) * 1_000_000_000
            + self.datetime.microsecond * 1_000
            + self.nanosecond_fraction
        )


class FrozenClock(UUIDClock):
    @classmethod
    def from_nano_datetime(cls, nano_datetime: NanoDateTime) -> "FrozenClock":
        return cls([nano_datetime])

    @classmethod
    def from_raw(
        cls,
        year: int,
        month: int,
        day: int,
        hour: int,
        minute: int,
        second: int,
        microsecond: int = 0,
        nanosecond_fraction: int = 0,
        tzinfo: Optional[timezone] = None,
    ) -> "FrozenClock":
        assert 0 <= microsecond <= 999_999
        assert 0 <= nanosecond_fraction <= 999

        tzinfo = tzinfo or timezone.utc
        dt_epoch_time = datetime(
            year=year,
            month=month,
            day=day,
            hour=hour,
            minute=minute,
            second=second,
            microsecond=microsecond,
            tzinfo=tzinfo,
        )
        return cls([NanoDateTime(dt_epoch_time, nanosecond_fraction)])

    def __init__(
        self,
        nano_datetimes: List[NanoDateTime],
    ) -> None:
        super().__init__()
        self._nano_datetimes = nano_datetimes
        self.index = -1

    def epoch_nano_seconds(self) -> int:
        self.index = (self.index + 1) % len(self._nano_datetimes)
        return self._nano_datetimes[self.index].time_ns
