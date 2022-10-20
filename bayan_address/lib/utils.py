import re


def clean_str(val: str) -> str:
    return val.lower().strip()


def concat_str(arg1: str, arg2: str) -> str:
    return f"{arg1.strip()} {arg2.strip()}".strip()


def is_valid_str(val: str) -> bool:
    if not isinstance(val, str) or val.strip() == "":
        return False

    return True


def match_pattern(arg1: str, arg2: str):
    pattern = re.compile(arg1, re.IGNORECASE)
    result = pattern.findall(arg2)

    if len(result) > 0:
        return (result[0], replace_str(result[0], arg2))


def replace_str(substring: str, string: str) -> str:
    return re.sub(re.escape(substring), "", string, flags=re.IGNORECASE)


def trim_str(str: str) -> str:
    return " ".join(str.split())
