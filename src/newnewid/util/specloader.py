# noqa: E401
import importlib

_SPECS = (
    "draft_peabody_dispatch_new_uuid_format_01",
    "draft_peabody_dispatch_new_uuid_format_02",
    "draft_peabody_dispatch_new_uuid_format_03",
    "draft_peabody_dispatch_new_uuid_format_04",
    "draft_ietf_uuidrev_rfc4122bis_00",
    "draft_ietf_uuidrev_rfc4122bis_01",
    "draft_ietf_uuidrev_rfc4122bis_02",
    "draft_ietf_uuidrev_rfc4122bis_03",
)


def load_modules(spec: str = "latest"):
    """Load modules for the given spec.

    Args:
        spec (str, optional): Specification to load. Defaults to "latest".
    """
    if spec in _SPECS:
        module = importlib.import_module(f"newnewid.{spec}")
    elif "latest":
        module = importlib.import_module(f"newnewid.{_SPECS[-1]}")
    else:
        raise ValueError(f"Unknown spec: {spec}")

    return module
