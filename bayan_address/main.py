from bayan_address.parser import BayanAddress


def parse(arg: str) -> dict:
    return BayanAddress(arg).parsed_address
