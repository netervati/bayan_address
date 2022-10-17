from typing import Union
from .lib.data import ADDRESS_FORMAT, PROVINCES
from .lib.utils import clean_str


def get_address_type(item: str) -> dict:
    stripped_item = item.strip()
    if is_valid_zipcode(stripped_item):
        return {"zip_code": stripped_item}

    cleaned_address = clean_str(item)
    for k, v in ADDRESS_FORMAT.items():
        for el in v:
            if clean_str(el) in cleaned_address:
                return {k: stripped_item}

    return {"barangay": stripped_item}


def get_province_related_type(val: str) -> Union[str, None]:
    cleaned_str = clean_str(val)
    for el in PROVINCES:
        if clean_str(el) in cleaned_str:
            return PROVINCES[el]


def is_valid_zipcode(val: str) -> bool:
    if not val.isdigit():
        return False
    if len(val) != 4:
        return False

    return True
