import json
import os
from typing import List, Optional, Union
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "Loyalty Backend"
    ENVIRONMENT: str = "development"
    API_V1_STR: str = "/api/v1"
    PORT: int = 8000
    CORS_ORIGINS: Union[List[str], str] = ["*"]
    DATABASE_URL: Optional[str] = None
    FIREBASE_CREDENTIALS_BASE64: Optional[str] = None
    REDIS_URL: Optional[str] = None
    CARD_CACHE_TTL_SECONDS: int = 900

    @field_validator("DATABASE_URL", mode="before")
    @classmethod
    def assemble_db_url(cls, v: Optional[str]) -> str:
        if not v:
            v = (
                os.getenv("POSTGRES_URL")
                or os.getenv("DATABASE_PRIVATE_URL")
                or os.getenv("DATABASE_PUBLIC_URL")
                or "postgresql://postgres:postgrespassword@localhost:5432/loyalty_db"
            )
        if v and v.startswith("postgres://"):
            return v.replace("postgres://", "postgresql://", 1)
        return v

    @field_validator("REDIS_URL", mode="before")
    @classmethod
    def assemble_redis_url(cls, v: Optional[str]) -> Optional[str]:
        if not v:
            v = (
                os.getenv("REDIS_URL")
                or os.getenv("REDIS_PRIVATE_URL")
                or os.getenv("REDIS_PUBLIC_URL")
            )
        return v

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, str) and v.startswith("["):
            return json.loads(v)
        elif isinstance(v, list):
            return v
        raise ValueError(v)

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )


settings = Settings()
