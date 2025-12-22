from pydantic import BaseModel, model_validator
from typing import Optional
from urllib.parse import urlparse
from uuid import UUID

from src.core.exceptions import InvalidUrlOrShortcode, UrlNotProvided


class ShortenCreateRequest(BaseModel):
    url: str
    shortcode: Optional[str] = None

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
