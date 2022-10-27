import pytest
from bayan_address.parser.matchers import (
    match_address_type,
    match_administrative_region,
    match_barangay,
    match_city,
    match_province,
    match_street,
    match_subdivision,
    match_zip_code,
)


MOCK_PATH = "bayan_address.parser.matchers."


@pytest.fixture
def address_fixture():
    return " de la "


@pytest.fixture
def cities_fixture():
    return [
        "Berry",
        "Union City",
    ]


@pytest.fixture
def provinces_fixture():
    return {
        "Faraway": {"island_group": "Upper", "iso": "frwy", "region": "Region B"},
        "La Paz": {"island_group": "Lower", "iso": "la-paz", "region": "Region A"},
    }


@pytest.fixture
def street_format_fixture():
    return [
        "Street",
        "St.",
    ]


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


@pytest.fixture
def mock_matchinbetweenpattern(mocker):
    return mocker.patch(f"{MOCK_PATH}match_in_between_pattern")


@pytest.fixture
def mock_matchpattern(mocker):
    return mocker.patch(f"{MOCK_PATH}match_pattern")


@pytest.fixture
def mock_cleanstr(mocker):
    return mocker.patch(f"{MOCK_PATH}clean_str")


@pytest.fixture
def mock_isvalidstr(mocker):
    return mocker.patch(f"{MOCK_PATH}is_valid_str")


@pytest.fixture
def mock_replacestr(mocker):
    return mocker.patch(f"{MOCK_PATH}replace_str")


@pytest.mark.parametrize(
    ["arg", "mocked_result", "result"],
    [
        (
            "corner st. brgy. ville far city ncr 1000",
            [
                (
                    "corner st. brgy. ville far city 1000",
                    {"administrative_region": "ncr"},
                ),
                None,
                ("corner st. brgy. ville far city", {"zip_code": "1000"}),
                ("corner st. brgy. ville", {"city": "far city"}),
                ("brgy. ville", {"street": "corner st."}),
                None,
                ("", {"barangay": "brgy. ville"}),
            ],
            {
                "administrative_region": "ncr",
                "zip_code": "1000",
                "city": "far city",
                "street": "corner st.",
                "barangay": "brgy. ville",
            },
        ),
        (
            "",
            [
                None,
                None,
                None,
                None,
                None,
                None,
                None,
            ],
            {},
        ),
    ],
)
def test_match_address_type(
    arg,
    mock_matchadministrativeregion,
    mock_matchbarangay,
    mock_matchcity,
    mock_matchprovince,
    mock_matchstreet,
    mock_matchsubdivision,
    mock_matchzipcode,
    mocked_result,
    result,
):
    mock_matchadministrativeregion.return_value = mocked_result[0]
    mock_matchprovince.return_value = mocked_result[1]
    mock_matchzipcode.return_value = mocked_result[2]
    mock_matchcity.return_value = mocked_result[3]
    mock_matchstreet.return_value = mocked_result[4]
    mock_matchsubdivision.return_value = mocked_result[5]
    mock_matchbarangay.return_value = mocked_result[6]

    assert match_address_type(arg) == result


@pytest.mark.parametrize(
    ["arg", "result"],
    [
        ("test", None),
        ("metro manila", ("metro manila", "")),
    ],
)
def test_match_administrative_region(arg, mock_matchpattern, result):
    mock_matchpattern.return_value = result
    match_result = (
        None
        if not result
        else (
            result[1],
            {"administrative_region": result[0]},
        )
    )

    assert match_administrative_region(arg) == match_result
    mock_matchpattern.assert_called_with("metro manila", arg)


@pytest.mark.parametrize(
    ["arg", "isvalidstr"], [("Sample Barangay", True), ("", False)]
)
def test_match_barangay(arg, isvalidstr, mock_isvalidstr):
    mock_isvalidstr.return_value = isvalidstr
    result = None if not isvalidstr else ("", {"barangay": arg.strip()})

    assert match_barangay(arg) == result
    mock_isvalidstr.assert_called_with(arg)


