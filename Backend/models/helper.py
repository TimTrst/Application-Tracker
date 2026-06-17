from pydantic import HttpUrl


def must_not_be_empty(value: str | None) -> str | None:
    if not value:
        raise ValueError('Field cannot be an empty String')
    return value


def must_be_positive(value: int | None) -> int | None:
    if value < 1:
        raise ValueError('Value must be greater than 0')
    return value


def empty_str_to_none(value: str | None) -> str | None:
    if not value:
        return None
    return value
