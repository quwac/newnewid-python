from typing import Any, Dict
from uuid import UUID

from newnewid.util.nodoc import nodoc
from newnewid.uuidgenerator.uuid_generator import UUIDGenerator


class UUID8Generator(UUIDGenerator):
    """UUIDv8 generator class.

    UUIDv8 is a 128-bit UUID that is based on any time system and is sortable.

     0                   1                   2                   3
     0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |                          timestamp_32                         |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |           timestamp_48        |  ver  |      time_or_seq      |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |var|  seq_or_node  |          node                             |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |                              node                             |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

    You can extend the timestamp part of the UUIDv8 by using `time_or_seq` and the
    node part (pseudo-random value) by using `seq_or_node`. You can then determine
    the sequence (counter) part by using both `time_or_seq` and `seq_or_node`. In
    other words, it is important to ensure the monoticity of the UUIDv8 yourself.
    """

    def generate(
        self,
        timestamp_32: int,
        timestamp_48: int,  # Confusing. This is only 16 bit.
        time_or_seq: int,
        seq_or_node: int,
        node: int,
    ) -> UUID:
        """Generate UUID8.

        Args:
            timestamp_32: 32 bits timestamp.
            timestamp_48: 16 bits timestamp.
            time_or_seq: 12 bits timestamp or sequence.
            seq_or_node: 8 bits sequence or node.
            node: 54 bits node.

        Returns:
            UUIDv8.
        """
        # 32 bits
        timestamp_32 &= 0xFFFF_FFFF
        # 16 bits
        timestamp_48 &= 0xFFFF
        # 4 bits
        ver = 8
        # 12 bits
        time_or_seq &= 0x0FFF
        # 2 bits
        var = 0b10
        # 8 bits
        seq_or_node &= 0xFF
        # 54 bits
        node &= 0x3FFF_FFFF_FFFF

        uuid8_int = (
            (timestamp_32 << 96)
            | (timestamp_48 << 80)
            | (ver << 76)
            | (time_or_seq << 64)
            | (var << 62)
            | (seq_or_node << 54)
            | node
        )
        return UUID(int=uuid8_int)

    @classmethod
    @nodoc
    def parse(cls, uuid: UUID, **kwargs: Any) -> Dict[str, Any]:
        timestamp_32 = (uuid.int >> 96) & 0xFFFF_FFFF
        timestamp_48 = (uuid.int >> 80) & 0xFFFF
        version = (uuid.int >> 76) & 0xF
        assert version == 8, f"version must be 8, but {version}"
        time_or_seq = (uuid.int >> 64) & 0xFFF
        variant = (uuid.int >> 62) & 0x3
        seq_or_node = (uuid.int >> 54) & 0xFF
        node = uuid.int & 0x3FFF_FFFF_FFFF

        return {
            "timestamp_32": timestamp_32,
            "timestamp_48": timestamp_48,
            "ver": str(version),
            "time_or_seq": time_or_seq,
            "variant": variant,
            "seq_or_node": seq_or_node,
            "node": node,
        }


_uuid8_generator = UUID8Generator()


def uuid8(
    timestamp_32: int,
    timestamp_48: int,  # Don't get me wrong. This is only 16 bit.
    time_or_seq: int,
    seq_or_node: int,
    node: int,
) -> UUID:
    """Generate UUID8.

    Args:
        timestamp_32: 32 bits timestamp.
        timestamp_48: 16 bits timestamp.
        time_or_seq: 12 bits timestamp or sequence.
        seq_or_node: 8 bits sequence or node.
        node: 54 bits node.

    Returns:
        UUIDv8.
    """
    return _uuid8_generator.generate(timestamp_32, timestamp_48, time_or_seq, seq_or_node, node)
