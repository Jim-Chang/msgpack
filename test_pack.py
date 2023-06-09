import pytest

import msgpack
from pack import pack


def test_pack_none():
    test_input = None
    expected = b"\xc0"

    ret = pack(test_input)

    assert ret == expected


@pytest.mark.parametrize(
    "test_input,expected",
    [
        (True, b"\xc3"),
        (False, b"\xc2"),
    ],
)
def test_pack_bool(test_input, expected):
    ret = pack(test_input)

    assert ret == expected


@pytest.mark.parametrize(
    "test_input,expected",
    [
        (0, b"\x00"),
        (5, b"\x05"),
        (127, b"\x7f"),
    ],
)
def test_positive_fix_int(test_input, expected):
    ret = pack(test_input)

    assert ret == expected


@pytest.mark.parametrize(
    "test_input,expected",
    [
        (128, b"\xcc\x80"),
        (200, b"\xcc\xc8"),
        (255, b"\xcc\xff"),
    ],
)
def test_uint8(test_input, expected):
    ret = pack(test_input)

    assert ret == expected


@pytest.mark.parametrize(
    "test_input,expected",
    [
        (256, b"\xcd\x01\x00"),
        (20000, b"\xcd\x4e\x20"),
        (65535, b"\xcd\xff\xff"),
    ],
)
def test_uint16(test_input, expected):
    ret = pack(test_input)

    assert ret == expected


@pytest.mark.parametrize(
    "test_input,expected",
    [
        (65536, b"\xce\x00\x01\x00\x00"),
        (100000, b"\xce\x00\x01\x86\xa0"),
        (4294967295, b"\xce\xff\xff\xff\xff"),
    ],
)
def test_uint32(test_input, expected):
    ret = pack(test_input)

    assert ret == expected


@pytest.mark.parametrize(
    "test_input,expected",
    [
        (4294967296, b"\xcf\x00\x00\x00\x01\x00\x00\x00\x00"),
        (10000000000, b"\xcf\x00\x00\x00\x02\x54\x0b\xe4\x00"),
        (18446744073709551615, b"\xcf\xff\xff\xff\xff\xff\xff\xff\xff"),
    ],
)
def test_uint64(test_input, expected):
    ret = pack(test_input)

    assert ret == expected


@pytest.mark.parametrize(
    "test_input,expected",
    [
        (-1, b"\xff"),
        (-10, b"\xf6"),
        (-32, b"\xe0"),
    ],
)
def test_negative_fix_int(test_input, expected):
    ret = pack(test_input)

    assert ret == expected


@pytest.mark.parametrize(
    "test_input,expected",
    [
        (-33, b"\xd0\xdf"),
        (-50, b"\xd0\xce"),
        (-128, b"\xd0\x80"),
    ],
)
def test_int8(test_input, expected):
    ret = pack(test_input)

    assert ret == expected


@pytest.mark.parametrize(
    "test_input,expected",
    [
        (-129, b"\xd1\xff\x7f"),
        (-200, b"\xd1\xff8"),
        (-32768, b"\xd1\x80\x00"),
    ],
)
def test_int16(test_input, expected):
    ret = pack(test_input)

    assert ret == expected


@pytest.mark.parametrize(
    "test_input,expected",
    [
        (-32769, b"\xd2\xff\xff\x7f\xff"),
        (-100000, b"\xd2\xff\xfey`"),
        (-2147483648, b"\xd2\x80\x00\x00\x00"),
    ],
)
def test_int32(test_input, expected):
    ret = pack(test_input)

    assert ret == expected


@pytest.mark.parametrize(
    "test_input,expected",
    [
        (-2147483649, b"\xd3\xff\xff\xff\xff\x7f\xff\xff\xff"),
        (-10000000000, b"\xd3\xff\xff\xff\xfd\xab\xf4\x1c\x00"),
        (-9223372036854775808, b"\xd3\x80\x00\x00\x00\x00\x00\x00\x00"),
    ],
)
def test_int64(test_input, expected):
    ret = pack(test_input)

    assert ret == expected


def test_int_sz_fail():
    with pytest.raises(ValueError):
        pack(18446744073709551616)
        pack(-9223372036854775809)


