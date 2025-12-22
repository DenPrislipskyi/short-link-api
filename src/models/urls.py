from sqlalchemy.orm import Mapped, mapped_column

from src.core.database import Base


class ShortUrls(Base):
    __tablename__ = "short_urls"

    id: Mapped[int] = mapped_column(primary_key=True)
    shortcode: Mapped[str] = mapped_column(unique=True)
    url: Mapped[str] = mapped_column()
    update_id: Mapped[int] = mapped_column(unique=True)
