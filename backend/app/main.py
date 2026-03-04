import os
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import engine
from app.models import Base
from app.routers import populations_router, tests_router, runs_router


class _InvalidRequestFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        return "Invalid HTTP request received" not in record.getMessage()


logging.getLogger("uvicorn.error").addFilter(_InvalidRequestFilter())


def _configure_llm_providers() -> None:
    """Push provider credentials into the process environment for LiteLLM."""
    if settings.AWS_ACCESS_KEY_ID:
        os.environ["AWS_ACCESS_KEY_ID"] = settings.AWS_ACCESS_KEY_ID
    if settings.AWS_SECRET_ACCESS_KEY:
        os.environ["AWS_SECRET_ACCESS_KEY"] = settings.AWS_SECRET_ACCESS_KEY
    if settings.AWS_DEFAULT_REGION:
        os.environ["AWS_DEFAULT_REGION"] = settings.AWS_DEFAULT_REGION

    if settings.VERTEXAI_PROJECT:
        os.environ["VERTEXAI_PROJECT"] = settings.VERTEXAI_PROJECT
    if settings.VERTEXAI_LOCATION:
        os.environ["VERTEXAI_LOCATION"] = settings.VERTEXAI_LOCATION
    if settings.GOOGLE_VERTEX_AI_CREDENTIALS_CONTENT:
        # LiteLLM reads VERTEXAI_CREDENTIALS as raw service-account JSON
        os.environ["VERTEXAI_CREDENTIALS"] = settings.GOOGLE_VERTEX_AI_CREDENTIALS_CONTENT


@asynccontextmanager
async def lifespan(app: FastAPI):
    _configure_llm_providers()
    # Dev: create tables on startup. Use Alembic migrations for prod.
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(title="Country Simulator API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(populations_router)
app.include_router(tests_router)
app.include_router(runs_router)


@app.get("/health")
async def health():
    return {"status": "ok"}
