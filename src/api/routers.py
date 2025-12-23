from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from fastapi.responses import RedirectResponse

from src.core.database import get_session
from src.schemas.schema import (
    ShortenCreateRequest,
    ShortenCreateResponse,
    ShortenUpdateRequest,
    ShortenUpdateResponse,
)
from src.services.shorten import ShortenService

router = APIRouter(tags=["url"])


@router.post(
    "/shorten",
    status_code=201,
    response_model=ShortenCreateResponse,
)
async def create_short_url(
    payload: ShortenCreateRequest,
    session: AsyncSession = Depends(get_session),
):
    service = ShortenService(session)
    short_url = await service.create(
        url=payload.url,
        shortcode=payload.shortcode,
    )

    return ShortenCreateResponse(
        shortcode=short_url.shortcode,
        update_id=short_url.update_id,
    )


@router.patch(
    "/update/{update_id}",
    status_code=201,
    response_model=ShortenUpdateResponse,
)
async def update_short_url(
    update_id: UUID,
    body: ShortenUpdateRequest,
    session: AsyncSession = Depends(get_session),
) -> ShortenUpdateResponse:
    service = ShortenService(session)
    short_url = await service.update(update_id=update_id, url=body.url)

    return ShortenUpdateResponse(shortcode=short_url.shortcode)


@router.get("/{shortcode}", status_code=302)
async def redirect_by_shortcode(
    shortcode: str,
    session: AsyncSession = Depends(get_session),
) -> RedirectResponse:
    service = ShortenService(session)
    short_url = await service.get_by_shortcode(shortcode)

    return RedirectResponse(
        url=short_url,
        status_code=302,
    )
