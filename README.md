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
* [draft-ietf-uuidrev-rfc4122bis-03](https://datatracker.ietf.org/doc/draft-ietf-uuidrev-rfc4122bis/03/)

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

# Generate 5 UUIDv6
newnewid generate -u 6 5
# 1eddc0a5-337c-6a70-828f-c8be267b2009
# 1eddc0a5-337c-6b76-8a9a-6b477fe20182
# 1eddc0a5-337c-6c69-9cc6-554230efb097
# 1eddc0a5-337c-6d1d-9ab7-d0bc161043f8
# 1eddc0a5-337c-6d97-980d-ea6785b84ab9

# Generate 5 UUIDv7 (Method 1, counter bits length=12)
newnewid generate -u 7 5
# 01878833-7b1f-7156-8bd8-c5f2ecdafecf
# 01878833-7b1f-7157-8979-a795e96dd0b4
# 01878833-7b1f-7158-b385-aa0e5050391f
# 01878833-7b1f-7159-9944-a7e0617c461b
# 01878833-7b1f-715a-841d-a77ba09f1898

# Generate 5 UUIDv7 (Method 1, counter bits length=26)
newnewid generate -u 7 -m METHOD-1-26 5
# 01878835-438b-7727-81e1-cfa064822793
# 01878835-438b-7727-81e2-1e9b0b4a373d
# 01878835-438b-7727-81e3-3ae237b27bed
# 01878835-438b-7727-81e4-1c0404d70ced
# 01878835-438b-7727-81e5-bb8049d4f30f

# Generate 5 UUIDv7 (Method 2, max increment bit length=62)
newnewid generate -u 7 -m METHOD-2 4
# 01878836-005f-7155-8ed0-1c9cb30834ba
# 01878836-005f-7155-b302-b5eba4225edc
# 01878836-005f-7156-a3a4-17d13653bdec
# 01878836-005f-7157-9467-20aaac891b0e
# 01878836-005f-7158-9318-45de1581728c

# Generate 5 UUIDv7 (Method 3, max increment bit length=62)
newnewid generate -u 7 -m METHOD-3 5
# 0187a76b-10ef-74c5-ab81-93ea62965bbb
# 0187a76b-10ef-7814-8e5f-fa4891e102df
# 0187a76b-10ef-7fd7-85f9-c53549b9c23c
# 0187a76b-10ef-7fdd-8c9f-29d5fb2c9552
# 0187a76b-10ef-7fe4-89fb-a167e0a150ab

# Generate 5 UUIDv7 (Method 4, time fraction bits length=12, no counter)
newnewid generate -u 7 -m METHOD-4-WITHOUT-COUNTER 5
# 0187ad6e-3db2-7367-b0de-127e7c72ddab
# 0187ad6e-3db2-73ea-8076-d41d54feae5b
# 0187ad6e-3db2-7442-b3de-0a466c744a0f
# 0187ad6e-3db2-7485-8847-92143239b0fc
# 0187ad6e-3db2-74a9-be1d-c80c36c3fadd

# Generate 5 UUIDv7 (Method 4, time fraction bits length=12, counter bits length=14)
newnewid generate -u 7 -m METHOD-4-WITH-COUNTER 5
# 0187ade8-dd73-765d-943f-a87c8351469e
# 0187ade8-dd73-76e2-9071-1fe8d28dd397
# 0187ade8-dd73-7740-8ebc-225cddfc419a
# 0187ade8-dd73-7788-9d61-e47cffa47b05
# 0187ade8-dd73-77c1-8db4-3bcbaa771022

# Generate UUIDv8
newnewid generate -u 8 --custom-a 1 --custom-b 2 --custom-c
# 00000000-0001-8002-8000-000000000003
```

#### Parse

```bash
# Parse UUIDv6
newnewid parse 1eddc0a3-3b61-6872-9eb9-e8ea56a8a2d4
# {"uuid": "1eddc0a3-3b61-6872-9eb9-e8ea56a8a2d4", "time_high": 517849251, "time_mid": 15201, "ver": "6", "time_low": 2162, "variant": 2, "clock_seq": 7865, "node": 256093173883604, "gregorian_100_nano_seconds": 139009099893708914, "time": "2023-04-16T03:53:09.370891", "epoch_nano_fraction": 400}

# Parse 5 UUIDv7 created by Method 1, counter bits length=12
newnewid parse \
    01878833-7b1f-7156-8bd8-c5f2ecdafecf \
    01878833-7b1f-7157-8979-a795e96dd0b4 \
    01878833-7b1f-7158-b385-aa0e5050391f \
    01878833-7b1f-7159-9944-a7e0617c461b \
    01878833-7b1f-715a-841d-a77ba09f1898
# {"uuid": "01878833-7b1f-7156-8bd8-c5f2ecdafecf", "unix_ts_ms": 1681617287967, "ver": "7", "rand_a": 342, "var": 2, "rand_b": 853649776533241551, "time": "2023-04-16T03:54:47.967000", "nano_fraction": null, "seq": 342, "rand": 853649776533241551}
# {"uuid": "01878833-7b1f-7157-8979-a795e96dd0b4", "unix_ts_ms": 1681617287967, "ver": "7", "rand_a": 343, "var": 2, "rand_b": 682761080831594676, "time": "2023-04-16T03:54:47.967000", "nano_fraction": null, "seq": 343, "rand": 682761080831594676}
# {"uuid": "01878833-7b1f-7158-b385-aa0e5050391f", "unix_ts_ms": 1681617287967, "ver": "7", "rand_a": 344, "var": 2, "rand_b": 3712560446290540831, "time": "2023-04-16T03:54:47.967000", "nano_fraction": null, "seq": 344, "rand": 3712560446290540831}
# {"uuid": "01878833-7b1f-7159-9944-a7e0617c461b", "unix_ts_ms": 1681617287967, "ver": "7", "rand_a": 345, "var": 2, "rand_b": 1820764731514570267, "time": "2023-04-16T03:54:47.967000", "nano_fraction": null, "seq": 345, "rand": 1820764731514570267}
# {"uuid": "01878833-7b1f-715a-841d-a77ba09f1898", "unix_ts_ms": 1681617287967, "ver": "7", "rand_a": 346, "var": 2, "rand_b": 296577299893917848, "time": "2023-04-16T03:54:47.967000", "nano_fraction": null, "seq": 346, "rand": 296577299893917848}

# Parse 5 UUIDv7 created by Method 1, counter bits length=26
newnewid parse -m METHOD-1-26 \
    01878835-438b-7727-81e1-cfa064822793 \
    01878835-438b-7727-81e2-1e9b0b4a373d \
    01878835-438b-7727-81e3-3ae237b27bed \
    01878835-438b-7727-81e4-1c0404d70ced \
    01878835-438b-7727-81e5-bb8049d4f30f
# {"uuid": "01878835-438b-7727-81e1-cfa064822793", "unix_ts_ms": 1681617404811, "ver": "7", "rand_a": 1831, "var": 2, "rand_b": 135617751585793939, "time": "2023-04-16T03:56:44.811000", "nano_fraction": null, "seq": 29999585, "rand": 228287787968403}
# {"uuid": "01878835-438b-7727-81e2-1e9b0b4a373d", "unix_ts_ms": 1681617404811, "ver": "7", "rand_a": 1831, "var": 2, "rand_b": 135704590032713533, "time": "2023-04-16T03:56:44.811000", "nano_fraction": null, "seq": 29999586, "rand": 33651258177341}
# {"uuid": "01878835-438b-7727-81e3-3ae237b27bed", "unix_ts_ms": 1681617404811, "ver": "7", "rand_a": 1831, "var": 2, "rand_b": 136017157022710765, "time": "2023-04-16T03:56:44.811000", "nano_fraction": null, "seq": 29999587, "rand": 64743271463917}
# {"uuid": "01878835-438b-7727-81e4-1c0404d70ced", "unix_ts_ms": 1681617404811, "ver": "7", "rand_a": 1831, "var": 2, "rand_b": 136264692314606829, "time": "2023-04-16T03:56:44.811000", "nano_fraction": null, "seq": 29999588, "rand": 30803586649325}
# {"uuid": "01878835-438b-7727-81e5-bb8049d4f30f", "unix_ts_ms": 1681617404811, "ver": "7", "rand_a": 1831, "var": 2, "rand_b": 136721523373568783, "time": "2023-04-16T03:56:44.811000", "nano_fraction": null, "seq": 29999589, "rand": 206159668900623}

# Parse 10 UUIDv7 created by Method 2
newnewid parse -m METHOD-2 \
    01878836-005f-7155-8ed0-1c9cb30834ba \
    01878836-005f-7155-b302-b5eba4225edc \
    01878836-005f-7156-a3a4-17d13653bdec \
    01878836-005f-7157-9467-20aaac891b0e \
    01878836-005f-7158-9318-45de1581728c
# {"uuid": "01878836-005f-7155-8ed0-1c9cb30834ba", "unix_ts_ms": 1681617453151, "ver": "7", "rand_a": 341, "var": 2, "rand_b": 1067384571030942906, "time": "2023-04-16T03:57:33.151000", "nano_fraction": null, "seq": 1573652316854770218170, "rand": null}
# {"uuid": "01878836-005f-7155-b302-b5eba4225edc", "unix_ts_ms": 1681617453151, "ver": "7", "rand_a": 341, "var": 2, "rand_b": 3675700269563403996, "time": "2023-04-16T03:57:33.151000", "nano_fraction": null, "seq": 1576260632553302679260, "rand": null}
# {"uuid": "01878836-005f-7156-a3a4-17d13653bdec", "unix_ts_ms": 1681617453151, "ver": "7", "rand_a": 342, "var": 2, "rand_b": 2568203874835086828, "time": "2023-04-16T03:57:33.151000", "nano_fraction": null, "seq": 1579764822177001749996, "rand": null}
# {"uuid": "01878836-005f-7157-9467-20aaac891b0e", "unix_ts_ms": 1681617453151, "ver": "7", "rand_a": 343, "var": 2, "rand_b": 1470179720770951950, "time": "2023-04-16T03:57:33.151000", "nano_fraction": null, "seq": 1583278484041365003022, "rand": null}
# {"uuid": "01878836-005f-7158-9318-45de1581728c", "unix_ts_ms": 1681617453151, "ver": "7", "rand_a": 344, "var": 2, "rand_b": 1375926506307547788, "time": "2023-04-16T03:57:33.151000", "nano_fraction": null, "seq": 1587795916845328986764, "rand": null}

# Parse 5 UUIDv7 (Method 3, max increment bit length=62)
newnewid parse -m METHOD-3 \
    0187a76b-10ef-74c5-ab81-93ea62965bbb \
    0187a76b-10ef-7814-8e5f-fa4891e102df \
    0187a76b-10ef-7fd7-85f9-c53549b9c23c \
    0187a76b-10ef-7fdd-8c9f-29d5fb2c9552 \
    0187a76b-10ef-7fe4-89fb-a167e0a150ab
# {"uuid": "0187a76b-10ef-74c5-ab81-93ea62965bbb", "unix_ts_ms": 1682141024495, "ver": "7", "rand_a": 1221, "var": 2, "rand_b": 3134949450512227259, "time": "2023-04-22T05:23:44.495000", "nano_fraction": null, "seq": null, "rand": 5634003577950352858043}
# {"uuid": "0187a76b-10ef-7814-8e5f-fa4891e102df", "unix_ts_ms": 1682141024495, "ver": "7", "rand_a": 2068, "var": 2, "rand_b": 1035821628910535391, "time": "2023-04-22T05:23:44.495000", "nano_fraction": null, "seq": null, "rand": 9538002507736748720863}
# {"uuid": "0187a76b-10ef-7fd7-85f9-c53549b9c23c", "unix_ts_ms": 1682141024495, "ver": "7", "rand_a": 4055, "var": 2, "rand_b": 430592072051442236, "time": "2023-04-22T05:23:44.495000", "nano_fraction": null, "seq": null, "rand": 18700817396795109392956}
# {"uuid": "0187a76b-10ef-7fdd-8c9f-29d5fb2c9552", "unix_ts_ms": 1682141024495, "ver": "7", "rand_a": 4061, "var": 2, "rand_b": 909491648770905426, "time": "2023-04-22T05:23:44.495000", "nano_fraction": null, "seq": null, "rand": 18728966412482393183570}
# {"uuid": "0187a76b-10ef-7fe4-89fb-a167e0a150ab", "unix_ts_ms": 1682141024495, "ver": "7", "rand_a": 4068, "var": 2, "rand_b": 719346033018097835, "time": "2023-04-22T05:23:44.495000", "nano_fraction": null, "seq": null, "rand": 18761058068995632091307}

# Generate 5 UUIDv7 (Method 4, time fraction bits length=12, no counter)
newnewid parse -m METHOD-4-WITHOUT-COUNTER \
    0187ad6e-3db2-7367-b0de-127e7c72ddab \
    0187ad6e-3db2-73ea-8076-d41d54feae5b \
    0187ad6e-3db2-7442-b3de-0a466c744a0f \
    0187ad6e-3db2-7485-8847-92143239b0fc \
    0187ad6e-3db2-74a9-be1d-c80c36c3fadd
# {"uuid": "0187ad6e-3db2-7367-b0de-127e7c72ddab", "unix_ts_ms": 1682241895858, "ver": "7", "rand_a": 871, "var": 2, "rand_b": 3521272293113388459, "time": "2023-04-23T09:24:55.858212", "nano_fraction": 646, "seq": null, "rand": 3521272293113388459}
# {"uuid": "0187ad6e-3db2-73ea-8076-d41d54feae5b", "unix_ts_ms": 1682241895858, "ver": "7", "rand_a": 1002, "var": 2, "rand_b": 33447269696974427, "time": "2023-04-23T09:24:55.858244", "nano_fraction": 628, "seq": null, "rand": 33447269696974427}
# {"uuid": "0187ad6e-3db2-7442-b3de-0a466c744a0f", "unix_ts_ms": 1682241895858, "ver": "7", "rand_a": 1090, "var": 2, "rand_b": 3737436038347639311, "time": "2023-04-23T09:24:55.858266", "nano_fraction": 113, "seq": null, "rand": 3737436038347639311}
# {"uuid": "0187ad6e-3db2-7485-8847-92143239b0fc", "unix_ts_ms": 1682241895858, "ver": "7", "rand_a": 1157, "var": 2, "rand_b": 596606091089522940, "time": "2023-04-23T09:24:55.858282", "nano_fraction": 470, "seq": null, "rand": 596606091089522940}
# {"uuid": "0187ad6e-3db2-74a9-be1d-c80c36c3fadd", "unix_ts_ms": 1682241895858, "ver": "7", "rand_a": 1193, "var": 2, "rand_b": 4475953559460117213, "time": "2023-04-23T09:24:55.858291", "nano_fraction": 259, "seq": null, "rand": 4475953559460117213}

# Generate 5 UUIDv7 (Method 4, time fraction bits length=12, counter bits length=14)
newnewid parse -m METHOD-4-WITH-COUNTER \
    0187ade8-dd73-765d-943f-a87c8351469e \
    0187ade8-dd73-76e2-9071-1fe8d28dd397 \
    0187ade8-dd73-7740-8ebc-225cddfc419a \
    0187ade8-dd73-7788-9d61-e47cffa47b05 \
    0187ade8-dd73-77c1-8db4-3bcbaa771022
# {"uuid": "0187ade8-dd73-765d-943f-a87c8351469e", "unix_ts_ms": 1682249932147, "ver": "7", "rand_a": 1629, "var": 2, "rand_b": 1459070057023882910, "time": "2023-04-23T11:38:52.147397", "nano_fraction": 705, "seq": 5183, "rand": 185252732552862}
# {"uuid": "0187ade8-dd73-76e2-9071-1fe8d28dd397", "unix_ts_ms": 1682249932147, "ver": "7", "rand_a": 1762, "var": 2, "rand_b": 1184763261800534935, "time": "2023-04-23T11:38:52.147430", "nano_fraction": 175, "seq": 4209, "rand": 35084825383831}
# {"uuid": "0187ade8-dd73-7740-8ebc-225cddfc419a", "unix_ts_ms": 1682249932147, "ver": "7", "rand_a": 1856, "var": 2, "rand_b": 1061761394409226650, "time": "2023-04-23T11:38:52.147453", "nano_fraction": 125, "seq": 3772, "rand": 37782256632218}
# {"uuid": "0187ade8-dd73-7788-9d61-e47cffa47b05", "unix_ts_ms": 1682249932147, "ver": "7", "rand_a": 1928, "var": 2, "rand_b": 2117224525356890885, "time": "2023-04-23T11:38:52.147470", "nano_fraction": 703, "seq": 7521, "rand": 251225516047109}
# {"uuid": "0187ade8-dd73-77c1-8db4-3bcbaa771022", "unix_ts_ms": 1682249932147, "ver": "7", "rand_a": 1985, "var": 2, "rand_b": 987479964225310754, "time": "2023-04-23T11:38:52.147484", "nano_fraction": 619, "seq": 3508, "rand": 65745924329506}

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

print("[NOT RECOMMENDED]UUIDv6 (MAC address node)")
uuid6 = newnewid.uuid6()
uuid6_mac_address = newnewid.uuid6(uses_mac_address=True)
print(uuid6_mac_address)
print("")

# Generate UUIDv7
print(
    "UUIDv7 (Default=Method 1: Fixed length dedicated counter bits, counter bits length=12)"
)
for _ in range(5):
    uuid7 = newnewid.uuid7()
    print(uuid7)
print("")

print("UUIDv7 (Method 1, counter bits length=26)")
for _ in range(5):
    uuid7_method1_26 = newnewid.uuid7(
        newnewid.METHOD_1_FIXED_LENGTH_DEDICATED_COUNTER_BITS_26
    )
    print(uuid7_method1_26)
print("")

print("UUIDv7 (Method 1, counter bits length=42)")
for _ in range(5):
    uuid7_method1_42 = newnewid.uuid7(
        newnewid.METHOD_1_FIXED_LENGTH_DEDICATED_COUNTER_BITS_42
    )
    print(uuid7_method1_42)
print("")

print("UUIDv7 (Method 1, counter bits length=you need)")
for _ in range(5):
    uuid7_method1_you_need = newnewid.uuid7(
        newnewid.UUID7Option.method_1_fixed_length_dedicated_counter_bits(
            33
        )  # When you need 33 bits
    )
    print(uuid7_method1_you_need)
print("")

print("UUIDv7 (Method 2: Monotonic random, max increment bits length=62)")
for _ in range(5):
    uuid7_method2_62 = newnewid.uuid7(newnewid.METHOD_2_MONOTONIC_RANDOM_62_BITS)
    print(uuid7_method2_62)
print("")

print("UUIDv7 (Method 2: Monotonic random, max increment bits length=you need)")
for _ in range(5):
    uuid7_method2_you_need = newnewid.uuid7(
        newnewid.UUID7Option.method_2_monotonic_random(33)
    )  # When you need 33 bits
    print(uuid7_method2_you_need)
print("")

print("UUIDv7 (Method 3: Re-randomize until monotonic)")
for _ in range(5):
    uuid7_method3 = newnewid.uuid7(newnewid.METHOD_3_RERANDOMIZE_UNTIL_MONOTONIC)
    print(uuid7_method3)
print("")

print(
    "UUIDv7 (Method 4: Replace left most random bits with increased clock precision, "
    + "time fraction bits length=12, counter bits length=0)"
)
for _ in range(5):
    uuid7_method4_12_0 = newnewid.uuid7(
        newnewid.METHOD_4_REPLACE_LEFT_MOST_RANDOM_BITS_WITH_INCREASED_CLOCK_PRECISION_12_BITS
    )
    print(uuid7_method4_12_0)
print("")

print(
    "UUIDv7 (Method 4: Replace left most random bits with increased clock precision, "
    + "time fraction bits length=12, counter bits length=14)"
)
for _ in range(5):
    uuid7_method4_12_14 = newnewid.uuid7(
        newnewid.METHOD_4_REPLACE_LEFT_MOST_RANDOM_BITS_WITH_INCREASED_CLOCK_PRECISION_12_BITS_WITH_COUNTER_14_BITS  # type: ignore
    )
    print(uuid7_method4_12_14)
print("")

print(
    "UUIDv7 (Method 4: Replace left most random bits with increased clock precision, "
    + "time fraction bits length, counter bits length=you_need)"
)
for _ in range(5):
    uuid7_method4_you_need = newnewid.uuid7(
        newnewid.UUID7Option.method_4_replace_left_most_random_bits_with_increased_clock_precision(
            33, 17
        )  # type: ignore
    )
    print(uuid7_method4_you_need)
print("")

print("[NOT RECOMMENDED] UUIDv7 (Method 0: No counter)")
for _ in range(5):
    uuid7_method0 = newnewid.uuid7(newnewid.METHOD_0_NO_COUNTER)
    print(uuid7_method0)
print("")

print("[BONUS TRACK] ULID compatible UUIDv7")
for _ in range(5):
    ulid_compatible = newnewid.ulid_compatible()
    print(ulid_compatible)
print("")

# Generate UUIDv8
import time

print("UUIDv8")
custom_a = 0x00
custom_b = 0x00
custom_c = time.time_ns() & 0x3FFFFFFFFFFFFFFF
uuid8 = newnewid.uuid8(custom_a, custom_b, custom_c)
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
print("UUIDv7 (Millisecond precision)")
uuid7_milli = draft_peabody_dispatch_new_uuid_format_01.uuid7(precision="milli")
print(uuid7_milli)
print("")

# Generate UUIDv7 microsecond precision
print("UUIDv7 (Microsecond precision)")
uuid7_micro = draft_peabody_dispatch_new_uuid_format_01.uuid7(precision="micro")
print(uuid7_micro)
print("")

# Generate UUIDv7 nanosecond precision
print("UUIDv7 (Nanosecond precision)")
uuid7_nano = draft_peabody_dispatch_new_uuid_format_01.uuid7(precision="nano")
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

## Appendix 1: UUIDv7 (>= draft-peabody-dispatch-new-uuid-format-03, <= draft-ietf-uuidrev-rfc4122bis-02) implementation

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

* [When generating two or more UUIDs within one millisecond].
    * Method 1: A fixed length counter of between 12 and 42 bits. Typically, the following versions are available:
        * 12 bits
        * 26 bits
        * 42 bits
    * Method 2: Monotonic random counter.
        * [Must be unguessable] Increment is a random value with a length of 62 bits
        * [May be guessable] Increment is fixed at one
    * Method 3: Implementation convenient monotonic random
    * Method 4: Fractional time field
        * Without counter. Typically, the following versions are available:
            * one microseconds precision: 12 bits
            * one nanoseconds precision: 22 bits
        * With counter. Typically, the following versions are available:
            * one microseconds precision: 12 bits with 14 bits counter
            * one nanoseconds precision: 22 bits with 8 bits counter
* [When generating one or less UUIDs within one millisecond].
    * Method 0: No counter

For systems that require multiple UUIDv7s within the same time period, since `unix_ts_ms` is the same, Method 1, 2, 3 or 4 guarantees monotonicity for the subsequent bits.

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

**Fig 2: UUIDv7 bits layout of Method 1, 12 bits counter field.**

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

**Fig 3: UUIDv7 bits layout of Method 1, 26 bits counter field.**

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

**Fig 4: UUIDv7 bits layout of Method 1, 42 bits counter field.**

In *Method 1*, if `unix_ts_ms` does not change, the counter increments the previous value by one.
When `unix_ts_ms` changes, the counter is reset.
It is important to note that the counter SHOULD be reset using a pseudo-random value, not zero.
This is to ensure ease of guessing.

*Method 2* uses a random number field with guaranteed monotonicity.

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
Similar to Method 1, it uses a pseudo-random value for resetting.
However, the increment value is not one, but a pseudo-random value.
To prevent frequent rollovers, this increment value generates a pseudo-random number with a bit length somewhat smaller than `monotonicity_random`.
The specification does not mention the bit length of `monotonicity_random`, so implementers are free to decide it.
In Fig 5, all `rand_b` bits are assigned to incrementable fields.

Note: The increment value MAY be a fixed value of 1 if unguessability is not required.
This design is similar to the [ULID specification](https://github.com/ulid/spec).
ULID also stores UNIX milliseconds in the most significant 48 bits. The following 80 bits are a monotonicity random counter with an increment value of one.
UUIDv7 of Method 2, which has an increment value of one, is compatible with ULID, although the six bits of `ver` and `var` limit the number of bits that can be used for the counter to 74.

*Method 3* is a method of re-generating pseudo-random numbers until monotonicity is satisfied.
When the created pseudo-random number value is the same as or lower than the previous value, new pseudo-random number value is created.
The process is repeated until the desired pseudo-random number value is generated.

Although Method 3 does not mention bit lengths explicitly, a straightforward interpretation would suggest that the procedure outlined above applies to the 74 bit pseudo-random value.

```text
         0                   1                   2                   3
         0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        |                           unix_ts_ms                          |
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        |          unix_ts_ms           |  ver  |  monotonicity_random  |
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        |var|                    monotonicity_random                    |
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        |                      monotonicity_random                      |
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

**Fig 6: UUIDv7 bits layout of Method 3**

*Method 4* extends the time field.
Following `unix_ts_ms`, which stores time in milliseconds, it can store time values with a precision of less than one millisecond.

The specification does not specify how much precision less than one millisecond is required or how many bits are used for storage.
In actual use cases, the precision may be either one microsecond or one nanosecond.
At least 10 bits are needed to represent everything when one microsecond is used, and 20 bits are needed when one nanosecond is used.
If the field boundary is to be 4 bits while honoring the bit lengths of the other fields, 12 bits should be selected for one microsecond increments and 22 bits for one nanosecond increments.

```text
         0                   1                   2                   3
         0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        |                           unix_ts_ms                          |
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        |          unix_ts_ms           |  ver  |    micro_fraction     |
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        |var|                          random                           |
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        |                            random                             |
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

**Fig 7: UUIDv7 bits layout of Method 4, 1 microseconds precision without counter.**

```text
         0                   1                   2                   3
         0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        |                           unix_ts_ms                          |
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        |          unix_ts_ms           |  ver  |     nano_fraction     |
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        |var|   nano_fraction   |                random                 |
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        |                            random                             |
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

**Fig 8: UUIDv7 bits layout of Method 4, 1 nanoseconds precision without counter.**

Method 4 can also have an additional counter.
The bit length of the counter is also not specified in the specification.
The old specification [draft-peabody-dispatch-new-uuid-format-02](https://datatracker.ietf.org/doc/draft-peabody-dispatch-new-uuid-format/02/) had a counter of 14 bits for 1 microseconds, and an eight bit counter for 1 nanosecond.

```text
         0                   1                   2                   3
         0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        |                           unix_ts_ms                          |
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        |          unix_ts_ms           |  ver  |    micro_fraction     |
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        |var|          counter          |            random             |
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        |                            random                             |
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

**Fig 9: UUIDv7 bits layout of Method 4, 1 microseconds precision with 14 bits counter.**

```text
         0                   1                   2                   3
         0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        |                           unix_ts_ms                          |
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        |          unix_ts_ms           |  ver  |     nano_fraction     |
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        |var|   nano_fraction   |    counter    |        random         |
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        |                            random                             |
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

**Fig 10: UUIDv7 bits layout of Method 4, 1 nanoseconds precision with eight bits counter.**

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

**Fig 11: UUIDv7 bits layout of Method 0.**

Note: "Method 0" is a name I gave for convenience, not something mentioned in the specification. It is a dialectal term.

The difference from Method 2 and 4 is that `random` does nothing to guarantee monotonicity.
Since a pseudo-random value is set each time a UUID is generated, the next value may increase, decrease, or remain the same.

Note: The advantage of Method 0 is that it is stateless and the overall tendency is to expect monotonicity.
While other methods require the last generated UUID to be retained as state, Method 0 does not, simplifying implementation.
Method 0 does not guarantee perfect monotonicity when multiple UUIDs are generated within one millisecond.
When strict monotonicity is not required, however, UUIDv7 in Method 0 will perform well compared to UUIDv1 or UUIDv4.

### Implementations

I investigated which methods are implemented in the UUIDv7 library:

| Name                                                                                             | Language     | Method 1                | Method 2                    | Method 3 | Method 4                | Method 0 | Note                   |
| ------------------------------------------------------------------------------------------------ | ------------ | ----------------------- | --------------------------- | -------- | ----------------------- | -------- | ---------------------- |
| **[quwac/newnewid](https://github.com/quwac/newnewid)**                                          | **Python**   | Yes, all bits supported | Yes, all bits supported     | Yes      | Yes, all bits supported | Yes      |                        |
| [oittaa/uuid6-python](https://github.com/oittaa/uuid6-python)                                    | Python       | No                      | No                          | No       | No                      | Yes      |                        |
| [jdknezek/uuid6-zig](https://github.com/jdknezek/uuid6-zig)                                      | Zig          | No                      | No                          | No       | No                      | Yes      |                        |
| [daegalus/dart-uuid](https://github.com/Daegalus/dart-uuid)                                      | Dart         | No                      | No                          | No       | No                      | Yes      |                        |
| [f4b6a3/uuid-creator](https://github.com/f4b6a3/uuid-creator)                                    | Java         | Yes, 26 bits supported  | Yes, 1 to 63 bits supported | No       | No                      | No       |                        |
| [oittaa/uuid-php](https://github.com/oittaa/uuid-php)                                            | PHP          | No                      | No                          | No       | No                      | Yes      |                        |
| [symfony/uid](https://github.com/symfony/uid/tree/6.2)                                           | PHP          | No                      | Yes, 1 bits supported       | No       | No                      | No       |                        |
| [gofrs/uuid](https://github.com/gofrs/uuid)                                                      | Go           | Yes, 12 bits supported  | No                          | No       | No                      | No       |                        |
| [kjmph/UUID_v7_for_Postgres.sql](https://gist.github.com/kjmph/5bd772b2c2df145aa645b837da7eca74) | Postgres     | No                      | No                          | No       | No                      | Yes      |                        |
| [LiosK/uuidv7](https://github.com/LiosK/uuidv7)                                                  | TypeScript   | Yes, 42 bits supported  | No                          | No       | No                      | No       |                        |
| [kripod/uuidv7](https://github.com/kripod/uuidv7)                                                | TypeScript   | Yes, 12 bits supported  | No                          | No       | No                      | No       | Counter is reset to 0. |
| [fabiolimace/UUIDv7_for_C](https://gist.github.com/fabiolimace/9873fe7bbcb1e6dc40638a4f98676d72) | C            | Yes, 12 bits supported  | Yes, 1 or 8 bits supported  | No       | No                      | Yes      |                        |
| [LiosK/uuidv7-h](https://github.com/LiosK/uuidv7-h)                                              | C/C++        | Yes, 42 bits supported  | No                          | No       | No                      | No       |                        |
| [mareek/UUIDNext](https://github.com/mareek/UUIDNext)                                            | C#           | Yes, 12 bits supported  | No                          | No       | No                      | No       |                        |
| [Medo/Uuid7](https://github.com/medo64/Medo.Uuid7)                                               | C#           | Yes, 26 bits supported  | No                          | No       | No                      | No       |                        |
| [LiosK/uuid7-rs](https://github.com/LiosK/uuid7-rs)                                              | Rust         | Yes, 42 bits supported  | No                          | No       | No                      | No       |                        |
| [DianaNites/nuuid](https://github.com/DianaNites/nuuid)                                          | Rust         | No                      | No                          | No       | No                      | Yes      |                        |
| [jakwings/uuid.sh](https://github.com/jakwings/uuid.sh)                                          | Shell        | Yes, 12 bits supported  | No                          | No       | No                      | No       |                        |
| [x4m/pg_uuid_next](https://github.com/x4m/pg_uuid_next)                                          | C            | No                      | No                          | No       | No                      | Yes      |                        |
| [pluots/udf-suite](https://github.com/pluots/udf-suite/tree/main)                                | MariaDB/MySQ | No                      | No                          | No       | No                      | Yes      |                        |

* The source of the listing is [uuid6/prototypes](https://github.com/uuid6/prototypes).
* I investigated around April 23rd 2023.
* I am not fluent in all languages. [Let me know if I'm wrong.](https://github.com/quwac/newnewid-python/issues)
