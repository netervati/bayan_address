import pytest
from bayan_address.parser.core import (
    BayanAddress,
    get_province_related_type,
    InvalidValue,
)


MOCK_PATH = "bayan_address.parser.core."


@pytest.fixture
def provinces_fixture():
    return {"La Paz": {"island_group": "Lower", "iso": "la-paz", "region": "Region A"}}


@pytest.fixture
def mock_cleanstr(mocker):
    return mocker.patch(f"{MOCK_PATH}clean_str")


@pytest.fixture
def mock_getprovincerelatedtype(mocker):
    return mocker.patch(f"{MOCK_PATH}get_province_related_type")


@pytest.fixture
def mock_isvalidstr(mocker):
    return mocker.patch(f"{MOCK_PATH}is_valid_str")


@pytest.fixture
def mock_matchaddresstype(mocker):
    return mocker.patch(f"{MOCK_PATH}match_address_type")


@pytest.fixture
def monkpatch_provinces(monkeypatch, provinces_fixture):
    return monkeypatch.setattr(f"{MOCK_PATH}PROVINCES", provinces_fixture)


@pytest.mark.parametrize(
    ["arg", "cleanstr", "matched"],
    [
        ("La Paz", ("la paz", "la paz"), True),
        ("Dela Paz", ("la paz", "dela paz"), False),
        ("Dela Pazco", ("la paz", "dela pazco"), False),
    ],
)
def test_get_province_related_type(
    arg, cleanstr, matched, mock_cleanstr, monkpatch_provinces, provinces_fixture
):
    mock_cleanstr.side_effect = cleanstr
    result = provinces_fixture[arg] if matched else None

    assert get_province_related_type(arg) == result


@pytest.mark.parametrize(
    ["arg", "isvalidstr", "matchaddresstype", "getprovincerelatedtype"],
    [
        (
            "Sample City La Paz",
            True,
            {"city": "Sample City", "province": "La Paz"},
            None,
        ),
        (
            "sample city la paz",
            True,
            {"city": "sample city", "province": "la paz"},
            "La Paz",
        ),
        (
            "Sample City",
            True,
            {"city": "Sample City"},
            None,
        ),
    ],
)
def test_bayan_address(
    arg,
    getprovincerelatedtype,
    isvalidstr,
    matchaddresstype,
    mock_getprovincerelatedtype,
    mock_isvalidstr,
    mock_matchaddresstype,
    monkpatch_provinces,
    provinces_fixture,
):
    mock_isvalidstr.return_value = isvalidstr

    if isvalidstr is False:
        with pytest.raises(InvalidValue):
            BayanAddress(arg)
    else:
        mock_matchaddresstype.return_value = matchaddresstype
        extra_types = {}
        if "province" in matchaddresstype:
            if getprovincerelatedtype:
                extra_types = provinces_fixture[getprovincerelatedtype]
                mock_getprovincerelatedtype.return_value = extra_types
            else:
                extra_types = provinces_fixture[matchaddresstype["province"]]

        subject = BayanAddress(arg)
        result = matchaddresstype | extra_types

        assert subject.parsed_address == result
        if getprovincerelatedtype:
            mock_getprovincerelatedtype.assert_called()
        else:
            mock_getprovincerelatedtype.assert_not_called()
