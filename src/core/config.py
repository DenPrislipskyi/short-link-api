from functools import lru_cache

from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str
    SHORTCODE_LENGTH: int

    DATABASE_URL: PostgresDsn
    DB_POOL_SIZE: int
    MIGRATION_ON_STARTUP: bool = True

    model_config = SettingsConfigDict(
        case_sensitive=True, frozen=True, env_file=".env", extra="ignore"
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
