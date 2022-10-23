from typing import Union
from bayan_address.parser.matchers import match_address_type
from bayan_address.lib.data import PROVINCES
from bayan_address.lib.errors import InvalidValue
from bayan_address.lib.utils import clean_str, is_valid_str


def get_province_related_type(val: str) -> Union[str, None]:
    cleaned_str = clean_str(val)
    for el in PROVINCES:
        if clean_str(el) in cleaned_str:
            return PROVINCES[el]


class BayanAddress:
    def __init__(self, address: str) -> None:
        if not is_valid_str(address):
            raise InvalidValue(address)

        self.parsed_address = match_address_type(address)

        if "province" in self.parsed_address:
            prov_val = self.parsed_address["province"]
            if prov_val in PROVINCES:
                self.parsed_address |= PROVINCES[prov_val]
            elif related_type := get_province_related_type(prov_val):
                self.parsed_address |= related_type
