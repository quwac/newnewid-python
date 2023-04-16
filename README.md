# NewNewID

**NewNewID** generates/parses UUIDv1, UUIDv3, UUIDv4, UUIDv5, UUIDv6, UUIDv7, UUIDv8, Nil UUID, and Max UUID.

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
pip install newnewid

# poetry
poetry add newnewid
```

## Usage

### CLI

#### Generate

```bash
# Generate UUIDv6
newnewid generate -u 6
# 1eddc0a3-3b61-6872-9eb9-e8ea56a8a2d4

# Generate 10 UUIDv6
newnewid generate -u 6 10
# 1eddc0a5-337c-6a70-828f-c8be267b2009
# 1eddc0a5-337c-6b76-8a9a-6b477fe20182
# 1eddc0a5-337c-6c69-9cc6-554230efb097
# 1eddc0a5-337c-6d1d-9ab7-d0bc161043f8
# 1eddc0a5-337c-6d97-980d-ea6785b84ab9
# 1eddc0a5-337c-6e2a-963b-cef6bd5e9bd2
# 1eddc0a5-337c-6e93-9cc9-6f49a4fed295
# 1eddc0a5-337c-6f11-916d-350fd609d0ed
# 1eddc0a5-337c-6f7e-9b88-15d5e884e031
# 1eddc0a5-337d-6009-916c-1341224f7a36

# Generate 10 UUIDv7 (Method 1, counter bits length=12)
newnewid generate -u 7 10
# 01878833-7b1f-7156-8bd8-c5f2ecdafecf
# 01878833-7b1f-7157-8979-a795e96dd0b4
# 01878833-7b1f-7158-b385-aa0e5050391f
# 01878833-7b1f-7159-9944-a7e0617c461b
# 01878833-7b1f-715a-841d-a77ba09f1898
# 01878833-7b1f-715b-a52c-88147629e891
# 01878833-7b1f-715c-b396-6ee1bef23a92
# 01878833-7b1f-715d-98a4-e7824b11c100
# 01878833-7b1f-715e-a27d-b8861db00a71
# 01878833-7b1f-715f-a90c-c7c047250696

# Generate 10 UUIDv7 (Method 1, counter bits length=26)
newnewid generate -u 7 -m METHOD-1-26 10
# 01878835-438b-7727-81e1-cfa064822793
# 01878835-438b-7727-81e2-1e9b0b4a373d
# 01878835-438b-7727-81e3-3ae237b27bed
# 01878835-438b-7727-81e4-1c0404d70ced
# 01878835-438b-7727-81e5-bb8049d4f30f
# 01878835-438b-7727-81e6-a268724d7368
# 01878835-438b-7727-81e7-d76430587971
# 01878835-438b-7727-81e8-fdc840580f0c
# 01878835-438b-7727-81e9-48b83615e224
# 01878835-438b-7727-81ea-9e9b486e862c

# Generate 10 UUIDv7 (Method 2)
newnewid generate -u 7 -m METHOD-2 10
# 01878836-005f-7155-8ed0-1c9cb30834ba
# 01878836-005f-7155-b302-b5eba4225edc
# 01878836-005f-7156-a3a4-17d13653bdec
# 01878836-005f-7157-9467-20aaac891b0e
# 01878836-005f-7158-9318-45de1581728c
# 01878836-005f-7159-8f4f-d89315c708e0
# 01878836-005f-7159-acc2-da0b539f81bd
# 01878836-005f-715a-9c07-7292afe90ef1
# 01878836-005f-715b-901a-fd20a54b461f
# 01878836-005f-715b-b20b-4ce3a853729b

# Generate UUIDv8
newnewid generate -u 8 --custom-a 1 --custom-b 2 --custom-c
# 00000000-0001-8002-8000-000000000003
```

#### Parse

```bash
# Parse UUIDv6
newnewid parse 1eddc0a3-3b61-6872-9eb9-e8ea56a8a2d4
# {"uuid": "1eddc0a3-3b61-6872-9eb9-e8ea56a8a2d4", "time_high": 517849251, "time_mid": 15201, "ver": "6", "time_low": 2162, "variant": 2, "clock_seq": 7865, "node": 256093173883604, "gregorian_100_nano_seconds": 139009099893708914, "time": "2023-04-16T03:53:09.370891", "epoch_nano_fraction": 400}

