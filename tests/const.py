from datetime import timedelta, timezone

from frozen_clock import FrozenClock

TEST_CLOCK = FrozenClock.from_raw(
    year=2022,
    month=2,
    day=22,
    hour=14,
    minute=22,
    second=22,
    tzinfo=timezone(timedelta(hours=-5), "GMT"),
)
