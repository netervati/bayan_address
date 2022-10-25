from bayan_address.parser.matchers import match_address_type
from bayan_address.lib.errors import InvalidValue
from bayan_address.lib.utils import is_valid_str, replace_str


class BayanAddress:
    def __init__(self, address: str) -> None:
        if not is_valid_str(address):
            raise InvalidValue(address)

        cleaned_string = replace_str(",", address).strip()
        self.parsed_address = match_address_type(cleaned_string)
