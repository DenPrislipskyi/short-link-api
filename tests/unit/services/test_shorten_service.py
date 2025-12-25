import pytest
from uuid import uuid4
from unittest.mock import AsyncMock

from src.services.shorten import ShortenService
from src.models.urls import ShortUrls
from src.core.exceptions import (
    ShortcodeAlreadyExists,
    UpdateIdDoesNotExist,
    ShortcodeNotFound,
)


@pytest.mark.asyncio
async def test_create_generates_shortcode_when_none(mock_session):
    service = ShortenService(mock_session)

    service._get_by_shortcode = AsyncMock(return_value=None)

    short = await service.create(
        url="https://example.com",
        shortcode=None,
    )

    mock_session.add.assert_called_once()
    mock_session.commit.assert_awaited_once()

    assert short.url == "https://example.com"
    assert len(short.shortcode) == 6
    assert short.shortcode is not None


@pytest.mark.asyncio
async def test_create_raises_if_shortcode_exists(mock_session):
    service = ShortenService(mock_session)

    service._get_by_shortcode = AsyncMock(
        return_value=ShortUrls(
            url="https://old.com",
            shortcode="dup",
        )
    )

    with pytest.raises(ShortcodeAlreadyExists):
        await service.create(
            url="https://new.com",
            shortcode="dup",
        )

    mock_session.add.assert_not_called()
    mock_session.commit.assert_not_awaited()


@pytest.mark.asyncio
async def test_update_success(mock_session):
    service = ShortenService(mock_session)

    short = ShortUrls(
        url="https://old.com",
        shortcode="abc",
        update_id=uuid4(),
    )

    service._get_by_update_id = AsyncMock(return_value=short)

    updated = await service.update(
        update_id=short.update_id,
        url="https://new.com",
    )

    assert updated.url == "https://new.com"
    mock_session.commit.assert_awaited_once()


@pytest.mark.asyncio
async def test_update_raises_if_not_found(mock_session):
    service = ShortenService(mock_session)

    service._get_by_update_id = AsyncMock(return_value=None)

    with pytest.raises(UpdateIdDoesNotExist):
        await service.update(
            update_id=uuid4(),
            url="https://example.com",
        )

    mock_session.commit.assert_not_awaited()


@pytest.mark.asyncio
async def test_get_by_shortcode_raises_if_not_found(mock_session):
    service = ShortenService(mock_session)

    service._get_by_shortcode = AsyncMock(return_value=None)

    with pytest.raises(ShortcodeNotFound):
        await service.redirect("missing")

    mock_session.commit.assert_not_awaited()


@pytest.mark.asyncio
async def test_redirect_increments_counter_and_returns_url(mock_session):
    service = ShortenService(mock_session)

    service._get_by_shortcode = AsyncMock(
        return_value=ShortUrls(
            url="https://example.com",
            shortcode="abc",
            redirect_count=0,
            last_redirect_at=None,
        )
    )

    result = await service.redirect("abc")

    assert result == "https://example.com"
    mock_session.commit.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_stats_returns_short_url(mock_session):
    service = ShortenService(mock_session)

    short = ShortUrls(
        url="https://example.com",
        shortcode="abc",
        redirect_count=3,
    )
    service._get_by_shortcode = AsyncMock(return_value=short)

    result = await service.get_stats("abc")

    assert result is short
