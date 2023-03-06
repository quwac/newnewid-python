from typing import Any, Dict
from uuid import UUID

from newuuid.uuidgenerator.uuid_generator import UUIDGenerator

_nil_uuid = UUID("00000000-0000-0000-0000-000000000000")


class NilUUIDGenerator(UUIDGenerator):
    def generate(self) -> UUID:
        """Generate Nil UUID."""
        return _nil_uuid

    @classmethod
    def parse(cls, uuid: UUID, **kwargs: Any) -> Dict[str, Any]:
        return {
            "ver": "nil",
        }


_nil_uuid_generator = NilUUIDGenerator()


def nil_uuid() -> UUID:
    return _nil_uuid_generator.generate()
