from functools import lru_cache
from bayan_address.parser.matchers import match_address_type
from bayan_address.lib.data import PROVINCES
from bayan_address.lib.errors import InvalidValue
from bayan_address.lib.helpers import Immutable
from bayan_address.lib.utils import is_valid_str
from bayan_address.type import get_province_related_type


class BayanAddress(Immutable):
    ADDRESS_TYPES = [
        "administrative_region",
        "barangay",
        "building",
        "city",
        "province",
        "street",
        "subdivision",
    ]
    ERROR_MSG = "The address has no such value."

    def __init__(self, address: str) -> None:
        if not is_valid_str(address):
            raise InvalidValue(address)

        self.address = address
        self.parsed_address = match_address_type(address)

        for el in self.ADDRESS_TYPES:
            setattr(self, el, self.getprop(el))

        super().__init__()

    def __iter__(self):
        for k, v in self.parsed_address.items():
            yield (k, v)

    def getprop(self, type: str) -> str:
        return self.parsed_address.get(type, self.ERROR_MSG)

    def getsprop(self, type: str) -> str:
        f_key = next(iter(PROVINCES))
        if type not in PROVINCES[f_key]:
            return self.ERROR_MSG

        if "province" in self.parsed_address:
            prov_val = self.parsed_address["province"]
            if prov_val in PROVINCES:
                return PROVINCES[prov_val][type]

            if related_type := get_province_related_type(prov_val):
                return related_type[type]

        return f"The address has no valid province to check it's {type}."

    @property
    @lru_cache(maxsize=4)
    def island_group(self) -> str:
        return self.getsprop("island_group")

    @property
    @lru_cache(maxsize=4)
    def iso(self) -> str:
        return self.getsprop("iso")

    @property
    @lru_cache(maxsize=4)
    def region(self) -> str:
        return self.getsprop("region")

    @property
    def zip_code(self) -> str:
        return self.getprop("zip_code")
