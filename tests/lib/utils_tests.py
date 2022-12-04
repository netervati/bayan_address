import pytest
from bayan_address.lib.utils import (
    clean_str,
    match_in_between_pattern,
    match_pattern,
    is_valid_str,
    replace_str,
)


MOCK_PATH = "bayan_address.lib.utils."


@pytest.fixture
def mock_replacestr(mocker):
    return mocker.patch(f"{MOCK_PATH}replace_str")


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
        ("  ", False),
        ("Valid String", True),
    ],
)
def test_is_valid_str(arg, result):
    assert is_valid_str(arg) == result


@pytest.mark.parametrize(
    ["arg1", "arg2", "before", "after", "replacestr", "result"],
    [
        (
            r"\b{}(.*?){}+\b".format("Dela", "St."),
            "Dela Cruz St. Sample City",
            "Dela",
            "St.",
            "Sample City",
            ("Dela Cruz St.", "Sample City"),
        ),
        # TODO: Identify the issue with non-alphanumeric characters
        # (in this case, period)
        (
            r"\b{}(.*?){}+\b".format("Dela", "St."),
            "Dela Cruz Street Sample City",
            "Dela",
            "Street",
            "Dela Cruz Street Sample City",
            ("Dela Cruz Street", "Dela Cruz Street Sample City"),
        ),
        (
            r"\b{}(.*?){}+\b".format("Dela", "St."),
            "Mandela Cruz St. Sample City",
            None,
            None,
            None,
            None,
        ),
    ],
)
def test_match_in_between_pattern(
    after, arg1, arg2, before, mock_replacestr, replacestr, result
):
    mock_replacestr.return_value = replacestr

    assert match_in_between_pattern(arg1, arg2, before=before, after=after) == result
    if result is None:
        mock_replacestr.assert_not_called()
    else:
        mock_replacestr.assert_called_once()


@pytest.mark.parametrize(
    ["arg1", "arg2", "replacestr", "result"],
    [
        (r"\d{4}", "Sample City 1000", "Sample City", ("1000", "Sample City")),
        (
            "metro manila",
            "Sample City Metro Manila",
            "Sample City",
            ("Metro Manila", "Sample City"),
        ),
        (
            "san pablo",
            "Test Drive San pablo 1000 Sample City",
            "Test Drive  1000 Sample City",
            ("San pablo", "Test Drive  1000 Sample City"),
        ),
        (
            "dela cruz",
            "Test Drive La Cruz Dela Silva",
            None,
            None,
        ),
        # TODO: Utilize raw string to match
        # exact argument
        (
            "la cruz",
            "Test Drive Dela Cruz",
            "Test Drive Dela Cruz",
            ("la Cruz", "Test Drive Dela Cruz"),
        ),
    ],
)
def test_match_pattern(arg1, arg2, mock_replacestr, replacestr, result):
    mock_replacestr.return_value = replacestr

    assert match_pattern(arg1, arg2) == result
    if result is None:
        mock_replacestr.assert_not_called()
    else:
        mock_replacestr.assert_called_once()


@pytest.mark.parametrize(
    ["arg1", "arg2", "result"],
    [
        (",", "Test, with comma", "Test with comma"),
        ("mid", "  Sample Mid City  ", "Sample  City"),
        ("La", "Las Noches", "s Noches"),
    ],
)
def test_replace_str(arg1, arg2, result):
    assert replace_str(arg1, arg2) == result
