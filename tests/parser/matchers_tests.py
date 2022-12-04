import pytest
from collections import namedtuple
from bayan_address.parser.matchers import (
    match_administrative_region,
    match_barangay,
    match_city,
    match_province,
    match_street,
    match_subdivision,
    match_zip_code,
)


MOCK_PATH = "bayan_address.parser.matchers."
MatchResult = namedtuple("MatchResult", "address_type stripped")


@pytest.fixture
def address_fixture():
    return ["", "de", "la"]


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
    ["arg", "result"],
    [
        ("test", None),
        ("metro manila", MatchResult("metro manila", "")),
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
            [""],
            [
                None,
                MatchResult("Berry", ""),
            ],
            None,
            ("", {"city": "Berry"}),
        ),
        (
            "Berry Ire City",
            ["ire city", "berry", "union city"],
            [
                None,
                MatchResult("Berry", "Ire City"),
                None,
                None,
                None,
            ],
            None,
            None,
        ),
        (
            "Union Faraway",
            ["berry", "union city", "union city"],
            [
                None,
                None,
                MatchResult("Union City", "Faraway"),
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
    ["arg", "matchpattern", "ismatched"],
    [
        (
            "Faraway",
            [
                None,
                None,
                MatchResult("Faraway", ""),
            ],
            True,
        ),
        (
            "La Paz",
            [
                None,
                None,
                None,
                None,
                None,
                MatchResult("La Paz", ""),
            ],
            True,
        ),
        (
            "Faraway city",
            [
                MatchResult("Faraway city", ""),
            ],
            False,
        ),
        (
            "tryst",
            [
                None,
                None,
                None,
                None,
                None,
                None,
            ],
            False,
        ),
    ],
)
def test_match_province(
    arg, ismatched, matchpattern, mock_matchpattern, monkeypatch, provinces_fixture
):
    monkeypatch.setattr(f"{MOCK_PATH}PROVINCES", provinces_fixture)
    mock_matchpattern.side_effect = matchpattern

    result = None if not ismatched else ("", {"province": arg} | provinces_fixture[arg])

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
                MatchResult("Corner Street", ""),
            ],
            [None],
            ("", {"street": "Corner Street"}),
        ),
        (
            "24 La Porez St.",
            [
                None,
                None,
                MatchResult("24 La Porez St.", ""),
            ],
            [MatchResult("24", "La Porez St.")],
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
    monkeypatch,
    result,
    street_format_fixture,
):
    monkeypatch.setattr(f"{MOCK_PATH}ADDRESS_PREFIX", address_fixture)
    mock_matchinbetweenpattern.side_effect = matchinbetweenpattern
    mock_matchpattern.side_effect = matchpattern

    assert match_street(arg) == result


@pytest.mark.parametrize(
    ["arg", "matchinbetweenpattern"],
    [("Wide Subdivision", MatchResult("Wide Subdivision", "")), ("Dela Santos", None)],
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
    [("1000", MatchResult("1000", "")), ("Faraway", None)],
)
def test_match_zip_code(arg, matchpattern, mock_matchpattern):
    mock_matchpattern.return_value = matchpattern

    if matchpattern:
        result = (matchpattern[1], {"zip_code": matchpattern[0]})
    else:
        result = matchpattern

    assert match_zip_code(arg) == result