# Parse 10 UUIDv7 created by Method 1, counter bits length=12
newnewid parse \
    01878833-7b1f-7156-8bd8-c5f2ecdafecf \
    01878833-7b1f-7157-8979-a795e96dd0b4 \
    01878833-7b1f-7158-b385-aa0e5050391f \
    01878833-7b1f-7159-9944-a7e0617c461b \
    01878833-7b1f-715a-841d-a77ba09f1898 \
    01878833-7b1f-715b-a52c-88147629e891 \
    01878833-7b1f-715c-b396-6ee1bef23a92 \
    01878833-7b1f-715d-98a4-e7824b11c100 \
    01878833-7b1f-715e-a27d-b8861db00a71 \
    01878833-7b1f-715f-a90c-c7c047250696
# {"uuid": "01878833-7b1f-7156-8bd8-c5f2ecdafecf", "unix_ts_ms": 1681617287967, "ver": "7", "rand_a": 342, "var": 2, "rand_b": 853649776533241551, "time": "2023-04-16T03:54:47.967000", "seq": 342, "rand": 853649776533241551}
# {"uuid": "01878833-7b1f-7157-8979-a795e96dd0b4", "unix_ts_ms": 1681617287967, "ver": "7", "rand_a": 343, "var": 2, "rand_b": 682761080831594676, "time": "2023-04-16T03:54:47.967000", "seq": 343, "rand": 682761080831594676}
# {"uuid": "01878833-7b1f-7158-b385-aa0e5050391f", "unix_ts_ms": 1681617287967, "ver": "7", "rand_a": 344, "var": 2, "rand_b": 3712560446290540831, "time": "2023-04-16T03:54:47.967000", "seq": 344, "rand": 3712560446290540831}
# {"uuid": "01878833-7b1f-7159-9944-a7e0617c461b", "unix_ts_ms": 1681617287967, "ver": "7", "rand_a": 345, "var": 2, "rand_b": 1820764731514570267, "time": "2023-04-16T03:54:47.967000", "seq": 345, "rand": 1820764731514570267}
# {"uuid": "01878833-7b1f-715a-841d-a77ba09f1898", "unix_ts_ms": 1681617287967, "ver": "7", "rand_a": 346, "var": 2, "rand_b": 296577299893917848, "time": "2023-04-16T03:54:47.967000", "seq": 346, "rand": 296577299893917848}
# {"uuid": "01878833-7b1f-715b-a52c-88147629e891", "unix_ts_ms": 1681617287967, "ver": "7", "rand_a": 347, "var": 2, "rand_b": 2678665499841783953, "time": "2023-04-16T03:54:47.967000", "seq": 347, "rand": 2678665499841783953}
# {"uuid": "01878833-7b1f-715c-b396-6ee1bef23a92", "unix_ts_ms": 1681617287967, "ver": "7", "rand_a": 348, "var": 2, "rand_b": 3717280458291165842, "time": "2023-04-16T03:54:47.967000", "seq": 348, "rand": 3717280458291165842}
# {"uuid": "01878833-7b1f-715d-98a4-e7824b11c100", "unix_ts_ms": 1681617287967, "ver": "7", "rand_a": 349, "var": 2, "rand_b": 1775798699882037504, "time": "2023-04-16T03:54:47.967000", "seq": 349, "rand": 1775798699882037504}
# {"uuid": "01878833-7b1f-715e-a27d-b8861db00a71", "unix_ts_ms": 1681617287967, "ver": "7", "rand_a": 350, "var": 2, "rand_b": 2485345455541586545, "time": "2023-04-16T03:54:47.967000", "seq": 350, "rand": 2485345455541586545}
# {"uuid": "01878833-7b1f-715f-a90c-c7c047250696", "unix_ts_ms": 1681617287967, "ver": "7", "rand_a": 351, "var": 2, "rand_b": 2957958683916830358, "time": "2023-04-16T03:54:47.967000", "seq": 351, "rand": 2957958683916830358}

