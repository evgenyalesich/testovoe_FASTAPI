from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_USER: str = "DB_USER"
    DB_PASSWORD: str = "DB_PASSWORD"
 
    DB_HOST: str = "DB_HOST"   # Default to localhost
    DB_PORT: int = "DB_PORT"         # Default PostgreSQL port
    DB_NAME: str = "DB_NAME"

    class Config:
        env_file = ".env"  # Load from .env file

settings = Settings()

SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
