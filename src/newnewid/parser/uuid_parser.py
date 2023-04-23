from typing import Any, Dict
from uuid import UUID

from newnewid.clock.uuid_clock import UUIDClock
from newnewid.util.specloader import load_modules
from newnewid.uuidgenerator.uuid_generator import UUIDGenerator


class _OtherUUIDParser:
    @classmethod
    def parse_uuid1(cls, uuid: UUID, **kwargs: Any) -> Dict[str, Any]:
        """Parse UUIDv1."""
        #     0                   1                   2                   3
        #     0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
        #    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        #    |                           time_low                            |
        #    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        #    |           time_mid            |  ver  |       time_high       |
        #    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        #    |var|         clock_seq         |             node              |
        #    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        #    |                              node                             |
        #    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

        # 32 bits
        time_low = (uuid.int >> 96) & 0xFFFF_FFFF
        # 16 bits
        time_mid = (uuid.int >> 80) & 0xFFFF
        # 4 bits
        ver = (uuid.int >> 76) & 0xF
        # 12 bits
        time_high = (uuid.int >> 64) & 0xFFF
        # 2 bits
        var = (uuid.int >> 62) & 0x3
        # 14 bits
        clock_seq = (uuid.int >> 48) & 0x3FFF
        # 48 bits
        node = uuid.int & 0xFFFF_FFFF_FFFF

        gregorian_100_nano_seconds = (time_high << 48) | (time_mid << 32) | time_low
        time, epoch_nano_fraction = UUIDClock.to_datetime_from_gregorian_100_nano_seconds(
            gregorian_100_nano_seconds
        )

        return {
            "time_low": time_low,
            "time_mid": time_mid,
            "ver": str(ver),
            "time_high": time_high,
            "var": var,
            "clock_seq": clock_seq,
            "node": node,
            "gregorian_100_nano_seconds": gregorian_100_nano_seconds,
            "time": time.isoformat(),
            "epoch_nano_fraction": epoch_nano_fraction,
        }

    @classmethod
    def parse_uuid3(cls, uuid: UUID, **kwargs: Any) -> Dict[str, Any]:
        """Parse UUIDv3."""
        #     0                   1                   2                   3
        #     0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
        #    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        #    |                            md5_high                           |
        #    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        #    |          md5_high             |  ver  |       md5_mid         |
        #    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        #    |var|                        md5_low                            |
        #    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        #    |                            md5_low                            |
        #    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        # 48 bits
        md5_high = (uuid.int >> 80) & 0xFFFF_FFFF_FFFF
        # 4 bits
        ver = (uuid.int >> 76) & 0xF
        # 12 bits
        md5_mid = (uuid.int >> 64) & 0xFFF
        # 2 bits
        var = (uuid.int >> 62) & 0x3
        # 62 bits
        md5_low = uuid.int & 0x3FFF_FFFF_FFFF_FFFF

        md5 = (md5_high << 64) | (md5_mid << 48) | md5_low

        return {
            "md5_high": md5_high,
            "ver": str(ver),
            "md5_mid": md5_mid,
            "var": var,
            "md5_low": md5_low,
            "md5": md5,
        }

    @classmethod
    def parse_uuid4(cls, uuid: UUID, **kwargs: Any) -> Dict[str, Any]:
        """Parse UUIDv4."""
        #     0                   1                   2                   3
        #     0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
        #    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        #    |                           random_a                            |
        #    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        #    |          random_a             |  ver  |       random_b        |
        #    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        #    |var|                       random_c                            |
        #    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        #    |                           random_c                            |
        #    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        # 48 bits
        random_a = (uuid.int >> 80) & 0xFFFF_FFFF_FFFF
        # 4 bits
        ver = (uuid.int >> 76) & 0xF
        # 12 bits
        random_b = (uuid.int >> 64) & 0xFFF
        # 2 bits
        var = (uuid.int >> 62) & 0x3
        # 62 bits
        random_c = uuid.int & 0x3FFF_FFFF_FFFF_FFFF

        return {
            "random_a": random_a,
            "ver": str(ver),
            "random_b": random_b,
            "var": var,
            "random_c": random_c,
        }

    @classmethod
    def parse_uuid5(cls, uuid: UUID, **kwargs: Any) -> Dict[str, Any]:
        """Parse UUIDv5."""
        #     0                   1                   2                   3
        #     0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
        #    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        #    |                           sha1_high                           |
        #    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        #    |         sha1_high             |  ver  |      sha1_mid         |
        #    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        #    |var|                       sha1_low                            |
        #    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        #    |                           sha1_low                            |
        #    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        # 48 bits
        sha1_high = (uuid.int >> 80) & 0xFFFF_FFFF_FFFF
        # 4 bits
        ver = (uuid.int >> 76) & 0xF
        # 12 bits
        sha1_mid = (uuid.int >> 64) & 0xFFF
        # 2 bits
        var = (uuid.int >> 62) & 0x3
        # 62 bits
        sha1_low = uuid.int & 0x3FFF_FFFF_FFFF_FFFF

        sha1 = (sha1_high << 64) | (sha1_mid << 48) | sha1_low

        return {
            "sha1_high": sha1_high,
            "ver": str(ver),
            "sha1_mid": sha1_mid,
            "var": var,
            "sha1_low": sha1_low,
            "sha1": sha1,
        }


def parse(uuid: UUID, spec: str = "latest", **kwargs) -> Dict[str, Any]:
    """Parse UUID.

    Args:
        uuid (UUID): UUID.
        spec (str, optional): UUID spec. Defaults to "latest".

    Returns:
        Dict[str, Any]: Parsed UUID.
    """
    uuid_int = uuid.int
    version = UUIDGenerator.get_version(uuid)

    module = load_modules(spec)
    try:
        if uuid_int == 0:
            parse_func = module.NilUUIDGenerator.parse  # type: ignore # noqa: F821
        elif uuid_int == 0xFFFF_FFFF_FFFF_FFFF_FFFF_FFFF_FFFF_FFFF:
            parse_func = module.MaxUUIDGenerator.parse  # type: ignore # noqa: F821
        elif version == "1":
            parse_func = _OtherUUIDParser.parse_uuid1
        elif version == "3":
            parse_func = _OtherUUIDParser.parse_uuid3
        elif version == "4":
            parse_func = _OtherUUIDParser.parse_uuid4
        elif version == "5":
            parse_func = _OtherUUIDParser.parse_uuid5
        elif version == "6":
            parse_func = module.UUID6Generator.parse  # type: ignore # noqa: F821
        elif version == "7":
            parse_func = module.UUID7Generator.parse  # type: ignore # noqa: F821
        elif version == "8":
            parse_func = module.UUID8Generator.parse  # type: ignore # noqa: F821
        else:
            raise ValueError(f"Unsupported version: {version}")
    except UnboundLocalError:
        raise ValueError(f"Unsupported version: {version}")

    return parse_func(uuid, **kwargs)  # type: ignore # noqa: F821
