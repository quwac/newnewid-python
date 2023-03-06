from datetime import datetime

from assert_uuid import assert_uuid
from const import TEST_CLOCK
from frozen_clock import FrozenClock
from frozen_pseudo_random_generator import FrozenPseudoRandomGenerator

import newnewid
from newnewid import UUID, UUID7Option


class TestUUID7:
    def test_uuid7(self):
        uuid = newnewid.uuid7()
        assert uuid.version == 7
        assert uuid.variant == newnewid.RFC_4122

    def test_uuid7_generator(self):
        cbl = 12
        pseudo_random_generator = FrozenPseudoRandomGenerator(
            counter_reset=3267,
            random_binary=1784793296645077391,
        )
        uuid7_option = UUID7Option.method_1_fixed_length_dedicated_counter_bits(cbl)
        generator = newnewid.UUID7Generator(
            uuid7_option=uuid7_option,
            clock=TEST_CLOCK,
            pseudo_random_generator=pseudo_random_generator,
        )
        actual = generator.generate()
        expected = UUID("017F22E2-79B0-7CC3-98C4-DC0C0C07398F")
        assert_uuid(actual, expected, newnewid.UUID7Generator, uuid7_option=uuid7_option)

    def test_uuid7_monocity(self):
        cbl = 12
        pseudo_random_generator = FrozenPseudoRandomGenerator(
            counter_reset=3267,
            random_binary=[1784793296645077391, 4660],
        )
        uuid7_option = UUID7Option.method_1_fixed_length_dedicated_counter_bits(cbl)
        generator = newnewid.UUID7Generator(
            uuid7_option=uuid7_option,
            clock=TEST_CLOCK,
            pseudo_random_generator=pseudo_random_generator,
        )
        actual1 = generator.generate()
        assert_uuid(
            actual1,
            UUID("017F22E2-79B0-7CC3-98C4-DC0C0C07398F"),
            newnewid.UUID7Generator,
            uuid7_option=uuid7_option,
        )
        actual2 = generator.generate()
        assert_uuid(
            actual2,
            UUID("017F22E2-79B0-7CC4-8000-000000001234"),
            newnewid.UUID7Generator,
            uuid7_option=uuid7_option,
        )

    def test_uuid7s(self):
        cbl = 26
        test_cases = [
            {
                "uuid": "000020b7-bd03-75d0-8000-000df0b725d0",
                "time": "1970-01-07T08:28:32.387000",
                "seq": "24379392",
                "rand": "59873109456",
            },
            {
                "uuid": "000192d6-60d4-77bf-8000-0014689777bf",
                "time": "1970-03-20T05:21:30.324000",
                "seq": "32489472",
                "rand": "87654102975",
            },
            {
                "uuid": "00009e84-7e52-7791-8000-0012620b5791",
                "time": "1970-01-31T18:44:43.218000",
                "seq": "31735808",
                "rand": "78954321809",
            },
            {
                "uuid": "00021da7-391a-789a-8000-00058d6d789a",
                "time": "1970-04-16T04:17:12.986000",
                "seq": "36077568",
                "rand": "23847598234",
            },
            {
                "uuid": "0002d0f7-ee76-71d5-8000-00160501d1d5",
                "time": "1970-05-20T23:57:23.958000",
                "seq": "7684096",
                "rand": "94573285845",
            },
            {
                "uuid": "0000ad5a-4780-7ba3-8000-000890885ba3",
                "time": "1970-02-03T15:52:54.912000",
                "seq": "48807936",
                "rand": "36784593827",
            },
            {
                "uuid": "00020ebe-5969-7371-8000-001242c0e371",
                "time": "1970-04-13T06:48:10.345000",
                "seq": "14434304",
                "rand": "78429348721",
            },
            {
                "uuid": "0000ac7b-1bf6-767d-8000-0016e79b167d",
                "time": "1970-02-03T11:49:09.238000",
                "seq": "27213824",
                "rand": "98374981245",
            },
            {
                "uuid": "0001e2b2-9556-7a9a-8000-000662596a9a",
                "time": "1970-04-04T17:32:01.750000",
                "seq": "44466176",
                "rand": "27419830938",
            },
            {
                "uuid": "00043ee3-c444-74f8-8000-00112493b4f8",
                "time": "1970-07-31T01:16:23.492000",
                "seq": "20840448",
                "rand": "73628103928",
            },
            {
                "uuid": "018716c6-7343-7def-9234-567890abcdef",
                "time": "2023-03-25T03:18:37.123000",
                "seq": "58446388",
                "rand": "95075823242735",
            },
            {
                "uuid": "00000000-0000-7000-8001-000000000000",
                "time": "1970-01-01T00:00:00",
                "seq": "1",
                "rand": "0",
            },
            {
                "uuid": "01f3ffff-ffff-7def-9234-567890abcdef",
                "time": "2038-01-19T03:14:07.999000",
                "seq": "58446388",
                "rand": "95075823242735",
            },
            {
                "uuid": "01f40000-0000-7def-9234-567890abcdef",
                "time": "2038-01-19T03:14:08",
                "seq": "58446388",
                "rand": "95075823242735",
            },
        ]
        for test_case in test_cases:
            expected = UUID(test_case["uuid"])
            time = datetime.fromisoformat(test_case["time"])
            clock = FrozenClock.from_datetime(time)
            pseudo_random_generator = FrozenPseudoRandomGenerator(
                counter_reset=int(test_case["seq"]), random_binary=int(test_case["rand"])
            )

            generator = newnewid.UUID7Generator(
                uuid7_option=UUID7Option.method_1_fixed_length_dedicated_counter_bits(cbl),
                clock=clock,
                pseudo_random_generator=pseudo_random_generator,
            )
            actual = generator.generate()
            assert_uuid(actual, expected, newnewid.UUID7Generator)
