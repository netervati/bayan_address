import pytest
from bayan_address.type import (
    get_address_type,
    get_province_related_type,
    is_valid_zipcode,
)


TYPE_PATH = "bayan_address.type."


@pytest.fixture
def mock_cleanstr(mocker):
    return mocker.patch(f"{TYPE_PATH}clean_str")


@pytest.fixture
def mock_isvalidzipcode(mocker):
    return mocker.patch(f"{TYPE_PATH}is_valid_zipcode")


@pytest.fixture
def monkeypatch_address_format(monkeypatch):
    return monkeypatch.setattr(f"{TYPE_PATH}ADDRESS_FORMAT", {"barangay": ["brgy."]})


@pytest.fixture
def monkeypatch_provinces(monkeypatch, provinces_fixture):
    return monkeypatch.setattr(f"{TYPE_PATH}PROVINCES", provinces_fixture)


@pytest.mark.parametrize(
    ["arg", "isvalidzipcode", "addressformat", "cleanstr_sideeffect", "result"],
    [
        ("1000", True, [], [], {"zip_code": "1000"}),
        (
            "Test City",
            False,
            {"city": ["city"]},
            ["test city", "city"],
            {"city": "Test City"},
        ),
        (
            "Fallback",
            False,
            {"city": ["city"]},
            ["fallback", "city"],
            {"barangay": "Fallback"},
        ),
    ],
)
def test_get_address_type(
    addressformat,
    arg,
    cleanstr_sideeffect,
    isvalidzipcode,
    mock_cleanstr,
    mock_isvalidzipcode,
    monkeypatch,
    result,
):
    mock_isvalidzipcode.return_value = isvalidzipcode
    monkeypatch.setattr(f"{TYPE_PATH}ADDRESS_FORMAT", addressformat)
    mock_cleanstr.side_effect = cleanstr_sideeffect

    assert get_address_type(arg) == result
    mock_isvalidzipcode.assert_called_with(arg)
    if isvalidzipcode is False:
        mock_cleanstr.call_count == 2


@pytest.mark.parametrize(
    ["arg", "cleanstr_sideeffect", "is_successful"],
    [
        ("Sample Fail", ["sample fail", "province"], False),
        ("Province", ["province", "province"], True),
    ],
)
def test_get_province_related_type(
    arg,
    cleanstr_sideeffect,
    mock_cleanstr,
    monkeypatch_provinces,
    provinces_fixture,
    is_successful,
):
    mock_cleanstr.side_effect = cleanstr_sideeffect
    result = provinces_fixture[arg] if is_successful else None

    assert get_province_related_type(arg) == result


@pytest.mark.parametrize(
    ["arg", "result"],
    [
        ("", False),
        ("10", False),
        ("1000", True),
    ],
)
def test_is_valid_zipcode(arg, result):
    assert is_valid_zipcode(arg) == result
