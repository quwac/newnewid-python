from typing import Any, Dict
from uuid import UUID

from newnewid.util.nodoc import nodoc
from newnewid.uuidgenerator.uuid_generator import UUIDGenerator

_nil_uuid = UUID("00000000-0000-0000-0000-000000000000")


class NilUUIDGenerator(UUIDGenerator):
    """Nil UUID generator."""

    def generate(self) -> UUID:
        """Generate Nil UUID."""
        return _nil_uuid

    @classmethod
    @nodoc
    def parse(cls, uuid: UUID, **kwargs: Any) -> Dict[str, Any]:
        return {
            "ver": "nil",
        }


_nil_uuid_generator = NilUUIDGenerator()


def nil_uuid() -> UUID:
    """Generate Nil UUID.

    Returns:
        UUID: Nil UUID.
    """
    return _nil_uuid_generator.generate()
