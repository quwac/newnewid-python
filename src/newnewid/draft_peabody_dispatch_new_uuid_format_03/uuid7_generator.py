from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, Optional, Tuple
from uuid import UUID

from newnewid.clock.uuid_clock import UUIDClock
from newnewid.counter.counter import Counter
from newnewid.random.pseudo_random_binary_generator import PseudoRandomBinaryGenerator
from newnewid.random.pseudo_random_generator import PseudoRandomGenerator
from newnewid.util.nodoc import nodoc
from newnewid.uuidgenerator.clock_based_uuid_generator import ClockBasedUUIDGenerator


@dataclass(frozen=True)
class UUID7Option:
    """Option for UUIDv7."""

    counter_bits_length: int
    increment_bits_length: Optional[int]

    @nodoc
    def __post_init__(self):
        assert (
            0 <= self.counter_bits_length <= 74
        ), f"counter_bits_length must be between 0 and 74, not {self.counter_bits_length}"

        if self.increment_bits_length is not None:
            assert (
                self.increment_bits_length <= self.counter_bits_length
            ), f"increment_bits_length must be equal or less than counter_bits_length, not {self.increment_bits_length}"

    @classmethod
    def method_1_fixed_length_dedicated_counter_bits(
        cls, counter_bits_length: int
    ) -> "UUID7Option":
        """Create option for UUIDv7 of method 1.

        Args:
            counter_bits_length (int): Counter value length in bits.

        Returns:
            UUID7Option: Option for UUIDv7 of method 1.
        """
        assert (
            12 <= counter_bits_length <= 42
        ), f"counter_bits_length must be between 12 and 42, not {counter_bits_length}"

        return cls(
            counter_bits_length=counter_bits_length,
            increment_bits_length=1,
        )

    @classmethod
    def method_2_monotonic_random(cls, max_increment_bits_length: int) -> "UUID7Option":
        """Create option for UUIDv7 of method 2.

        Args:
            max_increment_bits_length (int): Maximum increment value length in bits.
            Range of the value is 1 to 2^max_increment_bits_length - 1.

        Returns:
            UUID7Option: Option for UUIDv7 of method 2.
        """
        assert (
            1 <= max_increment_bits_length <= 74
        ), f"increment_bits_length must be between 1 and 72, not {max_increment_bits_length}"

        return cls(
            counter_bits_length=74,
            increment_bits_length=max_increment_bits_length,
        )


METHOD_0_NO_COUNTER = UUID7Option(counter_bits_length=0, increment_bits_length=None)

METHOD_1_FIXED_LENGTH_DEDICATED_COUNTER_BITS_12 = (
    UUID7Option.method_1_fixed_length_dedicated_counter_bits(
        counter_bits_length=12,
    )
)

METHOD_1_FIXED_LENGTH_DEDICATED_COUNTER_BITS_26 = (
    UUID7Option.method_1_fixed_length_dedicated_counter_bits(
        counter_bits_length=26,
    )
)

METHOD_1_FIXED_LENGTH_DEDICATED_COUNTER_BITS_42 = (
    UUID7Option.method_1_fixed_length_dedicated_counter_bits(
        counter_bits_length=42,
    )
)


METHOD_2_MONOTONIC_RANDOM_62_BITS = UUID7Option.method_2_monotonic_random(
    max_increment_bits_length=62,
)


_ULID_COMPATIBLE_OPTION = UUID7Option.method_2_monotonic_random(
    max_increment_bits_length=1,
)


