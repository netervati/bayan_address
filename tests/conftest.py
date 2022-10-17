import pytest


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
        "drive": ["drive", "dr."],
        "province": [x for x in provinces_fixture],
        "street": ["street", "st."],
        "subdivision": ["subdivision"],
    }


@pytest.fixture
def parsed_address_fixture():
    return {
        "administrative_region": "Metro Manila",
        "barangay": "Ville",
        "building": "BLDG. 24A",
        "city": "Sample City",
        "drive": "Test Dr.",
        "province": "Province",
        "street": "Corner St.",
        "subdivision": "Subdivision Test",
        "zip_code": "1111",
    }