# Parse 10 UUIDv7 created by Method 1, counter bits length=26
newnewid parse -m METHOD-1-26 \
    01878835-438b-7727-81e1-cfa064822793 \
    01878835-438b-7727-81e2-1e9b0b4a373d \
    01878835-438b-7727-81e3-3ae237b27bed \
    01878835-438b-7727-81e4-1c0404d70ced \
    01878835-438b-7727-81e5-bb8049d4f30f \
    01878835-438b-7727-81e6-a268724d7368 \
    01878835-438b-7727-81e7-d76430587971 \
    01878835-438b-7727-81e8-fdc840580f0c \
    01878835-438b-7727-81e9-48b83615e224 \
    01878835-438b-7727-81ea-9e9b486e862c
# {"uuid": "01878835-438b-7727-81e1-cfa064822793", "unix_ts_ms": 1681617404811, "ver": "7", "rand_a": 1831, "var": 2, "rand_b": 135617751585793939, "time": "2023-04-16T03:56:44.811000", "seq": 29999585, "rand": 228287787968403}
# {"uuid": "01878835-438b-7727-81e2-1e9b0b4a373d", "unix_ts_ms": 1681617404811, "ver": "7", "rand_a": 1831, "var": 2, "rand_b": 135704590032713533, "time": "2023-04-16T03:56:44.811000", "seq": 29999586, "rand": 33651258177341}
# {"uuid": "01878835-438b-7727-81e3-3ae237b27bed", "unix_ts_ms": 1681617404811, "ver": "7", "rand_a": 1831, "var": 2, "rand_b": 136017157022710765, "time": "2023-04-16T03:56:44.811000", "seq": 29999587, "rand": 64743271463917}
# {"uuid": "01878835-438b-7727-81e4-1c0404d70ced", "unix_ts_ms": 1681617404811, "ver": "7", "rand_a": 1831, "var": 2, "rand_b": 136264692314606829, "time": "2023-04-16T03:56:44.811000", "seq": 29999588, "rand": 30803586649325}
# {"uuid": "01878835-438b-7727-81e5-bb8049d4f30f", "unix_ts_ms": 1681617404811, "ver": "7", "rand_a": 1831, "var": 2, "rand_b": 136721523373568783, "time": "2023-04-16T03:56:44.811000", "seq": 29999589, "rand": 206159668900623}
# {"uuid": "01878835-438b-7727-81e6-a268724d7368", "unix_ts_ms": 1681617404811, "ver": "7", "rand_a": 1831, "var": 2, "rand_b": 136975408159355752, "time": "2023-04-16T03:56:44.811000", "seq": 29999590, "rand": 178569477976936}
# {"uuid": "01878835-438b-7727-81e7-d76430587971", "unix_ts_ms": 1681617404811, "ver": "7", "rand_a": 1831, "var": 2, "rand_b": 137315138965895537, "time": "2023-04-16T03:56:44.811000", "seq": 29999591, "rand": 236825307806065}
# {"uuid": "01878835-438b-7727-81e8-fdc840580f0c", "unix_ts_ms": 1681617404811, "ver": "7", "rand_a": 1831, "var": 2, "rand_b": 137638825149599500, "time": "2023-04-16T03:56:44.811000", "seq": 29999592, "rand": 279036514799372}
# {"uuid": "01878835-438b-7727-81e9-48b83615e224", "unix_ts_ms": 1681617404811, "ver": "7", "rand_a": 1831, "var": 2, "rand_b": 137721219630096932, "time": "2023-04-16T03:56:44.811000", "seq": 29999593, "rand": 79956018586148}
# {"uuid": "01878835-438b-7727-81ea-9e9b486e862c", "unix_ts_ms": 1681617404811, "ver": "7", "rand_a": 1831, "var": 2, "rand_b": 138097128360543788, "time": "2023-04-16T03:56:44.811000", "seq": 29999594, "rand": 174389772322348}

# Parse 10 UUIDv7 created by Method 2
newnewid parse -m METHOD-2 \
    01878836-005f-7155-8ed0-1c9cb30834ba \
    01878836-005f-7155-b302-b5eba4225edc \
    01878836-005f-7156-a3a4-17d13653bdec \
    01878836-005f-7157-9467-20aaac891b0e \
    01878836-005f-7158-9318-45de1581728c \
    01878836-005f-7159-8f4f-d89315c708e0 \
    01878836-005f-7159-acc2-da0b539f81bd \
    01878836-005f-715a-9c07-7292afe90ef1 \
    01878836-005f-715b-901a-fd20a54b461f \
    01878836-005f-715b-b20b-4ce3a853729b
