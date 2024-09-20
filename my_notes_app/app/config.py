from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str = "localhost"  # Default to localhost
    DB_PORT: int = 5432         # Default PostgreSQL port
    DB_NAME: str

    class Config:
        env_file = ".env"  # Load from .env file

settings = Settings()


SQLALCHEMY_DATABASE_URL = (
    f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWORD}"
    f"@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
)
print(settings.DB_PORT)  # Проверка типа данных
print(type(settings.DB_PORT))  # Это должно вывести <class 'int'>
