import argparse
import json
from typing import List, Optional

from newuuid import (
    UUID,
    UUID7Generator,
    UUIDGenerator,
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


class Color:
    YELLOW = "\033[33m"
    END = "\033[0m"


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
        "--sequence-bits",
        type=int,
        nargs="?",
        help="sequence-bits for UUIDv7. Default 12",
        default=12,
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

        seq_bits: int = args.sequence_bits

        def uuid7_wrapper():
            return uuid7(seq_bits)

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
        raise ValueError("Invalid version")

    for _ in range(args.n):
        print(uuid_module())


def parse_uuid():
    parser = argparse.ArgumentParser(description="Parse UUID")
    parser.add_argument("uuid", nargs="+", type=str, help="UUID")
    parser.add_argument(
        "--seq-bits", nargs="?", type=int, help="Sequence bits for UUIDv7", default=None
    )

    args = parser.parse_args()

    # --------------------------------------------------------------------------------

    uuid_strs: List[str] = args.uuid
    seq_bits: Optional[int] = args.seq_bits

    for uuid_str in uuid_strs:
        uuid = UUID(uuid_str)
        version = UUIDGenerator.get_version(uuid)
        if version == "7":
            if seq_bits is None:
                print(
                    Color.YELLOW
                    + f"[CAUTION] UUIDv7 has 0 - 72 bits of flexibility in the sequence binary length. The default sequence binary length for UUIDv7 created by this library is ${UUID7Generator.DEFAULT_SEQ_BITS} bits, but the sequence binary length for this UUIDv7 may be different. It is recommended to add the seq_bits option to the argument to specify the length explicitly. "
                    + Color.END
                )
                seq_bits = UUID7Generator.DEFAULT_SEQ_BITS
            parsed = parse(uuid, seq_bits=seq_bits)
        else:
            parsed = parse(uuid)
        obj = {**{"uuid": uuid_str}, **parsed}
        print(json.dumps(obj))