class UUID7Generator(ClockBasedUUIDGenerator):
    """UUIDv7 generator class.

    UUIDv7 is a 128-bit UUID that is based on Epoch time and is sortable.

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

    There are two variations of UUIDv7:

    * Method 1: Fixed-length dedicated counter bits: `rand_a` and `rand_b` are used as counters,
      with a length of 1 to 74 bits. When `unix_ts_ms` is the same as the previous timestamp,
      the counter is incremented by 1. The counter is reset to a random number when `unix_ts_ms`
      changes. The remaining 73 to 1 bits of `rand_a` and `rand_b` are used for pseudo-random
      numbers.
    * Method 2: Monotonic random: `rand_a` and `rand_b` are used to generate random numbers.
      This method is a special case of Method 1, with a counter length of 74 bits, incremented
      by a pseudo-random number. The number is generated from a range of values that can be
      represented by a fixed-length bit sequence, excluding 0.

    The parameter for Method 1 is `counter_bits_length`, which is the length of the counter bits.
    The parameter for Method 2 is `increment_bits_length`, which is the bit length that determines
    the range of pseudo-random values generated during incrementation.

    Method 1 with counter_bits_length=74 is equivalent to Method 2 with increment_bits_length=1.
    """

    def __init__(
        self,
        uuid7_option: UUID7Option,
        raise_exception_on_backward: bool = False,
        clock: Optional[UUIDClock] = None,
        pseudo_random_generator: Optional[PseudoRandomGenerator] = None,
        last_uuid: Optional[UUID] = None,
    ) -> None:
        """Create UUIDv7 generator.

        Args:
            uuid7_option (UUID7Option): UUIDv7 option.
            raise_exception_on_backward (bool, optional): Raise exception when backward UUID is generated. Otherwise, sleep until the next milliseconds. Defaults to False.
            clock (Optional[UUIDClock], optional): Clock. Defaults to None.
            pseudo_random_generator (Optional[PseudoRandomGenerator], optional): Pseudo random generator. Defaults to None.
            last_uuid (Optional[UUID], optional): Last UUID. Defaults to None.
        """
        super().__init__(
            raise_exception_on_backward=raise_exception_on_backward,
            clock=clock,
            pseudo_random_generator=pseudo_random_generator,
            last_uuid=last_uuid,
        )

        last_timestamp: Optional[int] = None
        last_counter: Optional[int] = None
        if last_uuid:
            assert last_uuid.version == 7, f"last_uuid must be version 7, not {last_uuid.version}"

            last_timestamp, last_counter = self.__class__._parse_last_uuid(
                last_uuid,
                uuid7_option,
            )

        self._counter = Counter(
            bits_length=uuid7_option.counter_bits_length,
            max_increment_bits_length=uuid7_option.increment_bits_length,
            pseudo_random_generator=self._pseudo_random_generator,
            initial_timestamp=last_timestamp,
            initial_counter=last_counter,
        )

        assert (
            0 <= self._counter.bits_length <= 74
        ), f"mask_bits_length must be between 0 and 74, not {self._counter.bits_length}"
        self.rand_bits = 74 - self._counter.bits_length

        self._pseudo_random_binary_generator = PseudoRandomBinaryGenerator(
            self.rand_bits, self._pseudo_random_generator
        )

    @nodoc
    def timestamp(self, clock: UUIDClock) -> int:
        return clock.epoch_milli_seconds()

    @property
    @nodoc
    def clock_bits_length(self) -> int:
        return 48

    @property
    @nodoc
    def least_seconds(self) -> float:
        return 0.001

    @nodoc
    def generate_impl(self, timestamp: int) -> UUID:
        # 48 bits
        unix_ts_ms = timestamp

        # 4 bits
        ver = 7

        # 0 bits - 74 bits
        seq = self._counter.get_next(unix_ts_ms)
        # 74 bits - 0 bits
        node = self._pseudo_random_binary_generator.generate()

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
    def parse(cls, uuid: UUID, uuid7_option: UUID7Option, **kwargs: Any) -> Dict[str, Any]:
        """Parse UUIDv7.

        Args:
            uuid (UUID): UUID.
            uuid7_option (UUID7Option): UUIDv7 option.

        Returns:
            Dict[str, Any]: Parsed UUIDv7.
        """
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
        seq, rand = cls._parse_counter_and_rand(rand_a, rand_b, uuid7_option)

        time = datetime.fromtimestamp(unix_ts_ms / 1000)
        return {
            "unix_ts_ms": unix_ts_ms,
            "ver": "7",
            "rand_a": rand_a,
            "var": variant,
            "rand_b": rand_b,
            "time": time.isoformat(),
            "seq": seq,
            "rand": rand,
        }

    @classmethod
    def _parse_counter_and_rand(
        cls,
        rand_a: int,
        rand_b: int,
        uuid7_option: UUID7Option,
    ) -> Tuple[Optional[int], Optional[int]]:
        seq_and_rand = (rand_a << 62) | rand_b
        if uuid7_option.counter_bits_length == 0:
            return None, seq_and_rand
        elif uuid7_option.counter_bits_length == 74:
            return seq_and_rand, None

        seq_mask = (1 << uuid7_option.counter_bits_length) - 1
        rand_bits = 74 - uuid7_option.counter_bits_length
        rand_mask = (1 << rand_bits) - 1

        seq = (seq_and_rand >> rand_bits) & seq_mask
        rand = seq_and_rand & rand_mask

        return seq, rand

    @classmethod
    def _parse_last_uuid(
        cls,
        last_uuid: UUID,
        uuid7_option: UUID7Option,
    ) -> Tuple[int, Optional[int]]:
        parsed = cls.parse(last_uuid, uuid7_option)
        unix_ts_ms: int = parsed["unix_ts_ms"]
        counter, _ = cls._parse_counter_and_rand(
            rand_a=parsed["rand_a"],
            rand_b=parsed["rand_b"],
            uuid7_option=uuid7_option,
        )

        return (unix_ts_ms, counter)


_option_to_uuid7_generator: Dict[UUID7Option, UUID7Generator] = {}


def uuid7(
    uuid7_option: Optional[UUID7Option] = None,
) -> UUID:
    """Generate UUIDv7.

    Args:
        uuid7_option (Optional[UUID7Option], optional): UUIDv7 option. Defaults to None.

    Returns:
        UUID: UUIDv7.
    """
    uuid7_option = uuid7_option or METHOD_1_FIXED_LENGTH_DEDICATED_COUNTER_BITS_12
    if uuid7_option not in _option_to_uuid7_generator:
        _option_to_uuid7_generator[uuid7_option] = UUID7Generator(
            uuid7_option=uuid7_option,
        )
    uuid7_generator = _option_to_uuid7_generator[uuid7_option]

    return uuid7_generator.generate()


# ==================== BONUS TRACK ====================

_ulid_compatible_generator = UUID7Generator(_ULID_COMPATIBLE_OPTION)


def ulid_compatible() -> UUID:
    """Generate ULID compatible UUIDv7.

    Returns:
        UUID: UUIDv7.
    """
    return _ulid_compatible_generator.generate()
