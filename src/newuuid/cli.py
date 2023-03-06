import argparse
from typing import List

from newuuid import (
    UUID,
    max_uuid,
    nil_uuid,
    parse,
    uuid1,
    uuid3,
    uuid4,
    uuid5,
    uuid6,
    uuid7,
)


def generate():
    parser = argparse.ArgumentParser(description="Generate UUID")
    parser.add_argument(
        "n", type=int, nargs="?", help="Number of UUIDs to generate. example: 10", default=1
    )
    parser.add_argument(
        "u", type=str, nargs="?", help="Version of UUID. 1, 3, 4, 5, 6, 7, nil or max", default="7"
    )
    parser.add_argument(
        "namespace",
        type=str,
        nargs="?",
        help="Namespace for UUIDv3 or UUIDv5. example: '0186b748-053d-7c24-be59-de03734bb9ab'",
    )
    parser.add_argument(
        "name",
        type=str,
        nargs="?",
        help="Name for UUIDv3 or UUIDv5. example: 'name'",
        default="name",
    )
    args = parser.parse_args()

    # --------------------------------------------------------------------------------

    uuid_version = args.u

    if uuid_version == "1":

        def uuid1_wrapper():
            return uuid1()

        uuid_module = uuid1_wrapper
    elif uuid_version == "3":

        def uuid3_wrapper():
            return uuid3(UUID(args.u), args.a)

        uuid_module = uuid3_wrapper
    elif uuid_version == "4":
        uuid_module = uuid4
    elif uuid_version == "5":

        def uuid5_wrapper():
            return uuid5(UUID(args.u), args.a)

        uuid_module = uuid5_wrapper
    elif uuid_version == "6":
        uuid_module = uuid6
    elif uuid_version == "7":
        uuid_module = uuid7
    elif uuid_version == "nil":
        uuid_module = nil_uuid
    elif uuid_version == "max":
        uuid_module = max_uuid
    else:
        raise ValueError("Invalid version")

    for i in range(args.n):
        print(uuid_module())


def parse_uuid():
    parser = argparse.ArgumentParser(description="Parse UUID")
    parser.add_argument("uuid", nargs="+", type=str, help="UUID")

    args = parser.parse_args()

    # --------------------------------------------------------------------------------

    uuids: List[str] = args.uuid

    for uuid in uuids:
        print(parse(UUID(uuid)))
