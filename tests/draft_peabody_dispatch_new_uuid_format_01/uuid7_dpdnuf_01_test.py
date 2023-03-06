from uuid import RFC_4122, UUID

from assert_uuid import assert_uuid
from frozen_clock import FrozenClock
from frozen_pseudo_random_generator import FrozenPseudoRandomGenerator

import newnewid.draft_peabody_dispatch_new_uuid_format_01 as newnewid


class TestUUID7Dpdnuf01:
    def test_uuid7(self):
        uuid = newnewid.uuid7()
        assert uuid.version == 7
        assert uuid.variant == RFC_4122

    def test_uuid7_generator_milli(self):
        clock = FrozenClock(
            year=2021,
            month=8,
            day=11,
            hour=0,
            minute=57,
            second=56,
            microsecond=783000,
        )
        pseudo_random_generator = FrozenPseudoRandomGenerator(
            counter_reset=2107,
            random_binary=700424987533113857,
        )

        generator = newnewid.UUID7Generator(
            "milli",
            clock=clock,
            pseudo_random_generator=pseudo_random_generator,
        )
        actual = generator.generate()
        assert_uuid(
            actual,
            UUID("06113209-430f-783b-89b8-68d0adb7fa01"),
            newnewid.UUID7Generator,
            precision="milli",
        )

    def test_uuid6_generator_micro(self):
        clock = FrozenClock(
            2021,
            8,
            11,
            0,
            57,
            50,
            280160,
        )
        pseudo_random_generator = FrozenPseudoRandomGenerator(
            counter_reset=14164,
            random_binary=198164501276449,
        )
        generator = newnewid.UUID7Generator(
            "micro",
            clock=clock,
            pseudo_random_generator=pseudo_random_generator,
        )
        actual = generator.generate()
        assert_uuid(
            actual,
            UUID("06113208-e044-7660-b754-b43ac4b4a721"),
            newnewid.UUID7Generator,
            precision="micro",
        )

    def test_uuid6_generator_nano(self):
        clock = FrozenClock(
            year=2021,
            month=8,
            day=11,
            hour=0,
            minute=57,
            second=42,
            microsecond=272136,
            nanosecond_fraction=45,
        )
        pseudo_random_generator = FrozenPseudoRandomGenerator(
            counter_reset=170,
            random_binary=1004681078690,
        )
        generator = newnewid.UUID7Generator(
            "nano",
            clock=clock,
            pseudo_random_generator=pseudo_random_generator,
        )
        actual = generator.generate()
        assert_uuid(
            actual,
            UUID("06113208-6004-70e1-b76d-aae9eba8a7a2"),
            newnewid.UUID7Generator,
            precision="nano",
        )
