from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite+aiosqlite:///./dev.db"
    MODEL: str = "claude-sonnet-4-6"
    LLM_TEMPERATURE: float = 0.7
    LLM_BATCH_SIZE: int = 100
    CORS_ORIGINS: list[str] = ["http://localhost:5173"]
    DEBUG: bool = True
    STUB_LLM: bool = True

    # AWS Bedrock (for Anthropic models via bedrock/...)
    AWS_ACCESS_KEY_ID: str = ""
    AWS_SECRET_ACCESS_KEY: str = ""
    AWS_DEFAULT_REGION: str = ""

    # GCP Vertex AI (for Gemini models via vertex_ai/...)
    VERTEXAI_PROJECT: str = ""
    VERTEXAI_LOCATION: str = "global"
    GOOGLE_VERTEX_AI_CREDENTIALS_CONTENT: str = ""  # raw service account JSON

    model_config = {"env_file": ".env", "extra": "ignore"}


settings = Settings()
