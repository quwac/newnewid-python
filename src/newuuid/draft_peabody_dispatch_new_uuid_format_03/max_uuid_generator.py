from typing import Any, Dict
from uuid import UUID

from newuuid.uuidgenerator.uuid_generator import UUIDGenerator

_max_uuid = UUID("FFFFFFFF-FFFF-FFFF-FFFF-FFFFFFFFFFFF")


class MaxUUIDGenerator(UUIDGenerator):
    def generate(self) -> UUID:
        """Generate Max UUID."""
        return _max_uuid

    @classmethod
    def parse(cls, uuid: UUID, **kwargs: Any) -> Dict[str, Any]:
        return {
            "ver": "nil",
        }


_max_uuid_generator = MaxUUIDGenerator()


def max_uuid() -> UUID:
    return _max_uuid_generator.generate()
