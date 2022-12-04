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
def mock_replacestr(mocker):
    return mocker.patch(f"{MOCK_PATH}replace_str")


@pytest.fixture
def mock_matchadministrativeregion(mocker):
    return mocker.patch(f"{MOCK_PATH}match_administrative_region")


@pytest.fixture
def mock_matchprovince(mocker):
    return mocker.patch(f"{MOCK_PATH}match_province")


@pytest.fixture
def mock_matchzipcode(mocker):
    return mocker.patch(f"{MOCK_PATH}match_zip_code")


@pytest.fixture
def mock_matchcity(mocker):
    return mocker.patch(f"{MOCK_PATH}match_city")


@pytest.fixture
def mock_matchstreet(mocker):
    return mocker.patch(f"{MOCK_PATH}match_street")


@pytest.fixture
def mock_matchsubdivision(mocker):
    return mocker.patch(f"{MOCK_PATH}match_subdivision")


@pytest.fixture
def mock_matchbarangay(mocker):
    return mocker.patch(f"{MOCK_PATH}match_barangay")


@pytest.mark.parametrize(
    ["arg", "isvalidstr", "replacestr", "mockedresult", "parsedaddress"],
    [
        (
            "  24 Test Street, Brgy. Lorem, Ipsum City, Somewhere Province, 8000  ",
            True,
            "  24 Test Street Brgy. Lorem Ipsum City Somewhere Province 8000  ",
            [
                None,
                ("24 Test Street Brgy. Lorem Ipsum City 8000", {"province": "Somewhere Province"}),
                ("24 Test Street Brgy. Lorem Ipsum City", {"zip_code": "8000"}),
                ("24 Test Street Brgy. Lorem", {"city": "Ipsum City"}),
                ("Brgy. Lorem", {"building": "24", "street": "Test Street"}),
                None,
                ("", {"barangay": "Brgy. Lorem"}),
            ],
            {
                "building": "24",
                "barangay": "Brgy. Lorem",
                "city": "Ipsum City",
                "province": "Somewhere Province",
                "street": "Test Street",
                "zip_code": "8000",
            },
        ),
    ],
)
def test_bayan_address(
    arg,
    isvalidstr,
    mock_isvalidstr,
    mock_matchadministrativeregion,
    mock_matchbarangay,
    mock_matchcity,
    mock_matchprovince,
    mock_matchstreet,
    mock_matchsubdivision,
    mock_matchzipcode,
    mock_replacestr,
    mockedresult,
    parsedaddress,
    replacestr,
):
    mock_isvalidstr.return_value = isvalidstr

    if isvalidstr is False:
        with pytest.raises(InvalidValue):
            BayanAddress(arg)
        return

    mock_replacestr.return_value = replacestr

    mock_matchadministrativeregion.return_value = mockedresult[0]
    mock_matchprovince.return_value = mockedresult[1]
    mock_matchzipcode.return_value = mockedresult[2]
    mock_matchcity.return_value = mockedresult[3]
    mock_matchstreet.return_value = mockedresult[4]
    mock_matchsubdivision.return_value = mockedresult[5]
    mock_matchbarangay.return_value = mockedresult[6]

    assert BayanAddress(arg).parsed_address == parsedaddress
