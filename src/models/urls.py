from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from uuid import UUID, uuid4

from src.core.database import Base


class ShortUrls(Base):
    __tablename__ = "short_urls"

    id: Mapped[int] = mapped_column(primary_key=True)
    shortcode: Mapped[str] = mapped_column(unique=True)
    url: Mapped[str] = mapped_column()
    update_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        default=uuid4,
        unique=True,
        nullable=False,
    )
