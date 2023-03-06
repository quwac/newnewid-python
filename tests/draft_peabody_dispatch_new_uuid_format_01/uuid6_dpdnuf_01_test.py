from uuid import RFC_4122, UUID

from const import TEST_CLOCK
from frozen_pseudo_random_generator import FrozenPseudoRandomGenerator

import newnewid.draft_peabody_dispatch_new_uuid_format_01 as newnewid


class TestUUID6Dpdnuf01:
    def test_uuid6(self):
        uuid = newnewid.uuid6()
        assert uuid.version == 6
        assert uuid.variant == RFC_4122

    def test_uuid6_generator(self):
        random_generator = FrozenPseudoRandomGenerator(
            counter_reset=13256,
            random_binary=174186136787014,
        )
        generator = newnewid.UUID6Generator(
            uses_mac_address=False,
            clock=TEST_CLOCK,
            pseudo_random_generator=random_generator,
        )

        uuid = generator.generate()
        assert uuid == UUID("1EC9414C-232A-6B00-B3C8-9E6BDECED846")
