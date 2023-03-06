from abc import ABCMeta, abstractmethod
from typing import Any, Dict
from uuid import UUID


class UUIDGenerator(metaclass=ABCMeta):
    """UUID generator."""

    @abstractmethod
    def generate(self) -> UUID:
        """Generate UUID.

        Returns:
            UUID: UUID.
        """

    @classmethod
    @abstractmethod
    def parse(cls, uuid: UUID, **args: Any) -> Dict[str, Any]:
        """Parse UUID.

        Args:
            uuid (UUID): UUID

        Returns:
            Dict[str, Any]: Parsed UUID.
        """

    @classmethod
    def get_version(cls, uuid: UUID) -> str:
        """Get version of UUID.

        Args:
            uuid (UUID): UUID

        Returns:
            str: Version of UUID.
        """
        uuid_int = uuid.int
        version = int((uuid_int >> 76) & 0xF)
        if version == 0:
            return "nil"
        elif version == 0b1111:
            return "max"
        else:
            return str(version)
