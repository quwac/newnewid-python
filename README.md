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

## Old draft UUID

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

## License

[Unlicense](./LICENSE)

## Reference

* [uuid6/prototypes](https://github.com/uuid6/prototypes)

## Appendix: UUIDv7 >= draft-peabody-dispatch-new-uuid-format-03 implementation

```text
         0                   1                   2                   3
         0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        |                           unix_ts_ms                          |
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        |          unix_ts_ms           |  ver  |       rand_a          |
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        |var|                        rand_b                             |
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        |                            rand_b                             |
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

In fact, UUIDv7 allows the use of a counter with `rand_a` and `rand_b`, which provides some degree of freedom.
The length of this counter can be freely determined between 0 and 74 bits. Bits not used for the counter are filled with pseudo-random numbers.

If multiple UUIDv7 implementations with different counter bit lengths are used in a system, the system may behave in an unexpected manner.
For example, consider a system that uses UUIDv7 for the ID column of a database table.
If multiple UUIDv7 implementations, each with different counter bit lengths, independently number the IDs in the table, monotonically increasing table IDs would not be expected.

Typical bit lengths of the counter are shown below:

* 0 bits: No counter. There will be no graduality for UUIDv7 generated at the same time.
* 12 bits: The same bit length as the `rand_a` is used for the counter, where X represents the counter portion in the UUID string representation: `xxxxxxxx-xxxx-7XXX-xxxx-xxxxxxxxxxxx`.
* 26 bits: The third and fourth parts of the UUID string representation are used for the counter, where X and Y represents the counter part: `xxxxxxxx-xxxx-7XXX-YXXX-xxxxxxxxxxxx`. Note that Y is limited to c, d, e or f.
* 42 bits: The bit length used for pseudo-random numbers is exactly 32 bits, where X and Y are counters in the string representation of the UUID: `xxxxxxxx-xxxx-7XXX-YXXX-XXXXxxxxxxxx`.
* 74 bits: all bits are used for the counter and pseudo-random numbers are not used.

I investigated how many bits each library implementation uses for counters:

| Name                                                                                             | Language   | Counter bits | Counter                         |
| ------------------------------------------------------------------------------------------------ | ---------- | ------------ | ------------------------------- |
| **[quwac/newuuid6](https://github.com/quwac/newuuid)**                                           | **Python** | **0 - 74**   |
| [oittaa/uuid6-python](https://github.com/oittaa/uuid6-python)                                    | Python     | 0            |                                 |
| [jdknezek/uuid6-zig](https://github.com/jdknezek/uuid6-zig)                                      | Zig        | 0            |                                 |
| [daegalus/uuid/tree/uuid6](https://github.com/daegalus/dart-uuid)                                | Dart       | 0            |                                 |
| [f4b6a3/uuid-creator](https://github.com/f4b6a3/uuid-creator)                                    | Java       | 0 or 26      |                                 |
| [oittaa/uuid-php](https://github.com/oittaa/uuid-php)                                            | PHP        | 0            |                                 |
| [symfony/uid](https://github.com/symfony/uid/tree/6.2)                                           | PHP        | 74           |                                 |
| [gofrs/uuid](https://github.com/gofrs/uuid)                                                      | Go         | ?            |                                 |
| [sprql/uuid7-ruby](https://github.com/sprql/uuid7-ruby)                                          | Ruby       | 0            |                                 |
| [kjmph/UUID_v7_for_Postgres.sql](https://gist.github.com/kjmph/5bd772b2c2df145aa645b837da7eca74) | Postgres   | 0            |                                 |
| [MatrixAI/js-id](https://github.com/MatrixAI/js-id)                                              | TypeScript | 12           |                                 |
| [LiosK/uuidv7](https://github.com/LiosK/uuidv7)                                                  | TypeScript | 42           |                                 |
| [kripod/uuidv7](https://github.com/kripod/uuidv7)                                                | TypeScript | 12           | Sequence counter is reset to 0. |
| [fabiolimace/UUIDv7_for_C](https://gist.github.com/fabiolimace/9873fe7bbcb1e6dc40638a4f98676d72) | C          | 12 or 74     |                                 |
| [LiosK/uuidv7-h](https://github.com/LiosK/uuidv7-h)                                              | C/C++      | 42           |                                 |
| [mareek/UUIDNext](https://github.com/mareek/UUIDNext)                                            | C#         | 12           |                                 |
| [BaerMitUmlaut/GuidPlus](https://github.com/BaerMitUmlaut/GuidPlus)                              | C#         | 12           | Sequence counter is reset to 0. |
| [Medo/Uuid7](https://github.com/medo64/Medo.Uuid7)                                               | C#         | 26           |                                 |
| [LiosK/uuid7-rs](https://github.com/LiosK/uuid7-rs)                                              | Rust       | 42           |                                 |
| [DianaNites/nuuid](https://github.com/DianaNites/nuuid)                                          | Rust       | 0            |                                 |
| [jakwings/uuid.sh](https://github.com/jakwings/uuid.sh)                                          | Shell      | 12           |                                 |
| [x4m/pg_uuid_next](https://github.com/x4m/pg_uuid_next)                                          | C          | 0            |                                 |

The source of the listing is [uuid6/prototypes](https://github.com/uuid6/prototypes).

[Let me know if I'm wrong.](https://github.com/quwac/newuuid-python/issues)
