import re


def clean_str(val: str) -> str:
    return val.lower().strip()


def concat_str(arg1: str, arg2: str) -> str:
    return f"{arg1.strip()} {arg2.strip()}".strip()


def is_valid_str(val: str) -> bool:
    if not isinstance(val, str) or val.strip() == "":
        return False

    return True


def replace_str(substring: str, string: str) -> str:
    return re.sub(re.escape(substring), "", string, flags=re.IGNORECASE)
