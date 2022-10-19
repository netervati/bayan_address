from functools import lru_cache
from .lib.config import Immutable
from .lib.data_v2 import ADDRESS_PREFIX, PROVINCES
from .lib.errors import InvalidValue
from .lib.utils import clean_str, concat_str, is_valid_str, replace_str
from .type_v2 import get_address_type, get_province_related_type, strip_matching_data


class Parser:
    def __init__(self, arg: str) -> None:
        self.address_type = {}
        self.arg = arg
        self.defined_type = {}
        self.pending_prefix = ""
        self.street = ""
        self.undefined_type = {}

    def run(self) -> dict:
        init_strip = strip_matching_data(self.arg)
        result = init_strip["pre_selected_formats"]
        stripped_arg = replace_str(",", init_strip["stripped_address"]).split()

        for idx, el in enumerate(stripped_arg):
            if clean_str(el) in ADDRESS_PREFIX:
                self.pending_prefix = el
            else:
                self.address_type = get_address_type(el)
                if "undefined" in self.address_type:
                    self.set_undefined_address(idx)
                else:
                    self.set_defined_address(idx)
                    result |= self.defined_type

        remaining_values = self.set_remaining_values()
        if is_valid_str(remaining_values):
            l_val = remaining_values
            if "barangay" in result:
                l_val = concat_str(result["barangay"], l_val)
            result["barangay"] = l_val.strip()

        return result

    def set_defined_address(self, idx: int) -> None:
        self.defined_type = self.address_type
        if "street" in self.address_type:
            prev_idx = idx - 1
            street_val = self.address_type["street"]
            if prev_idx in self.undefined_type:
                street_val = concat_str(self.undefined_type[prev_idx], street_val)
                del self.undefined_type[prev_idx]

            self.defined_type = {"street": concat_str(self.pending_prefix, street_val)}
            self.pending_prefix = ""

    def set_remaining_values(self) -> str:
        remaining_str = ""
        for _, val in self.undefined_type.items():
            remaining_str += f" {val.strip()}"
        return remaining_str.strip()

    def set_undefined_address(self, idx: int) -> None:
        self.undefined_type[idx] = concat_str(
            self.pending_prefix, self.address_type["undefined"]
        )
        self.pending_prefix = ""


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
