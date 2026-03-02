from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import engine
from app.models import Base
from app.routers import populations_router, tests_router, runs_router


@asynccontextmanager
async def lifespan(app: FastAPI):
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
