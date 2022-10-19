import pytest
from bayan_address.parser import BayanAddress, Parser
from bayan_address.lib.errors import InvalidValue


PARSER_ERROR_MSG = "The address has no such value."
PARSER_PATH = "bayan_address.parser."


@pytest.fixture
def mock_cleanstr(mocker):
    return mocker.patch(f"{PARSER_PATH}clean_str")


@pytest.fixture
def mock_concatstr(mocker):
    return mocker.patch(f"{PARSER_PATH}concat_str")


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
def mock_replacestr(mocker):
    return mocker.patch(f"{PARSER_PATH}replace_str")


@pytest.fixture
def mock_stripmatchingdata(mocker):
    return mocker.patch(f"{PARSER_PATH}strip_matching_data")


@pytest.fixture
def mock_parser(mocker):
    return mocker.patch(f"{PARSER_PATH}Parser.run")


@pytest.fixture
def monkeypatch_addressprefix(monkeypatch, address_prefix_fixture):
    return monkeypatch.setattr(f"{PARSER_PATH}ADDRESS_PREFIX", address_prefix_fixture)


@pytest.fixture
def monkeypatch_provinces(monkeypatch, provinces_fixture):
    return monkeypatch.setattr(f"{PARSER_PATH}PROVINCES", provinces_fixture)


@pytest.mark.parametrize(
    [
        "arg",
        "pre_selected_formats",
        "stripped_address",
        "replacestr_sideeffect",
        "cleanstr_sideeffect",
        "getaddresstype",
        "concatstr_sideeffect",
        "isvalidstr",
        "result",
    ],
    [
        (
            "",
            {},
            "",
            [""],
            ["de"],
            {"undefined": ""},
            [""],
            False,
            {},
        ),
    ],
)
def test_parser_run(
    arg,
    cleanstr_sideeffect,
    concatstr_sideeffect,
    getaddresstype,
    isvalidstr,
    mock_cleanstr,
    mock_concatstr,
    mock_getaddresstype,
    mock_isvalidstr,
    mock_replacestr,
    mock_stripmatchingdata,
    monkeypatch_addressprefix,
    pre_selected_formats,
    replacestr_sideeffect,
    result,
    stripped_address,
):
    mock_stripmatchingdata.return_value = {
        "pre_selected_formats": pre_selected_formats,
        "stripped_address": stripped_address,
    }
    mock_replacestr.side_effect = replacestr_sideeffect
    mock_cleanstr.side_effect = cleanstr_sideeffect
    mock_getaddresstype.return_value = getaddresstype
    mock_concatstr.side_effect = concatstr_sideeffect
    mock_isvalidstr.return_value = isvalidstr

    assert Parser(arg).run() == result


def test_bayan_address_init(
    mock_isvalidstr,
    mock_parser,
    parsed_address_fixture,
):
    with pytest.raises(InvalidValue):
        mock_isvalidstr.return_value = False
        BayanAddress(1)

    arg = "test_value"
    mock_isvalidstr.return_value = True
    mock_parser.return_value = parsed_address_fixture

    assert BayanAddress(arg).parsed_address == parsed_address_fixture
    mock_isvalidstr.assert_called_with(arg)
    mock_parser.assert_called


def test_bayan_address_getprop(
    mock_isvalidstr,
    mock_parser,
    parsed_address_fixture,
):
    arg = "test_value"
    data_city = parsed_address_fixture["city"]
    mock_isvalidstr.return_value = True
    mock_parser.return_value = {"city": data_city}
    subject = BayanAddress(arg)

    assert subject.getprop("barangay") == PARSER_ERROR_MSG
    assert subject.getprop("city") == data_city
    mock_isvalidstr.assert_called_with(arg)
    mock_parser.assert_called()


def test_bayan_address_getsprop(
    mock_getprovincerelatedtype,
    mock_isvalidstr,
    mock_parser,
    monkeypatch_provinces,
    parsed_address_fixture,
    provinces_fixture,
):
    arg_1 = "Province"
    arg_propkey = "region"
    data_region = "Region A"
    mock_isvalidstr.return_value = True
    mock_parser.return_value = parsed_address_fixture
    subject = BayanAddress("Province")

    assert subject.getsprop("key") == PARSER_ERROR_MSG
    assert subject.getsprop(arg_propkey) == data_region
    mock_isvalidstr.assert_called_with(arg_1)
    mock_parser.assert_called()

    arg_2 = "Province B"
    parsed_address_fixture["province"] = arg_2
    mock_getprovincerelatedtype.return_value = provinces_fixture["Province"]

    assert BayanAddress(arg_2).getsprop(arg_propkey) == data_region
    mock_isvalidstr.assert_called_with(arg_2)
    mock_parser.assert_called()
    mock_getprovincerelatedtype.assert_called_once()

    mock_getprovincerelatedtype.return_value = None
    assert (
        BayanAddress(arg_2).getsprop(arg_propkey)
        == f"The address has no valid province to check it's {arg_propkey}."
    )


def test_bayan_address_properties(
    address_format_fixture,
    mock_getprovincerelatedtype,
    mock_isvalidstr,
    mock_parser,
    monkeypatch_provinces,
    parsed_address_fixture,
    provinces_fixture,
):
    arg = ""
    for _, v in parsed_address_fixture.items():
        arg += f", {v}"

    data_province = provinces_fixture[parsed_address_fixture["province"]]
    mock_isvalidstr.return_value = True
    mock_parser.return_value = parsed_address_fixture
    mock_getprovincerelatedtype.return_value = data_province
    subject_1 = BayanAddress(arg)

    assert subject_1.parsed_address == parsed_address_fixture
    for el in address_format_fixture:
        assert getattr(subject_1, el) == parsed_address_fixture[el]
    province_related_types = data_province
    assert subject_1.island_group == province_related_types["island_group"]
    assert subject_1.iso == province_related_types["iso"]
    assert subject_1.region == province_related_types["region"]
