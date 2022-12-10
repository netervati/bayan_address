from typing import Union, NamedTuple


MatchResult = NamedTuple("MatchResult", [("address_type", str), ("stripped", str)])
MatchPattern = Union[MatchResult, None]
ParsedAddressType = Union[tuple[str, dict[str, str]], None]
