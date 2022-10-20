import pytest


@pytest.fixture
def address_prefix_fixture():
    return ["De"]


@pytest.fixture
def cities_fixture():
    return ["Bayan City"]


@pytest.fixture
def provinces_fixture():
    return {
        "Province": {
            "iso": "ISO-PROV",
            "region": "Region A",
            "island_group": "Island",
        }
    }


@pytest.fixture
def address_format_fixture(provinces_fixture):
    return {
        "administrative_region": ["metro manila"],
        "barangay": ["barangay", "brgy."],
        "building": ["building", "bldg", "floor"],
        "city": ["city"],
        "province": [x for x in provinces_fixture],
        "street": [
            "dr.",
            "drive",
            "st.",
            "street",
        ],
        "subdivision": ["subdivision"],
    }


@pytest.fixture
def parsed_address_fixture():
    return {
        "administrative_region": "Metro Manila",
        "barangay": "Ville",
        "building": "BLDG. 24A",
        "city": "Sample City",
        "province": "Province",
        "street": "Corner St.",
        "subdivision": "Subdivision Test",
        "zip_code": "1111",
    }
