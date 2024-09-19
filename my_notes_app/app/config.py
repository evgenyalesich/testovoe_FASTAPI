from pydantic import BaseSettings

class Settings(BaseSettings):
    DB_USER: str = "your_db_user"
    DB_PASSWORD: str = "your_db_password"
    DB_HOST: str = "localhost"
    DB_NAME: str = "your_db_name"
    SECRET_KEY: str = "your_secret_key"

settings = Settings()
