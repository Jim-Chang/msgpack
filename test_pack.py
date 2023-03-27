import pytest

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
