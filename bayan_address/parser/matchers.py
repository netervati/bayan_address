from bayan_address.lib._typings import ParsedAddressType
from bayan_address.lib.data import ADDRESS_PREFIX, CITIES, PROVINCES, STREET_FORMAT
from bayan_address.lib.utils import (
    clean_str,
    is_valid_str,
    match_in_between_pattern,
    match_pattern,
    replace_str,
)

__all__ = [
    "match_administrative_region",
    "match_province",
    "match_zip_code",
    "match_city",
    "match_street",
    "match_subdivision",
    "match_barangay",
]


def match_administrative_region(arg: str) -> ParsedAddressType:
    if res := match_pattern("metro manila", arg):
        return (res.stripped, {"administrative_region": res.address_type})
    return None


def match_barangay(arg: str) -> ParsedAddressType:
    if is_valid_str(arg):
        return ("", {"barangay": arg.strip()})
    return None


def match_city(arg: str) -> ParsedAddressType:
    address_city = None
    stripped = arg

    def city_patterns(el, stripped):
        # Ensures that if city with no "City" in name will match
        # with address that has City (e.g. Quezon == Quezon City)
        if res := match_pattern(f"{el} city", stripped):
            return res

        # Ensures that the value that matches the city is the actual
        # city in the address string and not a different address
        # type (e.g. parser should not treat San Jose in
        # San Jose Zamboanga City as city)
        if res := match_pattern(el, stripped):
            if "city" not in clean_str(res.stripped):
                return res
            if res_b := match_pattern(f"{el} city", stripped):
                return res_b
            return None

        # Ensures that if city with "City" in name will match
        # with address that has no City (e.g. Quezon City == Quezon)
        if "city" in clean_str(el):
            if res := match_pattern(
                replace_str("city", clean_str(el)).strip(), stripped
            ):
                return res
        return None

    for el in CITIES:
        if res := city_patterns(el, stripped):
            address_city = res.address_type
            stripped = res.stripped

        if address_city:
            break

    if address_city:
        return (stripped, {"city": address_city})
    return None


def match_province(arg: str) -> ParsedAddressType:
    for el in PROVINCES:
        if match_pattern(f"{el} city", arg) or match_pattern(f"city of {el}", arg):
            return None
        if res := match_pattern(el, arg):
            return (res.stripped, {"province": res.address_type} | PROVINCES[el])
    return None


def match_street(arg: str) -> ParsedAddressType:
    address_building = None
    address_street = None
    stripped = arg

    for pref in ADDRESS_PREFIX:
        for x in STREET_FORMAT:
            if res := match_in_between_pattern(
                r"\b{}(.*?){}+\b".format(pref, x),
                stripped,
                before=pref,
                after=x,
            ):
                if resb := match_pattern(r"\b\d+\b", res[0]):
                    address_street = resb.stripped
                    address_building = resb.address_type
                    stripped = res.stripped
                    break
                address_street = res.address_type
                stripped = res.stripped
                break

        if address_street:
            break

    if address_street:
        address_dict = {"street": address_street}
        if address_building:
            address_dict |= {"building": address_building}

        return (stripped, address_dict)
    return None


def match_subdivision(arg: str) -> ParsedAddressType:
    if res := match_in_between_pattern(
        r"(.*?)subdivision+\b", arg, before="", after="Subdivision"
    ):
        return (res.stripped, {"subdivision": res.address_type})
    return None


def match_zip_code(arg: str) -> ParsedAddressType:
    if res := match_pattern(r"\d{4}", arg):
        return (res.stripped, {"zip_code": res.address_type})
    return None
