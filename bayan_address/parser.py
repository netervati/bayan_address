from functools import lru_cache
from .lib.config import Immutable
from .lib.data import ADDRESS_PREFIX, PROVINCES, STREET_FORMAT
from .lib.errors import InvalidValue
from .lib.utils import (
    is_valid_str,
    match_in_between_pattern,
    match_pattern,
    replace_str,
    trim_str,
)
from .type import get_province_related_type, strip_matching_data


class Parser:
    def __init__(self, arg: str) -> None:
        self.address_type = {}
        self.arg = trim_str(arg)
        self.defined_type = {}
        self.pending_prefix = ""
        self.street = ""
        self.undefined_type = {}

    def run(self) -> dict:
        matched = strip_matching_data(self.arg)
        prefixes = ADDRESS_PREFIX.split() + [""]
        result = matched["pre_selected_formats"]
        stripped_address = matched["stripped_address"]

        for pref in prefixes:
            for x in STREET_FORMAT:
                if res := match_in_between_pattern(
                    r"\b{}(.*?){}+\b".format(pref, x),
                    stripped_address,
                    before=pref,
                    after=x,
                ):
                    if resb := match_pattern(r"\b\d+\b", res[0]):
                        result["street"] = resb[0]
                        result["building"] = resb[0]
                        stripped_address = res[1]
                        break
                    result["street"] = res[0]
                    stripped_address = res[1]
                    break

            if "street" in result:
                break

        stripped_address = replace_str(",", stripped_address).strip()

        if is_valid_str(stripped_address):
            result["barangay"] = stripped_address.strip()

        return result


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
        self.parsed_address = Parser(address).run()

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