# {"uuid": "01878836-005f-7155-8ed0-1c9cb30834ba", "unix_ts_ms": 1681617453151, "ver": "7", "rand_a": 341, "var": 2, "rand_b": 1067384571030942906, "time": "2023-04-16T03:57:33.151000", "seq": 1573652316854770218170, "rand": null}
# {"uuid": "01878836-005f-7155-b302-b5eba4225edc", "unix_ts_ms": 1681617453151, "ver": "7", "rand_a": 341, "var": 2, "rand_b": 3675700269563403996, "time": "2023-04-16T03:57:33.151000", "seq": 1576260632553302679260, "rand": null}
# {"uuid": "01878836-005f-7156-a3a4-17d13653bdec", "unix_ts_ms": 1681617453151, "ver": "7", "rand_a": 342, "var": 2, "rand_b": 2568203874835086828, "time": "2023-04-16T03:57:33.151000", "seq": 1579764822177001749996, "rand": null}
# {"uuid": "01878836-005f-7157-9467-20aaac891b0e", "unix_ts_ms": 1681617453151, "ver": "7", "rand_a": 343, "var": 2, "rand_b": 1470179720770951950, "time": "2023-04-16T03:57:33.151000", "seq": 1583278484041365003022, "rand": null}
# {"uuid": "01878836-005f-7158-9318-45de1581728c", "unix_ts_ms": 1681617453151, "ver": "7", "rand_a": 344, "var": 2, "rand_b": 1375926506307547788, "time": "2023-04-16T03:57:33.151000", "seq": 1587795916845328986764, "rand": null}
# {"uuid": "01878836-005f-7159-8f4f-d89315c708e0", "unix_ts_ms": 1681617453151, "ver": "7", "rand_a": 345, "var": 2, "rand_b": 1103338559966218464, "time": "2023-04-16T03:57:33.151000", "seq": 1592135014917415045344, "rand": null}
# {"uuid": "01878836-005f-7159-acc2-da0b539f81bd", "unix_ts_ms": 1681617453151, "ver": "7", "rand_a": 345, "var": 2, "rand_b": 3225380025333154237, "time": "2023-04-16T03:57:33.151000", "seq": 1594257056382781981117, "rand": null}
# {"uuid": "01878836-005f-715a-9c07-7292afe90ef1", "unix_ts_ms": 1681617453151, "ver": "7", "rand_a": 346, "var": 2, "rand_b": 2019708932241034993, "time": "2023-04-16T03:57:33.151000", "seq": 1597663071308117249777, "rand": null}
# {"uuid": "01878836-005f-715b-901a-fd20a54b461f", "unix_ts_ms": 1681617453151, "ver": "7", "rand_a": 347, "var": 2, "rand_b": 1160518170655278623, "time": "2023-04-16T03:57:33.151000", "seq": 1601415566564958881311, "rand": null}
# {"uuid": "01878836-005f-715b-b20b-4ce3a853729b", "unix_ts_ms": 1681617453151, "ver": "7", "rand_a": 347, "var": 2, "rand_b": 3606060467305542299, "time": "2023-04-16T03:57:33.151000", "seq": 1603861108861609144987, "rand": null}

# Parse UUIDv8
newnewid parse 00000000-0001-8002-8000-000000000003
# {"uuid": "00000000-0001-8002-8000-000000000003", "ver": "8", "custom_a": 1, "custom_b": 2, "variant": 2, "custom_c": 3}
```

### Development

The usage of newnewid is similar to the usage of the built-in uuid package.

```python
import newnewid

print("")

# Generate UUIDv6
print("UUIDv6 (Default=Random node)")
uuid6 = newnewid.uuid6()
print(uuid6)
print("")
uuid6 = newnewid.uuid6()
print("[NOT RECOMMENDED]UUIDv6 (MAC address node)")
uuid6_mac_address = newnewid.uuid6(uses_mac_address=True)
print(uuid6_mac_address)
print("")

# Generate UUIDv7
print(
    "UUIDv7 (Default=Method 1: Fixed length dedicated counter bits, counter bits length=12)"
)
for _ in range(10):
    uuid7 = newnewid.uuid7()
    print(uuid7)
