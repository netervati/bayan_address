from typing import Union
from .lib.data import ADDRESS_FORMAT, CITIES, PROVINCES
from .lib.utils import clean_str, replace_str


def get_address_type(item: str) -> dict:
    stripped_item = item.strip()
    if is_building_no(stripped_item):
        return {"building": stripped_item}
    if is_valid_zipcode(stripped_item):
        return {"zip_code": stripped_item}

    cleaned_address = clean_str(item)
    for k, v in ADDRESS_FORMAT.items():
        for el in v:
            cleaned_element = clean_str(el)
            if cleaned_element in cleaned_address:
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
    pre_selected_formats = {}
    stripped_address = val

    cleaned_str = clean_str(val)
    if "metro manila" in cleaned_str:
        stripped_address = replace_str("metro manila", stripped_address)
        pre_selected_formats["administrative_region"] = "Metro Manila"

    for el in PROVINCES:
        if clean_str(el) in cleaned_str:
            stripped_address = replace_str(el, stripped_address)
            pre_selected_formats["province"] = el
            break

    cleaned_str = clean_str(stripped_address)
    for el in CITIES:
        cleaned_element = clean_str(el)
        if cleaned_element in cleaned_str:
            stripped_address = replace_str(el, stripped_address)
            pre_selected_formats["city"] = el
            break
        elif "city" in cleaned_element:
            cleaned_element = replace_str("city", cleaned_element).strip()
            if cleaned_element in cleaned_str:
                stripped_address = replace_str(cleaned_element, stripped_address)
                pre_selected_formats["city"] = cleaned_element.capitalize()
                break

    return {
        "pre_selected_formats": pre_selected_formats,
        "stripped_address": stripped_address,
    }
