from uuid import RFC_4122, UUID

from const import TEST_CLOCK

import newuuid.draft_peabody_dispatch_new_uuid_format_01 as newuuid
from newuuid.random.pseudo_random_generator import PseudoRandomGenerator
from newuuid.sequence.sequencer import Sequencer


class _PseudoRandomGenerator(PseudoRandomGenerator):
    def generate(self) -> int:
        return 174186136787014


class TestUUID6Dpdnuf01:
    def test_uuid6(self):
        uuid = newuuid.uuid6()
        assert uuid.version == 6
        assert uuid.variant == RFC_4122

    def test_uuid6_generator(self):
        generator = newuuid.UUID6Generator(
            clock=TEST_CLOCK,
            pseudo_random_generator=_PseudoRandomGenerator(1),
            sequencer=Sequencer(
                48,
                TEST_CLOCK.gregorian_100_nano_seconds(),
                13256 - 1,
            ),
        )
        uuid = generator.generate()
        assert uuid == UUID("1EC9414C-232A-6B00-B3C8-9E6BDECED846")
