class TestSample:
    def test_sample(self):
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

        assert True

    def test_old_sample(self):
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

    def test_parse_uuid(self):
        import newnewid
        from newnewid.parser.uuid_parser import parse

        parsed = parse(newnewid.UUID("2cf1c828-dc02-11ed-b270-0242ac110002"))
        print(f"parsed {parsed}")
