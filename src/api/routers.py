from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.schema import ShortenCreateRequest, ShortenCreateResponse
from src.services.shorten import ShortenService
from src.core.database import get_session


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
        url=str(payload.url),
        shortcode=payload.shortcode,
    )

    return ShortenCreateResponse(
        shortcode=short_url.shortcode,
        update_id=short_url.update_id,
    )
