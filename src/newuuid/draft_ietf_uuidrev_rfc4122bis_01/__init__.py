from typing import Any, Dict
from uuid import (
    NAMESPACE_DNS,
    NAMESPACE_OID,
    NAMESPACE_URL,
    NAMESPACE_X500,
    RESERVED_FUTURE,
    RESERVED_MICROSOFT,
    RESERVED_NCS,
    RFC_4122,
    UUID,
    SafeUUID,
    getnode,
    uuid1,
    uuid3,
    uuid4,
    uuid5,
)

from newuuid.clock.uuid_clock import UUIDClock
from newuuid.draft_ietf_uuidrev_rfc4122bis_01.max_uuid_generator import (
    MaxUUIDGenerator,
    max_uuid,
)
from newuuid.draft_ietf_uuidrev_rfc4122bis_01.nil_uuid_generator import (
    NilUUIDGenerator,
    nil_uuid,
)
from newuuid.draft_ietf_uuidrev_rfc4122bis_01.uuid6_generator import (
    UUID6Generator,
    uuid6,
)
from newuuid.draft_ietf_uuidrev_rfc4122bis_01.uuid7_generator import (
    UUID7Generator,
    uuid7,
)
from newuuid.draft_ietf_uuidrev_rfc4122bis_01.uuid8_generator import (
    UUID8Generator,
    uuid8,
)
from newuuid.exception.backward_uuid_exception import BackwardUUIDException
from newuuid.parser.uuid_parser import parse as base_parse
from newuuid.random.pseudo_random_generator import PseudoRandomGenerator
from newuuid.sequence.sequencer import Sequencer
from newuuid.util.specloader import UUIDSpec
from newuuid.uuidgenerator.uuid_generator import UUIDGenerator


def parse(
    uuid: UUID, spec: UUIDSpec = "draft_ietf_uuidrev_rfc4122bis_01", **kwargs
) -> Dict[str, Any]:
    return base_parse(uuid, spec, **kwargs)


__all__ = [
    # Compatibility
    "NAMESPACE_DNS",
    "NAMESPACE_OID",
    "NAMESPACE_URL",
    "NAMESPACE_X500",
    "RESERVED_FUTURE",
    "RESERVED_MICROSOFT",
    "RESERVED_NCS",
    "RFC_4122",
    "UUID",
    "SafeUUID",
    "getnode",
    "uuid1",
    "uuid3",
    "uuid4",
    "uuid5",
    # New UUID
    "UUIDGenerator",
    "max_uuid",
    "MaxUUIDGenerator",
    "nil_uuid",
    "NilUUIDGenerator",
    "uuid6",
    "UUID6Generator",
    "uuid7",
    "UUID7Generator",
    "uuid8",
    "UUID8Generator",
    "parse",
    "BackwardUUIDException",
    "PseudoRandomGenerator",
    "Sequencer",
    "UUIDClock",
    "UUIDSpec",
]
