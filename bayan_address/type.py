from typing import Union
from .lib.data import ADDRESS_FORMAT, ADDRESS_PREFIX, CITIES, PROVINCES
from .lib.utils import clean_str, match_pattern, replace_str


def get_address_type(item: str) -> dict:
    stripped_item = item.strip()
    if is_building_no(stripped_item):
        return {"building": stripped_item}

    cleaned_address = clean_str(item)
    for k, v in ADDRESS_FORMAT.items():
        for el in v:
            cleaned_element = clean_str(el)
            if match_pattern(cleaned_element, cleaned_address):
                return {k: stripped_item}

    return {"undefined": stripped_item}


def get_province_related_type(val: str) -> Union[str, None]:
    cleaned_str = clean_str(val)
    for el in PROVINCES:
        if clean_str(el) in cleaned_str:
            return PROVINCES[el]


def is_building_no(val: str) -> bool:
    if len(val) == 4 or not val.isdigit():
        return False

    return True


def is_valid_zipcode(val: str) -> bool:
    if len(val) != 4 or not val.isdigit():
        return False

    return True


def strip_matching_data(val: str) -> dict:
    patterns = {
        "administrative_region": ["metro manila"],
        "province": PROVINCES,
        "zip_code": [r"\d{4}"],
    }

    address = {}
    stripped = val

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

    return {
        "pre_selected_formats": address,
        "stripped_address": stripped,
    }