@pytest.mark.parametrize(
    "test_input,expected",
    [
        (1.1, b"\xca?\x8c\xcc\xcd"),
        (1.11, b"\xca?\x8e\x14{"),
        (-1.1, b"\xca\xbf\x8c\xcc\xcd"),
    ],
)
def test_single_float(test_input, expected):
    ret = pack(test_input, using_single_float=True)

    assert ret == expected


@pytest.mark.parametrize(
    "test_input,expected",
    [
        (1.1, b"\xcb?\xf1\x99\x99\x99\x99\x99\x9a"),
        (1.11, b"\xcb?\xf1\xc2\x8f\(\xf5\xc3"),
        (-1.1, b"\xcb\xbf\xf1\x99\x99\x99\x99\x99\x9a"),
    ],
)
def test_double_float(test_input, expected):
    ret = pack(test_input)

    assert ret == expected


# because following testing data are too long, so we use msgpack.packb to generate expected result
# it's not a good practice, but it's ok for this demo
@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("t", msgpack.packb("t")),
        ("test", msgpack.packb("test")),
        ("t" * 31, msgpack.packb("t" * 31)),
    ],
)
def test_fix_str(test_input, expected):
    ret = pack(test_input)

    assert ret == expected


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("t" * 32, msgpack.packb("t" * 32, use_bin_type=True)),
        ("t" * 150, msgpack.packb("t" * 150, use_bin_type=True)),
        ("t" * 255, msgpack.packb("t" * 255, use_bin_type=True)),
    ],
)
def test_str8(test_input, expected):
    ret = pack(test_input)

    assert ret == expected


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("t" * 256, msgpack.packb("t" * 256, use_bin_type=True)),
        ("t" * 300, msgpack.packb("t" * 300, use_bin_type=True)),
        ("t" * 65535, msgpack.packb("t" * 65535, use_bin_type=True)),
    ],
)
def test_str16(test_input, expected):
    ret = pack(test_input)

    assert ret == expected


@pytest.mark.skip(reason="This test is too slow")
# @pytest.mark.parametrize(
#     "test_input,expected",
#     [
#         ("t"*65536, msgpack.packb("t"*65536, use_bin_type=True)),
#         ("t"*100000, msgpack.packb("t"*100000, use_bin_type=True)),
#         ("t"*4294967295, msgpack.packb("t"*4294967295, use_bin_type=True)),
#     ],
# )
def test_str32(test_input, expected):
    ret = pack(test_input)

    assert ret == expected


@pytest.mark.skip(reason="This test is too slow")
def test_str_sz_fail():
    with pytest.raises(ValueError):
        pack("t" * 4294967296)


@pytest.mark.parametrize(
    "test_input,expected",
    [
        (b"t", msgpack.packb(b"t", use_bin_type=True)),
        (b"t" * 10, msgpack.packb(b"t" * 10, use_bin_type=True)),
        (b"t" * 255, msgpack.packb(b"t" * 255, use_bin_type=True)),
    ],
)
def test_bin8(test_input, expected):
    ret = pack(test_input)

    assert ret == expected


@pytest.mark.parametrize(
    "test_input,expected",
    [
        (b"t" * 256, msgpack.packb(b"t" * 256, use_bin_type=True)),
        (b"t" * 300, msgpack.packb(b"t" * 300, use_bin_type=True)),
        (b"t" * 65535, msgpack.packb(b"t" * 65535, use_bin_type=True)),
    ],
)
def test_bin16(test_input, expected):
    ret = pack(test_input)

    assert ret == expected


@pytest.mark.skip(reason="This test is too slow")
# @pytest.mark.parametrize(
#     "test_input,expected",
#     [
#         (b"t"*65536, msgpack.packb(b"t"*65536, use_bin_type=True)),
#         (b"t"*100000, msgpack.packb(b"t"*100000, use_bin_type=True)),
#         (b"t"*4294967295, msgpack.packb(b"t"*4294967295, use_bin_type=True)),
#     ],
# )
def test_bin32(test_input, expected):
    ret = pack(test_input)

    assert ret == expected


@pytest.mark.skip(reason="This test is too slow")
def test_bin_sz_fail():
    with pytest.raises(ValueError):
        pack(b"t" * 4294967296)


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ([1], msgpack.packb([1])),
        ([1] * 10, msgpack.packb([1] * 10)),
        ([1] * 15, msgpack.packb([1] * 15)),
    ],
)
def test_fix_array(test_input, expected):
    ret = pack(test_input)

    assert ret == expected


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ([1] * 16, msgpack.packb([1] * 16)),
        ([1] * 100, msgpack.packb([1] * 100)),
        ([1] * 65535, msgpack.packb([1] * 65535)),
    ],
)
def test_array16(test_input, expected):
    ret = pack(test_input)

    assert ret == expected


