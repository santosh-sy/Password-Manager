from pydantic import BaseModel, Field, AnyHttpUrl
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "Secure Password Manager"
    ENV: str = "dev"
    JWT_SECRET: str = Field(..., min_length=32)
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    DATABASE_URL: str = "postgresql://postgres:postgres@db:5432/secure_password"

    CORS_ORIGINS: list[str] = ["http://localhost:3000"]
    HTTPS_REDIRECT: bool = True

    MASTER_ENCRYPTION_KEY: str = Field(..., min_length=32)

    class Config:
        env_file = "../.env"


settings = Settings()
