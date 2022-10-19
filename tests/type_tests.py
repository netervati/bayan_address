import pytest
from bayan_address.type import (
    get_address_type,
    get_province_related_type,
    is_building_no,
    is_valid_zipcode,
    strip_matching_data,
)


TYPE_PATH = "bayan_address.type."


@pytest.fixture
def mock_cleanstr(mocker):
    return mocker.patch(f"{TYPE_PATH}clean_str")


@pytest.fixture
def mock_isbuildingno(mocker):
    return mocker.patch(f"{TYPE_PATH}is_building_no")


@pytest.fixture
def mock_isvalidzipcode(mocker):
    return mocker.patch(f"{TYPE_PATH}is_valid_zipcode")


@pytest.fixture
def mock_replacestr(mocker):
    return mocker.patch(f"{TYPE_PATH}replace_str")


@pytest.fixture
def monkeypatch_address_format(monkeypatch):
    return monkeypatch.setattr(f"{TYPE_PATH}ADDRESS_FORMAT", {"barangay": ["brgy."]})


@pytest.fixture
def monkeypatch_cities(monkeypatch, cities_fixture):
    return monkeypatch.setattr(f"{TYPE_PATH}CITIES", cities_fixture)


@pytest.fixture
def monkeypatch_provinces(monkeypatch, provinces_fixture):
    return monkeypatch.setattr(f"{TYPE_PATH}PROVINCES", provinces_fixture)


@pytest.mark.parametrize(
    [
        "arg",
        "isbuildingno",
        "isvalidzipcode",
        "addressformat",
        "cleanstr_sideeffect",
        "result",
    ],
    [
        ("24", True, False, [], [], {"building": "24"}),
        ("1000", False, True, [], [], {"zip_code": "1000"}),
        (
            "Test City",
            False,
            False,
            {"city": ["city"]},
            ["test city", "city"],
            {"city": "Test City"},
        ),
        (
            "Fallback",
            False,
            False,
            {"city": ["city"]},
            ["fallback", "city"],
            {"undefined": "Fallback"},
        ),
    ],
)
def test_get_address_type(
    addressformat,
    arg,
    cleanstr_sideeffect,
    isbuildingno,
    isvalidzipcode,
    mock_cleanstr,
    mock_isbuildingno,
    mock_isvalidzipcode,
    monkeypatch,
    result,
):
    mock_isbuildingno.return_value = isbuildingno
    mock_isvalidzipcode.return_value = isvalidzipcode
    monkeypatch.setattr(f"{TYPE_PATH}ADDRESS_FORMAT", addressformat)
    mock_cleanstr.side_effect = cleanstr_sideeffect

    assert get_address_type(arg) == result
    if isbuildingno is False:
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
        ("10", True),
        ("1000", False),
    ],
)
def test_is_building_no(arg, result):
    assert is_building_no(arg) == result


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


@pytest.mark.parametrize(
    ["arg", "cleanstr_sideeffect", "replacestr_sideeffect", "result"],
    [
        (
            "Metro Manila",
            ["metro manila", "province", "", "bayan city"],
            ["", "bayan", ""],
            {
                "pre_selected_formats": {"administrative_region": "Metro Manila"},
                "stripped_address": "",
            },
        ),
        (
            "Province",
            ["province", "province", "", "bayan city"],
            ["", "bayan", ""],
            {"pre_selected_formats": {"province": "Province"}, "stripped_address": ""},
        ),
        (
            "Bayan City",
            ["bayan city", "province", "bayan city", "bayan city", ""],
            ["", "bayan", ""],
            {"pre_selected_formats": {"city": "Bayan City"}, "stripped_address": ""},
        ),
        (
            "Bayan",
            ["bayan", "province", "bayan", "bayan city"],
            ["bayan", "", ""],
            {"pre_selected_formats": {"city": "Bayan"}, "stripped_address": ""},
        ),
    ],
)
def test_strip_matching_data(
    arg,
    cleanstr_sideeffect,
    mock_cleanstr,
    mock_replacestr,
    monkeypatch_cities,
    monkeypatch_provinces,
    replacestr_sideeffect,
    result,
):
    mock_cleanstr.side_effect = cleanstr_sideeffect
    mock_replacestr.side_effect = replacestr_sideeffect

    subject = strip_matching_data(arg)

    assert subject == result