@pytest.mark.skip(reason="This test is too slow")
# @pytest.mark.parametrize(
#     "test_input,expected",
#     [
#         ([1]*65536, msgpack.packb([1]*65536)),
#         ([1]*100000, msgpack.packb([1]*100000)),
#         ([1]*4294967295, msgpack.packb([1]*4294967295)),
#     ],
# )
def test_array32(test_input, expected):
    ret = pack(test_input)

    assert ret == expected


@pytest.mark.skip(reason="This test is too slow")
def test_array_sz_fail():
    with pytest.raises(ValueError):
        pack([1] * 4294967296)


@pytest.mark.parametrize(
    "test_input,expected",
    [
        (
            [1, 1000, "t", "t" * 10, "t" * 1000, b"t", b"t" * 10, b"t" * 1000],
            msgpack.packb(
                [1, 1000, "t", "t" * 10, "t" * 1000, b"t", b"t" * 10, b"t" * 1000],
                use_bin_type=True,
            ),
        ),
        (
            [[1, 2, 3], ["t", "t" * 100], [1, [200, 30000]]],
            msgpack.packb(
                [[1, 2, 3], ["t", "t" * 100], [1, [200, 30000]]], use_bin_type=True
            ),
        ),
    ],
)
def test_general_array(test_input, expected):
    ret = pack(test_input)

    assert ret == expected


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ({1: 1}, msgpack.packb({1: 1})),
        ({1: 1, 2: 2}, msgpack.packb({1: 1, 2: 2})),
        ({i: i for i in range(16)}, msgpack.packb({i: i for i in range(16)})),
    ],
)
def test_fix_map(test_input, expected):
    ret = pack(test_input)

    assert ret == expected


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ({i: i for i in range(17)}, msgpack.packb({i: i for i in range(17)})),
        ({i: i for i in range(100)}, msgpack.packb({i: i for i in range(100)})),
        ({i: i for i in range(65536)}, msgpack.packb({i: i for i in range(65536)})),
    ],
)
def test_map16(test_input, expected):
    ret = pack(test_input)

    assert ret == expected


@pytest.mark.skip(reason="This test is too slow")
# @pytest.mark.parametrize(
#     "test_input,expected",
#     [
#         ({i: i for i in range(65537)}, msgpack.packb({i: i for i in range(65537)})),
#         ({i: i for i in range(100000)}, msgpack.packb({i: i for i in range(100000)})),
#         ({i: i for i in range(4294967296)}, msgpack.packb({i: i for i in range(4294967296)})),
#     ],
# )
def test_map32(test_input, expected):
    ret = pack(test_input)

    assert ret == expected


@pytest.mark.skip(reason="This test is too slow")
def test_map_sz_fail():
    with pytest.raises(ValueError):
        pack({i: i for i in range(4294967297)})


@pytest.mark.parametrize(
    "test_input,expected",
    [
        (
            {"a": "b", "a" * 100: "b" * 100},
            msgpack.packb({"a": "b", "a" * 100: "b" * 100}, use_bin_type=True),
        ),
        (
            {"a": 1, "a" * 100: 100, "b" * 100: 1.111111},
            msgpack.packb(
                {"a": 1, "a" * 100: 100, "b" * 100: 1.111111}, use_bin_type=True
            ),
        ),
        (
            {"a": {"x": 100}, "b": {"y": {"z": 100}}},
            msgpack.packb({"a": {"x": 100}, "b": {"y": {"z": 100}}}, use_bin_type=True),
        ),
    ],
)
def test_general_map(test_input, expected):
    ret = pack(test_input)

    assert ret == expected


def test_general_json_data():
    data = {
        "name": "Jane Smith",
        "age": 25,
        "height": 1.6,
        "hobbies": [
            "reading",
            "painting",
            {"name": "hiking", "location": "mountain"},
            10,
            3.14,
        ],
        "address": {
            "street": "456 Oak Ave",
            "city": "Somewhereville",
            "state": "NY",
            "zip": "67890",
        },
    }
    expected = msgpack.packb(data, use_bin_type=True)

    ret = pack(data)

    assert ret == expected
