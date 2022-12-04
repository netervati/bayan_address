from bayan_address.lib.errors import InvalidValue
from bayan_address.lib.utils import is_valid_str, replace_str
from bayan_address.parser.matchers import *


class BayanAddress:
    def __init__(self, address: str) -> None:
        if not is_valid_str(address):
            raise InvalidValue(address)

        self.parsed_address = {}

        matchers = [
            match_administrative_region,
            match_province,
            match_zip_code,
            match_city,
            match_street,
            match_subdivision,
            match_barangay,
        ]
        stripped = replace_str(",", address).strip()

        for parse in matchers:
            if result := parse(stripped):
                stripped = result[0]
                self.parsed_address |= result[1]
