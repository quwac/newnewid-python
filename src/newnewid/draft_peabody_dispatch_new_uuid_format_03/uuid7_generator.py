import math
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any, Dict, Optional, Tuple
from uuid import UUID

from newnewid.clock.uuid_clock import UUIDClock
from newnewid.counter.counter import Counter
from newnewid.random.pseudo_random_binary_generator import PseudoRandomBinaryGenerator
from newnewid.random.pseudo_random_generator import PseudoRandomGenerator
from newnewid.util.nodoc import nodoc
from newnewid.uuidgenerator.clock_based_uuid_generator import ClockBasedUUIDGenerator


@dataclass(frozen=True)
class CounterOption:
    """Option for counter bits generation."""

    counter_bits_length: int
    max_increment_bits_length: int

    def __post_init__(self):
        assert (
            0 < self.counter_bits_length <= 74
        ), f"counter_bits_length must be 0 < x <= 74, not {self.counter_bits_length}"

        assert self.max_increment_bits_length <= self.max_increment_bits_length, (
            "max_increment_bits_length must be less than or equal to counter_bits_length, "
            + f"not {self.max_increment_bits_length} > {self.counter_bits_length}"
        )


@dataclass(frozen=True)
class RandomOption:
    """Option for random bits generation."""

    random_bits_length: int
    rerandomize_until_monotonic: bool

    @nodoc
    def __post_init__(self):
        assert (
            self.random_bits_length > 0
        ), f"random_bits_length must be greater than 0, not {self.random_bits_length}"


@dataclass(frozen=True)
class UUID7Option:
    """Option for UUIDv7."""

    time_fraction_bits_length: int
    counter_option: Optional[CounterOption]
    random_option: Optional[RandomOption]

    @nodoc
    def __post_init__(self):
        all_bits_length = (
            self.time_fraction_bits_length
            + (self.counter_option.counter_bits_length if self.counter_option else 0)
            + (self.random_option.random_bits_length if self.random_option else 0)
        )

        assert all_bits_length == 74, "all bits length must be 74"

    @property
    @nodoc
    def counter_bits_length(self) -> int:
        return self.counter_option.counter_bits_length if self.counter_option else 0

    @property
    @nodoc
    def max_increment_bits_length(self) -> int:
        return self.counter_option.max_increment_bits_length if self.counter_option else 0

    @property
    @nodoc
    def random_bits_length(self) -> int:
        return self.random_option.random_bits_length if self.random_option else 0

    @property
    @nodoc
    def rerandomize_until_monotonic(self) -> bool:
        return self.random_option.rerandomize_until_monotonic if self.random_option else False

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
            time_fraction_bits_length=0,
            counter_option=CounterOption(
                counter_bits_length=counter_bits_length,
                max_increment_bits_length=1,
            ),
            random_option=RandomOption(
                random_bits_length=74 - counter_bits_length,
                rerandomize_until_monotonic=False,
            ),
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
            time_fraction_bits_length=0,
            counter_option=CounterOption(
                counter_bits_length=74,
                max_increment_bits_length=max_increment_bits_length,
            ),
            random_option=None,
        )

    @classmethod
    def method_3_rerandomize_until_monotonic(cls) -> "UUID7Option":
        """Create option for UUIDv7 of method 3.

        This implementation is provided for reference and my study.
        The committed outputs of Method 2 and Method 3 are the same. For users of this package,
        Method 3 has only the disadvantages of longer computation time and a tendency to rollover.

        Returns:
            UUID7Option: Option for UUIDv7 of method 3.
        """
        return cls(
            time_fraction_bits_length=0,
            counter_option=None,
            random_option=RandomOption(
                random_bits_length=74,
                rerandomize_until_monotonic=True,
            ),
        )

    @classmethod
    def method_4_replace_left_most_random_bits_with_increased_clock_precision(
        cls,
        time_fraction_bits_length: int,
        counter_bits_length: int,
    ) -> "UUID7Option":
        """Create option for UUIDv7 of method 4.

        Args:
            counter_bits_length (int): Counter value length in bits.
            time_fraction_bits_length (int): Time fraction length in bits.

        Returns:
            UUID7Option: Option for UUIDv7 of method 1.
        """
        if counter_bits_length > 0:
            assert (
                12 <= counter_bits_length <= 42
            ), f"counter_bits_length must be between 12 and 42, not {counter_bits_length}"
            assert (
                12 <= counter_bits_length + time_fraction_bits_length <= 74
            ), f"counter_bits_length + time_fraction_bits_length must be between 12 and 74, not counter_bits_length={counter_bits_length}, time_fraction_bits_length={time_fraction_bits_length}"
        else:
            assert (
                1 <= time_fraction_bits_length <= 74
            ), f"time_fraction_bits_length must be between 1 and 74, not {counter_bits_length}"

        if counter_bits_length == 0:
            counter_option = None
        else:
            counter_option = CounterOption(
                counter_bits_length=counter_bits_length,
                max_increment_bits_length=1,
            )

        return cls(
            time_fraction_bits_length=time_fraction_bits_length,
            counter_option=counter_option,
            random_option=RandomOption(
                random_bits_length=74 - counter_bits_length - time_fraction_bits_length,
                rerandomize_until_monotonic=False,
            ),
        )


