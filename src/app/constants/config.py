from pydantic import BaseSettings


class Settings(BaseSettings):
    """Config class read from .env"""

    API_VERSION: str
    DATABASE_PORT: int
    POSTGRES_PASSWORD: str
    POSTGRES_USER: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_HOSTNAME: str

    # This block of codes will be used when user run the server locally (not use Docker)
    # class Config:
    #     env_file = "../.env"


settings = Settings()
