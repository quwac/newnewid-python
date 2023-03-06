from datetime import datetime, timezone
from typing import Optional

from newnewid.clock.uuid_clock import UUIDClock


class FrozenClock(UUIDClock):
    @classmethod
    def from_datetime(cls, datetime: datetime, nanosecond_fraction: int = 0) -> "FrozenClock":
        return cls(
            year=datetime.year,
            month=datetime.month,
            day=datetime.day,
            hour=datetime.hour,
            minute=datetime.minute,
            second=datetime.second,
            microsecond=datetime.microsecond,
            nanosecond_fraction=nanosecond_fraction,
            tzinfo=datetime.tzinfo,  # type: ignore
        )

    def __init__(
        self,
        year: int,
        month: int,
        day: int,
        hour: int,
        minute: int,
        second: int,
        microsecond: int = 0,
        nanosecond_fraction: int = 0,
        tzinfo: Optional[timezone] = None,
    ) -> None:
        tzinfo = tzinfo or timezone.utc
        super().__init__()
        dt_epoch_time = datetime(
            year=year,
            month=month,
            day=day,
            hour=hour,
            minute=minute,
            second=second,
            tzinfo=tzinfo,
        )
        self._time_ns = (
            int(dt_epoch_time.timestamp()) * 1_000_000_000
            + microsecond * 1_000
            + nanosecond_fraction
        )

    def time_ns(self) -> int:
        return self._time_ns
