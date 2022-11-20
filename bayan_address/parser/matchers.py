from bayan_address.lib._typings import ParsedAddressType
from bayan_address.lib.data import ADDRESS_PREFIX, CITIES, PROVINCES, STREET_FORMAT
from bayan_address.lib.utils import (
    clean_str,
    is_valid_str,
    match_in_between_pattern,
    match_pattern,
    replace_str,
)


def match_address_type(val: str) -> dict:
    address = {}
    matchers = [
        match_administrative_region,
        match_province,
        match_zip_code,
        match_city,
        match_street,
        match_subdivision,
        match_barangay,
    ]
    stripped = val

    for parse in matchers:
        if result := parse(stripped):
            stripped = result[0]
            address |= result[1]

    return address


# Matchers based on the address type
# ==================================


def match_administrative_region(arg: str) -> ParsedAddressType:
    if res := match_pattern("metro manila", arg):
        return (res[1], {"administrative_region": res[0]})


def match_barangay(arg: str) -> ParsedAddressType:
    if is_valid_str(arg):
        return ("", {"barangay": arg.strip()})


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
            if "city" in clean_str(res[1]):
                if res_b := match_pattern(f"{el} city", stripped):
                    return res_b
                else:
                    return
            else:
                return res

        # Ensures that if city with "City" in name will match
        # with address that has no City (e.g. Quezon City == Quezon)
        if "city" in clean_str(el):
            cleaned_element = replace_str("city", clean_str(el)).strip()
            if res := match_pattern(cleaned_element, stripped):
                return res

    for el in CITIES:
        if res := city_patterns(el, stripped):
            address_city = res[0]
            stripped = res[1]

        if address_city:
            break

    if address_city:
        return (stripped, {"city": address_city})


def match_province(arg: str) -> ParsedAddressType:
    is_city = lambda prov, arg: (
        match_pattern(f"{prov} city", arg) or match_pattern(f"city of {prov}", arg)
    )

    for el in PROVINCES:
        if is_city(el, arg):
            return
        elif res := match_pattern(el, arg):
            province_dict = {"province": res[0]} | PROVINCES[el]
            return (res[1], province_dict)


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
                    address_street = resb[1]
                    address_building = resb[0]
                    stripped = res[1]
                    break
                address_street = res[0]
                stripped = res[1]
                break

        if address_street:
            break

    if address_street:
        address_dict = {"street": address_street}
        if address_building:
            address_dict |= {"building": address_building}

        return (stripped, address_dict)


def match_subdivision(arg: str) -> ParsedAddressType:
    if res := match_in_between_pattern(
        r"(.*?)subdivision+\b", arg, before="", after="Subdivision"
    ):
        return (res[1], {"subdivision": res[0]})


def match_zip_code(arg: str) -> ParsedAddressType:
    if res := match_pattern(r"\d{4}", arg):
        return (res[1], {"zip_code": res[0]})
