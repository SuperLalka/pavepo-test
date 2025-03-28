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
    SECRET_KEY: Optional[str] = os.getenv("SECRET_KEY")
    ALGORITHM: Optional[str] = os.getenv("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: Optional[int] = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
    # Origins
    ORIGINS: Optional[str] = os.getenv("ORIGINS")
    # PostgreSQL
    POSTGRES_HOST: Optional[str] = os.getenv("POSTGRES_HOST")
    POSTGRES_PORT: Optional[int] = int(os.getenv("POSTGRES_PORT"))
    POSTGRES_DB: Optional[str] = os.getenv("POSTGRES_DB")
    POSTGRESS_USER: Optional[str] = os.getenv("POSTGRES_USER")
    POSTGRESS_PASSWORD: Optional[str] = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_CONNECTION_STRING: str = (
        f"postgresql+asyncpg://{POSTGRESS_USER}:{POSTGRESS_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    )


settings = Settings()
