import pytest
from bayan_address.lib.utils import clean_str, is_valid_str


@pytest.mark.parametrize(
    ["arg", "result"],
    [
        ("Bayan", "bayan"),
        ("BAYAN", "bayan"),
        ("Bayan Address", "bayan address"),
        (" Bayan Address ", "bayan address"),
        (" Bayan  Address ", "bayan  address"),
    ],
)
def test_clear_str(arg, result):
    assert clean_str(arg) == result


@pytest.mark.parametrize(
    ["arg", "result"],
    [
        (True, False),
        (1, False),
        ({}, False),
        ("", False),
        ("Valid String", True),
    ],
)
def test_is_valid_str(arg, result):
    assert is_valid_str(arg) == result
