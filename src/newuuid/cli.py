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
    uuid8,
)


def generate_uuid():
    parser = argparse.ArgumentParser(description="Generate UUID")
    parser.add_argument(
        "n", type=int, nargs="?", help="Number of UUIDs to generate. example: 10", default=7
    )
    parser.add_argument(
        "-u",
        "--uuid-version",
        type=str,
        nargs="?",
        help="Version of UUID. 1, 3, 4, 5, 6, 7, 8, nil or max",
        default="7",
    )
    parser.add_argument(
        "--namespace",
        type=str,
        nargs="?",
        help="Namespace for UUIDv3 or UUIDv5. example: '0186b748-053d-7c24-be59-de03734bb9ab'",
        default=None,
    )
    parser.add_argument(
        "--name",
        type=str,
        nargs="?",
        help="Name for UUIDv3 or UUIDv5. example: 'name'",
        default=None,
    )
    parser.add_argument(
        "--custom-a",
        type=int,
        nargs="?",
        help="cuatom-a binary for UUIDv8.",
        default=None,
    )
    parser.add_argument(
        "--custom-b",
        type=int,
        nargs="?",
        help="cuatom-b binary for UUIDv8.",
        default=None,
    )
    parser.add_argument(
        "--custom-c",
        type=int,
        nargs="?",
        help="cuatom-c binary for UUIDv8.",
        default=None,
    )
    args = parser.parse_args()

    # --------------------------------------------------------------------------------

    print(f"args: {args}")
    uuid_version = args.uuid_version

    if uuid_version == "1":

        def uuid1_wrapper():
            return uuid1()

        uuid_module = uuid1_wrapper
    elif uuid_version == "3":

        namespace = args.namespace
        name = args.name
        if namespace is None or name is None:
            raise ValueError("namespace and name are required for UUIDv3")

        def uuid3_wrapper():
            return uuid3(UUID(namespace), name)

        uuid_module = uuid3_wrapper
    elif uuid_version == "4":
        uuid_module = uuid4
    elif uuid_version == "5":

        namespace = args.namespace
        name = args.name
        if namespace is None or name is None:
            raise ValueError("namespace and name are required for UUIDv5")

        def uuid5_wrapper():
            return uuid5(UUID(namespace), name)

        uuid_module = uuid5_wrapper
    elif uuid_version == "6":
        uuid_module = uuid6
    elif uuid_version == "7":
        uuid_module = uuid7
    elif uuid_version == "8":

        if args.custom_a is None or args.custom_b is None or args.custom_c is None:
            raise ValueError("custom-a, custom-b and custom-c are required for UUIDv8")

        def uuid8_wrapper():
            return uuid8(args.custom_a, args.custom_b, args.custom_c)

        uuid_module = uuid8_wrapper
    elif uuid_version == "nil":
        uuid_module = nil_uuid
    elif uuid_version == "max":
        uuid_module = max_uuid
    else:
        raise ValueError("Invalid version")

    for _ in range(args.n):
        print(uuid_module())


def parse_uuid():
    parser = argparse.ArgumentParser(description="Parse UUID")
    parser.add_argument("uuid", nargs="+", type=str, help="UUID")

    args = parser.parse_args()

    # --------------------------------------------------------------------------------

    uuids: List[str] = args.uuid

    for uuid in uuids:
        obj = {**{"uuid": uuid}, **parse(UUID(uuid))}
        print(obj)
