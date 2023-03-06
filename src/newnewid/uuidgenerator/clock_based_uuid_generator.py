from abc import ABCMeta, abstractmethod
from threading import Lock
from time import sleep
from typing import Optional
from uuid import UUID

from newnewid.clock.uuid_clock import UUIDClock
from newnewid.exception.backward_uuid_exception import BackwardUUIDException
from newnewid.random.pseudo_random_generator import PseudoRandomGenerator
from newnewid.util.nodoc import nodoc
from newnewid.uuidgenerator.uuid_generator import UUIDGenerator


class ClockBasedUUIDGenerator(
    UUIDGenerator,
    metaclass=ABCMeta,
):
    """UUID generator that uses clock."""

    def __init__(
        self,
        raise_exception_on_backward: bool,
        clock: Optional[UUIDClock],
        pseudo_random_generator: Optional[PseudoRandomGenerator],
        last_uuid: Optional[UUID],
    ) -> None:
        """Create ClockBasedUUIDGenerator.

        Args:
            raise_exception_on_backward (bool): Raise exception when backward UUID is generated if True. Otherwise, sleep until next UUID can be generated.
            clock (Optional[UUIDClock]): Clock.
            pseudo_random_generator (Optional[PseudoRandomGenerator]): Pseudo random generator.
            last_uuid (Optional[UUID]): Last generated UUID.
        """
        super().__init__()
        self.raise_exception_on_backward = raise_exception_on_backward
        self._clock = clock or UUIDClock()
        self._pseudo_random_generator = pseudo_random_generator or PseudoRandomGenerator()
        self.last_generated = last_uuid
        self._mask: Optional[int] = None
        self._lock = Lock()

    @abstractmethod
    def timestamp(self, clock: UUIDClock) -> int:
        """Get current timestamp.

        Args:
            clock (UUIDClock): Clock.

        Returns:
            int: Current timestamp.
        """

    @property
    @abstractmethod
    def clock_bits_length(self) -> int:
        """Get clock bits length.

        Returns:
            int: Clock bits length.
        """

    @property
    @abstractmethod
    def least_seconds(self) -> float:
        """Get least seconds in UUID.

        Returns:
            float: Least seconds.
        """

    @nodoc
    def generate(self) -> UUID:
        with self._lock:
            while True:
                if self._mask is None:
                    self._mask = (1 << self.clock_bits_length) - 1

                uuid = self.generate_impl(self.timestamp(self._clock) & self._mask)

                # backward UUID check
                if self.last_generated is not None and uuid <= self.last_generated:
                    if self.raise_exception_on_backward:
                        raise BackwardUUIDException(self.last_generated, uuid)
                    else:
                        sleep(self.least_seconds)
                        continue

                self.last_generated = uuid
                return uuid

    @abstractmethod
    def generate_impl(self, timestamp: int) -> UUID:
        """Generate UUID.

        Args:
            timestamp (int): Current timestamp.

        Returns:
            UUID: UUID.
        """
