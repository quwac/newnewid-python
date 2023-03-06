# NewUUID

NewUUID generates UUIDv1, UUIDv3, UUIDv4, UUIDv5, UUIDv6, UUIDv7, UUIDv8, Nil UUID, and Max UUID.

All drafts are supported for UUIDv6, UUIDv7, UUIDv8, Nil UUID, and Max UUID.

* [draft-peabody-dispatch-new-uuid-format-01](https://datatracker.ietf.org/doc/draft-peabody-dispatch-new-uuid-format/01/)
* [draft-peabody-dispatch-new-uuid-format-02](https://datatracker.ietf.org/doc/draft-peabody-dispatch-new-uuid-format/02/)
* [draft-peabody-dispatch-new-uuid-format-03](https://datatracker.ietf.org/doc/draft-peabody-dispatch-new-uuid-format/03/)
* [draft-peabody-dispatch-new-uuid-format-04](https://datatracker.ietf.org/doc/draft-peabody-dispatch-new-uuid-format/04/)
* [draft-ietf-uuidrev-rfc4122bis-00](https://datatracker.ietf.org/doc/draft-ietf-uuidrev-rfc4122bis/00/)
* [draft-ietf-uuidrev-rfc4122bis-01](https://datatracker.ietf.org/doc/draft-ietf-uuidrev-rfc4122bis/01/)
* [draft-ietf-uuidrev-rfc4122bis-02](https://datatracker.ietf.org/doc/draft-ietf-uuidrev-rfc4122bis/02/)

## Installation

```sh
# pip
pip install newuuid-python

# poetry
poetry add newuuid-python
```

## Usage

The usage of NewUUID is similar to the usage of the built-in uuid package.

```python
import newuuid  # Current version is 'draft-ietf-uuidrev-rfc4122bis-02'

# Generate UUIDv6
uuidv6 = newuuid.uuid6()
print(uuidv6)

# Generate UUIDv7
uuid7 = newuuid.uuid7()
print(uuid7)

# Generate UUIDv8
import time
custom_a = 0x00
custom_b = 0x00
custom_c = time.time_ns() & 0x3FFFFFFFFFFFFFFF
uuid8 = newuuid.uuid8(custom_a, custom_b, custom_c)
print(uuid8)
```

# Old draft UUID

The older versions of the implementation are left for my study.

**Do not use these in your products.**

```python
# Generate UUIDv7, UUIDv8 in draft-peabody-dispatch-new-uuid-format-01
from newuuid import draft_peabody_dispatch_new_uuid_format_01  # You can use draft_peabody_dispatch_new_uuid_format_02, 03, 04 and draft_ietf_uuidrev_rfc4122bis_00, 01, 02.

# Generate UUIDv7 millisecond precision
uuid7_milli = draft_peabody_dispatch_new_uuid_format_01.uuid7(precision="milli")
# Generate UUIDv7 microsecond precision
uuid7_micro = draft_peabody_dispatch_new_uuid_format_01.uuid7(precision="micro")
# Generate UUIDv7 nanosecond precision
uuid7_nano = draft_peabody_dispatch_new_uuid_format_01.uuid7(precision="nano")
# Generate UUIDv8 nanosecond precision
import os
import time
timestamp_60bits = time.time_ns() & 0x0FFF_FFFF_FFFF_FFFF
node_62bits = int.from_bytes(os.urandom(8), byteorder="big") & 0x3FFF_FFFF_FFFF_FFFF
timestamp_32 = (timestamp_60bits >> 28) & 0xFFFF_FFFF
timestamp_48 = (timestamp_60bits >> 12) & 0xFFFF
time_or_seq = timestamp_60bits & 0x03FF
seq_or_node = (node_62bits >> 54) & 0x00FF
node = node_62bits & 0x003F_FFFF_FFFF_FFFF
uuid8 = draft_peabody_dispatch_new_uuid_format_01.uuid8(
    timestamp_32,
    timestamp_48,
    time_or_seq,
    seq_or_node,
    node,
)

print(f"uuid7_milli={uuid7_milli}, uuid7_micro={uuid7_micro}, uuid7_nano={uuid7_nano}, uuid8={uuid8}")
```

# License

[Unlicense](./LICENSE)


# Reference

* [uuid6/prototypes](https://github.com/uuid6/prototypes)
