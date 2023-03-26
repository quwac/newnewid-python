from abc import ABCMeta, abstractmethod
from threading import Lock
from time import sleep
from typing import Any, Dict, Optional
from uuid import UUID

from newuuid.clock.uuid_clock import UUIDClock
from newuuid.exception.backward_uuid_exception import BackwardUUIDException


class UUIDGenerator(metaclass=ABCMeta):
    @abstractmethod
    def generate(self) -> UUID:
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    def parse(cls, uuid: UUID, **args: Any) -> Dict[str, Any]:
        raise NotImplementedError()

    @classmethod
    def get_version(cls, uuid: UUID) -> str:
        uuid_int = uuid.int
        version = int((uuid_int >> 76) & 0xF)
        if version == 0:
            return "nil"
        elif version == 0b1111:
            return "max"
        else:
            return str(version)


class ClockBasedUUIDGenerator(
    UUIDGenerator,
    metaclass=ABCMeta,
):
    def __init__(
        self,
        raise_exception_on_backward: bool = False,
        clock: Optional[UUIDClock] = None,
        last_uuid: Optional[UUID] = None,
    ) -> None:
        super().__init__()
        self.raise_exception_on_backward = raise_exception_on_backward
        self._clock = clock or UUIDClock()
        self._last_uuid = last_uuid
        self._mask: Optional[int] = None
        self._lock = Lock()

    @abstractmethod
    def timestamp(self, clock: UUIDClock) -> int:
        raise NotImplementedError()

    @property
    @abstractmethod
    def clock_bits(self) -> int:
        raise NotImplementedError()

    @property
    @abstractmethod
    def least_seconds(self) -> float:
        raise NotImplementedError()

    def generate(self) -> UUID:
        with self._lock:
            if self._mask is None:
                self._mask = (1 << self.clock_bits) - 1

            uuid = self.generate_impl(self.timestamp(self._clock) & self._mask)

            # backward UUID check
            if self._last_uuid is not None and uuid <= self._last_uuid:
                if self.raise_exception_on_backward:
                    raise BackwardUUIDException(self._last_uuid, uuid)
                else:
                    sleep(self.least_seconds)
                    return self.generate()

            self._last_uuid = uuid
            return uuid

    @abstractmethod
    def generate_impl(self, timestamp: int) -> UUID:
        raise NotImplementedError()
