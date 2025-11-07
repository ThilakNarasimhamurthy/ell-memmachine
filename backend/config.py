"""Application configuration for environment and MongoDB settings."""

from functools import lru_cache
from pathlib import Path
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuration values sourced from environment variables or a `.env` file."""

    app_name: str = Field(
        "ELL Backend",
        alias="APP_NAME",
        validation_alias="APP_NAME",
        description="Human readable service name.",
    )
    mongodb_uri: str = Field(
        ...,
        alias="MONGODB_URI",
        validation_alias="MONGODB_URI",
        description="MongoDB connection string.",
    )
    mongodb_database: str = Field(
        "ell_db",
        alias="MONGODB_DATABASE",
        validation_alias="MONGODB_DATABASE",
        description="Default MongoDB database name.",
    )

    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parent / ".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        populate_by_name=True,
    )


@lru_cache
def get_settings() -> Settings:
    """Return cached settings instance to avoid re-parsing the environment."""

    return Settings()


def get_mongo_uri(override: Optional[str] = None) -> str:
    """Resolve the effective MongoDB URI with optional override."""

    if override:
        return override
    return get_settings().mongodb_uri

