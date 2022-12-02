import re
from collections import namedtuple


MatchResult = namedtuple("MatchResult", "address_type stripped")


def clean_str(val: str) -> str:
    return val.lower().strip()


def concat_str(arg1: str, arg2: str) -> str:
    return f"{arg1.strip()} {arg2.strip()}".strip()


def is_valid_str(val: str) -> bool:
    return isinstance(val, str) and val.strip() != ""


def match_in_between_pattern(*args: tuple, **kwargs: dict) -> tuple[str, str]:
    if result := re.search(args[0], args[1], re.IGNORECASE):
        substr = f"{kwargs['before'].capitalize()}{result.group(1)}{kwargs['after'].capitalize()}"
        return MatchResult(substr.strip(), replace_str(substr, args[1]))


def match_pattern(arg1: str, arg2: str) -> tuple[str, str]:
    pattern = re.compile(arg1, re.IGNORECASE)
    result = pattern.findall(arg2)

    if len(result) > 0:
        return MatchResult(result[0].strip(), replace_str(result[0], arg2))


def replace_str(substring: str, string: str) -> str:
    return re.sub(re.escape(substring), "", string, flags=re.IGNORECASE).strip()


def trim_str(str: str) -> str:
    return " ".join(str.split())
