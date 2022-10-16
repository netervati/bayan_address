def clean_str(val: str) -> str:
    return val.lower().strip()


def is_valid_str(val: str) -> bool:
    if not isinstance(val, str):
        return False
    if val.strip() == "":
        return False

    return True
