from datetime import datetime
from urllib.parse import urlparse
from uuid import UUID

from pydantic import BaseModel, model_validator
from pydantic import Field

from src.core.exceptions import InvalidUrlOrShortcode, UrlNotProvided


class ShortenCreateRequest(BaseModel):
    url: str
    shortcode: str | None = None

    @model_validator(mode="before")
    @classmethod
    def validate_url(cls, values: dict) -> dict:
        url = values.get("url")
        if not url:
            raise UrlNotProvided()

        parsed = urlparse(url)
        if not (parsed.scheme and parsed.netloc):
            raise InvalidUrlOrShortcode()

        return values


class ShortenCreateResponse(BaseModel):
    shortcode: str
    update_id: UUID


class ShortenUpdateRequest(BaseModel):
    url: str

    @model_validator(mode="before")
    @classmethod
    def validate_url(cls, values: dict) -> dict:
        url = values.get("url")
        if not url:
            raise UrlNotProvided()

        parsed = urlparse(url)
        if not (parsed.scheme and parsed.netloc):
            raise InvalidUrlOrShortcode("The provided url is invalid")

        return values


class ShortenUpdateResponse(BaseModel):
    shortcode: str


class ShortenStatsResponse(BaseModel):
    created: datetime
    last_redirect: datetime | None = Field(alias="lastRedirect")
    redirect_count: int = Field(alias="redirectCount")

    model_config = {"populate_by_name": True}
