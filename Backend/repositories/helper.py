from pydantic import HttpUrl, TypeAdapter


def url_to_httpurl(value: str | None) -> str | None:
    if not value:
        return None

    http_url_obj = TypeAdapter(HttpUrl).validate_strings(value)

    return http_url_obj
