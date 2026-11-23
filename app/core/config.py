from functools import lru_cache
from pathlib import Path

from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_PATH = Path(__file__).resolve().parents[2] / ".env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=ENV_PATH)

    APP_TITLE: str = "Shortly"
    APP_VERSION: str = "0.1.0"
    APP_PREFIX: str = "api/v1/"

    DB_URL: PostgresDsn

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    JWT_ACCESS_TOKEN_EXPIRES_MINUTES: int = 15
    JWT_REFRESH_TOKEN_EXPIRES_MINUTES: int = 7 * 24 * 60


@lru_cache
def get_settings():
    return Settings()


settings = get_settings()
