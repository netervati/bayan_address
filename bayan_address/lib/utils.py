import re
from bayan_address.lib._typings import MatchPattern, MatchResult


def clean_str(val: str) -> str:
    return val.lower().strip()


def is_valid_str(val: str) -> bool:
    return isinstance(val, str) and val.strip() != ""


def match_in_between_pattern(
    pattern: str, token: str, before: str, after: str
) -> MatchPattern:
    if result := re.search(pattern, token, re.IGNORECASE):
        substr = f"{before.capitalize()}{result.group(1)}{after.capitalize()}"
        return MatchResult(substr.strip(), replace_str(substr, token))
    return None


def match_pattern(arg1: str, arg2: str) -> MatchPattern:
    pattern = re.compile(arg1, re.IGNORECASE)
    result = pattern.findall(arg2)

    if len(result) > 0:
        return MatchResult(result[0].strip(), replace_str(result[0], arg2))
    return None


def replace_str(substring: str, string: str) -> str:
    return re.sub(re.escape(substring), "", string, flags=re.IGNORECASE).strip()


def trim_str(str: str) -> str:
    return " ".join(str.split())
