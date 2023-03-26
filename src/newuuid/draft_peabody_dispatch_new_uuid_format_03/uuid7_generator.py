from datetime import datetime
from typing import Any, Dict, Optional, Tuple
from uuid import UUID

from newuuid.clock.uuid_clock import UUIDClock
from newuuid.random.pseudo_random_generator import PseudoRandomGenerator
from newuuid.sequence.sequencer import Sequencer
from newuuid.uuidgenerator.uuid_generator import ClockBasedUUIDGenerator


class UUID7Generator(ClockBasedUUIDGenerator):
    DEFAULT_SEQ_BITS = 12

    def __init__(
        self,
        seq_bits: int,
        raise_exception_on_backward: bool = False,
        clock: Optional[UUIDClock] = None,
        last_uuid: Optional[UUID] = None,
        sequencer: Optional[Sequencer] = None,
        pseudo_random_generator: Optional[PseudoRandomGenerator] = None,
    ) -> None:
        assert 0 <= seq_bits <= 74, f"seq_bits must be between 0 and 74, not {seq_bits}"
        self.rand_bits = 74 - seq_bits

        super().__init__(
            raise_exception_on_backward=raise_exception_on_backward,
            clock=clock,
            last_uuid=last_uuid,
        )

        self._sequencer = sequencer or Sequencer(seq_bits)
        self._pseudo_random_generator = pseudo_random_generator or PseudoRandomGenerator(
            self.rand_bits
        )

    def timestamp(self, clock: UUIDClock) -> int:
        return clock.epoch_milli_seconds()

    @property
    def clock_bits(self) -> int:
        return 48

    @property
    def least_seconds(self) -> float:
        return 0.001

    def generate(self) -> UUID:
        """Generate UUIDv7.


         0                   1                   2                   3
         0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        |                           unix_ts_ms                          |
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        |          unix_ts_ms           |  ver  |       rand_a          |
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        |var|                        rand_b                             |
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        |                            rand_b                             |
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

        """
        return super().generate()

    def generate_impl(self, timestamp: int) -> UUID:
        # 48 bits
        unix_ts_ms = timestamp

        # 4 bits
        ver = 7

        # 0 bits - 74 bits
        seq = self._sequencer.next_sequence(unix_ts_ms)
        # 74 bits - 0 bits
        node = self._pseudo_random_generator.generate()

        # 74 bits
        seq_and_node = (seq << self.rand_bits) | node

        # 12 bits = 74 - 62
        rand_a = (seq_and_node >> 62) & 0x0FFF

        # 62 bits
        rand_b = seq_and_node & 0x3FFF_FFFF_FFFF_FFFF

        # 2 bits
        var = 0b10

        uuid_int = (unix_ts_ms << 80) | (ver << 76) | (rand_a << 64) | (var << 62) | rand_b
        return UUID(int=uuid_int)

    @classmethod
    def parse(cls, uuid: UUID, seq_bits: int = DEFAULT_SEQ_BITS, **kwargs: Any) -> Dict[str, Any]:
        assert 0 <= seq_bits <= 74, f"seq_bits must be between 0 and 74, not {seq_bits}"

        # 48 bits
        unix_ts_ms = (uuid.int >> 80) & 0xFFFF_FFFF_FFFF

        # 4 bits
        ver = (uuid.int >> 76) & 0x0F
        assert ver == 7, f"version must be 7, not {ver}"

        # 12 bits
        rand_a = (uuid.int >> 64) & 0x0FFF

        # 2 bits
        variant = (uuid.int >> 62) & 0x03

        # 62 bits
        rand_b = uuid.int & 0x3FFF_FFFF_FFFF_FFFF

        # 0 - 74 bits
        seq, rand = cls._parse_seq_and_rand(rand_a, rand_b, seq_bits)

        time = datetime.fromtimestamp(unix_ts_ms / 1000)
        return {
            "unix_ts_ms": unix_ts_ms,
            "ver": "7",
            "rand_a": rand_a,
            "var": variant,
            "rand_b": rand_b,
            "time": time.isoformat(),
            "seq": f"{seq}({hex(seq) if seq is not None else 'None'})",
            "rand": f"{rand}({hex(rand) if rand is not None else 'None'})",
        }

    @classmethod
    def _parse_seq_and_rand(cls, rand_a, rand_b, seq_bits) -> Tuple[Optional[int], Optional[int]]:
        seq_and_rand = (rand_a << 62) | rand_b
        if seq_bits == 0:
            return None, seq_and_rand
        elif seq_bits == 74:
            return seq_and_rand, None

        seq_mask = (1 << seq_bits) - 1
        rand_bits = 74 - seq_bits
        rand_mask = (1 << rand_bits) - 1

        seq = (seq_and_rand >> rand_bits) & seq_mask
        rand = seq_and_rand & rand_mask

        return seq, rand


_seq_bits_to_uuid7_generator: Dict[int, UUID7Generator] = {}


def uuid7(seq_bits: int = UUID7Generator.DEFAULT_SEQ_BITS) -> UUID:
    if seq_bits not in _seq_bits_to_uuid7_generator:
        _seq_bits_to_uuid7_generator[seq_bits] = UUID7Generator(seq_bits)
    uuid7_generator = _seq_bits_to_uuid7_generator[seq_bits]

    return uuid7_generator.generate()
