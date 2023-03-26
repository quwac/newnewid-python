from typing import Any, Dict
from uuid import UUID

from newuuid.clock.uuid_clock import UUIDClock
from newuuid.draft_peabody_dispatch_new_uuid_format_03 import (
    MaxUUIDGenerator,
    UUID6Generator,
    UUID7Generator,
    UUID8Generator,
    max_uuid,
    uuid6,
    uuid7,
    uuid8,
)
from newuuid.exception.backward_uuid_exception import BackwardUUIDException
from newuuid.parser.uuid_parser import parse as base_parse
from newuuid.random.pseudo_random_generator import PseudoRandomGenerator
from newuuid.sequence.sequencer import Sequencer
from newuuid.util.specloader import UUIDSpec


def parse(
    uuid: UUID, spec: UUIDSpec = "draft_peabody_dispatch_new_uuid_format_03", **kwargs
) -> Dict[str, Any]:
    return base_parse(uuid, spec, **kwargs)


__all__ = [
    "max_uuid",
    "MaxUUIDGenerator",
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