print("")
print("UUIDv7 (Method 1, counter bits length=26)")
for _ in range(10):
    uuid7_method1_26 = newnewid.uuid7(
        newnewid.METHOD_1_FIXED_LENGTH_DEDICATED_COUNTER_BITS_26
    )
    print(uuid7_method1_26)
print("")
print("UUIDv7 (Method 1, counter bits length=42)")
for _ in range(10):
    uuid7_method1_42 = newnewid.uuid7(
        newnewid.METHOD_1_FIXED_LENGTH_DEDICATED_COUNTER_BITS_42
    )
    print(uuid7_method1_42)
print("")
print("UUIDv7 (Method 1, counter bits length=you need)")
for _ in range(10):
    uuid7_method1_you_need = newnewid.uuid7(
        newnewid.UUID7Option.method_1_fixed_length_dedicated_counter_bits(
            33
        )  # When you need 33 bits
    )
    print(uuid7_method1_you_need)
print("")
print("UUIDv7 (Method 2: Monotonic random, incrementable bits length=62)")
for _ in range(10):
    uuid7_method2_62 = newnewid.uuid7(newnewid.METHOD_2_MONOTONIC_RANDOM_62_BITS)
    print(uuid7_method2_62)
print("")
print("UUIDv7 (Method 2: Monotonic random, incrementable bits length=you need)")
for _ in range(10):
    uuid7_method2_you_need = newnewid.uuid7(
        newnewid.UUID7Option.method_2_monotonic_random(33)
    )  # When you need 33 bits
    print(uuid7_method2_you_need)
print("")
print("[NOT RECOMMENDED] UUIDv7 (Method 0: No counter)")
for _ in range(10):
    uuid7_method0 = newnewid.uuid7(newnewid.METHOD_0_NO_COUNTER)
    print(uuid7_method0)
print("")
print("[BONUS TRACK] ULID compatible UUIDv7")
for _ in range(10):
    ulid_compatible = newnewid.ulid_compatible()
    print(ulid_compatible)
print("")

# Generate UUIDv8
import time

custom_a = 0x00
custom_b = 0x00
custom_c = time.time_ns() & 0x3FFFFFFFFFFFFFFF
uuid8 = newnewid.uuid8(custom_a, custom_b, custom_c)
print("UUIDv8")
print(uuid8)
print("")

# Generate nil UUID and max UUID
print("UUID nil")
uuid_nil = newnewid.nil_uuid()
print(uuid_nil)
print("")
print("UUID max")
uuid_nil = newnewid.max_uuid()
print(uuid_nil)
print("")
```

## Old draft UUID

The older versions of the implementation are left for my study.

**Do not use these in your products.**

```python
# Generate UUIDv7, UUIDv8 in draft-peabody-dispatch-new-uuid-format-01
from newnewid import draft_peabody_dispatch_new_uuid_format_01

print("")

# Generate UUIDv7 millisecond precision
uuid7_milli = draft_peabody_dispatch_new_uuid_format_01.uuid7(precision="milli")

print("UUIDv7 (Millisecond precision)")
print(uuid7_milli)
print("")
# Generate UUIDv7 microsecond precision
uuid7_micro = draft_peabody_dispatch_new_uuid_format_01.uuid7(precision="micro")
print("UUIDv7 (Microsecond precision)")
print(uuid7_micro)
print("")
# Generate UUIDv7 nanosecond precision
uuid7_nano = draft_peabody_dispatch_new_uuid_format_01.uuid7(precision="nano")
print("UUIDv7 (Nanosecond precision)")
print(uuid7_nano)
print("")

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
print("UUIDv8")
print(uuid8)
print("")
```

## License

[MIT License](./LICENSE)

## Reference

* [uuid6/prototypes](https://github.com/uuid6/prototypes)

## Appendix 1: UUIDv7 >= draft-peabody-dispatch-new-uuid-format-03 implementation

### `rand_a` and `rand_b` flexibility

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

**Fig 1: UUIDv7 bits layout.**

All time-based UUIDs must guarantee monotonicity.
According to the specification, UUIDv7 can guarantee monotonicity in the following ways:

* [Two or more UUIDv7s generated within the same time].
    * Method 1: A fixed length counter of between 12 and 42 bits. Typically the following three versions
        * 12 bit version
        * 26 bit version
        * 42 bit version
    * Method 2: Monotonic random counter.
        * [Must be non-guessable] Increment is a random value with a length of 62 bits
        * [May be guessable] Increment is fixed at 1
* [0 or 1 UUIDv7 generated in the same time].
    * Method 0: No counter

For systems that require multiple UUIDv7s within the same time period, since `unix_ts_ms` is the same, Method 1 or Method 2 guarantees monotonicity for the subsequent bits.

Method 1 uses a fixed-length counter like UUIDv1 and UUIDv6.
In UUIDv7, not only `rand_a` but also `rand_b` can be used for the counter, which means that there is flexibility from 0 to 74 bits, but the specification recommends a range from 12 to 42 bits.
Furthermore, considering implementation, there are three bit lengths that make sense: 12, 26, and 42 bits.

```text
         0                   1                   2                   3
         0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        |                           unix_ts_ms                          |
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        |          unix_ts_ms           |  ver  |        counter        |
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        |var|                        random                             |
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        |                            random                             |
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