@pytest.mark.parametrize(
    ["arg", "cleanstr", "matchpattern", "replacestr", "result"],
    [
        (
            "Berry",
            ["berry", ""],
            [
                None,
                ("Berry", ""),
            ],
            None,
            ("", {"city": "Berry"}),
        ),
        (
            "Berry Ire City",
            ["berry", "ire city", "union city"],
            [
                None,
                ("Berry", "Ire City"),
                None,
                None,
                None,
            ],
            None,
            None,
        ),
        (
            "Union Faraway",
            ["berry", "union city"],
            [
                None,
                None,
                ("Union City", "Faraway"),
            ],
            None,
            ("Faraway", {"city": "Union"}),
        ),
    ],
)
def test_match_city(
    arg,
    cities_fixture,
    cleanstr,
    matchpattern,
    mock_cleanstr,
    monkeypatch,
    replacestr,
    result,
):
    monkeypatch.setattr(f"{MOCK_PATH}CITIES", cities_fixture)
    mock_cleanstr.side_effect = cleanstr
    mock_matchpattern.side_effect = matchpattern
    mock_replacestr.return_value = replacestr

    assert match_city(arg) == result


@pytest.mark.parametrize(
    ["arg", "matchpattern"],
    [
        (
            "Faraway",
            [
                ("Faraway", ""),
            ],
        ),
        (
            "La Paz",
            [
                None,
                ("La Paz", ""),
            ],
        ),
        (
            "tryst",
            [
                None,
                None,
            ],
        ),
    ],
)
def test_match_province(
    arg, matchpattern, mock_matchpattern, monkeypatch, provinces_fixture
):
    monkeypatch.setattr(f"{MOCK_PATH}PROVINCES", provinces_fixture)
    mock_matchpattern.side_effect = matchpattern

    matched = list(filter(lambda x: x != None, matchpattern))
    if not matched:
        result = None
    else:
        key = matched[0][0]
        result = ("", {"province": key} | provinces_fixture[key])

    assert match_province(arg) == result
    assert mock_matchpattern.call_count == len(matchpattern)


@pytest.mark.parametrize(
    ["arg", "matchinbetweenpattern", "matchpattern", "result"],
    [
        (
            "Corner Street",
            [
                None,
                None,
                None,
                None,
                ("Corner Street", ""),
            ],
            [None],
            ("", {"street": "Corner Street"}),
        ),
        (
            "24 La Porez St.",
            [
                None,
                None,
                ("24 La Porez St.", ""),
            ],
            [("24", "La Porez St.")],
            ("", {"building": "24", "street": "La Porez St."}),
        ),
    ],
)
def test_match_street(
    address_fixture,
    arg,
    matchinbetweenpattern,
    matchpattern,
    mock_matchinbetweenpattern,
    mock_matchpattern,
    result,
    street_format_fixture,
):
    mock_matchinbetweenpattern.side_effect = matchinbetweenpattern
    mock_matchpattern.side_effect = matchpattern

    assert match_street(arg) == result


@pytest.mark.parametrize(
    ["arg", "matchinbetweenpattern"],
    [("Wide Subdivision", ["Wide Subdivision", ""]), ("Dela Santos", None)],
)
def test_match_subdivision(arg, matchinbetweenpattern, mock_matchinbetweenpattern):
    mock_matchinbetweenpattern.return_value = matchinbetweenpattern

    if matchinbetweenpattern:
        result = (matchinbetweenpattern[1], {"subdivision": matchinbetweenpattern[0]})
    else:
        result = matchinbetweenpattern

    assert match_subdivision(arg) == result


@pytest.mark.parametrize(
    ["arg", "matchpattern"],
    [("1000", ["1000", ""]), ("Faraway", None)],
)
def test_match_zip_code(arg, matchpattern, mock_matchpattern):
    mock_matchpattern.return_value = matchpattern

    if matchpattern:
        result = (matchpattern[1], {"zip_code": matchpattern[0]})
    else:
        result = matchpattern

    assert match_zip_code(arg) == result
