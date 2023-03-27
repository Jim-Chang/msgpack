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
    ret = pack(test_input, using_single_float=False)

    assert ret == expected


# because following tests strings are too long, so we use msgpack.packb to generate expected result
@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("t", msgpack.packb("t")),
        ("test", msgpack.packb("test")),
        ("t"*31, msgpack.packb("t"*31)),
    ],
)
def test_fix_str(test_input, expected):
    ret = pack(test_input, using_single_float=False)

    assert ret == expected


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("t"*32, msgpack.packb("t"*32, use_bin_type=True)),
        ("t"*150, msgpack.packb("t"*150, use_bin_type=True)),
        ("t"*255, msgpack.packb("t"*255, use_bin_type=True)),
    ],
)
def test_str8(test_input, expected):
    ret = pack(test_input, using_single_float=False)

    assert ret == expected

@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("t"*256, msgpack.packb("t"*256, use_bin_type=True)),
        ("t"*300, msgpack.packb("t"*300, use_bin_type=True)),
        ("t"*65535, msgpack.packb("t"*65535, use_bin_type=True)),
    ],
)
def test_str16(test_input, expected):
    ret = pack(test_input, using_single_float=False)

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
    ret = pack(test_input, using_single_float=False)

    assert ret == expected


@pytest.mark.skip(reason="This test is too slow")
def test_str_sz_fail():
    with pytest.raises(Exception):
        pack("t"*4294967296, using_single_float=False)

