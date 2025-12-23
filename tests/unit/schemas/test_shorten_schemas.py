import pytest

from src.schemas.schema import (
    ShortenCreateRequest,
    ShortenUpdateRequest,
)
from src.core.exceptions import (
    InvalidUrlOrShortcode,
    UrlNotProvided,
)


def test_create_schema_valid_url():
    data = ShortenCreateRequest(url="https://example.com")
    assert data.url == "https://example.com"
    assert data.shortcode is None


def test_create_schema_without_url():
    with pytest.raises(UrlNotProvided):
        ShortenCreateRequest(url="")


def test_create_schema_invalid_url():
    with pytest.raises(InvalidUrlOrShortcode):
        ShortenCreateRequest(url="not-a-url")


def test_update_schema_valid_url():
    data = ShortenUpdateRequest(url="https://google.com")
    assert data.url == "https://google.com"


def test_update_schema_invalid_url():
    with pytest.raises(InvalidUrlOrShortcode):
        ShortenUpdateRequest(url="ftp:/broken")
