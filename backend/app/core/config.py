from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings and configuration"""

    # Database
    DATABASE_URL: str

    # Redis
    REDIS_URL: str

    # JWT Authentication
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # AI
    ANTHROPIC_API_KEY: str

    # Environment
    ENVIRONMENT: str = "development"

    # CORS
    BACKEND_CORS_ORIGINS: list = ["http://localhost:3000", "http://localhost:8000"]

    # API
    API_V1_STR: str = "/api"
    PROJECT_NAME: str = "Data Engineering Interview Prep"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
