import secrets
import string
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.config import get_settings
from src.core.exceptions import (
    ShortcodeAlreadyExists,
    UpdateIdDoesNotExist,
    ShortcodeNotFound,
)
from src.models.urls import ShortUrls


class ShortenService:
    SHORTCODE_CHARS = string.ascii_letters + string.digits + "_"

    def __init__(self, session: AsyncSession):
        self.session = session
        self.settings = get_settings()

    def _generate_shortcode(self) -> str:
        return "".join(
            secrets.choice(self.SHORTCODE_CHARS)
            for _ in range(self.settings.SHORTCODE_LENGTH)
        )

    async def _get_by_shortcode(self, shortcode: str) -> ShortUrls | None:
        stmt = select(ShortUrls).where(ShortUrls.shortcode == shortcode)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def _get_by_update_id(self, update_id: UUID) -> ShortUrls | None:
        stmt = select(ShortUrls).where(ShortUrls.update_id == update_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def create(self, url: str, shortcode: str | None) -> ShortUrls:
        if shortcode is None:
            shortcode = self._generate_shortcode()

        existing = await self._get_by_shortcode(shortcode)
        if existing:
            raise ShortcodeAlreadyExists()

        short_url = ShortUrls(
            url=url,
            shortcode=shortcode,
        )

        self.session.add(short_url)
        await self.session.commit()

        return short_url

    async def update(self, update_id: UUID, url: str) -> ShortUrls:
        short_url = await self._get_by_update_id(update_id)
        if not short_url:
            raise UpdateIdDoesNotExist()

        short_url.url = url
        await self.session.commit()

        return short_url

    async def get_by_shortcode(self, shortcode: str) -> str | None:
        short_url = await self._get_by_shortcode(shortcode)

        if not short_url:
            raise ShortcodeNotFound()

        return short_url.url
