import typing
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "mediaserver"

    HOST: str = "0.0.0.0"
    PORT: int = 8000

    DEBUG: bool = True

    DB_PASSWORD: str
    DB_USER: str
    DB_NAME: str
    DB_HOST: str
    DB_PORT: str

    DATABASE_URI: str | None = None


    class Config:
        env_file = ".env"

    def __init__(self, **kwargs: typing.Any):
        super().__init__(**kwargs)
        self.DATABASE_URI = (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@"
            f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )


settings = Settings()
