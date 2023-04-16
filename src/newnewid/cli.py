import argparse
import json
import sys
from typing import List

from newnewid import (
    METHOD_0_NO_COUNTER,
    METHOD_1_FIXED_LENGTH_DEDICATED_COUNTER_BITS_12,
    METHOD_1_FIXED_LENGTH_DEDICATED_COUNTER_BITS_26,
    METHOD_1_FIXED_LENGTH_DEDICATED_COUNTER_BITS_42,
    METHOD_2_MONOTONIC_RANDOM_62_BITS,
    UUID,
    UUID7Option,
    UUIDGenerator,
    max_uuid,
    nil_uuid,
    uuid1,
    uuid3,
    uuid4,
    uuid5,
    uuid6,
    uuid7,
    uuid8,
)
from newnewid.parser.uuid_parser import parse


def _get_uuid7_option(method: str) -> UUID7Option:
    if method == "METHOD-0":
        return METHOD_0_NO_COUNTER
    elif method == "METHOD-1-12":
        return METHOD_1_FIXED_LENGTH_DEDICATED_COUNTER_BITS_12
    elif method == "METHOD-1-26":
        return METHOD_1_FIXED_LENGTH_DEDICATED_COUNTER_BITS_26
    elif method == "METHOD-42":
        return METHOD_1_FIXED_LENGTH_DEDICATED_COUNTER_BITS_42
    elif method == "METHOD-2":
        return METHOD_2_MONOTONIC_RANDOM_62_BITS
    else:
        raise ValueError(f"Invalid method: {method}")


def generate_uuid(args):
    """Generate UUID."""
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
        uuid7_option = _get_uuid7_option(args.method)

        def uuid7_wrapper():
            return uuid7(uuid7_option)

        uuid_module = uuid7_wrapper
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
        print("Invalid version.")
        sys.exit(1)

    for _ in range(args.n):
        print(uuid_module())


def parse_uuid(args):
    """Parse UUID."""
    uuid_strs: List[str] = args.uuid

    for uuid_str in uuid_strs:
        uuid = UUID(uuid_str)
        version = UUIDGenerator.get_version(uuid)
        if version == "7":
            uuid7_option = _get_uuid7_option(args.method)
            parsed = parse(uuid, uuid7_option=uuid7_option)
        else:
            parsed = parse(uuid)
        obj = {**{"uuid": uuid_str}, **parsed}
        print(json.dumps(obj))


def cli():
    """CLI."""
    parser = argparse.ArgumentParser(description="NewNewID")

    subparsers = parser.add_subparsers(required=True)
    gen_parser = subparsers.add_parser("generate", help="Generate UUID.")

    gen_parser.add_argument(
        "n",
        type=int,
        nargs="?",
        help="Number of UUIDs to generate. example: 10",
        default=1,
    )
    gen_parser.add_argument(
        "-u",
        "--uuid-version",
        type=str,
        help="Version of UUID. 1, 3, 4, 5, 6, 7, 8, nil or max",
        required=True,
    )
    gen_parser.add_argument(
        "--namespace",
        type=str,
        nargs="?",
        help="Namespace for UUIDv3 or UUIDv5. example: '0186b748-053d-7c24-be59-de03734bb9ab'",
        default=None,
    )
    gen_parser.add_argument(
        "--name",
        type=str,
        nargs="?",
        help="Name for UUIDv3 or UUIDv5. example: 'name'",
        default=None,
    )
    gen_parser.add_argument(
        "-m",
        "--method",
        nargs="?",
        type=str,
        help="Method for UUIDv7. 'METHOD-0', 'METHOD-1-12', 'METHOD-1-26', 'METHOD-1-42' or 'METHOD-2'. Default: 'METHOD-1-12'",
        default="METHOD-1-12",
    )
    gen_parser.add_argument(
        "--custom-a",
        type=int,
        nargs="?",
        help="cuatom-a binary for UUIDv8.",
        default=None,
    )
    gen_parser.add_argument(
        "--custom-b",
        type=int,
        nargs="?",
        help="cuatom-b binary for UUIDv8.",
        default=None,
    )
    gen_parser.add_argument(
        "--custom-c",
        type=int,
        nargs="?",
        help="cuatom-c binary for UUIDv8.",
        default=None,
    )

    def generate_uuid_wrapper(args):
        try:
            generate_uuid(args)
        except Exception:
            gen_parser.print_help()

    gen_parser.set_defaults(func=generate_uuid_wrapper)

    parse_parser = subparsers.add_parser("parse", help="Parse UUID.")
    parse_parser.add_argument("uuid", nargs="+", type=str, help="UUID")
    parse_parser.add_argument(
        "-m",
        "--method",
        nargs="?",
        type=str,
        help="Method for UUIDv7. 'METHOD-0', 'METHOD-1-12', 'METHOD-1-26', 'METHOD-1-42' or 'METHOD-2'. Default: 'METHOD-1-12'",
        default="METHOD-1-12",
    )

    def parse_uuid_wrapper(args):
        try:
            parse_uuid(args)
        except Exception:
            parse_parser.print_help()

    parse_parser.set_defaults(func=parse_uuid_wrapper)

    try:
        args = parser.parse_args()
        args.func(args)
    except Exception:
        parser.print_help()
