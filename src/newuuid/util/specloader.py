# noqa: E401
import importlib
from typing import Literal

UUIDSpec = Literal[
    "draft_peabody_dispatch_new_uuid_format_01",
    "draft_peabody_dispatch_new_uuid_format_02",
    "draft_peabody_dispatch_new_uuid_format_03",
    "draft_peabody_dispatch_new_uuid_format_04",
    "draft_ietf_uuidrev_rfc4122bis_00",
    "draft_ietf_uuidrev_rfc4122bis_01",
    "draft_ietf_uuidrev_rfc4122bis_02",
    "latest",
]


def load_modules(spec: UUIDSpec = "latest"):
    if spec == "draft_peabody_dispatch_new_uuid_format_01":
        module = importlib.import_module("newuuid.draft_peabody_dispatch_new_uuid_format_01")
    elif spec == "draft_peabody_dispatch_new_uuid_format_02":
        module = importlib.import_module("newuuid.draft_peabody_dispatch_new_uuid_format_02")
    elif spec == "draft_peabody_dispatch_new_uuid_format_03":
        module = importlib.import_module("newuuid.draft_peabody_dispatch_new_uuid_format_03")
    elif spec == "draft_peabody_dispatch_new_uuid_format_04":
        module = importlib.import_module("newuuid.draft_peabody_dispatch_new_uuid_format_04")
    elif spec == "draft_ietf_uuidrev_rfc4122bis_00":
        module = importlib.import_module("newuuid.draft_ietf_uuidrev_rfc4122bis_00")
    elif spec == "draft_ietf_uuidrev_rfc4122bis_01":
        module = importlib.import_module("newuuid.draft_ietf_uuidrev_rfc4122bis_01")
    elif spec == "draft_ietf_uuidrev_rfc4122bis_02" or spec == "latest":
        module = importlib.import_module("newuuid.draft_ietf_uuidrev_rfc4122bis_02")
    else:
        raise ValueError(f"Unknown spec: {spec}")

    return module
