from assert_uuid import assert_uuid
from const import TEST_CLOCK

import newuuid
from newuuid import UUID, PseudoRandomGenerator, Sequencer


class _PseudoRandomGenerator(PseudoRandomGenerator):
    def __init__(self) -> None:
        super().__init__(1)

    def generate(self) -> int:
        return 1784793296645077391


class TestUUID7:
    def test_uuid7(self):
        uuid = newuuid.uuid7()
        assert uuid.version == 7
        assert uuid.variant == newuuid.RFC_4122

    def test_uuid7_generator(self):
        seq_bits = 12
        generator = newuuid.UUID7Generator(
            seq_bits=seq_bits,
            clock=TEST_CLOCK,
            sequencer=Sequencer(seq_bits, TEST_CLOCK.epoch_milli_seconds(), 3267 - 1),
            pseudo_random_generator=_PseudoRandomGenerator(),
        )
        actual = generator.generate()
        excepted = UUID("017F22E2-79B0-7CC3-98C4-DC0C0C07398F")
        assert_uuid(actual, excepted, newuuid.UUID7Generator)
