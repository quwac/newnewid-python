import argparse
import json
import sys
from argparse import RawTextHelpFormatter
from typing import List

from newnewid import (
    METHOD_0_NO_COUNTER,
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

_DEBUG = False

_HELP_METHOD = """Method for UUIDv7.

* 'METHOD-0' Method 0: No counter
* 'METHOD-1-12' Method 1: Fixed length, dedicated counter bits (counter bits length: 12)
* 'METHOD-1-26' Method 1: Fixed length, dedicated counter bits (counter bits length: 26)
* 'METHOD-1-42' Method 1: Fixed length, dedicated counter bits (counter bits length: 42)
* 'METHOD-1-xx' Method 1: Fixed length, dedicated counter bits (counter bits length: xx)
* 'METHOD-2' Method 2: Monotonic random (max increment bits length: 62)
* 'METHOD-2-xx' Method 2: Monotonic random (max increment bits length: xx)
* 'METHOD-3' Method 3: Re-randomize until monotonic (max increment bits length: 62)
* 'METHOD-3-xx' Method 3: Re-randomize until monotonic (max increment bits length: xx)
* 'METHOD-4-WITHOUT-COUNTER' Method 4: Replace left most random bits with increased clock precision (time fraction bits length: 12, counter bits length: 0)
* 'METHOD-4-WITH-COUNTER' Method 4: Replace left most random bits with increased clock precision (time fraction bits length: 12, counter bits length: 14)
* 'METHOD-4-xx-yy' Method 4: Replace left most random bits with increased clock precision (time fraction bits length: xx, counter bits length: yy)

Default: 'METHOD-1-12'
"""


class _AppException(Exception):
    pass


def _get_uuid7_option(method: str) -> UUID7Option:
    method = method.upper()

    try:
        if method == "METHOD-0":
            return METHOD_0_NO_COUNTER
        elif method.startswith("METHOD-1"):
            bits_str = method.replace("METHOD-1", "")
            if bits_str == "":
                bits = 12
            else:
                bits = int(bits_str.replace("-", ""))
            return UUID7Option.method_1_fixed_length_dedicated_counter_bits(bits)
        elif method.startswith("METHOD-2"):
            bits_str = method.replace("METHOD-2", "")
            if bits_str == "":
                max_increment_bits_length = 62
            else:
                max_increment_bits_length = int(bits_str.replace("-", ""))
            return UUID7Option.method_2_monotonic_random(max_increment_bits_length)
        elif method.startswith("METHOD-3"):
            bits_str = method.replace("METHOD-3", "")
            if bits_str == "":
                max_increment_bits_length = 62
            else:
                max_increment_bits_length = int(bits_str.replace("-", ""))
            return UUID7Option.method_3_rerandomize_until_monotonic()
        elif method.startswith("METHOD-4"):
            if method == "METHOD-4-WITHOUT-COUNTER":
                time_fraction_bits_length = 12
                counter_bits_length = 0
            elif method == "METHOD-4-WITH-COUNTER":
                time_fraction_bits_length = 12
                counter_bits_length = 14
            else:
                bits_str = method.replace("METHOD-4-", "")
                time_fraction_bits_length, counter_bits_length = map(
                    lambda x: int(x), bits_str.split("-")
                )

            return (
                UUID7Option.method_4_replace_left_most_random_bits_with_increased_clock_precision(
                    time_fraction_bits_length=time_fraction_bits_length,
                    counter_bits_length=counter_bits_length,
                )
            )
        else:
            raise ValueError(f"Invalid method: {method}")
    except Exception as e:
        raise ValueError(f"-m/--method parse failed: {method}") from e


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
        try:
            print(uuid_module())
        except Exception as e:
            raise _AppException from e


def parse_uuid(args):
    """Parse UUID."""
    uuid_strs: List[str] = args.uuid

    for uuid_str in uuid_strs:
        uuid = UUID(uuid_str)
        version = UUIDGenerator.get_version(uuid)
        try:
            if version == "7":
                uuid7_option = _get_uuid7_option(args.method)
                parsed = parse(uuid, uuid7_option=uuid7_option)
            else:
                parsed = parse(uuid)
            obj = {**{"uuid": uuid_str}, **parsed}
            print(json.dumps(obj))
        except Exception as e:
            raise _AppException from e


def cli():
    """CLI."""
    parser = argparse.ArgumentParser(description="NewNewID", formatter_class=RawTextHelpFormatter)

    subparsers = parser.add_subparsers(required=True)
    gen_parser = subparsers.add_parser(
        "generate",
        help="Generate UUID.",
        formatter_class=RawTextHelpFormatter,
    )

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
        help=_HELP_METHOD,
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
        except _AppException as e:
            raise e
        except Exception as e:
            if _DEBUG:
                raise e
            gen_parser.print_help()

    gen_parser.set_defaults(func=generate_uuid_wrapper)

    parse_parser = subparsers.add_parser(
        "parse",
        help="Parse UUID.",
        formatter_class=RawTextHelpFormatter,
    )
    parse_parser.add_argument("uuid", nargs="+", type=str, help="UUID")
    parse_parser.add_argument(
        "-m",
        "--method",
        nargs="?",
        type=str,
        help=_HELP_METHOD,
        default="METHOD-1-12",
    )

    def parse_uuid_wrapper(args):
        try:
            parse_uuid(args)
        except _AppException as e:
            raise e
        except Exception as e:
            if _DEBUG:
                raise e
            parse_parser.print_help()

    parse_parser.set_defaults(func=parse_uuid_wrapper)

    try:
        args = parser.parse_args()
        args.func(args)
    except _AppException as e:
        raise e
    except Exception as e:
        if _DEBUG:
            raise e
        parser.print_help()
