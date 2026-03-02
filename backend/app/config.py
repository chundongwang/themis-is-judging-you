from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite+aiosqlite:///./dev.db"
    MODEL: str = "claude-sonnet-4-6"
    LLM_TEMPERATURE: float = 0.7
    LLM_BATCH_SIZE: int = 100
    CORS_ORIGINS: list[str] = ["http://localhost:5173"]
    DEBUG: bool = True
    STUB_LLM: bool = True

    model_config = {"env_file": ".env", "extra": "ignore"}


settings = Settings()
