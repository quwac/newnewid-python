from typing import Any, Dict
from uuid import UUID

from newnewid.clock.uuid_clock import UUIDClock
from newnewid.util.nodoc import nodoc
from newnewid.uuidgenerator.gregorian_based_uuid_generator import (
    GregorianBasedUUIDGenerator,
)


class UUID6Generator(GregorianBasedUUIDGenerator):
    """UUIDv6 generator class.

    UUIDv6 is a 128-bit UUID that is based on Gregorian calendar time and is sortable.

     0                   1                   2                   3
     0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |                           time_high                           |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |           time_mid            |  ver  |       time_low        |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |var|         clock_seq         |             node              |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |                              node                             |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

    There are two variations of UUIDv6:

    * [Recommended] Pseudo-random node: pseudo-random number is used for `node`.
    * [NOT Recommended] MAC address node: MAC address is used for `node`.

    """

    @nodoc
    def build(
        self,
        time: int,
        ver: int,
        var: int,
        clock_seq: int,
        node: int,
    ) -> UUID:
        # 32 bits
        time_high = (time >> 28) & 0xFFFF_FFFF
        # 16 bits
        time_mid = (time >> 12) & 0xFFFF
        # lower 12 bits
        time_low = time & 0x0FFF

        return UUID(
            int=(time_high << 96)
            | (time_mid << 80)
            | (ver << 76)
            | (time_low << 64)
            | (var << 62)
            | (clock_seq << 48)
            | node
        )

    @classmethod
    @nodoc
    def parse(cls, uuid: UUID, **kwargs: Any) -> Dict[str, Any]:
        # 32 bits
        time_high = (uuid.int >> 96) & 0xFFFF_FFFF

        # 16 bits
        time_mid = (uuid.int >> 80) & 0xFFFF

        # 4 bits
        version = (uuid.int >> 76) & 0xF
        assert version == 6, f"version must be 6, but {version}"

        # 12 bits
        time_low = (uuid.int >> 64) & 0x0FFF

        # 2 bits
        variant = (uuid.int >> 62) & 0x3

        # 14 bits
        clock_seq = (uuid.int >> 48) & 0x3FFF

        # 48 bits
        node = uuid.int & 0xFFFF_FFFF_FFFF

        gregorian_100_nano_seconds = (time_high << 28) | (time_mid << 12) | time_low
        time, epoch_nano_fraction = UUIDClock.to_datetime_from_gregorian_100_nano_seconds(
            gregorian_100_nano_seconds
        )

        return {
            "time_high": time_high,
            "time_mid": time_mid,
            "ver": str(version),
            "time_low": time_low,
            "variant": variant,
            "clock_seq": clock_seq,
            "node": node,
            "gregorian_100_nano_seconds": gregorian_100_nano_seconds,
            "time": time.isoformat(),
            "epoch_nano_fraction": epoch_nano_fraction,
        }


_uses_mac_address_to_uuid6_generator: Dict[int, UUID6Generator] = {}


def uuid6(uses_mac_address: bool = False) -> UUID:
    """Generate UUIDv6.

    Args:
        uses_mac_address (bool, optional): MAC address is used for `node` if True. Otherwise, pseudo-random number is used. Defaults to False.
    Returns:
        UUID: UUIDv6.
    """
    if uses_mac_address not in _uses_mac_address_to_uuid6_generator:
        _uses_mac_address_to_uuid6_generator[uses_mac_address] = UUID6Generator(
            uses_mac_address=uses_mac_address
        )

    return _uses_mac_address_to_uuid6_generator[uses_mac_address].generate()
