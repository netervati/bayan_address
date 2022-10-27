import pytest
from bayan_address.parser.core import (
    BayanAddress,
    InvalidValue,
)


MOCK_PATH = "bayan_address.parser.core."


@pytest.fixture
def mock_cleanstr(mocker):
    return mocker.patch(f"{MOCK_PATH}clean_str")


@pytest.fixture
def mock_isvalidstr(mocker):
    return mocker.patch(f"{MOCK_PATH}is_valid_str")


@pytest.fixture
def mock_matchaddresstype(mocker):
    return mocker.patch(f"{MOCK_PATH}match_address_type")


@pytest.fixture
def mock_replacestr(mocker):
    return mocker.patch(f"{MOCK_PATH}replace_str")


@pytest.mark.parametrize(
    ["arg", "isvalidstr", "replacestr", "matchaddresstype"],
    [
        (
            "  24 Test Street, Brgy. Lorem, Ipsum City, Somewhere Province, 8000  ",
            True,
            "  24 Test Street Brgy. Lorem Ipsum City Somewhere Province 8000  ",
            {
                "building": "24",
                "barangay": "Brgy. Lorem",
                "city": "Ipsum City",
                "province": "Somewhere Province",
                "zip_code": "8000",
            },
        ),
        (
            "  24   Test Street,   Brgy. Lorem, Ipsum City  , Somewhere   Province, 8000  ",
            True,
            "  24   Test Street   Brgy. Lorem Ipsum City   Somewhere   Province 8000  ",
            {
                "building": "24",
                "barangay": "Brgy. Lorem",
                "city": "Ipsum City",
                "province": "Somewhere Province",
                "zip_code": "8000",
            },
        ),
    ],
)
def test_bayan_address(
    arg,
    isvalidstr,
    matchaddresstype,
    mock_isvalidstr,
    mock_matchaddresstype,
    mock_replacestr,
    replacestr,
):
    mock_isvalidstr.return_value = isvalidstr

    if isvalidstr is False:
        with pytest.raises(InvalidValue):
            BayanAddress(arg)
        return

    mock_replacestr.return_value = replacestr
    mock_matchaddresstype.return_value = matchaddresstype

    assert BayanAddress(arg).parsed_address == matchaddresstype
    mock_matchaddresstype.assert_called_with(replacestr.strip())
