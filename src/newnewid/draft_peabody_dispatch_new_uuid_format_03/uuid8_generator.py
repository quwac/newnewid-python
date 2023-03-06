from typing import Any, Dict
from uuid import UUID

from newnewid.util.nodoc import nodoc


class UUID8Generator:
    """UUIDv8 generator class.

     0                   1                   2                   3
     0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |                           custom_a                            |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |          custom_a             |  ver  |       custom_b        |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |var|                       custom_c                            |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |                           custom_c                            |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    """

    def generate(
        self,
        custom_a: int,
        custom_b: int,
        custom_c: int,
    ) -> UUID:
        """Generate UUIDv8.

        UUIDv8 can define 122 bits of information as desired.
        The 122 bits are stored in 48-bits, 12-bits, and 62-bits parts.

        Args:
            custom_a (int): 48-bits part
            custom_b (int): 12-bits part
            custom_c (int): 62-bits part

        Returns:
            UUID: UUIDv8
        """
        # 48 bits
        custom_a &= 0xFFFF_FFFF_FFFF
        # 4 bits
        ver = 8
        # 12 bits
        custom_b &= 0x0FFF
        # 2 bits
        var = 2
        # 62 bits
        custom_c &= 0x3FFF_FFFF_FFFF_FFFF

        return UUID(int=(custom_a << 80) | (ver << 76) | (custom_b << 64) | (var << 62) | custom_c)

    @classmethod
    @nodoc
    def parse(cls, uuid: UUID, **kwargs: Any) -> Dict[str, Any]:
        custom_a = (uuid.int >> 80) & 0xFFFF_FFFF_FFFF
        version = (uuid.int >> 76) & 0xF
        custom_b = (uuid.int >> 64) & 0x0FFF
        variant = (uuid.int >> 62) & 0x03
        custom_c = uuid.int & 0x3FFF_FFFF_FFFF_FFFF

        return {
            "ver": str(version),
            "custom_a": custom_a,
            "custom_b": custom_b,
            "variant": variant,
            "custom_c": custom_c,
        }


_uuid8_generator = UUID8Generator()


def uuid8(
    custom_a: int,
    custom_b: int,
    custom_c: int,
) -> UUID:
    """Generate UUIDv8.

    UUIDv8 can define 122 bits of information as desired.
    The 122 bits are stored in 48-bits, 12-bits, and 62-bits parts.

    Args:
        custom_a (int): 48-bits part
        custom_b (int): 12-bits part
        custom_c (int): 62-bits part

    Returns:
        UUID: UUIDv8
    """
    return _uuid8_generator.generate(custom_a, custom_b, custom_c)
