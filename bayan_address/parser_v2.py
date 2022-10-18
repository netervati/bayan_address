from functools import lru_cache
import re
from .lib.config import Immutable
from .lib.data_v2 import ADDRESS_PREFIX, PROVINCES
from .lib.errors import InvalidValue
from .lib.utils import clean_str, is_valid_str
from .type_v2 import get_address_type, get_province_related_type, strip_matching_data


class Parser:
    def __init__(self, arg: str) -> None:
        self.arg = arg
        self.street = ""

    def run(self):
        init_strip = strip_matching_data(self.arg)
        result = init_strip["pre_selected_formats"]

        stripped_arg = re.sub(",", "", init_strip["stripped_address"]).split()
        undefined_type = {}
        pending_prefix = ""

        for idx, el in enumerate(stripped_arg):
            if clean_str(el) in ADDRESS_PREFIX:
                pending_prefix = el
            else:
                address_type = get_address_type(el)

                if "undefined" in address_type:
                    undefined_type[
                        idx
                    ] = f"{pending_prefix.strip()} {address_type['undefined']}".strip()
                    pending_prefix = ""
                else:
                    defined_type = address_type
                    if "street" in address_type:
                        prev_idx = idx - 1
                        street_val = address_type["street"]
                        if prev_idx in undefined_type:
                            street_val = f"{undefined_type[prev_idx]} {street_val}"
                            del undefined_type[prev_idx]

                        defined_type = {
                            "street": f"{pending_prefix} {street_val}".strip()
                        }
                        pending_prefix = ""

                    result |= defined_type

        remaining_values = ""
        for _, val in undefined_type.items():
            remaining_values += f" {val.strip()}"
        remaining_values.strip()

        if is_valid_str(remaining_values):
            l_val = remaining_values
            if "barangay" in result:
                l_val = f"{result['barangay'].strip()} {l_val.strip()}"
            result["barangay"] = l_val.strip()

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
