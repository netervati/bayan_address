from functools import lru_cache
from .lib.config import Immutable
from .lib.data import ADDRESS_FORMAT, PROVINCES
from .lib.errors import InvalidValue
from .lib.utils import is_valid_str
from .type import get_address_type, get_province_related_type


class BayanAddress(Immutable):
    ERROR_MSG = "The address has no such value."

    def __init__(self, address: str) -> None:
        if not is_valid_str(address):
            raise InvalidValue(address)

        self.address = address
        self.parsed_address = {}

        split_address = self.address.split(",")
        for el in split_address:
            if result := get_address_type(el):
                self.parsed_address |= result

        for el in ADDRESS_FORMAT:
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
