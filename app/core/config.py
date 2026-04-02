from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str
    APP_ENV: str
    POSTGRES_URL: str
    MONGO_URL: str
    MONGO_DB_NAME: str
    ANTHROPIC_API_KEY: str
    UPLOAD_DIR: str = "./uploads"
    AGENT_URL: str = "http://agent:8000"
    AGENT_TIMEOUT_SECONDS: float = 40.0

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
