import pytest
from bayan_address import BayanAddress
from bayan_address.lib.errors import InvalidValue


PARSER_ERROR_MSG = "The address has no such value."
PARSER_PATH = "bayan_address.parser."


@pytest.fixture
def mock_isvalidstr(mocker):
    return mocker.patch(f"{PARSER_PATH}is_valid_str")


@pytest.fixture
def mock_getaddresstype(mocker):
    return mocker.patch(f"{PARSER_PATH}get_address_type")


@pytest.fixture
def mock_getprovincerelatedtype(mocker):
    return mocker.patch(f"{PARSER_PATH}get_province_related_type")


@pytest.fixture
def monkeypatch_address_format(monkeypatch, address_format_fixture):
    return monkeypatch.setattr(f"{PARSER_PATH}ADDRESS_FORMAT", address_format_fixture)


@pytest.fixture
def monkeypatch_provinces(monkeypatch, provinces_fixture):
    return monkeypatch.setattr(f"{PARSER_PATH}PROVINCES", provinces_fixture)


def test_bayan_address_init(
    mock_getaddresstype,
    mock_isvalidstr,
    monkeypatch_address_format,
    parsed_address_fixture,
):
    with pytest.raises(InvalidValue):
        mock_isvalidstr.return_value = False
        BayanAddress(1)

    arg = "test_value"
    mock_isvalidstr.return_value = True
    mock_getaddresstype.return_value = parsed_address_fixture

    assert BayanAddress(arg).parsed_address == parsed_address_fixture
    mock_isvalidstr.assert_called_with(arg)
    mock_getaddresstype.assert_called_with(arg)


@pytest.mark.parametrize(
    ["arg", "count"],
    [
        ("Brgy. Test, Test City", 2),
        ("Test Dr., Brgy. Test, Test City, Test Province", 4),
        ("Test Dr., Brgy. Test, Test City, Test Province, 1111", 5),
    ],
)
def test_bayan_address_init_split(
    arg,
    count,
    mock_getaddresstype,
    mock_isvalidstr,
    monkeypatch_address_format,
):
    mock_isvalidstr.return_value = True
    mock_getaddresstype.return_value = {}
    BayanAddress(arg)

    assert mock_getaddresstype.call_count == count
    mock_isvalidstr.assert_called_with(arg)


def test_bayan_address_getprop(
    mock_getaddresstype,
    mock_isvalidstr,
    monkeypatch_address_format,
    parsed_address_fixture,
):
    arg = "test_value"
    data_city = parsed_address_fixture["city"]
    mock_isvalidstr.return_value = True
    mock_getaddresstype.return_value = {"city": data_city}
    subject = BayanAddress(arg)

    assert subject.getprop("barangay") == PARSER_ERROR_MSG
    assert subject.getprop("city") == data_city
    mock_isvalidstr.assert_called_with(arg)
    mock_getaddresstype.assert_called_with(arg)


def test_bayan_address_getsprop(
    mock_getaddresstype,
    mock_getprovincerelatedtype,
    mock_isvalidstr,
    monkeypatch_address_format,
    monkeypatch_provinces,
    parsed_address_fixture,
    provinces_fixture,
):
    arg_1 = "Province"
    arg_propkey = "region"
    data_region = "Region A"
    mock_isvalidstr.return_value = True
    mock_getaddresstype.return_value = parsed_address_fixture
    subject = BayanAddress("Province")

    assert subject.getsprop("key") == PARSER_ERROR_MSG
    assert subject.getsprop(arg_propkey) == data_region
    mock_isvalidstr.assert_called_with(arg_1)
    mock_getaddresstype.assert_called_with(arg_1)

    arg_2 = "Province B"
    parsed_address_fixture["province"] = arg_2
    mock_getprovincerelatedtype.return_value = provinces_fixture["Province"]

    assert BayanAddress(arg_2).getsprop(arg_propkey) == data_region
    mock_isvalidstr.assert_called_with(arg_2)
    mock_getaddresstype.assert_called_with(arg_2)
    mock_getprovincerelatedtype.assert_called_once()

    mock_getprovincerelatedtype.return_value = None
    assert (
        BayanAddress(arg_2).getsprop(arg_propkey)
        == f"The address has no valid province to check it's {arg_propkey}."
    )


def test_bayan_address_properties(
    address_format_fixture,
    mock_getaddresstype,
    mock_getprovincerelatedtype,
    mock_isvalidstr,
    monkeypatch_address_format,
    monkeypatch_provinces,
    parsed_address_fixture,
    provinces_fixture,
):
    arg = ""
    for _, v in parsed_address_fixture.items():
        arg += f", {v}"

    data_province = provinces_fixture[parsed_address_fixture["province"]]
    mock_isvalidstr.return_value = True
    mock_getaddresstype.return_value = parsed_address_fixture
    mock_getprovincerelatedtype.return_value = data_province
    subject_1 = BayanAddress(arg)

    assert subject_1.parsed_address == parsed_address_fixture
    for el in address_format_fixture:
        assert getattr(subject_1, el) == parsed_address_fixture[el]
    province_related_types = data_province
    assert subject_1.island_group == province_related_types["island_group"]
    assert subject_1.iso == province_related_types["iso"]
    assert subject_1.region == province_related_types["region"]
