import os

from pydantic import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    SQLALCHEMY_DATABASE_URL: str

    class Config:
        env_file = os.path.abspath(os.path.join(os.path.abspath(__file__), "..", "..", ".env"))


@lru_cache()
def get_settings() -> Settings:
    return Settings()
