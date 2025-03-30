import os
from typing import Optional

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    # FastAPI
    DEBUG: Optional[bool] = os.getenv("DEBUG") == "True"
    TITLE: Optional[str] = os.getenv("TITLE")
    # JWT
    JWT_SECRET: Optional[str] = os.getenv("JWT_SECRET")
    JWT_ALGORITHM: Optional[str] = os.getenv("JWT_ALGORITHM")
    JWT_EXPIRES: Optional[int] = int(os.getenv("JWT_EXPIRES"))
    # PostgreSQL
    POSTGRES_HOST: Optional[str] = os.getenv("POSTGRES_HOST")
    POSTGRES_PORT: Optional[int] = int(os.getenv("POSTGRES_PORT"))
    POSTGRES_DB: Optional[str] = os.getenv("POSTGRES_DB")
    POSTGRES_USER: Optional[str] = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD: Optional[str] = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_CONNECTION_STRING: str = (
        f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    )
    # OAuth2
    OAUTH2_YANDEX_CLIENT_ID: Optional[str] = os.getenv("OAUTH2_YANDEX_CLIENT_ID")
    OAUTH2_YANDEX_CLIENT_SECRET: Optional[str] = os.getenv("OAUTH2_YANDEX_CLIENT_SECRET")


settings = Settings()
