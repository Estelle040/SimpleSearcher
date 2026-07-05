from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    ELASTIC_URL: str
    ELASTIC_INDEX: str = "documents"

    class Config:
        env_file = ".env"


settings = Settings()