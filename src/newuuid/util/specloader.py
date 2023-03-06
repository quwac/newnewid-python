# noqa: E401
from typing import Literal

Spec = Literal[
    "draft_peabody_dispatch_new_uuid_format_01",
    "draft_peabody_dispatch_new_uuid_format_02",
    "draft_peabody_dispatch_new_uuid_format_03",
    "draft_peabody_dispatch_new_uuid_format_04",
    "draft_ietf_uuidrev_rfc4122bis_00",
    "draft_ietf_uuidrev_rfc4122bis_01",
    "draft_ietf_uuidrev_rfc4122bis_02",
    "latest",
]


def load_modules(spec: Spec = "latest"):
    if spec == "draft_peabody_dispatch_new_uuid_format_01":
        from newuuid.draft_peabody_dispatch_new_uuid_format_01 import (  # noqa: E401
            UUID6Generator,
            UUID7Generator,
            UUID8Generator,
        )
    elif spec == "draft_peabody_dispatch_new_uuid_format_02":
        from newuuid.draft_peabody_dispatch_new_uuid_format_02 import (  # noqa: E401
            UUID6Generator,
            UUID7Generator,
            UUID8Generator,
        )
    elif spec == "draft_peabody_dispatch_new_uuid_format_03":
        from newuuid.draft_peabody_dispatch_new_uuid_format_03 import (  # noqa: E401
            MaxUUIDGenerator,
            UUID6Generator,
            UUID7Generator,
            UUID8Generator,
        )
    elif spec == "draft_peabody_dispatch_new_uuid_format_04":
        from newuuid.draft_peabody_dispatch_new_uuid_format_04 import (  # noqa: E401
            MaxUUIDGenerator,
            UUID6Generator,
            UUID7Generator,
            UUID8Generator,
        )
    elif spec == "draft_ietf_uuidrev_rfc4122bis_00":
        from newuuid.draft_ietf_uuidrev_rfc4122bis_00 import (  # noqa: E401
            MaxUUIDGenerator,
            NilUUIDGenerator,
            UUID6Generator,
            UUID7Generator,
            UUID8Generator,
        )
    elif spec == "draft_ietf_uuidrev_rfc4122bis_01":
        from newuuid.draft_ietf_uuidrev_rfc4122bis_01 import (  # noqa: E401
            MaxUUIDGenerator,
            NilUUIDGenerator,
            UUID6Generator,
            UUID7Generator,
            UUID8Generator,
        )
    elif spec == "draft_ietf_uuidrev_rfc4122bis_02" or spec == "latest":
        from newuuid.draft_ietf_uuidrev_rfc4122bis_02 import (  # noqa: E401
            MaxUUIDGenerator,
            NilUUIDGenerator,
            UUID6Generator,
            UUID7Generator,
            UUID8Generator,
        )
    else:
        raise ValueError(f"Unknown spec: {spec}")
