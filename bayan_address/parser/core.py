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
    PROVINCE_RELATED_TYPES = [
        "island_group",
        "iso",
        "region",
    ]

    def __init__(self, address: str) -> None:
        if not is_valid_str(address):
            raise InvalidValue(address)

        self.address = address
        self.parsed_address = match_address_type(address)

        for el in self.PROVINCE_RELATED_TYPES:
            if "province" in self.parsed_address:
                prov_val = self.parsed_address["province"]
                if prov_val in PROVINCES:
                    self.parsed_address[el] = PROVINCES[prov_val][el]

                if related_type := get_province_related_type(prov_val):
                    self.parsed_address[el] = related_type[el]
