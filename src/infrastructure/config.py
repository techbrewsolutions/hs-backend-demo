from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    HUBSPOT_CLIENT_ID: str
    HUBSPOT_CLIENT_SECRET: str
    HUBSPOT_REDIRECT_URI: str
    HUBSPOT_SCOPES: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_parse_values={
            "HUBSPOT_SCOPES": lambda v: v.split() if isinstance(v, str) else v
        },
    )


def get_settings() -> Settings:
    """Get application settings."""
    return Settings()
