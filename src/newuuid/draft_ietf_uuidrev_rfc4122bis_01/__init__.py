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

from .max_uuid_generator import MaxUUIDGenerator, max_uuid
from .nil_uuid_generator import NilUUIDGenerator, nil_uuid
from .uuid6_generator import UUID6Generator, uuid6
from .uuid7_generator import UUID7Generator, uuid7
from .uuid8_generator import UUID8Generator, uuid8

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
]
