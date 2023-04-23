import uuid
from abc import ABCMeta, abstractmethod
from typing import Optional
from uuid import UUID

from newnewid.clock.uuid_clock import UUIDClock
from newnewid.counter.counter import Counter
from newnewid.random.pseudo_random_binary_generator import PseudoRandomBinaryGenerator
from newnewid.random.pseudo_random_generator import PseudoRandomGenerator
from newnewid.util.nodoc import nodoc
from newnewid.uuidgenerator.clock_based_uuid_generator import ClockBasedUUIDGenerator


class MacAddressGenerator(PseudoRandomBinaryGenerator):
    """MAC address generator."""

    def __init__(self) -> None:
        super().__init__(48, PseudoRandomGenerator())

    @nodoc
    def generate(self) -> int:
        return uuid.getnode()


class GregorianBasedUUIDGenerator(ClockBasedUUIDGenerator, metaclass=ABCMeta):
    """UUID generator that uses Gregorian calendar."""

    def __init__(
        self,
        uses_mac_address: bool,
        raise_exception_on_backward: bool = False,
        clock: Optional[UUIDClock] = None,
        pseudo_random_generator: Optional[PseudoRandomGenerator] = None,
        last_uuid: Optional[UUID] = None,
    ) -> None:
        """Create GregorianBasedUUIDGenerator.

        Args:
            uses_mac_address (bool): Uses MAC address if True. Otherwise, uses pseudo random generator.
            raise_exception_on_backward (bool, optional): Raise exception when backward UUID is generated if True. Otherwise, sleep until next UUID can be generated. Defaults to False.
            clock (Optional[UUIDClock], optional): Clock. Defaults to None.
            pseudo_random_generator (Optional[PseudoRandomGenerator], optional): Pseudo random generator. Defaults to None.
            last_uuid (Optional[UUID], optional): Last generated UUID. Defaults to None.
        """
        super().__init__(raise_exception_on_backward, clock, pseudo_random_generator, last_uuid)

        last_timestamp: Optional[int] = None
        last_counter: Optional[int] = None
        if last_uuid:
            assert last_uuid.version == 6, f"last_uuid must be version 6, not {last_uuid.version}"
            parsed = self.__class__.parse(last_uuid)
            (time_high, time_mid, time_low) = (
                parsed["time_high"],
                parsed["time_mid"],
                parsed["time_low"],
            )

            last_timestamp = time_high << 20 | time_mid << 4 | time_low
            last_counter = parsed["clock_seq"]

        self._counter = Counter(
            counter_bits_length=14,
            max_increment_bits_length=1,
            pseudo_random_generator=self._pseudo_random_generator,
            initial_timestamp=last_timestamp,
            initial_counter=last_counter,
        )
        if uses_mac_address:
            self._pseudo_random_binary_generator = MacAddressGenerator()
        else:
            self._pseudo_random_binary_generator = PseudoRandomBinaryGenerator(
                48, self._pseudo_random_generator
            )

    @nodoc
    def timestamp(self, clock: UUIDClock) -> int:
        return clock.gregorian_100_nano_seconds()

    @property
    @nodoc
    def clock_bits_length(self) -> int:
        return 60

    @nodoc
    @property
    def least_seconds(self) -> float:
        return 0.000_000_1

    @nodoc
    def generate_impl(self, timestamp: int) -> UUID:
        # timestamp is 60 bits

        # 4 bits
        ver = 6

        # 2 bits
        var = 0b10

        # 14 bits
        clock_seq = self._counter.get_next(timestamp)

        # 48 bits
        node = self._pseudo_random_binary_generator.generate()

        return self.build(timestamp, ver, var, clock_seq, node)

    @abstractmethod
    def build(
        self,
        time: int,
        ver: int,
        var: int,
        clock_seq: int,
        node: int,
    ) -> UUID:
        """Build UUID.

        Args:
            time (int): Timestamp.
            ver (int): Version
            var (int): Variant
            clock_seq (int): Clock sequence (Counter).
            node (int): Node.

        Returns:
            UUID: UUID.
        """
