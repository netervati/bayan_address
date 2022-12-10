from bayan_address.parser import BayanAddress


def parse(arg: str) -> dict[str, str]:
    return BayanAddress(arg).parsed_address