**Fig 2: UUIDv7 bits layout of Method 1, 12 bits version.**

```text
         0                   1                   2                   3
         0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        |                           unix_ts_ms                          |
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        |          unix_ts_ms           |  ver  |        counter        |
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        |var|          counter          |            random             |
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        |                            random                             |
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

**Fig 3: UUIDv7 bits layout of Method 1, 26 bits version.**

```text
         0                   1                   2                   3
         0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        |                           unix_ts_ms                          |
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        |          unix_ts_ms           |  ver  |        counter        |
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        |var|                          counter                          |
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        |                            random                             |
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

**Fig 4: UUIDv7 bits layout of Method 1, 42 bits version.**

In Method 1, if `unix_ts_ms` does not change, the counter increments the previous value by 1.
When `unix_ts_ms` changes, the counter is reset.
It is important to note that the counter SHOULD be reset using a pseudo-random value, not 0.
This is to ensure ease of guessing.

Method 2 uses a random number field with guaranteed monotonicity.

```text
         0                   1                   2                   3
         0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        |                           unix_ts_ms                          |
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        |          unix_ts_ms           |  ver  |  monotonicity_random  |
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        |var|         monotonicity_random (incrementable field)         |
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        |           monotonicity_random (incrementable field)           |
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

**Fig 5: UUIDv7 bits layout of Method 2, 62 bits incrementable field.**

`monotonicity_random` is a special counter.
Like the counter of Method 1, it uses a pseudo-random value for resetting.
However, the increment value is not 1, but a pseudo-random value.
To prevent frequent rollovers, this increment value generates a random number with a bit length somewhat smaller than `monotonicity_random`. Specifically, random numbers are generated in the range of 62 bits (1 to 2^62 - 1).

Note: The increment value MAY be a fixed value of 1 if guessability is not required.
This design is closer to the [ULID specification](https://github.com/ulid/spec).
ULID also stores UNIX milliseconds in the most significant 48 bits. The following 80 bits are a monotonicity random counter with an increment value of 1.
UUIDv7 of Method 2, which has an increment value of 1, is compatible with ULID, although the 6 bits of `ver` and `var` limit the number of bits that can be used for the counter to 74.

By the way, if your system requires only one UUIDv7 at the same time, `unix_ts_ms` guarantees monotonicity, so you don't need to do any tricks. Since `rand_a` and `rand_b` need not be guessable, pseudo-random values can be applied.
I call this Method 0.

```text
         0                   1                   2                   3
         0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        |                           unix_ts_ms                          |
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        |          unix_ts_ms           |  ver  |        random         |
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        |var|                          random                           |
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        |                            random                             |
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

**Fig 6: UUIDv7 bits layout of Method 0.**

Note: "Method 0" is a name I gave for convenience, not something mentioned in the specification. It is a dialectal term.

The difference from Method 2 is that `random` does nothing to guarantee monotonicity.
Since a pseudo-random value is set each time a UUID is generated, the next value may increase, decrease, or remain the same.

IMO: I doubt that a developer considering using UUIDv7 would need Method 0. Apart from being less easy to guess, this is simply UNIX milliseconds, and choosing Method 0 implies the assumption that only one UUID can be generated within one millisecond, but it is also unclear whether that assumption can be met in many cases.

### Implementations

