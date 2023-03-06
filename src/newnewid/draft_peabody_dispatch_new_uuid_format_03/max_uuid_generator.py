from typing import Any, Dict
from uuid import UUID

from newnewid.util.nodoc import nodoc
from newnewid.uuidgenerator.uuid_generator import UUIDGenerator

_max_uuid = UUID("FFFFFFFF-FFFF-FFFF-FFFF-FFFFFFFFFFFF")


class MaxUUIDGenerator(UUIDGenerator):
    """Max UUID generator."""

    def generate(self) -> UUID:
        """Generate Max UUID."""
        return _max_uuid

    @classmethod
    @nodoc
    def parse(cls, uuid: UUID, **kwargs: Any) -> Dict[str, Any]:
        return {
            "ver": "max",
        }


_max_uuid_generator = MaxUUIDGenerator()


def max_uuid() -> UUID:
    """Generate Max UUID.

    Returns:
        UUID: Max UUID.
    """
    return _max_uuid_generator.generate()
