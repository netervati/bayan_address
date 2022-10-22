from bayan_address.lib.data import ADDRESS_PREFIX, CITIES, PROVINCES, STREET_FORMAT
from bayan_address.lib.utils import (
    clean_str,
    is_valid_str,
    match_in_between_pattern,
    match_pattern,
    replace_str,
)


def match_address_type(val: str) -> dict:
    patterns = {
        "administrative_region": ["metro manila"],
        "province": PROVINCES,
        "zip_code": [r"\d{4}"],
    }

    address = {}
    stripped = replace_str(",", val).strip()

    for k, v in patterns.items():
        for el in v:
            if res := match_pattern(el, stripped):
                address[k] = res[0]
                stripped = res[1]
                break

    cleaned_str = clean_str(stripped)
    prefixes = ADDRESS_PREFIX.split()

    for el in CITIES:
        cleaned_element = clean_str(el)
        skip = False

        for v in prefixes:
            if f"{v} {cleaned_element.strip()}" in cleaned_str:
                skip = True
                break

        if skip is True:
            continue

        # Ensures that if city with no "City" in name will match
        # with address that has City (e.g. Quezon == Quezon City)
        if res := match_pattern(f"{el} city", stripped):
            address["city"] = res[0]
            stripped = res[1]
        elif res := match_pattern(el, stripped):
            if "city" in clean_str(res[1]):
                if res_b := match_pattern(f"{el} city", stripped):
                    address["city"] = res_b[0]
                    stripped = res_b[1]
                else:
                    continue
            else:
                address["city"] = res[0]
                stripped = res[1]
        # Ensures that if city with "City" in name will match
        # with address that has no City (e.g. Quezon City == Quezon)
        elif "city" in cleaned_element:
            cleaned_element = replace_str("city", cleaned_element).strip()
            if res := match_pattern(cleaned_element, stripped):
                address["city"] = res[0]
                stripped = res[1]

        if "city" in address:
            break

    prefixes += [""]
    for pref in prefixes:
        for x in STREET_FORMAT:
            if res := match_in_between_pattern(
                r"\b{}(.*?){}+\b".format(pref, x),
                stripped,
                before=pref,
                after=x.capitalize(),
            ):
                if resb := match_pattern(r"\b\d+\b", res[0]):
                    address["street"] = resb[1]
                    address["building"] = resb[0]
                    stripped = res[1]
                    break
                address["street"] = res[0]
                stripped = res[1]
                break

        if "street" in address:
            break

    if res := match_in_between_pattern(
        r"(.*?)subdivision+\b", stripped, before="", after="Subdivision"
    ):
        address["subdivision"] = res[0]
        stripped = res[1]

    if is_valid_str(stripped):
        address["barangay"] = stripped.strip()

    return address