METHOD_0_NO_COUNTER = UUID7Option(
    time_fraction_bits_length=0,
    counter_option=None,
    random_option=RandomOption(
        random_bits_length=74,
        rerandomize_until_monotonic=False,
    ),
)

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

METHOD_3_RERANDOMIZE_UNTIL_MONOTONIC = UUID7Option.method_3_rerandomize_until_monotonic()

METHOD_4_REPLACE_LEFT_MOST_RANDOM_BITS_WITH_INCREASED_CLOCK_PRECISION_12_BITS = (
    UUID7Option.method_4_replace_left_most_random_bits_with_increased_clock_precision(
        time_fraction_bits_length=12,
        counter_bits_length=0,
    )
)

METHOD_4_REPLACE_LEFT_MOST_RANDOM_BITS_WITH_INCREASED_CLOCK_PRECISION_12_BITS_WITH_COUNTER_14_BITS = UUID7Option.method_4_replace_left_most_random_bits_with_increased_clock_precision(
    time_fraction_bits_length=12,
    counter_bits_length=14,
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
            counter_bits_length=uuid7_option.counter_bits_length,
            max_increment_bits_length=uuid7_option.max_increment_bits_length,
            pseudo_random_generator=self._pseudo_random_generator,
            initial_timestamp=last_timestamp,
            initial_counter=last_counter,
        )

        self.time_fraction_bits_length = uuid7_option.time_fraction_bits_length
        self.time_fraction_max = (
            (1 << self.time_fraction_bits_length) if self.time_fraction_bits_length > 0 else 0
        )

        self.rand_bits_length = uuid7_option.random_bits_length

        self._pseudo_random_binary_generator = PseudoRandomBinaryGenerator(
            self.rand_bits_length, self._pseudo_random_generator
        )
        self.rerandomize_until_monotonic = (
            uuid7_option.rerandomize_until_monotonic
            if uuid7_option.rerandomize_until_monotonic
            else False
        )

    @nodoc
    def timestamp(self, clock: UUIDClock) -> int:
        return clock.epoch_nano_seconds()

    @property
    @nodoc
    def clock_bits_length(self) -> int:
        # unix_ts_ms is 48 and time_fraction may be 0 bits to 72 bits.
        return 122

    @property
    @nodoc
    def least_seconds(self) -> float:
        if self.time_fraction_bits_length == 0:
            return 0.001
        else:
            return 0.000_000_001

    @nodoc
    def generate_impl(self, timestamp: int) -> UUID:
        unix_ts_ms, fraction_nano = divmod(timestamp, 1_000_000)

        # 48 bits
        unix_ts_ms &= 0xFFFF_FFFF_FFFF

        # 4 bits
        ver = 7

        # 0 bits - 74 bits
        time_fraction = math.ceil(self.time_fraction_max * fraction_nano / 1_000_000) & (
            self.time_fraction_max - 1
        )
        # 0 bits or 12 bits - 48 bits
        seq = self._counter.get_next(timestamp)
        # 0 bits - 74 bits
        node = self._pseudo_random_binary_generator.generate(
            monotonic=self.rerandomize_until_monotonic
        )

        # 74 bits
        randomize_section = (
            (time_fraction << (self.rand_bits_length + self._counter.counter_bits_length))
            | (seq << self.rand_bits_length)
            | node
        )

        # 12 bits = 74 - 62
        rand_a = (randomize_section >> 62) & 0x0FFF

        # 62 bits
        rand_b = randomize_section & 0x3FFF_FFFF_FFFF_FFFF

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
        time_fraction, seq, rand = cls._parse_from_random_section(rand_a, rand_b, uuid7_option)

        unix_ts, milliseconds = divmod(unix_ts_ms, 1000)
        time = datetime.fromtimestamp(unix_ts).replace(microsecond=milliseconds * 1000)

        if time_fraction is not None:
            micro_fraction, nano_fraction = divmod(
                (time_fraction * 1_000_000) // (1 << uuid7_option.time_fraction_bits_length), 1000
            )
            time = time + timedelta(microseconds=micro_fraction)
        else:
            nano_fraction = None

        return {
            "unix_ts_ms": unix_ts_ms,
            "ver": "7",
            "rand_a": rand_a,
            "var": variant,
            "rand_b": rand_b,
            "time": time.isoformat(),
            "nano_fraction": nano_fraction,
            "seq": seq,
            "rand": rand,
        }

    @classmethod
    def _parse_from_random_section(
        cls,
        rand_a: int,
        rand_b: int,
        uuid7_option: UUID7Option,
    ) -> Tuple[Optional[int], Optional[int], Optional[int]]:
        random_section = (rand_a << 62) | rand_b

        time_fraction_bits_length = uuid7_option.time_fraction_bits_length
        time_fraction_mask = (1 << time_fraction_bits_length) - 1
        counter_bits_length = uuid7_option.counter_bits_length
        seq_mask = (1 << uuid7_option.counter_bits_length) - 1
        rand_bits = uuid7_option.random_bits_length
        rand_mask = (1 << rand_bits) - 1

        time_fraction = (random_section >> (counter_bits_length + rand_bits)) & time_fraction_mask
        seq = (random_section >> rand_bits) & seq_mask
        rand = random_section & rand_mask

        if uuid7_option.time_fraction_bits_length == 0:
            time_fraction = None
        if uuid7_option.counter_bits_length == 0:
            seq = None
        elif uuid7_option.random_bits_length == 0:
            rand = None

        return time_fraction, seq, rand

    @classmethod
    def _parse_last_uuid(
        cls,
        last_uuid: UUID,
        uuid7_option: UUID7Option,
    ) -> Tuple[int, Optional[int]]:
        parsed = cls.parse(last_uuid, uuid7_option)
        unix_ts_ms: int = parsed["unix_ts_ms"]
        time_fraction, counter, _ = cls._parse_from_random_section(
            rand_a=parsed["rand_a"],
            rand_b=parsed["rand_b"],
            uuid7_option=uuid7_option,
        )

        if time_fraction is not None and uuid7_option.time_fraction_bits_length is not None:
            timestamp = unix_ts_ms * 1_000_000 + time_fraction // (
                1 << uuid7_option.time_fraction_bits_length
            )
        else:
            timestamp = unix_ts_ms

        return (timestamp, counter)


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
