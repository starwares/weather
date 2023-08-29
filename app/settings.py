import os

from pydantic import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    SQLALCHEMY_DATABASE_URL: str
    BOT_TOKEN: str
    API_KEY: str

    class Config:
        env_file = os.path.abspath(os.path.join(os.path.abspath(__file__), "..", "..", ".env"))


@lru_cache()
def get_settings() -> Settings:
    return Settings()