I investigated how many bits each library implementation uses for counters:

| Name                                                                                             | Language   | Method 1              | Method 2                  | Method 0 | Note                                        |
| ------------------------------------------------------------------------------------------------ | ---------- | --------------------- | ------------------------- | -------- | ------------------------------------------- |
| **[quwac/newnewid](https://github.com/quwac/newnewid)**                                          | **Python** | Yes, all bits version | Yes, all bits version     | Yes      |                                             |
| [oittaa/uuid6-python](https://github.com/oittaa/uuid6-python)                                    | Python     | No                    | No                        | Yes      |                                             |
| [jdknezek/uuid6-zig](https://github.com/jdknezek/uuid6-zig)                                      | Zig        | No                    | No                        | Yes      |                                             |
| [daegalus/uuid/tree/uuid6](https://github.com/daegalus/dart-uuid)                                | Dart       | No                    | No                        | Yes      |                                             |
| [f4b6a3/uuid-creator](https://github.com/f4b6a3/uuid-creator)                                    | Java       | Yes. 26 bits version  | Yes, 1 to 63 bits version | No       |                                             |
| [oittaa/uuid-php](https://github.com/oittaa/uuid-php)                                            | PHP        | No                    | No                        | Yes      |                                             |
| [symfony/uid](https://github.com/symfony/uid/tree/6.2)                                           | PHP        | No                    | Yes, 1 bits version       | No       |                                             |
| [gofrs/uuid](https://github.com/gofrs/uuid)                                                      | Go         | Yes, 12 bits version  | No                        | No       |                                             |
| [sprql/uuid7-ruby](https://github.com/sprql/uuid7-ruby)                                          | Ruby       | No                    | No                        | Yes      |                                             |
| [kjmph/UUID_v7_for_Postgres.sql](https://gist.github.com/kjmph/5bd772b2c2df145aa645b837da7eca74) | Postgres   | No                    | No                        | Yes      |                                             |
| [MatrixAI/js-id](https://github.com/MatrixAI/js-id)                                              | TypeScript | Yes, 12 bits version  | No                        | No       | The bit storage in unix_ts_ms may be wrong. |
| [LiosK/uuidv7](https://github.com/LiosK/uuidv7)                                                  | TypeScript | Yes, 42 bits version  | No                        | No       |                                             |
| [kripod/uuidv7](https://github.com/kripod/uuidv7)                                                | TypeScript | Yes, 12 bits version  | No                        | No       | Counter is reset to 0.                      |
| [fabiolimace/UUIDv7_for_C](https://gist.github.com/fabiolimace/9873fe7bbcb1e6dc40638a4f98676d72) | C          | Yes, 12 bits version  | Yes, 1 or 8 bits version  | Yes      |                                             |
| [LiosK/uuidv7-h](https://github.com/LiosK/uuidv7-h)                                              | C/C++      | Yes, 42 bits version  | No                        | No       |                                             |
| [mareek/UUIDNext](https://github.com/mareek/UUIDNext)                                            | C#         | Yes, 12 bits version  | No                        | No       |                                             |
| [BaerMitUmlaut/GuidPlus](https://github.com/BaerMitUmlaut/GuidPlus)                              | C#         | Yes, 12 bits version  | No                        | No       | Counter is reset to 0.                      |
| [Medo/Uuid7](https://github.com/medo64/Medo.Uuid7)                                               | C#         | Yes, 26 bits version  | No                        | No       |                                             |
| [LiosK/uuid7-rs](https://github.com/LiosK/uuid7-rs)                                              | Rust       | Yes, 42 bits version  | No                        | No       |                                             |
| [DianaNites/nuuid](https://github.com/DianaNites/nuuid)                                          | Rust       | No                    | No                        | Yes      |                                             |
| [jakwings/uuid.sh](https://github.com/jakwings/uuid.sh)                                          | Shell      | Yes, 12 bits version  | No                        | No       |                                             |
| [x4m/pg_uuid_next](https://github.com/x4m/pg_uuid_next)                                          | C          | No                    | No                        | Yes      |                                             |

* The source of the listing is [uuid6/prototypes](https://github.com/uuid6/prototypes).
* I investigated around April 9th 2023.
* I am not fluent in all languages. [Let me know if I'm wrong.](https://github.com/quwac/newnewid-python/issues)
