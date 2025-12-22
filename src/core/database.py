from contextlib import asynccontextmanager
from datetime import datetime
from functools import lru_cache
from typing import AsyncIterable
from alembic.config import Config

from pydantic import PostgresDsn
from sqlalchemy import func, MetaData, TIMESTAMP
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    AsyncEngine,
    AsyncSession,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from src.core.config import get_settings

POSTGRES_INDEXES_NAMING_CONVENTION = {
    "ix": "%(column_0_label)s_idx",
    "uq": "%(table_name)s_%(column_0_name)s_key",
    "ck": "%(table_name)s_%(constraint_name)s_check",
    "fk": "%(table_name)s_%(column_0_name)s_fkey",
    "pk": "%(table_name)s_pkey",
}


class Base(DeclarativeBase):
    __abstract__ = True
    metadata = MetaData(naming_convention=POSTGRES_INDEXES_NAMING_CONVENTION)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now()
    )


@lru_cache
def _async_engine() -> AsyncEngine:
    settings = get_settings()
    return create_async_engine(
        settings.DATABASE_URL.unicode_string(),
        pool_pre_ping=True,
        pool_size=settings.DB_POOL_SIZE,
    )


@lru_cache
def _async_session_factory() -> async_sessionmaker:
    return async_sessionmaker(
        bind=_async_engine(),
        autoflush=False,
        expire_on_commit=False,
    )


async def get_session() -> AsyncIterable[AsyncSession]:
    """FastAPI uses per-request-cache if we called functions by Depends."""
    async with open_db_session() as session:
        yield session


@asynccontextmanager
async def open_db_session() -> AsyncSession:
    """For usage as context manager outside FastAPI Depends."""
    factory: async_sessionmaker = _async_session_factory()
    session: AsyncSession = factory()
    try:
        yield session
    except Exception as e:
        await session.rollback()
        raise e
    else:
        await session.commit()
    finally:
        await session.close()


def get_alembic_config(database_url: PostgresDsn, script_location: str = "migrations") -> Config:
    alembic_config = Config()
    alembic_config.set_main_option("script_location", script_location)
    alembic_config.set_main_option(
        "sqlalchemy.url",
        database_url.unicode_string().replace("postgresql+asyncpg", "postgresql+psycopg"),
    )
    return alembic_config
