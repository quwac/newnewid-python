from typing import Any, Dict
from uuid import UUID

from newuuid.util.specloader import UUIDSpec, load_modules


def parse(uuid: UUID, spec: UUIDSpec = "latest", **kwargs) -> Dict[str, Any]:
    uuid_int = uuid.int
    version = int((uuid_int >> 76) & 0xF)

    load_modules(spec)

    try:
        if uuid_int == 0:
            generator_class = NilUUIDGenerator  # type: ignore # noqa: F821
        elif uuid_int == 0xFFFF_FFFF_FFFF_FFFF_FFFF_FFFF_FFFF_FFFF:
            generator_class = MaxUUIDGenerator  # type: ignore # noqa: F821
        elif version == 6:
            generator_class = UUID6Generator  # type: ignore # noqa: F821
        elif version == 7:
            generator_class = UUID7Generator  # type: ignore # noqa: F821
        elif version == 8:
            generator_class = UUID8Generator  # type: ignore # noqa: F821
        else:
            raise ValueError(f"Unsupported version: {version}")
    except UnboundLocalError:
        raise ValueError(f"Max UUID not supported in spec: {spec}")

    generator_class.parse(uuid, **kwargs)

    raise ValueError(f"Unsupported version: {version}")
