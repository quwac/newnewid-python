from uuid import RFC_4122, UUID

from assert_uuid import assert_uuid
from frozen_clock import FrozenClock

import newuuid.draft_peabody_dispatch_new_uuid_format_01 as newuuid
from newuuid.draft_peabody_dispatch_new_uuid_format_01.uuid7_generator import Sequencer
from newuuid.random.pseudo_random_generator import PseudoRandomGenerator


class _PseudoRandomGenerator(PseudoRandomGenerator):
    def __init__(self, bits: int) -> None:
        super().__init__(1)
        self._rand_value = bits

    def generate(self) -> int:
        return self._rand_value


class TestUUID7Dpdnuf01:
    def test_uuid7(self):
        uuid = newuuid.uuid7()
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

        pseudo_random_generator = _PseudoRandomGenerator(700424987533113857)
        generator = newuuid.UUID7Generator(
            "milli",
            clock=clock,
            sequencer=Sequencer(
                12, clock.epoch_36_bits_seconds_with_12_bits_milli_seconds(), 2107 - 1
            ),
            pseudo_random_generator=pseudo_random_generator,
        )
        actual = generator.generate()
        assert_uuid(
            actual,
            UUID("06113209-430f-783b-89b8-68d0adb7fa01"),
            newuuid.UUID7Generator,
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
        pseudo_random_generator = _PseudoRandomGenerator(198164501276449)
        generator = newuuid.UUID7Generator(
            "micro",
            clock=clock,
            sequencer=Sequencer(
                14,
                clock.epoch_36_bits_seconds_with_24_bits_micro_seconds(),
                14164 - 1,
            ),
            pseudo_random_generator=pseudo_random_generator,
        )
        actual = generator.generate()
        assert_uuid(
            actual,
            UUID("06113208-e044-7660-b754-b43ac4b4a721"),
            newuuid.UUID7Generator,
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
        pseudo_random_generator = _PseudoRandomGenerator(1004681078690)
        generator = newuuid.UUID7Generator(
            "nano",
            clock=clock,
            sequencer=Sequencer(
                8, clock.epoch_36_bits_seconds_with_38_bits_nano_seconds(), 170 - 1
            ),
            pseudo_random_generator=pseudo_random_generator,
        )
        actual = generator.generate()
        assert_uuid(
            actual,
            UUID("06113208-6004-70e1-b76d-aae9eba8a7a2"),
            newuuid.UUID7Generator,
            precision="nano",
        )
