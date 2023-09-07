import os

from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    SQLALCHEMY_DATABASE_URL: str
    BOT_TOKEN: str
    API_KEY: str

    class Config:
        env_file = os.path.abspath(os.path.join(os.path.abspath(__file__), "..", "..", ".env"))
        env_file_encoding = 'utf-8'


@lru_cache()
def get_settings() -> Settings:
    return Settings()
